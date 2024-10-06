import openai_secrets
import openai
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

file_path = "transcription_result.txt"

loader = TextLoader(file_path)
documents = loader.load()

embeddings = OpenAIEmbeddings()
vector_store = Chroma.from_documents(documents, embeddings)

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0),
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 1})
)

question = "What are the main topics in this transcription, and the timestamps?"
response = qa_chain.invoke(question)

print(response['result'])