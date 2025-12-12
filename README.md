# Fake News Detection System

## Overview
This project uses Machine Learning (PassiveAggressiveClassifier) and Django to classify news articles as **REAL** or **FAKE**.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   cd FakeNewsDetector
   python manage.py runserver
   ```

3. Open your browser at `http://127.0.0.1:8000`.

## Features
- **Instant Analysis**: Check individual articles.
- **Batch Upload**: Upload CSV files for bulk API processing.

## Tech Stack
- **Backend**: Django
- **ML**: Scikit-Learn, Pandas, TfidfVectorizer
- **Frontend**: Bootstrap 5
