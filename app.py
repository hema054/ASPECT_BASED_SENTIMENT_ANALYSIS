from flask import Flask, render_template, request, jsonify # type: ignore
import pandas as pd # type: ignore
import nltk # type: ignore
from nltk.corpus import stopwords # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.svm import LinearSVC # type: ignore
import pickle
import numpy as np # type: ignore
import spacy # type: ignore
import os
from sklearn.svm import LinearSVC  # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.pipeline import Pipeline # type: ignore
import joblib # type: ignore
import string
from spacy.lang.en.stop_words import STOP_WORDS # type: ignore
from flask import Flask, request, jsonify, render_tempgit config --global user.email "you@example.com"
git config --global user.name "Your Name"late # type: ignore
from flask import session, redirect, url_for # type: ignore

app = Flask(__name__)


# Load models
with open('aspect_sentiment_model.pkl', 'rb') as model_file:
    sentiment_model = pickle.load(model_file)

with open('tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

stop_words = set(stopwords.words('english'))


@app.route('/rest1.html')
def rest1():
    return render_template('rest1.html')

@app.route('/rest1_1.html')
def rest1_1():
    return render_template('rest1_1.html')

@app.route('/rest2.html')
def rest2():
    return render_template('rest2.html')

@app.route('/rest3.html')
def rest3():
    return render_template('rest3.html')

@app.route('/rest4.html')
def rest4():
    return render_template('rest4.html')

@app.route('/rest5.html')
def rest5():
    return render_template('rest5.html')

@app.route('/rest6.html')
def rest6():
    return render_template('rest6.html')

@app.route('/Sign In.html')
def sign_in():
    return render_template('Sign In.html')

@app.route('/Sign Up.html')
def sign_up():
    return render_template('Sign Up.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/services.html')
def services():
    return render_template('services.html')




# Utility functions
def extract_aspects(text):
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    return [word for word, pos in pos_tags if pos in ['NN', 'NNS']]

def is_neutral(text):
    neutral_words = ["ok", "okay", "fine", "average", "mediocre", "fair"]
    return any(word in text.lower() for word in neutral_words)

def predict_aspect_sentiment(review):
    aspects = extract_aspects(review)
    sentences = nltk.sent_tokenize(review)
    results = {}
    for aspect in aspects:
        for sentence in sentences:
            if aspect in sentence:
                sentiment = sentiment_model.predict(vectorizer.transform([sentence]))[0]
                if sentiment == 0 or is_neutral(sentence):
                    results[aspect] = "neutral"
                else:
                    results[aspect] = "positive" if sentiment == 1 else "negative"
                break
    return results

def aggregate_sentiment(aspect_sentiments):
    score = sum([1 if s == "positive" else -1 if s == "negative" else 0 for s in aspect_sentiments.values()])
    return "positive" if score > 0 else "negative" if score < 0 else "neutral"



# ... [rest of the imports and model loading remains unchanged]

#to store review in Excel
# prev
# def store_review_in_excel(review_text):
#     filename = 'reviews.xlsx'
    
#     # Check if file already exists
#     try:
#         df = pd.read_excel(filename, engine='openpyxl')
#     except FileNotFoundError:
#         df = pd.DataFrame(columns=["Review"])

#     new_data = pd.DataFrame({"Review": [review_text]})
#     df = pd.concat([df, new_data], ignore_index=True)
#     df.to_excel(filename, index=False, engine='openpyxl')
def store_review_in_excel(restaurant, review_text, overall_sentiment, aspects):
    filename = 'reviews.xlsx'
    
    # Check if file already exists
    try:
        df = pd.read_excel(filename, engine='openpyxl')
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Restaurant", "Review", "Overall Sentiment", "Aspect", "Aspect Sentiment"])

    # For each aspect, create a new data entry
    data_entries = []
    for aspect, sentiment in aspects.items():
        data_entries.append({
            "Restaurant": restaurant,
            "Review": review_text,
            "Overall Sentiment": overall_sentiment,
            "Aspect": aspect,
            "Aspect Sentiment": sentiment
        })
    
    new_data = pd.DataFrame(data_entries)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(filename, index=False, engine='openpyxl')




#to show the stores data from excel file
# prev
# @app.route('/reviews', methods=['GET'])
# def show_reviews():
#     filename = 'reviews.xlsx'
#     try:
#         df = pd.read_excel(filename, engine='openpyxl')
#     except FileNotFoundError:
#         df = pd.DataFrame(columns=["Review"])
#     reviews = df['Review'].tolist()
#     return render_template('rest1_1.html', reviews=reviews)
# @app.route('/reviews', methods=['GET'])
# def show_reviews():
#     filename = 'reviews.xlsx'
#     try:
#         df = pd.read_excel(filename, engine='openpyxl')
#     except FileNotFoundError:
#         df = pd.DataFrame(columns=["Review", "Overall Sentiment", "Aspects", "Aspect Sentiments"])

#     data = [{
#         "review": row["Review"],
#         "overall_sentiment": row["Overall Sentiment"],
#         "aspects": row["Aspects"],
#         "aspect_sentiments": row["Aspect Sentiments"]
#     } for _, row in df.iterrows()]
    
#     return render_template('rest1_1.html', data=data)



@app.route('/', methods=['GET', 'POST'])
@app.route('/home.html')
def home():
    if request.method == 'POST':
        restaurant = request.form['restaurant']
        review = request.form['review']
        aspects = predict_aspect_sentiment(review)
        overall_sentiment = aggregate_sentiment(aspects)
        
        # Store the review in the Excel file
        # Store the review and other details in the Excel file
        store_review_in_excel(restaurant, review, overall_sentiment, aspects)
        return render_template('rest1.html', restaurant=restaurant, aspects=aspects, overall_sentiment=overall_sentiment, review=review)

    return render_template('home.html')
        


@app.route('/clear_history', methods=['POST'])
def clear_history():
    session['history'] = []  # Clear the session history
    return redirect(url_for('rest1'))

if __name__ == "__main__":
    app.run(debug=True)


# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         review = request.form['review']
#         aspects = predict_aspect_sentiment(review)
#         overall_sentiment = aggregate_sentiment(aspects)
#         return render_template('home.html', aspects=aspects, overall_sentiment=overall_sentiment, review=review)
#     return render_template('home.html')

# if __name__ == "__main__":
#     app.run(debug=True)