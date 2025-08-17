import streamlit as st
import pandas as pd

st.title("About us - Data information")

st.markdown("""
### Available Data and Samples
The data collected are publicly available and the datasets from data.gov.sg include both the data dictionary and sample data with the links are provided. 
For the other two datasets that do not include these, the information are provided below for reference.
            
https://data.gov.sg/datasets/d_64e1695700519d4c8998689f259c2af7/view 
https://data.gov.sg/datasets/d_47fb406d7f66774bfc19c6bc7a903c08/view
https://data.gov.sg/datasets/d_8a85a5c3982306278f3c98c1d973996e/view
https://data.gov.sg/datasets/d_cede40b47cc51ab5c94168c323bc55ba/view
https://data.gov.sg/datasets/d_4f4214e1c94b5132bd25aace0be0fb77/view
https://www.np.edu.sg/docs/default-source/np-articles/media-releases/poly-ges-2024---media-release.pdf?sfvrsn=c36c4613_3\n
https://www.np.edu.sg/schools-courses/full-time-courses

""")

st.markdown("#### Data Dictionary for Graduate Employment Data\nhttps://www.np.edu.sg/docs/default-source/np-articles/media-releases/poly-ges-2024---media-release.pdf?sfvrsn=c36c4613_3")

# Create the DataFrame
data_dict = [
    {"Column Name": "Indicator", "Description": "The employment or work status category of graduates", "Data Type": "String", "Notes": "Examples: Employed, In Full-Time Permanent Employment, Freelancing, etc."},
    {"Column Name": "Fresh Graduates 2022", "Description": "Percentage of fresh graduates in 2022 falling under the corresponding Indicator", "Data Type": "Float (percentage)", "Notes": "Values stored as numeric percentages (e.g., 91.4 for 91.4%)"},
    {"Column Name": "Fresh Graduates 2023", "Description": "Percentage of fresh graduates in 2023 falling under the corresponding Indicator", "Data Type": "Float (percentage)", "Notes": ""},
    {"Column Name": "Fresh Graduates 2024", "Description": "Percentage of fresh graduates in 2024 falling under the corresponding Indicator", "Data Type": "Float (percentage)", "Notes": ""},
    {"Column Name": "Post-NS (PNS) Graduates 2022", "Description": "Percentage of post-NS (PNS) graduates in 2022 falling under the corresponding Indicator", "Data Type": "Float (percentage)", "Notes": ""},
    {"Column Name": "Post-NS (PNS) Graduates 2023", "Description": "Percentage of post-NS (PNS) graduates in 2023 falling under the corresponding Indicator", "Data Type": "Float (percentage)", "Notes": ""},
    {"Column Name": "Post-NS (PNS) Graduates 2024", "Description": "Percentage of post-NS (PNS) graduates in 2024 falling under the corresponding Indicator", "Data Type": "Float (percentage)", "Notes": ""},
    {"Column Name": "Combined (Fresh and PNS Graduates) 2022", "Description": "Percentage of all graduates (Fresh + PNS) in 2022 falling under the corresponding Indicator", "Data Type": "Float (percentage)", "Notes": ""},
    {"Column Name": "Combined (Fresh and PNS Graduates) 2023", "Description": "Percentage of all graduates (Fresh + PNS) in 2023 falling under the corresponding Indicator", "Data Type": "Float (percentage)", "Notes": ""},
    {"Column Name": "Combined (Fresh and PNS Graduates) 2024", "Description": "Percentage of all graduates (Fresh + PNS) in 2024 falling under the corresponding Indicator", "Data Type": "Float (percentage)", "Notes": ""}
]

df_data_dict = pd.DataFrame(data_dict)

# Display the table in Streamlit
st.dataframe(df_data_dict)  # Use st.table(df_data_dict) if you want a static table

st.markdown("""
#### Sample Data for Graduate Employment Data
Employed,91.4%,91.7%,85.6%,92.7%,95.1%,91.4%,91.8%,92.7%,87.5%
            
\n
### Data Dictionary for Graduate Salary by Course Cluster\nhttps://www.np.edu.sg/docs/default-source/np-articles/media-releases/poly-ges-2024---media-release.pdf?sfvrsn=c36c4613_3
""")            
salary_data_dict = [
    {"Column Name": "Course Cluster", 
     "Description": "Broader category or domain the course belongs to", 
     "Data Type": "String", 
     "Notes": "Examples: Arts, Design & Media, Business, Engineering, etc."},
    
    {"Column Name": "Fresh Graduates 2022", 
     "Description": "Average salary of fresh graduates in 2022 from the corresponding Course Cluster", 
     "Data Type": "Float", 
     "Notes": "Values stored in SGD"},
    
    {"Column Name": "Fresh Graduates 2023", 
     "Description": "Average salary of fresh graduates in 2023 from the corresponding Course Cluster", 
     "Data Type": "Float", 
     "Notes": ""},
    
    {"Column Name": "Fresh Graduates 2024", 
     "Description": "Average salary of fresh graduates in 2024 from the corresponding Course Cluster", 
     "Data Type": "Float", 
     "Notes": ""},
    
    {"Column Name": "Post-NS (PNS) Graduates 2022", 
     "Description": "Average salary of Post-NS (PNS) graduates in 2022 from the corresponding Course Cluster", 
     "Data Type": "Float", 
     "Notes": ""},
    
    {"Column Name": "Post-NS (PNS) Graduates 2023", 
     "Description": "Average salary of Post-NS (PNS) graduates in 2023 from the corresponding Course Cluster", 
     "Data Type": "Float", 
     "Notes": ""},
    
    {"Column Name": "Post-NS (PNS) Graduates 2024", 
     "Description": "Average salary of Post-NS (PNS) graduates in 2024 from the corresponding Course Cluster", 
     "Data Type": "Float", 
     "Notes": ""},
    
    {"Column Name": "Combined (Fresh and PNS Graduates) 2022", 
     "Description": "Average salary of all graduates (Fresh + PNS) in 2022 from the corresponding Course Cluster", 
     "Data Type": "Float", 
     "Notes": ""},
    
    {"Column Name": "Combined (Fresh and PNS Graduates) 2023", 
     "Description": "Average salary of all graduates (Fresh + PNS) in 2023 from the corresponding Course Cluster", 
     "Data Type": "Float", 
     "Notes": ""},
    
    {"Column Name": "Combined (Fresh and PNS Graduates) 2024", 
     "Description": "Average salary of all graduates (Fresh + PNS) in 2024 from the corresponding Course Cluster", 
     "Data Type": "Float", 
     "Notes": ""}
]

