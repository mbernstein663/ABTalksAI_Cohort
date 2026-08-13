import asyncio
import json
import os

from dotenv import load_dotenv

from ragas import EvaluationDataset, evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

from langchain_agent import retrieve, generate_answer
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is not set")
evaluator_llm = LangchainLLMWrapper(
    ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )
)

evaluator_embeddings = LangchainEmbeddingsWrapper(
    OpenAIEmbeddings(
        model="text-embedding-3-small"
    )
)

EVAL_FILE = "ragas_eval_set.jsonl"
RESULTS_FILE = "ragas_run_results.jsonl"
SCORECARD_FILE = "ragas_scorecard.md"


def load_eval_set():
    with open(EVAL_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def get_contexts(model_context):
    if not model_context:
        return []

    return [
        context.strip()
        for context in model_context.split("\n\n---\n\n")
        if context.strip()
    ]


def get_answer(question, context):
    result = generate_answer(question, context)

    if isinstance(result, str):
        return result.strip()

    return "".join(str(token) for token in result).strip()


async def collect_results():
    samples = []

    for item in load_eval_set():
        question = item["question"]

        context, _, _, _ = await retrieve(question)

        sample = {
            "user_input": question,
            "retrieved_contexts": get_contexts(context),
            "response": get_answer(question, context),
            "reference": item["ideal_answer"],
        }

        samples.append(sample)

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        for sample in samples:
            f.write(json.dumps(sample) + "\n")

    return samples


def evaluate_rag(samples):
    dataset = EvaluationDataset.from_list(samples)

    return evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
    )

def save_scorecard(result):
    df = result.to_pandas()

    metrics = [
        "faithfulness",
        "answer_relevancy",
        "context_precision",
        "context_recall",
    ]

    with open(SCORECARD_FILE, "w", encoding="utf-8") as f:
        f.write("# RAGAS Scorecard\n\n")

        f.write("## Average Scores\n\n")
        f.write("| Metric | Score |\n")
        f.write("|---|---:|\n")

        for metric in metrics:
            f.write(
                f"| {metric.replace('_', ' ').title()} | "
                f"{df[metric].mean():.3f} |\n"
            )

        f.write("\n## Per-Question Scores\n\n")
        f.write(
            "| Question | Faithfulness | Answer Relevancy | "
            "Context Precision | Context Recall |\n"
        )
        f.write("|---|---:|---:|---:|---:|\n")

        for _, row in df.iterrows():
            question = row["user_input"].replace("|", "\\|")

            f.write(
                f"| {question} | "
                f"{row['faithfulness']:.3f} | "
                f"{row['answer_relevancy']:.3f} | "
                f"{row['context_precision']:.3f} | "
                f"{row['context_recall']:.3f} |\n"
            )



def main():
    samples = asyncio.run(collect_results())

    result = evaluate_rag(samples)

    print(result)

    save_scorecard(result)


if __name__ == "__main__":
    main()