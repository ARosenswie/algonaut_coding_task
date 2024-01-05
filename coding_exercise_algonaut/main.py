import openai
import urllib.request
import streamlit as st
import time
import xml.etree.ElementTree as ET

# Read data from the data folder
def fetch_papers():
    url = 'http://export.arxiv.org/api/query?search_query=ti:llama&start=0&max_results=70'
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    root = ET.fromstring(data)
    papers_list = []

    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        paper_info = f"Title: {title}\nSummary: {summary}\n"
        papers_list.append(paper_info)
    # Sleep for three seconds. This is in accorcdance with the arXiv API Limitation guidelines
    time.sleep(3)
    return papers_list

# Generate embeddings using text-davinci-003 model
def generate_embeddings(texts, api_key):
    openai.api_key = api_key
    embeddings = openai.Completion.create(
        model="text-davinci-003", # My choice of model due to past familiarity
        prompt=texts[:4096],  # Max input size of tokens
        temperature=0, # Set to 0 to force concise output
        max_tokens=1024
    )
    return embeddings['choices'][0]['text'] # Returns the embeddings

# Answer a question based upon the embeddings
def answer_question(question, embeddings, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{embeddings}\n\nQuestion: {question}\nAnswer:",
        temperature=0.1, # Set to 0.1 to have conise responses.
        max_tokens=1024 # maximum number of tokens to generate for the output
    )
    return response['choices'][0]['text'] # Returns the answer from the model

st.markdown("# Information Gathering from self-collected Embeddings")
st.write("Designed and written by Andrew Rosenswie")

st.markdown("#### Please enter your OpenAI API key below:")
openai_api_key = st.text_input("", type="password")

texts = fetch_papers()
text_prompt = '\n'.join(texts)
embeddings = generate_embeddings(text_prompt, openai_api_key)
st.markdown("#### Please enter your question about Llama-2 below:")
user_question = st.text_input("")

if user_question:
    answer = answer_question(user_question, embeddings, openai_api_key)
    st.markdown("#### Answer:")
    st.write(answer)