import os
import openai_secrets
import openai
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# file paths (transcription and pdfs)
transcription_file_path = "transcription_result.txt"
pdf_file_path = "pdf_files/"
pdf_files = [f for f in os.listdir(pdf_file_path) if f.endswith('.pdf')]

# load in transcription file as data
loader = TextLoader(transcription_file_path)
documents = loader.load()

# load in any pdf files as data
for pdf_file in pdf_files:
    pdf_loader = PyMuPDFLoader(os.path.join(pdf_file_path, pdf_file))
    documents.extend(pdf_loader.load()) 

# create vector embeddings to put data into
embeddings = OpenAIEmbeddings()
vector_store = Chroma.from_documents(documents, embeddings)

# create question chain, including llm, data from vector store
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0),
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 1})
)

# use llm to ask question
# question = "What are the main topics in this transcription, and the timestamps?" # example question, will be from the user
question = "What are the main topics discussed in the PDF documents?"
response = qa_chain.invoke(question)

print(response['result'])