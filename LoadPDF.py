from openai_secrets1 import SECRET_KEY
import openai
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredPDFLoader


from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


file_path = "/Users/USER_ADMIN/Desktop/Csc332 Class/LABS/Lab3.pdf"
loader = UnstructuredPDFLoader(file_path)
docs = loader.load()
docs[0]

embeddings = OpenAIEmbeddings()
vector_store = Chroma.from_documents(docs, embeddings)


qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0),
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 1})
)
# Json bidy structure with post request route.
# load pdf into the vector store then it will added ti the chain.

question = "What are the main topics in this transcription, and the timestamps?"
response = qa_chain.invoke(question)

print(response['result'])