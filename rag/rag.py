from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import Ollama, OpenAI
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_chroma import Chroma
from transformers import AutoModel, AutoTokenizer
from util import CustomTransformerEmbeddings, send_response
import socket


# Load the model and tokenizer locally
print("Loading local model")
model_directory = "./embeddingModels/models/all-MiniLM-l6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_directory)
model = AutoModel.from_pretrained(model_directory)

# Load the corpus and split it into chunks
print("Loading corpus")
loader = PyPDFLoader("corpus/bygglovsregler.pdf")
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# Create an instance of the custom embedding class to work with Chroma
custom_embeddings = CustomTransformerEmbeddings(model_directory)

# Embed corpus using local embedding model
print("Embedding")
vectorstore = Chroma.from_documents(documents=all_splits, embedding=custom_embeddings)

# Connect to local llm. The llm should already be running using Ollama
print("Connect to local llm")
llm = Ollama(
    model="llama2", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)
instructions = ("You are a large language model that gets asked questions about building rules. You will receive "
                "relevant excerpts from the swedish building rule handbook. The question and instructions are in "
                "swedish.")


# Create a socket and listen on the specified port
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 9999
serversocket.bind((host, port))
serversocket.listen(5)
print(f"Server listening on port {port}")

while True:
    # Establish a connection
    clientsocket, addr = serversocket.accept()
    print("Got a connection from %s" % str(addr))

    # Receive the question
    question = clientsocket.recv(1024).decode('utf-8')
    if len(question) == 0:
        continue
    print("Received question: %s" % question)

    # Embed and do a similarity search for the user question
    print("Searching corpus for relevant data")
    docs = vectorstore.similarity_search(question)

    # Create prompt
    prompt = (
        instructions
        + "Here are the relevant excerpts from the handbook: "
        + str(docs)
        + " Here is the question: "
        + question
    )

    # Invoke local llm
    print("Sending prompt to llm")
    response = llm.invoke(prompt)

    # Send response back to client
    send_response(clientsocket, response)
    clientsocket.close()
