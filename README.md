# Retrieval-Augmented-Generation-RAG-System
RAG System: Retrieval-Augmented Generation with Google's Generative AI and LangChain

 Retrieval-Augmented Generation (RAG) System

This repository contains a Python script implementing a Retrieval-Augmented Generation (RAG) system using Google's Generative AI and LangChain. The RAGSystem class encapsulates the functionality for loading documents, setting up models, creating embeddings, and performing QA tasks.

## Features

- Load and split PDF or DOCX documents into pages.
- Set up the Gemini model for text generation.
- Create embeddings for text chunks and build a vector index for retrieval.
- Perform retrieval-augmented generation QA tasks.

## Requirements

- Python 3.9
- Google Colab (for mounting Google Drive)
- Dependencies:
  - `google.generativeai`
  - `langchain_community`
  - `langchain_google_genai`
  - `docx`

## Usage

1. Clone the repository or copy the `rag_system.py` file into your project directory.
2. Import the `RAGSystem` class into your Python script.
3. Instantiate the `RAGSystem` class with the required parameters (Google API key and document path).
4. Call the `main()` method to execute the RAG workflow.

Example:

```python
from rag_system import RAGSystem

# Constants
GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'
DOCUMENT_PATH = "/path/to/your/document.docx"

# Create RAGSystem instance and execute main function
rag_system = RAGSystem(google_api_key=GOOGLE_API_KEY, document_path=DOCUMENT_PATH)
rag_system.main()


Note

    Replace 'YOUR_GOOGLE_API_KEY' with your actual Google API key.
    Ensure that your document path is correct and points to a valid DOCX file.
