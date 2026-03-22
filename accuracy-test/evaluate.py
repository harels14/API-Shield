import json
import re
import time
import os
from collections import defaultdict
import requests

BASE_URL = "http://localhost:8080"
DATASET_FILE = "dataset.json"
RESULTS_DIR = "results"

LAYER1_TYPES = {"ISRAELI_ID", "CREDIT_CARD", "PHONE_NUMBER", "EMAIL"}
LAYER2_TYPES = {"PERSON", "LOCATION", "DATE", "ORG", "NRP"}
PLACEHOLDER_RE = re.compile(r'\[([A-Z_]+)\]')

os.makedirs(RESULTS_DIR, exist_ok=True)


def call_detect(text):
    try:
        resp = requests.get(f"{BASE_URL}/detect", params={"text": text}, timeout=10)
        if resp.status_code != 200 or not resp.text.strip():
            return []
        try:
            return resp.json()
        except Exception:
            return []
    except Exception:
        return []


def call_clean(text):
    try:
        resp = requests.get(f"{BASE_URL}/clean", params={"text": text}, timeout=30)
        if resp.status_code != 200:
            return None
        return resp.text
    except Exception:
        return None


def run():
    with open(DATASET_FILE, encoding="utf-8") as f:
        dataset = json.load(f)

    positives = [e for e in dataset if e["entities"]]
    negatives = [e for e in dataset if not e["entities"]]

    print(f"Loaded {len(dataset)} examples ({len(positives)} positive, {len(negatives)} negative)\n")

    # Per-type counters
    l1_tp   = defaultdict(int)
    l1_fn   = defaultdict(int)
    l1_fp   = defaultdict(int)   # from negative examples
    both_tp = defaultdict(int)
    both_fn = defaultdict(int)
    both_fp = defaultdict(int)  # from negative examples

    l1_latencies   = []
    both_latencies = []

    # --- Positive examples ---
    print("Evaluating positive examples...")
    for i, ex in enumerate(positives):
        print(f"\r  [{i+1}/{len(positives)}]", end="", flush=True)

        # Layer 1: /detect
        t0 = time.time()
        detections = call_detect(ex["text"])
        l1_latencies.append((time.time() - t0) * 1000)

        for entity in ex["entities"]:
            if entity["type"] not in LAYER1_TYPES:
                continue
            found = any(
                d["type"] == entity["type"] and entity["value"] in d["originalValue"]
                for d in detections
            )
            if found:
                l1_tp[entity["type"]] += 1
            else:
                l1_fn[entity["type"]] += 1

        # Both layers: /clean
        t0 = time.time()
        cleaned = call_clean(ex["text"])
        both_latencies.append((time.time() - t0) * 1000)

        if cleaned is not None:
            for entity in ex["entities"]:
                if entity["value"] not in cleaned:
                    both_tp[entity["type"]] += 1
                else:
                    both_fn[entity["type"]] += 1

    # --- Negative examples (FP counting) ---
    print(f"\n\nCounting false positives on {len(negatives)} negative examples...")
    for i, ex in enumerate(negatives):
        print(f"\r  [{i+1}/{len(negatives)}]", end="", flush=True)

        detections = call_detect(ex["text"])
        for d in detections:
            l1_fp[d["type"]] += 1

        cleaned = call_clean(ex["text"])
        if cleaned:
            for match in PLACEHOLDER_RE.finditer(cleaned):
                both_fp[match.group(1)] += 1

    # --- Compute metrics ---
    all_types = sorted(set(list(l1_tp.keys()) + list(l1_fn.keys()) +
                           list(both_tp.keys()) + list(both_fn.keys())))

    def metrics(tp, fp, fn):
        p = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        r = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
        return round(p, 3), round(r, 3), round(f, 3)

    print(f"\n\n{'Entity Type':<16} | {'L1 P':>6} {'L1 R':>6} {'L1 F1':>7} | {'Both P':>6} {'Both R':>6} {'Both F1':>8}")
    print("-" * 75)

    final = {}
    l1_f1_vals, both_f1_vals = [], []

    for etype in all_types:
        l1_p, l1_r, l1_f1 = metrics(l1_tp[etype], l1_fp[etype], l1_fn[etype])
        b_p,  b_r,  b_f1  = metrics(both_tp[etype], both_fp[etype], both_fn[etype])

        final[etype] = {
            "layer1": {"precision": l1_p, "recall": l1_r, "f1": l1_f1,
                       "tp": l1_tp[etype], "fp": l1_fp[etype], "fn": l1_fn[etype]},
            "both":   {"precision": b_p,  "recall": b_r,  "f1": b_f1,
                       "tp": both_tp[etype], "fp": both_fp[etype], "fn": both_fn[etype]},
        }

        l1_f1_vals.append(l1_f1)
        both_f1_vals.append(b_f1)

        print(f"{etype:<16} | {l1_p:>6.2f} {l1_r:>6.2f} {l1_f1:>7.2f} | {b_p:>6.2f} {b_r:>6.2f} {b_f1:>8.2f}")

    # Overall macro F1
    overall_l1   = round(sum(l1_f1_vals)   / len(l1_f1_vals),   3) if l1_f1_vals   else 0
    overall_both = round(sum(both_f1_vals) / len(both_f1_vals), 3) if both_f1_vals else 0

    avg_l1   = round(sum(l1_latencies)   / len(l1_latencies),   1) if l1_latencies   else 0
    avg_both = round(sum(both_latencies) / len(both_latencies), 1) if both_latencies else 0

    print("-" * 75)
    print(f"{'Overall Macro F1':<16} | {'':>6} {'':>6} {overall_l1:>7.2f} | {'':>6} {'':>6} {overall_both:>8.2f}")
    print(f"\nAvg Latency  — Layer 1: {avg_l1}ms | Both: {avg_both}ms")
    print(f"FP (negative examples) counted per entity type")

    final["_meta"] = {
        "overall_macro_f1": {"layer1": overall_l1, "both": overall_both},
        "latency": {"layer1_avg_ms": avg_l1, "both_avg_ms": avg_both},
        "dataset_size": len(dataset),
    }

    with open(f"{RESULTS_DIR}/metrics.json", "w") as f:
        json.dump(final, f, indent=2)

    print(f"\nSaved to {RESULTS_DIR}/metrics.json")
    return final


if __name__ == "__main__":
    run()
