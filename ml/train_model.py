
import os
import sys
import traceback

# Setup logging immediately
LOG_FILE = r'c:\FINAL YEAR PROJECTS\Fake News Detection\ml_log.txt'

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")

if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

log("Script started.")

try:
    log("Importing standard libs...")
    import pickle
    import re
    
    log("Importing pandas...")
    import pandas as pd
    
    log("Importing sklearn...")
    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import PassiveAggressiveClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    log("Imports successful.")
except Exception as e:
    log("Import failed: " + str(e))
    # log(traceback.format_exc())
    sys.exit(1)

# Configuration
DATASET_PATH = r'c:\FINAL YEAR PROJECTS\Fake News Detection\fake_or_real_news.csv\fake_or_real_news.csv'
MODEL_PATH = r'c:\FINAL YEAR PROJECTS\Fake News Detection\ml\model.pkl'
VECTORIZER_PATH = r'c:\FINAL YEAR PROJECTS\Fake News Detection\ml\vectorizer.pkl'

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def train():
    log("Starting training process...")
    
    if not os.path.exists(DATASET_PATH):
        log(f"Error: Dataset not found at {DATASET_PATH}")
        return

    try:
        log("Reading CSV...")
        df = pd.read_csv(DATASET_PATH)
        
        if 'text' not in df.columns or 'label' not in df.columns:
            log(f"Error: Missing columns. Found {df.columns}")
            return

        if 'title' in df.columns:
            log("Combining title and text...")
            df['content'] = df['title'] + " " + df['text']
        else:
            df['content'] = df['text']

        log(f"Data loaded. Shape: {df.shape}")
        
        log("Cleaning data (head)...")
        # Optimization: Don't print entire cleaning loop, just sample
        df['content'] = df['content'].apply(clean_text)

        log("Splitting data...")
        x_train, x_test, y_train, y_test = train_test_split(df['content'], df['label'], test_size=0.2, random_state=7)

        log("Vectorizing...")
        tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
        tfidf_train = tfidf_vectorizer.fit_transform(x_train) 
        tfidf_test = tfidf_vectorizer.transform(x_test)

        log("Training model...")
        pac = PassiveAggressiveClassifier(max_iter=50)
        pac.fit(tfidf_train, y_train)

        log("Predicting...")
        y_pred = pac.predict(tfidf_test)
        score = accuracy_score(y_test, y_pred)
        log(f'Accuracy: {round(score*100,2)}%')
        
        log("Saving artifacts...")
        with open(MODEL_PATH, 'wb') as file:
            pickle.dump(pac, file)
        with open(VECTORIZER_PATH, 'wb') as file:
            pickle.dump(tfidf_vectorizer, file)
            
        log("Done.")
        
    except Exception as e:
        log("Training failed: " + str(e))
        log(traceback.format_exc())

if __name__ == "__main__":
    train()
