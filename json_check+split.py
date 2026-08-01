import json
import openai
import random

from pathlib import Path

root=Path(r"C:\Users\micro\Documents\ABTalksAI-Cohort")
json_path = root / "fine_tune_dataset.jsonl"
valid_roles = ["system", "user", "assistant"]
errors = []

with json_path.open("r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        try:
            record = json.loads(line)

            assert isinstance(record, dict)
            assert "messages" in record
            assert isinstance(record["messages"], list)
            assert len(record["messages"]) == 3

            roles = [message.get("role") for message in record["messages"]]
            assert roles == valid_roles

            for message in record["messages"]:
                assert isinstance(message.get("content"), str)
                assert message["content"].strip()

        except (json.JSONDecodeError, AssertionError) as error:
            errors.append(f"Line {line_number}: {error or 'Invalid schema'}")

if errors:
    print("Validation failed:")
    for error in errors:
        print(error)
else:
    print(f"Success: all {line_number} lines contain valid JSON and follow the schema.")



"""
T-T Split

---


"""

train_path = Path("fine_tune_train.jsonl")
test_path = Path("fine_tune_test.jsonl")

lines = [
    line for line in json_path.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

random.seed(42)
random.shuffle(lines)

test_lines = lines[:5]
train_lines = lines[5:]

train_path.write_text("\n".join(train_lines) + "\n", encoding="utf-8")
test_path.write_text("\n".join(test_lines) + "\n", encoding="utf-8")

print(f"Train examples: {len(train_lines)}")
print(f"Test examples: {len(test_lines)}")
print(f"Saved to {train_path} and {test_path}")