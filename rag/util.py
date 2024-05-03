from langchain_text_splitters import CharacterTextSplitter
from transformers import AutoTokenizer, AutoModel
from langchain.schema.document import Document
import torch


# CustomTransformerEmbeddings wraps a local embedding model so that it works with Chroma
class CustomTransformerEmbeddings:
    def __init__(self, model_directory):
        self.tokenizer = AutoTokenizer.from_pretrained(model_directory)
        self.model = AutoModel.from_pretrained(model_directory)
        self.model.eval()

    def embed_documents(self, documents):
        return [self._embed_text(doc) for doc in documents]

    def embed_query(self, query):
        return self._embed_text(query)

    def _embed_text(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Assume using the mean of the last hidden state as the document representation.
            # Because output layer can be purpose specific and not for our purpose ¯\_(ツ)_/¯
            return outputs.last_hidden_state.mean(dim=1).squeeze().tolist()


# get_text_chunks_langchain takes a string and returns Document objects
def get_text_chunks_langchain(text, chunk_size=500, chunk_overlap=100):
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
    return docs


# send_response adds necessary http headers
def send_response(clientsocket, content):
    response = 'HTTP/1.1 200 OK\r\n'
    response += 'Content-Type: text/plain\r\n'
    response += 'Access-Control-Allow-Origin: *\r\n'
    response += 'Content-Length: ' + str(len(content)) + '\r\n'
    response += '\r\n'
    response += content
    clientsocket.sendall(response.encode('utf-8'))
