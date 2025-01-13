import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Step 1: Load and Extract Text from PDF
def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents

# Step 2: Split Text into Chunks
def split_documents(documents, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)

# Step 3: Create Vector Store
def create_vector_store(documents, embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"):
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store

# Step 4: Set up the RetrievalQA Chain
def setup_qa_chain(vector_store):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    prompt_template = PromptTemplate(
        template="Answer the question based on the document: \n{context}\n\nQuestion: {question}\nAnswer:",
        input_variables=["context", "question"]
    )
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0)  # Replace with your LLM API call if needed
    chain = RetrievalQA(llm=llm, retriever=retriever, prompt_template=prompt_template)
    return chain

# Step 5: Query the Chain
def query_chain(chain, question):
    response = chain.run(question)
    return response

# Main Function
def main():
    pdf_path = "your_document.pdf"  # Replace with your PDF file path
    
    # Load and preprocess PDF
    print("Loading and preprocessing PDF...")
    documents = load_pdf(pdf_path)
    split_docs = split_documents(documents)

    # Create vector store
    print("Creating vector store...")
    vector_store = create_vector_store(split_docs)

    # Set up RetrievalQA chain
    print("Setting up QA chain...")
    qa_chain = setup_qa_chain(vector_store)

    # Query the chain
    print("Ready to answer questions.\n")
    while True:
        question = input("Enter your question (or 'exit' to quit): ")
        if question.lower() == "exit":
            break
        response = query_chain(qa_chain, question)
        print(f"\nAnswer: {response}\n")

if __name__ == "__main__":
    main()




# Modify this function to use your LLM API
def call_llm_api(context, question):
    # Combine context and question into a single input
    input_text = f"Answer the question based on the document: \n{context}\n\nQuestion: {question}\nAnswer:"
    # Call your LLM API function here and return the output
    response = your_llm_api_function(input_text)  # Replace with actual API function
    return response

# Modified query function
def query_chain(vector_store, question):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})  # Retrieve top 3 chunks
    docs = retriever.get_relevant_documents(question)
    
    # Combine the content of retrieved documents for the context
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Call your LLM API
    answer = call_llm_api(context, question)
    return answer

