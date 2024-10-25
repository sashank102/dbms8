from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)
# Load the saved Naive Bayes model and TF-IDF vectorizer
model_filename = os.path.join(os.getcwd(), r"C:\Users\sashank\Downloads\dbms8\naive_bayes_model.pkl")
tfidf_filename = os.path.join(os.getcwd(), r"C:\Users\sashank\Downloads\dbms8\tfidf_vectorizer.pkl")

naive_bayes_model = joblib.load(model_filename)
tfidf_vectorizer = joblib.load(tfidf_filename)

# Function to predict whether a given text is spam or not
def predict_spam(text):
    text_transformed = tfidf_vectorizer.transform([text])
    prediction = naive_bayes_model.predict(text_transformed)
    return "Spam" if prediction == 1 else "Not Spam"

# Define the Flask route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get the JSON data
    text = data.get('text', '')  # Extract the text field from the data
    if text:
        result = predict_spam(text)  # Call the prediction function
        return jsonify({'prediction': result})
    else:
        return jsonify({'error': 'No text provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)