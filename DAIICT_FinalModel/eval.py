# eval.py
import argparse
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from preprocess import csv_to_sft_dataset

def messages_to_prompt(text: str):
    # keep prompt consistent with training messages
    return f"{text}\n\nAssistant:"

def predict_label(model, tokenizer, text, labels, max_new_tokens=32):
    prompt = messages_to_prompt(text)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )
    gen = tokenizer.decode(out[0][inputs['input_ids'].shape[-1]:], skip_special_tokens=True).strip().lower()
    # try to map generation to one of labels
    for lbl in labels:
        if lbl.lower() in gen:
            return lbl
    # fallback: return first token or unknown
    first_word = gen.split()[0] if gen.split() else gen
    # if first_word matches label exactly:
    for lbl in labels:
        if first_word == lbl.lower():
            return lbl
    return None

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True)
    p.add_argument("--model_dir", required=True)
    p.add_argument("--max_new_tokens", type=int, default=32)
    args = p.parse_args()

    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(args.model_dir, device_map="auto", trust_remote_code=True)

    ds, labels, _, _ = csv_to_sft_dataset(args.data, test_frac=0.1)
    total = 0
    correct = 0
    print("Evaluating on test set of size:", len(ds['test']))
    for ex in ds['test']:
        user_text = ex['messages'][0]['content']
        true_label = ex['messages'][1]['content'].strip()
        pred = predict_label(model, tokenizer, user_text, labels, max_new_tokens=args.max_new_tokens)
        total += 1
        if pred is not None and pred.strip().lower() == true_label.strip().lower():
            correct += 1

    print(f"Accuracy: {correct}/{total} = {correct/total:.4f}")

if __name__ == "__main__":
    main()
