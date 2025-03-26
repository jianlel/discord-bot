import openai 
import os

from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS 
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from dotenv import load_dotenv

from utils import process_chat_logs

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

chat_text = str(process_chat_logs("chatlog\cleaned_whatsapp_chat_hursh.txt"))

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.create_documents([chat_text])

embedding_model = OpenAIEmbeddings()
embeddings = embedding_model.embed_documents([doc.page_content for doc in docs])

vector_db = FAISS.from_documents(docs, embedding_model)

vector_db.save_local("database/hursh_db")