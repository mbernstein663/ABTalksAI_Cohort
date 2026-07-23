import sqlite3
import ollama
import pandas as pd 
from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

root=Path(r"C:\Users\micro\Documents\ABTalksAI-Cohort")
jsonroot = root / "knowledge_base_embed.jsonl"
db_path = root / "chroma_db"
dpath = root / "data"


dfp = pd.read_csv(dpath / "plans.csv")
dfc = pd.read_csv(dpath / "claims.csv")

conn = sqlite3.connect(dpath / "coverage.db")
dfp.to_sql("plans", conn, if_exists="replace", index=False)
dfc.to_sql("claims", conn, if_exists="replace", index=False)
conn.commit()

client = chromadb.PersistentClient(path=db_path)
collection = client.get_collection(name="coverage_kb")



# write a function that classifies our question using simple keyword classifiers
def define_function(question):
    question = question.lower()

    structured_keywords = [
        "deductible", "premium", "claim status", "claim amount",
        "claim id", "member id", "plan id", "date filed", "copay"
    ]

    unstructured_keywords = [
        "covered", "coverage", "procedure", "prior authorization",
        "appeal", "in-network", "out-of-network", "excluded", "eligible"
    ]

    structured_match = any(word in question for word in structured_keywords)
    unstructured_match = any(word in question for word in unstructured_keywords)

    if structured_match and unstructured_match:
        return "both"
    elif structured_match:
        return "structured"
    else:
        return "unstructured"



def sql_lookup(question):

    
    user = f"""
    Convert the question into exactly one read-only SQLite SELECT statement for structured RAG retrieval.

    Question: {question}

    Database schema:
    plans:plan_id,plan_name,monthly_premium,annual_deductible,copay_pct,coverage_type,network_tier
    claims:claim_id,member_id,plan_id,procedure,claim_amount,status,date_filed

    Return only the SELECT statement.
    Do not use markdown, code fences, explanations, or labels.
    Never use INSERT, UPDATE, DELETE, DROP, ALTER, or CREATE.

    Example question: What is the monthly premium for the Gold PPO plan?
    Example output: SELECT monthly_premium FROM plans WHERE plan_name = 'Gold PPO';
    """

    reply = ollama.chat(
        model="qwen2.5-coder:14b",
        messages=[
            {"role": "user", "content": user}
        ]
    )

    text = reply["message"]["content"]
    cursor = conn.cursor()

    no_fly_list = ["```", "delete", "create", "update", "drop", "insert", "alter"]
    if any(word in text.lower() for word in no_fly_list):
        return []

    cursor.execute(text)
    rows = cursor.fetchall()

    return rows


def vector_lookup(question): 

    emb_query = model.encode(question)
    results = collection.query(
        query_embeddings=[emb_query],
        n_results=5,
    )
    return results


def merge_context(rows, results):
    context_items = []

    for row in rows or []:
        context_items.append(f"Structured database result:\n{row}")

    documents = results.get("documents", [[]])[0] if results else []

    for document in documents:
        context_items.append(f"Retrieved document:\n{document}")

    seen = set()
    unique_items = []

    for item in context_items:
        normalized = " ".join(item.lower().split())

        if normalized not in seen:
            seen.add(normalized)
            unique_items.append(item)

    return "\n\n---\n\n".join(unique_items)


# call all the functions:
def retrieve(question):
    structure = define_function(question)

    rows = []
    results = {}

    if structure in ("structured", "both"):
        rows = sql_lookup(question) or []

    if structure in ("unstructured", "both"):
        results = vector_lookup(question) or {}

    model_context = merge_context(rows, results)

    print("RAW SQL ROWS:", rows)
    print("RAW VECTOR RESULTS:", results)

    return model_context, structure




test_questions = [
    "What's my copay percentage?",
    "What is the annual deductible for Silver HMO?",
    "What is the monthly premium for Gold PPO?",
    "What is the claim status for C1003?",
    "What is the claim amount for C1002?",
    "Is maternity care covered on the Bronze HMO plan?",
    "Do I need prior authorization for surgery?",
    "Can I use an out-of-network doctor?",
    "How do I appeal a denied claim?",
    "What is the claim status for C1003, and how do I appeal if it was denied?"
]

output = root / "retrieval_test_results.md"

with output.open("w", encoding="utf-8") as file:
    for question in test_questions:
        model_context, structure = retrieve(question)

        print("=" * 80)
        print("Question:", question)
        print("Structure:", structure)
        print("Result:", model_context)

        file.write(f"## {question}\n\n")
        file.write(f"**Structure:** {structure}\n\n")
        file.write(f"**Result:**\n\n{model_context}\n\n")
        file.write("**Score:** ---\n\n")
        file.write("---\n\n")

# I also had AI generate these questions to keep things simple.