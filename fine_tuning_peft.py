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



"""
1. Load JSONL + packages
2. Add base model + tokenizer
3. Attach LoRA adapter
4. Tokenize training examples and run `Trainer`
5. Reload and evaluate models

"""


dataset = load_dataset(
    "json",
    data_files={
        "train": str(json_train),
        "test": str(json_test)
    }
)

train_dataset = dataset["train"]
test_dataset = dataset["test"]




model_id = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto"
)


peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    task_type=TaskType.CAUSAL_LM
)



model = get_peft_model(model, peft_config)







# Training arguments (AI generated)

training_args = TrainingArguments(
    output_dir=str(root / "qwen_training"),
    num_train_epochs=1,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=1,
    save_strategy="no",
    report_to="none"
)

# tokenize the json quesitons for model input
def tokenize(record):
    text = tokenizer.apply_chat_template(
        record["messages"],
        tokenize=False
    )
    tokens = tokenizer(
        text,
        truncation=True,
        max_length=1024
    )
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens


train_dataset = train_dataset.map(
    tokenize,
    remove_columns=["messages"]
)


trainer = Trainer(
    model=model,
    train_dataset=train_dataset,
    args=training_args
)

trainer.train()
adapter_path = root / "qwen-lora"
model.save_pretrained(adapter_path)


