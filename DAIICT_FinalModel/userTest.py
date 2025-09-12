import joblib

# Path to your saved model
MODEL_PATH = r"C:\\Users\\parth\\OneDrive\\Desktop\\DAIICT_FinalModel\\spam_model_out\\sklearn_pipeline.joblib"

# Load the trained model
model = joblib.load(MODEL_PATH)

print("📩 Spam Detection Model Loaded!")
print("Type a message to classify (or type 'exit' to quit)\n")

while True:
    user_text = input("Enter message: ").strip()
    if user_text.lower() == "exit":
        print("👋 Goodbye!")
        break

    # Predict label and probability
    pred = model.predict([user_text])[0]
    prob = model.predict_proba([user_text])[0]

    print(f"🔍 Prediction: {pred}")
    print(f"📊 Probabilities: Ham={prob[0]:.2f}, Spam={prob[1]:.2f}\n")
