import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns


#This page is accessible to both roles
st.set_page_config(page_title="Data Dashboard", layout="wide")
st.title("Data Dashboard")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("🚫 You must log in first.")
    st.stop()

DATA_DIR = "Data"
error_list = []

try:
    # -----------------------------
    # Load CSVs
    # -----------------------------
    df_enrol = pd.read_csv(os.path.join(DATA_DIR, "EnrolmentInPolytechnicDiplomaCoursesByTypeOfCourseAndSexAnnual.csv"))
    df_grad = pd.read_csv(os.path.join(DATA_DIR, "GraduatesFromPolytechnicDiplomaCoursesByTypeOfCourseAndSexAnnual.csv"))
    df_fees = pd.read_csv(os.path.join(DATA_DIR, "2024NgeeAnnPolytechnicFulltimeDiplomaCourseFeesSemester.csv"))
    df_employment = pd.read_csv(os.path.join(DATA_DIR, "ges_employment_indicators.csv"))
    df_salary = pd.read_csv(os.path.join(DATA_DIR, "ges_median_salary.csv"))
    # -----------------------------
    # KPI SUMMARY ROW
    # -----------------------------
    st.header("Fees Overview")
    col1, col2, col3 = st.columns(3)

    # KPI 1: Average Course Fee SG (Year 1 Sem 1)

    df_sg = df_fees[df_fees["Citizenship"] == "Singapore Citizens"]
    # Pivot table: Semesters as columns
    df_pivot = df_sg.pivot_table(index="Year", columns="Semester", values="Fees", aggfunc="mean")
    # Get total tuition for the single year
    total_fee = df_pivot.loc[df_pivot.index[0], ["Semester 1", "Semester 2"]].sum()
    # Display KPI in Streamlit
    col1.metric("💰 Annual Tuition Fee (SG Citizens)", f"${total_fee:,.2f}")

    # KPI 2: Average Course Fee PR (Year 1 Sem 1)

    df_sg = df_fees[df_fees["Citizenship"] == "Singapore Permanent Residents"]
    # Pivot table: Semesters as columns
    df_pivot = df_sg.pivot_table(index="Year", columns="Semester", values="Fees", aggfunc="mean")
    # Get total tuition for the single year
    total_fee = df_pivot.loc[df_pivot.index[0], ["Semester 1", "Semester 2"]].sum()
    # Display KPI in Streamlit
    col2.metric("💰 Annual Tuition Fee (PR)", f"${total_fee:,.2f}")

    # KPI 3: Average Course Fee Int (Year 1 Sem 1)

    df_sg = df_fees[df_fees["Citizenship"] == "International students (includes GST)"]
    # Pivot table: Semesters as columns
    df_pivot = df_sg.pivot_table(index="Year", columns="Semester", values="Fees", aggfunc="mean")
    # Get total tuition for the single year
    total_fee = df_pivot.loc[df_pivot.index[0], ["Semester 1", "Semester 2"]].sum()
    # Display KPI in Streamlit
    col3.metric("💰 Annual Tuition Fee (International students (includes GST))", f"${total_fee:,.2f}")

    ################## Enrolment stats ########################
    st.header("Enrolment by Sex and Course (2022–2024)")

    def preprocess_df(df, type_label):
        # Clean column names
        df.columns = df.columns.str.strip()

        # Melt wide → long
        df_long = df.melt(id_vars=["DataSeries"], var_name="Year", value_name="Count")

        # Convert Year and Count
        df_long["Year"] = pd.to_numeric(df_long["Year"], errors="coerce")
        df_long["Count"] = pd.to_numeric(df_long["Count"], errors="coerce")

        # Split DataSeries into Sex and Course
        df_long["Sex"] = df_long["DataSeries"].apply(
            lambda x: "Male" if str(x).strip().startswith("Males") 
                    else ("Female" if str(x).strip().startswith("Females") else None)
        )
        df_long["Course"] = df_long["DataSeries"].str.split(":", n=1).str[-1].str.strip()
        df_long["Course"].fillna("Total", inplace=True)

        # Add type column
        df_long["Type"] = type_label

        return df_long

    # Preprocess datasets
    df_enrol_long = preprocess_df(df_enrol, "Enrolment")

    # Keep last 3 years only
    latest_years = sorted(df_enrol_long["Year"].unique())[-3:]
    df_enrol_long = df_enrol_long[df_enrol_long["Year"].isin(latest_years)]
    df_enrol_long["Year"] = df_enrol_long["Year"].astype(int)

    # Streamlit multiselect filter for courses
    courses = sorted(df_enrol_long["Course"].unique())
    selected_courses = st.multiselect("Select Courses", options=courses, default=courses[:3],key="enrol_course_selector")  # default to first 3
    df_filtered = df_enrol_long[df_enrol_long["Course"].isin(selected_courses)]

    # Filter out Total rows
    df_filtered_courses = df_filtered[df_filtered["Course"] != "Total"]

    plt.figure(figsize=(14, 7))

    # Create combined label without modifying the original DataFrame in-place
    df_plot = df_filtered_courses.copy()
    df_plot["SexCourse"] = df_plot["Sex"] + " - " + df_plot["Course"]

    # interactive table, scrollable
    st.dataframe(df_plot)  

    sns.lineplot(
        data=df_plot,
        x=df_plot["Year"].astype(str),  # discrete axis
        y="Count",
        hue="SexCourse",    # separate line for Male/Female per course
        markers=True,
        dashes=False,
        errorbar=None
    )

    plt.title("Polytechnic Enrolment by Sex and Course (Last 3 Years)")
    plt.ylabel("Number of Students")
    plt.xlabel("Year")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)


    ################# Graduation stats ########################
    st.header("Graduates by Sex and Course (2022–2024)")

    # Preprocess datasets
    df_grad_long = preprocess_df(df_grad, "Graduates")

    # Keep last 3 years only
    latest_years = sorted(df_grad_long["Year"].unique())[-3:]
    df_grad_long = df_grad_long[df_grad_long["Year"].isin(latest_years)]
    df_grad_long["Year"] = df_grad_long["Year"].astype(int)

    # Streamlit multiselect filter for courses
    courses = sorted(df_grad_long["Course"].unique())
    selected_courses = st.multiselect("Select Courses", options=courses, default=courses[:3],key="grad_course_selector")  # default to first 3
    df_grad_filtered = df_grad_long[df_grad_long["Course"].isin(selected_courses)]

    # Filter out Total rows
    df_grad_filtered_courses = df_grad_filtered[df_grad_filtered["Course"] != "Total"]

    plt.figure(figsize=(14, 7))

    # Create combined label without modifying the original DataFrame in-place
    df_plot = df_grad_filtered_courses.copy()
    df_plot["SexCourse"] = df_plot["Sex"] + " - " + df_plot["Course"]

    st.dataframe(df_plot)   

    sns.lineplot(
        data=df_plot,
        x=df_plot["Year"].astype(str), 
        y="Count",
        hue="SexCourse",   
        markers=True,
        dashes=False,
        errorbar=None
    )

    plt.title("Polytechnic Graduates by Sex and Course (Last 3 Years)")
    plt.ylabel("Number of Students")
    plt.xlabel("Year")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)


    st.header("Employment Indicators from 2022 to 2024 ")

    # Convert percentage strings to numeric
    for col in df_employment.columns[1:]:
        df_employment[col] = df_employment[col].str.rstrip("%").astype(float)

    # Melt the DataFrame: wide → long
    df_long = df_employment.melt(id_vars="Indicator", var_name="TypeYear", value_name="Percentage")

    # Split TypeYear into Type (Fresh/Post/Combined) and Year
    df_long["Type"] = df_long["TypeYear"].str.split(" ").str[0]
    df_long["Year"] = df_long["TypeYear"].str[-4:].astype(int)

    # Plot grouped bar chart
    plt.figure(figsize=(16, 7))
    sns.barplot(
        data=df_long,
        x="Indicator",
        y="Percentage",
        hue="Type",
        ci=None,
        palette="Set2"
    )

    # Overlay the Year info by changing x-axis labels
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Percentage (%)")
    plt.title("Graduate Employment by Type (Fresh / Post-NS / Combined) 2022–2024")
    plt.legend(title="Graduate Type")
    plt.tight_layout()
    st.pyplot(plt)

    ################## Salary ########################
    st.header("Median Gross Monthly Salary by Course Cluster (2022–2024)")

    # Melt wide → long
    df_long = df_salary.melt(id_vars="Course Cluster", var_name="TypeYear", value_name="Salary")

    # Extract Type and Year
    def split_type_year(s):
        s = s.strip()
        if "Fresh Graduates" in s:
            type_ = "Fresh"
        elif "Post-NS" in s:
            type_ = "Post-NS"
        elif "Combined" in s:
            type_ = "Combined"
        else:
            type_ = "Unknown"
        year = int(s[-4:])
        return pd.Series([type_, year])


    df_long[["Type", "Year"]] = df_long["TypeYear"].apply(split_type_year)


    # Create a new column combining Course and Year for x-axis
    df_long["CourseYear"] = df_long["Course Cluster"] + " (" + df_long["Year"].astype(str) + ")"

    # Omit the "Overall" row
    df_long = df_long[df_long["Course Cluster"] != "Overall"]

    # Plot grouped bar chart
    plt.figure(figsize=(18, 8))
    sns.barplot(
        data=df_long,
        x="CourseYear",
        y="Salary",
        hue="Type",
        ci=None,
        palette="Set2"
    )

    plt.title("Graduate Salary by Course Cluster (Fresh / Post-NS / Combined) 2022–2024")
    plt.ylabel("Salary ($)")
    plt.xlabel("Course Cluster (Year)")
    plt.xticks(rotation=45, ha='right')
    plt.legend(title="Graduate Type")
    plt.tight_layout()
    st.pyplot(plt)

except Exception as e:
    st.error("❌ An error has occured, please inform the team creators")
    print(f"View Data Page Error: {e}")