# Convert to DataFrame and display
df_salary_dict = pd.DataFrame(salary_data_dict)
st.dataframe(df_salary_dict)

st.markdown("""
#### Sample Data for Graduate Salary by Course Cluster
Overall,2550,2700,2800,2800,2963,3000,2600,2800,2900

                                    
\n\n
### Data Dictionary for Ngee Ann Polytechnic Diploma Courses\nhttps://www.np.edu.sg/schools-courses/full-time-courses

This table describes the columns, their data types, and notes for the diploma courses dataset.
""")
# Create the data dictionary as a list of dictionaries
course_data_dict = [
    {"Column Name": "course_code", "Description": "Unique code identifying each diploma course", "Data Type": "String", "Notes": "Example: N51"},
    {"Column Name": "course_name", "Description": "Full name of the diploma course", "Data Type": "String", "Notes": "Example: Diploma in Accountancy (N51)"},
    {"Column Name": "school", "Description": "Name of the school within the polytechnic offering the course", "Data Type": "String", "Notes": "Example: School of Business & Accountancy"},
    {"Column Name": "course_cluster", "Description": "Broader category or domain the course belongs to", "Data Type": "String", "Notes": "Example: Business & Management"},
    {"Column Name": "section", "Description": "Section type of the content being described", "Data Type": "String", "Notes": "Examples: About, Content, Requirements, etc."},
    {"Column Name": "content", "Description": "Detailed description of the course, including curriculum, skills, career outcomes, and industry linkages", "Data Type": "String", "Notes": "May include long text with multiple paragraphs. Can contain information about internships, electives, future-ready skills, and accreditation."}
]

# Convert to DataFrame
df_course_dict = pd.DataFrame(course_data_dict)

# Display the data dictionary
st.dataframe(df_course_dict)  # Use st.table(df_course_dict) for a static table

st.markdown("""
#### Sample Data for Ngee Ann Polytechnic Diploma Courses
 N70,Diploma in Chinese Studies (N70),School of Humanities & Interdisciplinary Studies,Humanities,About,"Have a love for the Chinese language and culture or a flair for business? Armed with a Diploma in Chinese Studies (CHS), you will be a cut above the rest in meeting the rising demand for specialists in Chinese culture and language! Understanding Chinese Language & Culture As the only course of its kind offered at the polytechnic level and with at least half of it conducted in Chinese, CHS sharpens your language skills while preparing you for careers in the education, marketing and advertising, tourism and business sectors. You will go on field trips to a wide variety of organisations that reach out to Mandarin-speaking communities to broaden your perspective of Chinese culture and society. In the first year of study, you will uncover the different facets of Chinese history, culture and literature. You will also learn to use digitalised translation tools effectively and to present, write and speak with proficient Chinese communication skills. Industry Exposure Work on collaborative projects with our reputable industry partners in sectors such as education, translation, business and event management, culture and heritage, as well as marketing and advertising. You can choose either a one-year internship or opt for a combination of a six-month internship and project work or elective modules to sharpen your skill sets and build an outstanding portfolio. Choose from 2 Specialisations* Embark on either the Education or Business track in your second year. Education Get equipped for a career as a primary school teacher as you learn about teaching, curriculum planning, and child development Spend your final semester at the National Institute of Education (NIE) as part of the MOE Teacher Training Sponsorship Complete an NIE-conferred Diploma in Education (Chinese Specialisation) in one year upon graduation Apply for the MOE Teacher Training Sponsorship that covers tuition fees and offers a monthly allowance Business Hone skills in translation and interpretation, technology in business, integrated marketing communication, as well as project management Gain an in-depth understanding of Chinese business knowledge and business ethics *All specialisation options are subject to availability"

#### Data Classification        
Data is classified to be Official (Closed) / Non-Sensitive.            
""")

