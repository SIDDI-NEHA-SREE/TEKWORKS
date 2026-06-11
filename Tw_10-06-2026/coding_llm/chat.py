import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "./tinyllama-coding-model"

print("Loading model... Please wait.\n")

# Debug information
print("Model folder exists:", os.path.exists(model_path))

if os.path.exists(model_path):
    files = os.listdir(model_path)
    print("Files in model folder:")
    for f in files:
        print(" -", f)

    if len(files) == 0:
        print("\nERROR: Model folder is empty!")
        print("Your training did not save any model files.")
        exit()
else:
    print("\nERROR: Folder './tinyllama-coding-model' not found!")
    exit()

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    model_path,
    use_fast=False
)

# Load model
model = AutoModelForCausalLM.from_pretrained(model_path)

print("\nCoding Assistant Ready!")
print("Type 'exit' to quit.\n")

while True:
    prompt = input("You: ")

    if prompt.lower() == "exit":
        print("Goodbye!")
        break

    text = f"""
You are a professional coding assistant.
Give correct, beginner-friendly, clean programming answers.
If code is requested, provide complete working code.

Instruction: {prompt}

Answer:
"""

    inputs = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.3,
            top_p=0.9,
            do_sample=True,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id
        )

    result = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    answer = result.replace(text, "").strip()

    print("\nAI:", answer)
    print()