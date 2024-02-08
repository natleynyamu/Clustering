import streamlit as st  # Import the Streamlit library
import requests  # Import the requests library for making HTTP requests
from sklearn.feature_extraction.text import TfidfVectorizer  # Import TF-IDF vectorizer
from sklearn.cluster import KMeans  # Import K-means clustering algorithm

# Function to fetch news articles from the News API
def fetch_news(api_key, query, sources=None, language='en', page_size=100):
    url = 'https://newsapi.org/v2/everything'  # Define the News API endpoint
    params = {  # Define query parameters
        'q': query,
        'sources': sources,
        'language': language,
        'pageSize': page_size,
        'apiKey': api_key
    }
    response = requests.get(url, params=params)  # Make GET request to News API
    data = response.json()  # Parse JSON response
    articles = [article['content'] for article in data.get('articles', [])]  # Extract article content
    return articles

# Function to preprocess news articles
def preprocess_articles(articles):
    # Perform preprocessing steps like tokenization, removing stopwords, etc.
    # For simplicity, we'll just convert text to lowercase
    return [article.lower() for article in articles]

# Function to cluster news articles
def cluster_articles(articles, num_clusters=5):
    # Vectorize the text using TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(articles)
    
    # Apply K-means clustering
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(tfidf_matrix)
    
    # Assign cluster labels to articles
    cluster_labels = kmeans.labels_
    
    # Organize articles into clusters
    clustered_articles = {}
    for i, label in enumerate(cluster_labels):
        if label not in clustered_articles:
            clustered_articles[label] = []
        clustered_articles[label].append(articles[i])
    
    return clustered_articles

# Streamlit web app code
st.title('News Article Clustering')  # Set title of the Streamlit app

# Get user input for query and number of clusters
query = st.text_input('Enter search query:', 'food')  # Input widget for search query
num_clusters = st.slider('Number of clusters:', min_value=2, max_value=10, value=5)  # Slider for number of clusters

# Fetch news articles from the News API
api_key = '2c4e8e1e899b4a96b9f5b18692cc595c'  
articles = fetch_news(api_key, query)

# Preprocess and cluster the articles
preprocessed_articles = preprocess_articles(articles)
clustered_articles = cluster_articles(preprocessed_articles, num_clusters)

# Display clustered articles
for cluster_id, cluster_articles in clustered_articles.items():
    st.subheader(f'Cluster {cluster_id}:')  # Add heading for each cluster
    # Create columns to organize articles into a grid layout
    col1, col2, col3 = st.columns(3)
    for i, article in enumerate(cluster_articles):
        # Alternate between columns for better distribution of articles
        if i % 3 == 0:
            st.write(f"**{i+1}.** {article}", unsafe_allow_html=True)
        elif i % 3 == 1:
            col2.write(f"**{i+1}.** {article}", unsafe_allow_html=True)
        else:
            col3.write(f"**{i+1}.** {article}", unsafe_allow_html=True)
    st.markdown('---')  # Add horizontal line between clusters
