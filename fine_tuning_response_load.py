import json
import openai
import random

from peft import LoraConfig, get_peft_model, TaskType, PeftModel
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, Trainer, TrainingArguments, set_seed
from pathlib import Path
from datasets import load_dataset

root=Path(r"C:\Users\micro\Documents\ABTalksAI-Cohort")
json_train = root / "fine_tune_train.jsonl"
json_test = root / "fine_tune_test.jsonl"


model_id = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)

if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token



"""
Pretrained model is now saved. We just need to add the same LoRA adapter to the original base model and compare results in a new markdown.

- load test set
- define get_responses function
- add LoRA adapter
- compute results and save to markdown.
"""



with json_test.open("r", encoding="utf-8") as file:
    test_records = [json.loads(line) for line in file]


def get_responses(model):
    responses = []
    model.eval()

    for record in test_records:
        inputs = tokenizer.apply_chat_template(
            record["messages"][:-1],
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        )

        inputs = {
            key: value.to(model.device)
            for key, value in inputs.items()
        }

        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

        prompt_length = inputs["input_ids"].shape[1]

        response = tokenizer.decode(
            outputs[0, prompt_length:],
            skip_special_tokens=True
        ).strip()

        responses.append(response)

    return responses


adapter_path = root / "qwen-lora"

# if not (adapter_path / "adapter_config.json").exists():
#     raise FileNotFoundError(
#         f"No LoRA adapter found at: {adapter_path}"
#     )


# Original base model
base_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto"
)

base_responses = get_responses(base_model)


# Attach the trained LoRA adapter
fine_tuned_model = PeftModel.from_pretrained(
    base_model,
    adapter_path
)

fine_tuned_responses = get_responses(fine_tuned_model)





"""
Write final scoring markdown:


"""

sections = ["# Fine-Tuning Comparison", ""]

for index, record in enumerate(test_records, start=1):
    messages = record["messages"]
    question = messages[-2]["content"]
    reference_answer = messages[-1]["content"]

    sections.extend([
        f"### Test {index}",
        "",
        "**Question**",
        "",
        question,
        "",
        "**Held-out reference answer**",
        "",
        reference_answer,
        "",
        "**Base model response**",
        "",
        base_responses[index - 1],
        "",
        "**Fine-tuned model response**",
        "",
        fine_tuned_responses[index - 1],
        "",
        "*tone:*",
        "*correctness:*",
        "*disclaimer usage:*",
        "*terminology clarity:*",
        "",
        "---",
        "",
    ])


(root / "fine_tune_comparison.md").write_text(
    "\n".join(sections),
    encoding="utf-8"
)