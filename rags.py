

# Importing necessary libraries
import os
import textwrap
from IPython.display import Markdown
from docx import Document
import google.generativeai as genai
from google.colab import drive
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

class RAGSystem:
    def __init__(self, google_api_key, document_path, gemini_model_name="gemini-pro", embedding_model_name="models/embedding-001", temperature=1, chunk_size=700, chunk_overlap=100):
        self.google_api_key = google_api_key
        self.document_path = document_path
        self.gemini_model_name = gemini_model_name
        self.embedding_model_name = embedding_model_name
        self.temperature = temperature
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def mount_drive(self):
        """
        Mounts Google Drive to access files.
        """
        drive.mount('/content/drive')

    def to_markdown(self, text, bullet_point='*', blockquote_symbol='> '):
        """
        Converts a given text to Markdown format.
        """
        if not isinstance(text, str):
            raise ValueError("Input must be a string")

        # Replace bullet points and handle new lines for blockquotes
        wrapped_text = text.replace('•', f'  {bullet_point}')
        wrapped_text = textwrap.indent(wrapped_text, blockquote_symbol, lambda line: True)

        return Markdown(wrapped_text)

    def load_and_split_document(self):
        """
        Loads a document and splits it into pages.
        """
        _, file_extension = os.path.splitext(self.document_path)
        if file_extension.lower() == '.pdf':
            pdf_loader = PyPDFLoader(self.document_path)
            return pdf_loader.load_and_split()
        elif file_extension.lower() == '.docx':
            doc = Document(self.document_path)
            pages = [paragraph.text for paragraph in doc.paragraphs]
            return pages
        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")

    def setup_gemini_model(self):
        """
        Sets up the Gemini model for text generation.
        """
        return ChatGoogleGenerativeAI(model=self.gemini_model_name, google_api_key=self.google_api_key, temperature=self.temperature, convert_system_message_to_human=True)

    def create_embeddings_and_index(self, texts):
        """
        Creates embeddings for texts and builds a vector index for retrieval.
        """
        embeddings = GoogleGenerativeAIEmbeddings(model=self.embedding_model_name, google_api_key=self.google_api_key)
        vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k":5})
        return vector_index

    def create_rag_qa_chain(self, model, vector_index):
        """
        Creates a Retrieval-Augmented Generation QA chain.
        """
        return RetrievalQA.from_chain_type(model, retriever=vector_index, return_source_documents=True)

    def main(self):
        """
        Main function to execute the RAG workflow.
        """
        self.mount_drive()
        pages = self.load_and_split_document()

        # Splitting text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        context = "\n\n".join(pages)
        chunks = text_splitter.split_text(context)

        # Setting up the Gemini model and embeddings
        gemini_model = self.setup_gemini_model()
        vector_index = self.create_embeddings_and_index(chunks)

        # Creating RAG QA Chain
        qa_chain = self.create_rag_qa_chain(gemini_model, vector_index)

        # Example Usage
        question = "What is an inlier?"
        result = qa_chain({"query": question})
        print("Answer:", result["result"])

# Constants
GOOGLE_API_KEY = ''
DOCUMENT_PATH = ""

# Create RAGSystem instance and execute main function
rag_system = RAGSystem(google_api_key=GOOGLE_API_KEY, document_path=DOCUMENT_PATH)
rag_system.main()

