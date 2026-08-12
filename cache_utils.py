import hashlib


cache = {}


def normalize_question(question: str) -> str:
    return " ".join(question.lower().strip().split())


def hash_question(question: str) -> str:
    normalized = normalize_question(question)

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()


def get_cached_response(question: str):
    return cache.get(hash_question(question))


def save_cached_response(question: str, response: dict):
    cache[hash_question(question)] = response