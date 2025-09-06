from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib

# Load model + vectorizer
model = joblib.load("sustain_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# FastAPI app
app = FastAPI(title="Sustainability Scorer API")

# ✅ Allow Chrome Extension + localhost (CORS fix)
origins = [
    "chrome-extension://ngckmgjoiiebjjgeejoegiigcoofbolo",  # replace with your extension ID
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # Use ["*"] if debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root test endpoint
@app.get("/")
def root():
    return {"message": "Sustainability Scorer API is running 🚀"}

# Request schema
class Product(BaseModel):
    text: str

# ✅ Main analyze endpoint
@app.post("/analyze")
def analyze(product: Product):
    X = vectorizer.transform([product.text])
    score = model.predict(X)[0]

    # Clamp between 0–100
    score = max(0, min(100, round(score, 2)))

    return {
        "score": score,
        "factors": ["ML-based prediction from product text"],
        "alternatives": [
            {"name": "Reusable Bottle", "score": 85},
            {"name": "Bamboo Toothbrush", "score": 90}
        ]
    }
