#!/usr/bin/env python3
"""
Simple test script to verify the AI model works
"""

import joblib
import os

def test_model():
    try:
        MODEL_PATH = os.path.join(os.path.dirname(__file__), "spam_model_out", "sklearn_pipeline.joblib")
        print(f"Loading model from: {MODEL_PATH}")
        
        _pipeline = joblib.load(MODEL_PATH)
        print("✓ Model loaded successfully")
        
        # Test prediction
        test_text = "Congratulations! You won $1000!"
        proba = _pipeline.predict_proba([test_text])[0]
        spam_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])
        
        print(f"Test text: '{test_text}'")
        print(f"Spam probability: {spam_prob:.3f}")
        print(f"Is spam (>0.5): {spam_prob > 0.5}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing AI Model...")
    test_model()
