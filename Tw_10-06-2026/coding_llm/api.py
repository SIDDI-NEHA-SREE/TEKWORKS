from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
ADAPTER_PATH = "./tinyllama-coding-model"

print("Loading model...")

# Load tokenizer from base model
tokenizer = AutoTokenizer.from_pretrained(
    BASE_MODEL,
    use_fast=False
)

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float32
)

# Load LoRA adapter if present
try:
    model = PeftModel.from_pretrained(
        model,
        ADAPTER_PATH
    )
    print("LoRA adapter loaded successfully.")
except Exception as e:
    print("Adapter not found or invalid.")
    print(e)
    print("Using base TinyLlama model.")

model.eval()

class Query(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "Coding Assistant API Running"}

@app.post("/generate")
def generate(data: Query):

    text = f"""
You are a professional coding assistant.
Give correct, beginner-friendly, clean programming answers.
If code is requested, provide complete working code.

Instruction: {data.prompt}

Answer:
"""

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

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

    return {"response": answer}