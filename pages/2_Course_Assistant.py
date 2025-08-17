import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate




#from dotenv import load_dotenv
#import os

st.title("Course Assistant")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("🚫 You must log in first.")
    st.stop()

try:
    # --- Load Parameters ---
    #load_dotenv("env_variables.env")  # Load from .env
    apikey = st.secrets["OPENAI"]["OPENAI_API_KEY"]
    #model_name = os.getenv("OPENAI_MODEL_NAME")

    # --- Load ChromaDB Vectorstore ---
    PERSIST_DIR = "./chroma_db"  # ensure this matches your saved path
    embeddings = OpenAIEmbeddings(api_key=apikey,model='text-embedding-3-small')
    vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)

    # --- Create retriever ---
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # --- Custom prompt for student-focused recommendations ---
    template = """
    You are a helpful academic advisor. 
    A prospective student is asking about courses, career goals, industry sectors, or job prospects. 
    Use the retrieved course information below to provide a personalised recommendation.

    Retrieved context:
    {context}

    Student query: {question}

    Answer helpfully and make specific course or career recommendations when possible.
    """
    qa_prompt = PromptTemplate.from_template(template)

    # --- RetrievalQA chain (RAG) ---
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3,api_key=apikey)  # small, fast model
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": qa_prompt}
    )

    # --- Streamlit UI ---
    st.title("🎓 Student Course & Career Advisor")

    st.write("Ask personalised questions like:")
    st.markdown("""
    - *Which course suits a career in AI and data science?*  
    - *What are the job prospects in the financial sector?*  
    - *Which diploma is best if I want to work in healthcare technology?*
    """)

    query = st.text_input("Type your query here:")

    if query:
        with st.spinner("Thinking..."):
            response = qa_chain.run(query)
        st.subheader("💡 Recommendation")
        st.write(response)
except Exception as e:
    st.error("❌ An error has occured, please inform the team creators")
    print(f"Course Assistant Page Error: {e}")