# preprocess.py
import re
import argparse
from pathlib import Path
import pandas as pd
from datasets import Dataset

# Simple PII regexes (heuristic)
EMAIL_RE = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
URL_RE   = re.compile(r'https?://\S+|www\.\S+')
PHONE_RE = re.compile(r'(\+?\d[\d\-\s\(\)]{6,}\d)')

def mask_pii(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = EMAIL_RE.sub('[EMAIL]', text)
    text = URL_RE.sub('[URL]', text)
    text = PHONE_RE.sub('[PHONE]', text)
    return text

def find_label_text_cols(df: pd.DataFrame):
    cols = {c.lower().strip(): c for c in df.columns}
    label_col = None
    text_col = None
    # pick likely label column
    for k, v in cols.items():
        if k == 'label' or 'label' in k or 'target' in k:
            label_col = v
            break
    for k, v in cols.items():
        if k == 'text' or 'message' in k or 'sms' in k or 'body' in k or 'content' in k:
            text_col = v
            break
    # fallback to first/second columns
    if label_col is None:
        label_col = list(df.columns)[0]
    if text_col is None:
        text_col = list(df.columns)[1] if len(df.columns) > 1 else list(df.columns)[0]
    return label_col, text_col

def csv_to_sft_dataset(csv_path: str, label_col: str = None, text_col: str = None, test_frac: float = 0.1, save_processed: bool = False, out_dir: str = None):
    csv_path = Path(csv_path).expanduser()
    if not csv_path.exists():
        raise FileNotFoundError(f"{csv_path} not found")
    # robust CSV load
    df = pd.read_csv(csv_path, dtype=str, engine='python', encoding_errors='replace')
    df.columns = [c.strip() for c in df.columns]
    detected_label, detected_text = (label_col, text_col) if (label_col and text_col) else find_label_text_cols(df)
    # keep only needed cols
    df = df[[detected_label, detected_text]].dropna()
    # mask PII inside text
    df[detected_text] = df[detected_text].astype(str).apply(mask_pii)
    df[detected_label] = df[detected_label].astype(str).str.strip()
    # messages format expected by TRL/SFTTrainer
    df['messages'] = df.apply(lambda r: [{"role": "user", "content": r[detected_text]},
                                         {"role": "assistant", "content": r[detected_label]}], axis=1)
    ds = Dataset.from_pandas(df[['messages']])
    ds = ds.train_test_split(test_size=test_frac, seed=42)
    if save_processed:
        out_dir = Path(out_dir or "./processed_data")
        out_dir.mkdir(parents=True, exist_ok=True)
        # write train/test to jsonl for quick inspection
        ds['train'].to_json(out_dir / 'train.jsonl', orient='records', lines=True)
        ds['test'].to_json(out_dir / 'test.jsonl', orient='records', lines=True)
    labels = sorted(df[detected_label].unique().tolist())
    return ds, labels, detected_label, detected_text

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True, help="Path to csv")
    p.add_argument("--label_col", default=None)
    p.add_argument("--text_col", default=None)
    p.add_argument("--test_frac", type=float, default=0.1)
    p.add_argument("--save_processed", action="store_true")
    p.add_argument("--out_dir", default="./processed_data")
    args = p.parse_args()

    ds, labels, label_col, text_col = csv_to_sft_dataset(
        args.csv, label_col=args.label_col, text_col=args.text_col,
        test_frac=args.test_frac, save_processed=args.save_processed, out_dir=args.out_dir
    )
    print("Detected label column:", label_col)
    print("Detected text column:", text_col)
    print("Labels:", labels)
    print("Train size:", len(ds['train']), "Test size:", len(ds['test']))
    if args.save_processed:
        print("Saved processed jsonl to:", args.out_dir)
