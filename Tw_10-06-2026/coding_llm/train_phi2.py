
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model

model_name = "distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)

lora_config = LoraConfig(
    r=4,
    lora_alpha=8,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

dataset = load_dataset(
    "json",
    data_files="expanded_dataset.jsonl"
)["train"]

def tokenize(example):
    text = f"Instruction: {example['instruction']}\nAnswer: {example['output']}"

    return tokenizer(
        text,
        truncation=True,
        max_length=64
    )

tokenized = dataset.map(
    tokenize,
    remove_columns=dataset.column_names
)

training_args = TrainingArguments(
    output_dir="./cpu-model",
    num_train_epochs=1,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=1,
    learning_rate=5e-4,
    logging_steps=10,
    save_strategy="no",
    report_to="none",
    dataloader_num_workers=0
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    data_collator=DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
)

trainer.train()

model.save_pretrained("./cpu-model")
tokenizer.save_pretrained("./cpu-model")