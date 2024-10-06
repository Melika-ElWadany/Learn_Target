import openai
#from langchain.chat_models import ChatOpenAI DEPRICATED
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import RetryOutputParser
from langchain.chains import RetrievalQA
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import asyncio
from langchain_community.chat_models import ChatOpenAI

import os
import time
from getpass import getpass

import kdbai_client as kdbai
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import KDBAI

# Function to load documents asynchronously
async def load_documents(loader):
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    return pages

async def main():
    # Path to your PDF
    file_path = "/Users/USER_ADMIN/Desktop/Csc332 Class/LABS/Lab3.pdf"
    
    # Load the PDF asynchronously
    loader = UnstructuredPDFLoader(file_path)
    docs = await load_documents(loader)

    # Check document metadata
    print(docs[0].metadata)

    # Create embeddings for documents
    embeddings = OpenAIEmbeddings()

    # Create a vector store (Chroma) from documents and their embeddings
    vector_store = Chroma.from_documents(docs, embeddings)

    # Set up a QA chain with retrieval
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0),
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 1})
    )

    # Query the chain with a question
    question = "What are the main topics in this transcription, and the timestamps?"
    response = qa_chain.invoke({"input": question})

    # Print the response
    print(response['result'])

# Run the async main function
asyncio.run(main())
