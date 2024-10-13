from flask import Flask, request, render_template, jsonify
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

newsgroups = fetch_20newsgroups(subset='all')

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(newsgroups.data)

svd = TruncatedSVD(n_components=100)  # You can adjust n_components as needed
X_reduced = svd.fit_transform(X)

def process_query(query):
    query_vec = vectorizer.transform([query])
    query_reduced = svd.transform(query_vec)
    return query_reduced

def get_top_documents(query_reduced, X_reduced, top_n=5):
    cosine_sim = cosine_similarity(query_reduced, X_reduced)
    top_docs = cosine_sim.argsort()[0][-top_n:][::-1]
    return top_docs, cosine_sim[0][top_docs]


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    query_reduced = process_query(query)

    top_docs, scores = get_top_documents(query_reduced, X_reduced)
    scores = scores.tolist() if isinstance(scores, np.ndarray) else scores

    results_html = render_template('results.html', 
                                   query=query, 
                                   documents=[newsgroups.data[i] for i in top_docs], 
                                   scores=scores, 
                                   zip=zip)
    
    return jsonify({
        'html': results_html,  # The rendered HTML for the results section
        'scores': scores       # The similarity scores for the bar chart
    })
    # return render_template('results.html', query=query, documents=[newsgroups.data[i] for i in top_docs], scores=scores, zip=zip)
