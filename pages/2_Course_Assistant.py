import streamlit as st
import re
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# --- Security Config ---
FORBIDDEN_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"hidden instructions",
    r"internal instructions",
    r"reveal secret",
    r"output hidden",
    r"hidden",
    r"revealing",
    r"python script",
    r"exfiltrate"
]

SENSITIVE_KEYWORDS = [
    "system instructions",
    "hidden instructions",
    "developer prompt",
    "template value",
    "API Key"
]

def is_suspicious(user_input: str) -> bool:
    """
    Detect if the user input contains prompt injection attempts.
    """
    user_input_lower = user_input.lower()
    return any(re.search(pattern, user_input_lower) for pattern in FORBIDDEN_PATTERNS)

def sanitize_output(output: str) -> str:
    """
    Redact any sensitive keywords accidentally revealed in the output.
    """
    sanitized = output
    for keyword in SENSITIVE_KEYWORDS:
        sanitized = re.sub(keyword, "[REDACTED]", sanitized, flags=re.IGNORECASE)
    return sanitized

# --- Streamlit UI ---
st.title("Course Assistant")

# --- Login Check ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("🚫 You must log in first.")
    st.stop()

try:
    # --- Load OpenAI API Key ---
    apikey = st.secrets["OPENAI"]["OPENAI_API_KEY"]

    # --- Load FAISS Vectorstore ---
    PERSIST_DIR = "./faiss_db"  # Path to your saved FAISS index
    embeddings = OpenAIEmbeddings(api_key=apikey, model='text-embedding-3-small')
    vectorstore = FAISS.load_local(
        folder_path=PERSIST_DIR,
        embeddings=embeddings,
        allow_dangerous_deserialization=True  # safe if you created this index
    )

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

    # --- RetrievalQA chain ---
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=apikey)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": qa_prompt}
    )

    # --- Streamlit UI for query ---
    st.title("🎓 Student Course & Career Advisor")
    st.write("Ask personalised questions like:")
    st.markdown("""
    - *Which course suits a career in AI and data science?*  
    - *What are the job prospects in the financial sector?*  
    - *Which diploma is best if I want to work in healthcare technology?*
    """)

    query = st.text_input("Type your query here:")

    if query:
        if is_suspicious(query):
            st.warning("⚠️ Your query contains suspicious instructions and cannot be processed.")
        else:
            with st.spinner("Thinking..."):
                response = qa_chain.run(query)
            sanitized_response = sanitize_output(response)
            st.subheader("💡 Recommendation")
            st.write(sanitized_response)

except Exception as e:
    st.error("❌ An error has occurred, please inform the team creators")
    print(f"Course Assistant Page Error: {e}")

with st.expander("Disclaimer"):
    disclaimer = """
    **IMPORTANT NOTICE**  
    This web application is a prototype developed for educational purposes only.  
    The information provided here is **NOT** intended for real-world usage and should not be relied upon for making decisions, especially financial, legal, or healthcare matters.  

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information.  
    You assume full responsibility for how you use any generated output.  

    Always consult with qualified professionals for accurate and personalized advice. 
    """
    st.markdown(disclaimer)
