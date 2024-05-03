# RAG test

This project implements a local RAG, where both the retrieval and generational models are run locally

## Getting Started

### Prerequisites

In order to be able to invoke a llm we need to download and run it somewhere. For this we will use Ollama which allows
us to download and run pretrained open source large language models such as Llama3, Phi3, Mistar, Gemma etc. 

* Download and install [Ollama](https://ollama.com/download)
* Open the Ollama CLI and type `ollama run llama3`

This will automatically clone and run the llama3 model. You can of course use any other model that your computer can run. 
We can now call this model using Langchain

Also install python 3.1 and pip install a bunch of stuff from a terminal with admin rights

### Starting the RAG backend

After the LLM is up and running we can start the RAG backend. It is responsible for encoding the corpus,
listening to incoming questions, searching the corpus for relevant data, sending the question and data
to the LLM and then returning the answer to the frontend. To start the backend go to the rag folder
and type `python rag.py`

### Starting the frontend

Go to the frontend folder and run `npm run dev`