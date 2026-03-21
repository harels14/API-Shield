from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Entity types that regex (layer 1) cannot reliably detect
ENTITIES_TO_DETECT = ["LOCATION", "PERSON", "DATE_TIME", "NRP", "ORG"]

# Map each Presidio entity to a placeholder tag
OPERATOR_CONFIG = {
    "LOCATION":  OperatorConfig("replace", {"new_value": "[LOCATION]"}),
    "PERSON":    OperatorConfig("replace", {"new_value": "[PERSON]"}),
    "DATE_TIME": OperatorConfig("replace", {"new_value": "[DATE]"}),
    "NRP":       OperatorConfig("replace", {"new_value": "[NRP]"}),
    "ORG":       OperatorConfig("replace", {"new_value": "[ORG]"}),
}


def second_layer_clean(text: str) -> dict:
    results = analyzer.analyze(
        text=text,
        language="en",
        entities=ENTITIES_TO_DETECT,
    )

    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=OPERATOR_CONFIG,
    )

    detections = [
        {
            "entity_type": r.entity_type,
            "start": r.start,
            "end": r.end,
            "score": round(r.score, 3),
        }
        for r in results
    ]

    return {
        "original": text,
        "cleaned": anonymized.text,
        "detections": detections,
    }
