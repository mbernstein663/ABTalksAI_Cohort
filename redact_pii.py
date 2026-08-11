from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig


analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


# Custom member ID: M1003
member_id_recognizer = PatternRecognizer(
    supported_entity="MEMBER_ID",
    patterns=[
        Pattern(
            name="member_id",
            regex=r"\bM\d{4}\b",
            score=0.95
        )
    ],
    context=["member", "member id", "member number"]
)


# Custom claim ID: C1003
claim_id_recognizer = PatternRecognizer(
    supported_entity="CLAIM_ID",
    patterns=[
        Pattern(
            name="claim_id",
            regex=r"\bC\d{4}\b",
            score=0.95
        )
    ],
    context=["claim", "claim id", "claim number"]
)


analyzer.registry.add_recognizer(member_id_recognizer)
analyzer.registry.add_recognizer(claim_id_recognizer)


ENTITIES = [
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "US_SSN",
    "CREDIT_CARD",
    "US_PASSPORT",
    "US_DRIVER_LICENSE",
    "US_ITIN",
    "US_BANK_NUMBER",
    "MEMBER_ID",
    "CLAIM_ID",
]


def redact_pii(text: str) -> str:

    if not text:
        return text

    results = analyzer.analyze(
        text=text,
        language="en",
        entities=ENTITIES,
        score_threshold=0.4
    )

    operators = {
        entity: OperatorConfig(
            "replace",
            {"new_value": f"[{entity}]"}
        )
        for entity in ENTITIES
    }

    return anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=operators
    ).text

# sample = ["My member ID is M1002", "My phone number is 516-509-8364", "I'm not sure what my plan ID is"]


# for samp in sample:
#     print("\n \n ===== \n" + redact_pii(samp))