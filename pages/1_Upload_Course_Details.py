import streamlit as st
import zipfile
import tempfile
import os
import pandas as pd
import chardet
from langchain.vectorstores import Chroma

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
#from dotenv import load_dotenv

# Streamlit app title
st.title("Upload Relevant Course Details")

#Verify if you are login as Admin user
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("🚫 You must log in first.")
    st.stop()
elif st.session_state["role"] != "Admin":
    st.error("🚫 Access denied! Only Admins can view this page.")
    st.stop()

try:
    #load_dotenv("env_variables.env")  # Load from .env
    #apikey = os.getenv("OPENAI_API_KEY")
    #model_name = os.getenv("OPENAI_MODEL_NAME")
    apikey = st.secrets["OPENAI"]["OPENAI_API_KEY"]
    #model_name = st.secrets["OPENAI_MODEL_NAME"]

    # --- Helper function to read CSV with encoding detection ---
    def read_csv_with_fallback(path):
        try:
            return pd.read_csv(path, encoding="utf-8")
        except UnicodeDecodeError:
            # Auto-detect encoding with chardet
            with open(path, "rb") as f:
                raw = f.read()
                result = chardet.detect(raw)
                enc = result["encoding"] or "latin1"
            return pd.read_csv(path, encoding=enc)


    uploaded_file = st.file_uploader("Upload a ZIP file containing CSVs", type=["zip"])

    if uploaded_file is not None:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save the uploaded zip file
            zip_path = os.path.join(tmpdir, "uploaded.zip")
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Extract all files in zipfile
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(tmpdir)

            st.success("✅ ZIP file extracted!")

            # Collect CSV files
            csv_files = [os.path.join(tmpdir, f) for f in os.listdir(tmpdir) if f.endswith(".csv")]
            st.write(f"Found **{len(csv_files)}** CSV files.")

            documents = []
            for csv_file in csv_files:
                df = read_csv_with_fallback(csv_file)
                csv_text = df.to_csv(index=False)
                documents.append(csv_text)

            # Split into chunks
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs = splitter.create_documents(documents)

            # ⚡ Persist Chroma outside the temp directory
            persist_directory = "./chroma_db"  # permanent folder

            #Initialise embeddings and store in Vectorstore
            embeddings = OpenAIEmbeddings(api_key=apikey,model='text-embedding-3-small')
            vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=embeddings,
                persist_directory=persist_directory
            )

            vectorstore.persist()

            st.success("✅ Chroma vectorstore created and persisted successfully!")
            st.write(f"Chroma database saved at: `{persist_directory}`")

          
except Exception as e:
    st.error("❌ An error has occured, please inform the team creators")
    print(f"Upload Course Details Page Error: {e}")