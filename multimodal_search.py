# from haystack.document_stores import InMemoryDocumentStore
# from haystack.nodes.retriever.multimodal import MultiModalRetriever
# from googleapiclient.discovery import build
# from google_auth import google_login
# from haystack import Document
# from haystack import Pipeline
# import hashlib
# import requests
# from PIL import Image
# from io import BytesIO
# import os

# class MultimodalSearch:
#     def __init__(self):
#         # Initialize the DocumentStore to store 512 dim image embeddings
#         self.document_store = InMemoryDocumentStore(embedding_dim=512)

#         # Initialize Google Photos service
#         creds = google_login()
#         self.google_photos_service = build('photoslibrary', 'v1', static_discovery=False, credentials=creds)

#         self.retriever_text_to_image = MultiModalRetriever(
#             document_store=self.document_store,
#             query_embedding_model="sentence-transformers/clip-ViT-B-32",
#             query_type="text",
#             document_embedding_models={"image": "sentence-transformers/clip-ViT-B-32"},
#         )

#         # Load images from Google Photos and create embeddings
#         self.load_images_from_google_photos()

#         self.pipeline = Pipeline()
#         self.pipeline.add_node(component=self.retriever_text_to_image, name="retriever_text_to_image", inputs=["Query"])

#     def download_image(self, url, save_path='downloaded_images'):
#         if not os.path.exists(save_path):
#             os.makedirs(save_path)
#         response = requests.get(url)
#         if response.status_code == 200:
#             image = Image.open(BytesIO(response.content))
#             # Create a unique filename using a hash of the URL
#             file_name = hashlib.md5(url.encode()).hexdigest() + '.jpg'
#             file_path = os.path.join(save_path, file_name)
#             image.save(file_path)
#             return file_path
#         else:
#             return None

#     def load_images_from_google_photos(self):
#         # Fetch images from Google Photos
#         results = self.google_photos_service.mediaItems().list().execute()
#         for item in results['mediaItems']:
#             image_url = item['baseUrl']
#             local_image_path = self.download_image(image_url)
#             if local_image_path:
#                 doc = Document(content=local_image_path, content_type="image")
#                 self.document_store.write_documents([doc])

#         self.document_store.update_embeddings(retriever=self.retriever_text_to_image)

#     def search(self, query, top_k=15):
#         results = self.pipeline.run(query=query, params={"retriever_text_to_image": {"top_k": top_k}})
#         return sorted(results["documents"], key=lambda d: d.score, reverse=True)


from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes.retriever.multimodal import MultiModalRetriever
from googleapiclient.discovery import build
from google_auth import google_login
from haystack import Document
from haystack import Pipeline
import requests
from PIL import Image
from io import BytesIO
import os
import hashlib

class MultimodalSearch:
    def __init__(self, images_folder='downloaded_images'):
        # Initialize the DocumentStore to store 512 dim image embeddings
        self.document_store = InMemoryDocumentStore(embedding_dim=512)

        # Initialize Google Photos service
        creds = google_login()
        self.google_photos_service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

        self.images_folder = images_folder
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)

        self.retriever_text_to_image = MultiModalRetriever(
            document_store=self.document_store,
            query_embedding_model="sentence-transformers/clip-ViT-B-32",
            query_type="text",
            document_embedding_models={"image": "sentence-transformers/clip-ViT-B-32"},
        )

        # Load images from Google Photos and create embeddings
        self.load_images_from_google_photos()

        self.pipeline = Pipeline()
        self.pipeline.add_node(component=self.retriever_text_to_image, name="retriever_text_to_image", inputs=["Query"])

    def download_image(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            # Create a unique filename using a hash of the URL
            file_name = hashlib.md5(url.encode()).hexdigest() + '.jpg'
            file_path = os.path.join(self.images_folder, file_name)
            image.save(file_path)
            return file_path
        else:
            return None

    # def load_images_from_google_photos(self):
    # # Start with no page token
    #     page_token = None
    #     while True:
    #         # Fetch images from Google Photos
    #         results = self.google_photos_service.mediaItems().list(pageToken=page_token).execute()
    #         for item in results.get('mediaItems', []):
    #             image_url = item['baseUrl']
    #             local_image_path = self.download_image(image_url)
    #             if local_image_path:
    #                 doc = Document(content=local_image_path, content_type="image")
    #                 self.document_store.write_documents([doc])

    #         # Check if there is a next page
    #         page_token = results.get('nextPageToken')
    #         if not page_token:
    #             break

    #     self.document_store.update_embeddings(retriever=self.retriever_text_to_image)
        
    def load_images_from_google_photos(self):
        page_token = None
        total_images = 0
        max_images = 35  # Maximum number of images to fetch

        while total_images < max_images:
            # Fetch images from Google Photos
            results = self.google_photos_service.mediaItems().list(pageToken=page_token).execute()

            # Process each image in the results
            for item in results.get('mediaItems', []):
                if total_images >= max_images:
                    break  # Break if maximum number of images reached

                image_url = item['baseUrl']
                local_image_path = self.download_image(image_url)
                if local_image_path:
                    doc = Document(content=local_image_path, content_type="image")
                    self.document_store.write_documents([doc])
                    total_images += 1

            # Check if there is a next page
            page_token = results.get('nextPageToken')
            if not page_token:
                break  # Break if no more pages to fetch

        self.document_store.update_embeddings(retriever=self.retriever_text_to_image)


    def search(self, query, top_k=3):
        results = self.pipeline.run(query=query, params={"retriever_text_to_image": {"top_k": top_k}})
        return sorted(results["documents"], key=lambda d: d.score, reverse=True)
