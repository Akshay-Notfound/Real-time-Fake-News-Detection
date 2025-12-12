import pickle
import os
import re

# Paths
BASE_DIR = r'c:\FINAL YEAR PROJECTS\Fake News Detection\FakeNewsDetector'
MODEL_PATH = os.path.join(BASE_DIR, 'prediction', 'ml_models', 'model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'prediction', 'ml_models', 'vectorizer.pkl')

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def test_model():
    print(f"Loading models from {MODEL_PATH}...")
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(VECTORIZER_PATH, 'rb') as f:
            vectorizer = pickle.load(f)
        print("Models loaded.")
    except Exception as e:
        print(f"Failed to load models: {e}")
        return

    # Scenario 1: The User's Input (Headline only, very short)
    user_input = "Leopard Spotted in Pune Airport"
    cleaned_user = clean_text(user_input)
    tfidf_user = vectorizer.transform([cleaned_user])
    pred_user = model.predict(tfidf_user)[0]
    
    # Try to get decision function (distance to hyperplane) if available
    try:
        score_user = model.decision_function(tfidf_user)[0]
        print(f"\nUser Input: '{user_input}'")
        print(f"Prediction: {pred_user}")
        print(f"Confidence Score (Dist to Hyperplane): {score_user:.4f} (Close to 0 is uncertain)")
    except AttributeError:
        print(f"\nUser Input: '{user_input}'")
        print(f"Prediction: {pred_user}")
        print("Model does not support decision_function")

    # Scenario 2: Simulated longer article (same topic but with more context)
    simulated_body = """
    A leopard was spotted in the premises of the Pune International Airport area, causing panic among the staff and local residents. 
    The wild animal was seen near the cargo section early in the morning. Forest department officials were immediately alerted 
    and a rescue team was dispatched to the location. After a search operation lasting several hours, the leopard was finally 
    trapped in a cage. No injuries were reported during the incident. Authorities have stated that they will release the 
    leopard back into the wild after a medical examination. The incident highlights the growing human-wildlife conflict 
    in urban areas expanding into forest territories.
    """
    cleaned_sim = clean_text(simulated_body)
    tfidf_sim = vectorizer.transform([cleaned_sim])
    pred_sim = model.predict(tfidf_sim)[0]
    
    with open("debug_log.txt", "w") as log:
        try:
            score_user = model.decision_function(tfidf_user)[0]
            log.write(f"User Input: '{user_input}'\n")
            log.write(f"Prediction: {pred_user}\n")
            log.write(f"Score: {score_user:.4f}\n\n")
        except:
             log.write(f"User Input: '{user_input}'\nPrediction: {pred_user}\n\n")

        try:
            score_sim = model.decision_function(tfidf_sim)[0]
            log.write(f"Simulated Body: ...\n")
            log.write(f"Prediction: {pred_sim}\n")
            log.write(f"Score: {score_sim:.4f}\n")
        except:
             log.write(f"Simulated BodyPrediction: {pred_sim}\n")

if __name__ == "__main__":
    test_model()
