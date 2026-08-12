import asyncio
from pathlib import Path

from langchain_agent import (
    retrieve,
    generate_answer,
    count_tokens,
    define_function,
)


QUESTIONS = [
    "How does prior authorization work?",
    "When is prior authorization required?",
    "How do I appeal a denied claim?",
    "What steps are involved in an appeal after a denial?",
    "How does in-network coverage differ from out-of-network coverage?",
    "What happens if I receive care from an out-of-network provider?",
    "What kinds of services can be excluded from coverage?",
    "How can I tell whether a service is eligible for coverage?",
    "What information do I need to submit an appeal for a claim?",
    "How are denied claims handled during the appeal process?",
    "Does coverage require prior authorization for some services?",
    "How should I verify whether a provider is in-network?",
    "What should I do if a service is not covered?",
    "Can an out-of-network service still be eligible for coverage?",
    "What details should I review before appealing a denied claim?",
]


async def run_variant(question, k):
    context, structure, chunk_ids, tool_result = await retrieve(
        question,
        k=k
    )

    answer = generate_answer(question, context)

    return {
        "answer": answer,
        "tokens": count_tokens(answer),
        "structure": structure,
        "chunk_ids": chunk_ids,
    }


def clean_markdown(text):
    return text.replace("|", "\\|").replace("\n", "<br>")


async def main():
    output_path = Path("ab_test_results.md")

    results = []

    for i, question in enumerate(QUESTIONS, start=1):
        print(f"\n===== QUESTION {i}/15 =====")
        print(question)
        print("CLASSIFICATION:", define_function(question))

        print("\n--- k=3 ---")
        variant_3 = await run_variant(question, 3)

        print("\n--- k=5 ---")
        variant_5 = await run_variant(question, 5)

        results.append(
            (question, variant_3, variant_5)
        )

    with output_path.open("w", encoding="utf-8") as file:
        file.write("# A/B Test Results\n\n")
        file.write("**Variant A:** k=3 retrieved chunks  \n")
        file.write("**Variant B:** k=5 retrieved chunks  \n")
        file.write("**Sample size:** 15 questions\n\n")

        for i, (question, k3, k5) in enumerate(results, start=1):
            file.write(f"## Question {i}\n\n")
            file.write(f"**Question:** {question}\n\n")
            file.write(f"**Classification:** {k3['structure']}\n\n")

            file.write("| k=3 | k=5 |\n")
            file.write("|---|---|\n")

            left = (
                f"{clean_markdown(k3['answer'])}"
                f"<br><br>**Tokens:** {k3['tokens']}"
                f"<br>**Score:** "
                f"<br><br>**Chunks:** {', '.join(k3['chunk_ids'])}"
            )

            right = (
                f"{clean_markdown(k5['answer'])}"
                f"<br><br>**Tokens:** {k5['tokens']}"
                f"<br>**Score:** "
                f"<br><br>**Chunks:** {', '.join(k5['chunk_ids'])}"
            )

            file.write(f"| {left} | {right} |\n\n")

    print(f"\nResults written to {output_path}")


if __name__ == "__main__":
    asyncio.run(main())