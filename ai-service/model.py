from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

date_recognizer = PatternRecognizer(
    supported_entity="DATE_TIME",
    patterns=[
        Pattern("DATE_MONTH_YEAR", r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b", 0.85),
    ],
)

analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(date_recognizer)
anonymizer = AnonymizerEngine()

# Entity types that regex (layer 1) cannot reliably detect
ENTITIES_TO_DETECT = ["LOCATION", "PERSON", "DATE_TIME", "NRP"]

# Map each Presidio entity to a placeholder tag
OPERATOR_CONFIG = {
    "LOCATION":  OperatorConfig("replace", {"new_value": "[LOCATION]"}),
    "PERSON":    OperatorConfig("replace", {"new_value": "[PERSON]"}),
    "DATE_TIME": OperatorConfig("replace", {"new_value": "[DATE]"}),
    "NRP":       OperatorConfig("replace", {"new_value": "[NRP]"}),
}


def second_layer_clean(text: str) -> dict:
    results = analyzer.analyze(
        text=text,
        language="en",
        entities=ENTITIES_TO_DETECT,
        score_threshold=0.6,
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
