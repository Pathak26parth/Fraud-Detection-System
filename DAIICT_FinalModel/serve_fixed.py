from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
import uvicorn

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    spamLevel: float

# Load model
try:
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "spam_model_out", "sklearn_pipeline.joblib")
    print(f"Loading model from: {MODEL_PATH}")
    _pipeline = joblib.load(MODEL_PATH)
    print("✓ Model loaded successfully")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    _pipeline = None

app = FastAPI(title="Spam Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Spam Detection API is running", "model_loaded": _pipeline is not None}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        if _pipeline is None:
            return PredictResponse(spamLevel=0.0)
        
        # Expect binary classifier with predict_proba -> [p(ham), p(spam)]
        proba = _pipeline.predict_proba([req.text])[0]
        spam_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])
        # Clamp for safety
        spam_prob = max(0.0, min(1.0, spam_prob))
        print(f"Text: '{req.text}' -> Spam Level: {spam_prob:.3f}")
        return PredictResponse(spamLevel=spam_prob)
    except Exception as e:
        print(f"Error in prediction: {e}")
        # On any failure, return neutral 0.0 so chat isn't blocked
        return PredictResponse(spamLevel=0.0)

if __name__ == "__main__":
    print("Starting Spam Detection API...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
