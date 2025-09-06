import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# Check if CSV exists
csv_path = "sustainability_dataset.csv"
print("Looking for:", os.path.abspath(csv_path))

if not os.path.exists(csv_path):
    print("❌ CSV file not found! Did you run preprocess.py?")
    exit()

# Load dataset
df = pd.read_csv(csv_path)

print("✅ Dataset loaded!")
print("Shape:", df.shape)
print(df.head())

# Features and target
X = df["text"].fillna("")
y = df["score"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Text vectorization
vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Model: Ridge Regression
model = Ridge(alpha=1.0)
model.fit(X_train_tfidf, y_train)

# Evaluate
y_pred = model.predict(X_test_tfidf)
print("📊 MSE:", mean_squared_error(y_test, y_pred))
print("📊 R²:", r2_score(y_test, y_pred))

# Save model + vectorizer
joblib.dump(model, "sustain_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("✅ Model and vectorizer saved!")
