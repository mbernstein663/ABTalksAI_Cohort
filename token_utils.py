import tiktoken


encoding = tiktoken.get_encoding("cl100k_base")


INPUT_COST_PER_1K = 0.0
OUTPUT_COST_PER_1K = 0.0


def count_tokens(text: str) -> int:
    return len(encoding.encode(text))


def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    input_cost = (input_tokens / 1000) * INPUT_COST_PER_1K
    output_cost = (output_tokens / 1000) * OUTPUT_COST_PER_1K

    return input_cost + output_cost