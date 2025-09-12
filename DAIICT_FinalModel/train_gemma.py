import os, re, json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import FunctionTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils.class_weight import compute_class_weight

# ========================
# CONFIG
# ========================
CSV_PATH = r"C:\\Users\\parth\\OneDrive\\Desktop\\Fraud-Detection-System\\DAIICT_FinalModel\\Data\\sms_scam_detection_dataset_merged_with_lang.csv"
OUTPUT_DIR = "./spam_model_out"
TEST_FRAC = 0.1
VALID_FRAC = 0.1
RANDOM_SEED = 42
MAX_WORD_FEATS = 20000
MAX_CHAR_FEATS = 5000
CV_FOLDS = 2

# ========================
# Preprocessing
# ========================
URL_RE = re.compile(r"https?://\S+|www\.\S+")
EMAIL_RE = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b")
PHONE_RE = re.compile(r"\+?\d[\d\-\s]{5,}\d")
GREETINGS = {"hi","hello","hey","hiya","hii","helo","yo","gm","gn","good","morning","goodnight"}

def clean_text(s: str) -> str:
    s = str(s)
    s = URL_RE.sub(" ", s)
    s = EMAIL_RE.sub(" ", s)
    s = PHONE_RE.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip().lower()

def is_greeting(s: str) -> int:
    tokens = set(re.findall(r"[a-z]+", s.lower()))
    return int(bool(tokens & GREETINGS and len(tokens) <= 3))

def load_and_preprocess_csv(path):
    df = pd.read_csv(path, low_memory=False, dtype_backend="numpy_nullable")
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(str).str.lower().str.strip()

    text_cols = [c for c in ["text","URL","EMAIL","PHONE","lang"] if c in df.columns]
    for c in text_cols:
        df[c] = df[c].fillna("").astype(str)

    df["combined_text"] = df[text_cols].agg(" ".join, axis=1)
    df["cleaned_text"] = df["combined_text"].map(clean_text)
    df["is_greeting"] = df["cleaned_text"].map(is_greeting)
    return df

# Named function (fixes pickling error)
def get_cleaned_text(df):
    return df["cleaned_text"]

# ========================
# Training (FAST)
# ========================
def train_fast(df):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    X = df[["cleaned_text","combined_text"]]
    y = df["label"].values

    # train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_FRAC, stratify=y, random_state=RANDOM_SEED
    )

    # Class weights
    classes = np.unique(y_train)
    weights = compute_class_weight(class_weight="balanced", classes=classes, y=y_train)
    class_weights = dict(zip(classes, weights))
    print("Class weights:", class_weights)

    # TF-IDF
    word_tfidf = TfidfVectorizer(max_features=MAX_WORD_FEATS, ngram_range=(1,2), min_df=3,
                                 analyzer="word", dtype=np.float32)
    char_tfidf = TfidfVectorizer(max_features=MAX_CHAR_FEATS, ngram_range=(3,5), min_df=3,
                                 analyzer="char", dtype=np.float32)

    # Pipeline
    pipeline = Pipeline([
        ("select_text", FunctionTransformer(get_cleaned_text, validate=False)),
        ("features", FeatureUnion([
            ("word", word_tfidf),
            ("char", char_tfidf)
        ])),
        ("clf", LogisticRegression(
            max_iter=500, solver="saga",
            class_weight=class_weights, n_jobs=-1
        ))
    ])

    # Grid search for C (regularization)
    grid = GridSearchCV(
        pipeline, {"clf__C": [0.5, 1.0, 2.0]},
        cv=StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_SEED),
        scoring="f1_macro", n_jobs=-1, verbose=2
    )

    grid.fit(X_train, y_train)
    print("Best params:", grid.best_params_)

    # Evaluate
    preds = grid.predict(X_test)
    print("\nAccuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds, digits=4))

    # Save model
    model_dir = Path(OUTPUT_DIR)
    joblib.dump(grid.best_estimator_, model_dir/"sklearn_pipeline_fast.joblib")
    print("✅ Saved fast model to", model_dir)

# ========================
# MAIN
# ========================
if __name__ == "__main__":
    df = load_and_preprocess_csv(CSV_PATH)
    print("Loaded dataset:", df.shape)
    print(df["label"].value_counts())
    train_fast(df)
