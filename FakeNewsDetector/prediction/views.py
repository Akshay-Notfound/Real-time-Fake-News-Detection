from django.shortcuts import render
import pickle
import os
import re
import pandas as pd
from django.conf import settings

# Load model and vectorizer once
BASE_DIR = settings.BASE_DIR
# Note: BASE_DIR in settings.py inside `startproject` structure might preserve structure
# We copied ml_models to prediction/ml_models
# Assuming standard structure: FakeNewsDetector/prediction/ml_models/
MODEL_PATH = os.path.join(BASE_DIR, 'prediction', 'ml_models', 'model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'prediction', 'ml_models', 'vectorizer.pkl')

print("Loading ML models...")
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
    print("Models loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")
    model = None
    vectorizer = None

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def home(request):
    return render(request, 'home.html')

def predict(request):
    if request.method == 'POST':
        news_text = request.POST.get('news_text', '')
        
        if not news_text:
            return render(request, 'home.html', {'error': 'No text provided'})

        cleaned_text = clean_text(news_text)
        
        # Check for short text
        word_count = len(cleaned_text.split())
        is_short = word_count < 50
        
        tfidf_text = vectorizer.transform([cleaned_text])
        prediction = model.predict(tfidf_text)[0] # 'REAL' or 'FAKE'

        context = {
            'prediction': prediction,
            'is_short': is_short,
            'word_count': word_count
        }
        return render(request, 'result.html', context)
    return render(request, 'home.html')

def predict_batch(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        try:
            df = pd.read_csv(csv_file)
            
            # Find the text column (case insensitive)
            text_col = None
            for col in df.columns:
                if col.lower() in ['text', 'content', 'body', 'news']:
                    text_col = col
                    break
            
            if not text_col:
                # Fallback: Use first string column or first column
                text_col = df.columns[0] # Simplification
            
            results = []
            real_count = 0
            fake_count = 0
            
            # Process first 100 rows to avoid timeout if huge
            for index, row in df.head(100).iterrows():
                if text_col in row:
                    text_content = str(row[text_col])
                    cleaned = clean_text(text_content)
                    tfidf = vectorizer.transform([cleaned])
                    pred = model.predict(tfidf)[0]
                    
                    if pred == 'REAL':
                        real_count += 1
                    else:
                        fake_count += 1
                        
                    results.append({
                        'text': text_content,
                        'prediction': pred
                    })
            
            context = {
                'results': results,
                'real_count': real_count,
                'fake_count': fake_count,
                'total_count': len(results)
            }
            return render(request, 'batch_result.html', context)
            
        except Exception as e:
            return render(request, 'home.html', {'error': f"Error processing file: {str(e)}"})
            
    return render(request, 'home.html')

import requests

def latest_news(request):
    api_key = "635ac2e8ac7c1bf92f8ae662864d392f" 
    # Fetching latest English news using Mediastack API
    # Params: languages=en, sort=published_desc, limit=25
    url = f"http://api.mediastack.com/v1/news?access_key={api_key}&languages=en&sort=published_desc&limit=25"
    
    news_items = []
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Log payload for debugging
        with open("debug_api.txt", "w") as f:
            f.write(f"Status Code: {response.status_code}\n")
            f.write(f"Response: {response.text}\n")

        # Mediastack returns 'data' list instead of 'results'
        if 'data' in data:
            articles = data.get('data', [])
            
            for article in articles:
                # Combine title and description for better context
                title = article.get('title', '')
                description = article.get('description', '')
                 # Handle None values
                if title is None: title = ""
                if description is None: description = ""

                content = f"{title}. {description}"
                
                # Predict
                cleaned = clean_text(content)
                # Check for short text (same logic as single prediction)
                is_short = len(cleaned.split()) < 20 # Lower threshold for aggregated list
                
                if cleaned:
                    tfidf = vectorizer.transform([cleaned])
                    pred = model.predict(tfidf)[0]
                else:
                    pred = "UNKNOWN"
                
                # Map Mediastack fields to our template structure
                news_items.append({
                    'title': title,
                    'description': description,
                    'link': article.get('url'),        # Mediastack uses 'url'
                    'image_url': article.get('image'), # Mediastack uses 'image'
                    'source_id': article.get('source'), # Mediastack uses 'source' (string)
                    'pubDate': article.get('published_at'), # Mediastack uses 'published_at'
                    'prediction': pred,
                    'is_short': is_short
                })
        else:
            print(f"API Error/No Data: {data}")
            if 'error' in data:
                 # Capture specific API error message
                error_msg = data['error'].get('info', 'Unknown API Error')
                context = {'news_items': [], 'api_error': f"API Error: {error_msg}"}
                return render(request, 'latest_news.html', context)
            
    except Exception as e:
        print(f"Fetch Error: {e}")
        return render(request, 'latest_news.html', {'news_items': [], 'api_error': f"Connection Error: {str(e)}"})

    return render(request, 'latest_news.html', {'news_items': news_items})
