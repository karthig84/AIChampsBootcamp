import streamlit as st
from PIL import Image
import os

# Set page title
st.set_page_config(page_title="Methodology", layout="wide")
st.title("Methodology for Application Flows")

# List of images and descriptions
diagrams = [
    {
        "file": "images/High_Level_program_flow.jpg",
        "title": "Diagram 1 – Login & Role Selection",
        "desc": "This flow ensures that only authenticated users can proceed. Users select their role (Admin or Student) and provide credentials. If login is unsuccessful, the system prompts for correction before granting access."
    },
    {
        "file": "images/Course_Upload_Details_flow.jpg",
        "title": "Diagram 2 – Admin: Course Upload Flow",
        "desc": "Admins upload course datasets, as ZIP files containing multiple CSVs. The system extracts, chunks, encodes, and stores the data into a local vector store. This structured storage enables later retrieval for recommendations."
    },
    {
        "file": "images/Course_Assistant_flow.jpg",
        "title": "Diagram 3 – Data Dashboard Flow",
        "desc": "Admin or user can select stored datasets for analysis and visualization. The system generates dashboards on key indicators such as enrolment and graduation breakdown by gender and course, diploma fees, employment outcomes, and median salaries by course cluster."
    },
    {
        "file": "images/Data_Dashboard_flow.jpg",
        "title": "Diagram 4 – User: Course Assistant Flow",
        "desc": "Students enter queries related to courses, career goals, or job prospects. The system retrieves relevant data from the vector store and passes it to an LLM with tailored academic advisor instructions. The LLM then generates personalised recommendations, which are returned to the student."
    },
]

# Display each diagram in a clean layout
for diagram in diagrams:
    if os.path.exists(diagram["file"]):
        image = Image.open(diagram["file"])
        
        # Numbered header
        st.subheader(diagram["title"])
        
        # Side-by-side layout
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(image, use_container_width=True)
        with col2:
            st.markdown(diagram["desc"])
        
        st.markdown("---")  # separator line
    else:
        st.warning(f"{diagram['file']} not found in the project folder.")
