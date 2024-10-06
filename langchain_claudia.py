from openai_secrets1 import SECRET_KEY
import openai
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredPDFLoader


file_path = "transcription_result.txt"

loader = TextLoader(file_path)
documents = loader.load()


embeddings = OpenAIEmbeddings()
vector_store = Chroma.from_documents(documents, embeddings)

data = loader.load()
data[0]

set(doc.metadata["category"] for doc in data)

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0),
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 1})
)

# load pdf into the vector store then it will added ti the chain.

question = "What are the main topics in this transcription, and the timestamps?"
response = qa_chain.invoke(question)

print(response['result'])