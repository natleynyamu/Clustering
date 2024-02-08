# Import necessary libraries
import streamlit as st
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Function to search for images on Unsplash
def search_images(query, client_id, per_page=10):
    url = 'https://api.unsplash.com/search/photos'  # Defining the endpoint URL for the Unsplash API

    # Setting up the parameters for the API request
    params = {
        'query': query,
        'per_page': per_page,
        'client_id': client_id
    }
    try:
        # Sending a GET request to the API endpoint with the specified parameters
        response = requests.get(url, params=params)
        # Raising an exception if there's an error with the request
        response.raise_for_status()
        # Parsing the JSON response into a Python dictionary
        data = response.json()
        # Extracting the list of image results from the response data, or return an empty list if no results
        return data.get('results', [])
    except requests.RequestException as e:
        # Displaying an error message if there's an issue with fetching images
        st.error(f"Error fetching images: {e}")
        return []

# Function to perform K-means clustering on image features
def perform_clustering(images, num_clusters=5):
    # Extracting alt descriptions from images to use as features for clustering
    features = [image['alt_description'] for image in images]
    # Initializing TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()
    # Fit and transform the TF-IDF matrix using the alt descriptions
    tfidf_matrix = tfidf_vectorizer.fit_transform(features)
    
    # Initializig KMeans clustering algorithm with the specified number of clusters
    kmeans = KMeans(n_clusters=num_clusters)
    # Fit the KMeans model to the TF-IDF matrix
    kmeans.fit(tfidf_matrix)
    
    # Getting cluster labels assigned to each image
    cluster_labels = kmeans.labels_
    return cluster_labels

# Main function
def main():
    # Setting the title of the web app
    st.title('Image Search and Clustering')

    # Setting an Unsplash API client ID 
    client_id = '0pgQM7-rB8Ax95boW-roStFO5xUikhiIwL1zFkMs880'

    # Prompt the user to enter a search query for images
    query = st.text_input('Enter search query:', 'nature')

    # Prompt the user to select the number of images to search for
    num_images_to_search = st.slider('Number of images to search:', min_value=1, max_value=50, value=10)

    # Prompt the user to select the number of clusters for image clustering
    num_clusters = st.slider('Number of clusters:', min_value=2, max_value=10, value=5)

    # Check if the search button is clicked
    if st.button('Search'):
        # Fetch images based on the search query and number of images to search for
        images = search_images(query, client_id, per_page=num_images_to_search)
        # Check if any images are found
        if not images:
            # Display a warning message if no images are found
            st.warning("No images found.")
        else:
            # Display the total number of images found
            st.write(f"Found {len(images)} images for '{query}':. They are clustered below")

            # Check if the number of clusters is valid
            if len(images) < num_clusters:
                # Display a warning message if the number of clusters exceeds the number of images
                st.warning("Number of clusters cannot exceed the number of images.")
            else:
                # Perform clustering on the images
                cluster_labels = perform_clustering(images, num_clusters=num_clusters)

                # Display images with captions based on clusters
                for cluster_id in range(num_clusters):
                    # Display subheader for each cluster
                    st.subheader(f'Cluster {cluster_id + 1}:')
                    # Extract images belonging to the current cluster
                    cluster_images = [images[i] for i, label in enumerate(cluster_labels) if label == cluster_id]
                    # Calculate the number of rows needed to display the images in a grid
                    num_rows = (len(cluster_images) - 1) // 4 + 1
                    # Display images in a grid layout
                    for i in range(num_rows):
                        row_images = cluster_images[i * 4: (i + 1) * 4]
                        col1, col2, col3, col4 = st.columns(4)
                        for j, image in enumerate(row_images):
                            with locals()[f"col{j+1}"]:
                                # Display each image with its alt description as caption
                                st.image(image['urls']['small'], caption=image['alt_description'], width=150)

if __name__ == "__main__":
    main()
