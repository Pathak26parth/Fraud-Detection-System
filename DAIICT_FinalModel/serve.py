from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    spamLevel: float


MODEL_PATH = os.path.join(os.path.dirname(__file__), "spam_model_out", "sklearn_pipeline.joblib")
_pipeline = joblib.load(MODEL_PATH)

app = FastAPI(title="Spam Detection API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        # Expect binary classifier with predict_proba -> [p(ham), p(spam)]
        proba = _pipeline.predict_proba([req.text])[0]
        spam_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])
        # Clamp for safety
        spam_prob = max(0.0, min(1.0, spam_prob))
        return PredictResponse(spamLevel=spam_prob)
    except Exception:
        # On any failure, return neutral 0.0 so chat isn't blocked
        return PredictResponse(spamLevel=0.0)


# To run locally: uvicorn serve:app --host 0.0.0.0 --port 8000 --reload


