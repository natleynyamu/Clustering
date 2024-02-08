# Clustering

## NewsClusteringApp
https://natleynyamu-clustering-news-clustering-app-asmdtl.streamlit.app/

This is a Streamlit web application that clusters news articles fetched from the News API based on their content similarity. It allows users to specify a search query and the number of clusters to generate.

### Features
- Fetches news articles from the News API based on user input.
- Preprocesses the articles by converting them to lowercase.
- Clusters the articles using the K-means algorithm.
- Displays the clustered articles in a visually appealing format.

### Installation
1. git clone https://github.com/natleynyamu/Clustering.git
2. cd Clustering
3. pip install -r requirements.txt
4. streamlit run news_clustering_app.py

### Usage
- Enter a search query in the text input field.
- Use the slider to select the number of clusters.
- View the clustered articles displayed in the app.




## ImageClusteringApp
This is a Streamlit web application that clusters product images retrieved from Unsplash based on their similarity. It allows users to specify a search query, the number of images to search for, and the number of clusters to generate.

### Features
- Searches for images on Unsplash based on user input.
- Clusters the images using the K-means algorithm.
- Displays the clustered images in a visually appealing format.

### Installation
1. git clone https://github.com/natleynyamu/Clustering.git
2. cd Clustering
3. pip install -r requirements.txt
4. streamlit run image_clustering_app.py

### Usage
- Enter a search query in the text input field.
- Use the sliders to select the number of images to search for and the number of clusters.
- Click the "Search" button to fetch and cluster images.
- View the clustered images displayed in the app.
