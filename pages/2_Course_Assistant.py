import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os

st.title("Course Assistant")

# Verify login
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("🚫 You must log in first.")
    st.stop()

try:
    # --- Load Parameters ---
    apikey = st.secrets["OPENAI"]["OPENAI_API_KEY"]

    # --- Load FAISS Vectorstore ---
    PERSIST_DIR = "./faiss_db"  # Update path if needed
    embeddings = OpenAIEmbeddings(api_key=apikey, model="text-embedding-3-small")

    if not os.path.exists(PERSIST_DIR):
        st.error(f"❌ FAISS database not found at `{PERSIST_DIR}`. Please upload course data first.")
        st.stop()

    vectorstore = FAISS.load_local(PERSIST_DIR, embeddings)

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
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=apikey)
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
    st.error("❌ An error has occurred, please inform the team creators")
    print(f"Course Assistant Page Error: {e}")
