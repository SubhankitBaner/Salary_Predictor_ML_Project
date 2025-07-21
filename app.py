import streamlit as st
import joblib
import pandas as pd 
import time
from babel.numbers import format_currency 
import base64

# Load the saved model pipeline
model = joblib.load('model/model_pipeline.pkl')

# --- Streamlit UI ---
st.set_page_config(
    page_title="Salary Predictor",
    page_icon="💰",
    layout="centered",
)

# --- Load CSS for background image and custom styles ---
def add_bg_and_styles(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png" if image_file.endswith(".png") else "jpeg"};base64,{encoded_string});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        h1, h2 {{
            padding-top: 5px !important;
            padding-bottom: 5px !important;
        }}

        .stButton button {{
            background-color: #f54242;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 0.75em 2em;
            font-size: 16px;
        }}

        .stButton button:hover {{
            background-color: #e03838;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_and_styles('images/bg.jpeg')

col1, col2 = st.columns([4, 6])
with col1:
    st.image("images/salary.jpg", width=400)
with col2:
    st.markdown("<h1 style='color:#f54242;'>Salary Prediction App</h1>", unsafe_allow_html=True)

st.divider()
st.write("""
Welcome to the Salary Prediction App — a tool designed to estimate salary based on key professional attributes like age, experience, education level, job title, and more. Using a machine learning model trained on real-world data, this app helps provide a quick and data-driven salary estimate to support career planning, hiring decisions, and compensation analysis.

Whether you're a job seeker, HR professional, or just curious — enter your details and get an instant prediction!
""")

with st.sidebar:
    st.markdown("### 🛑 About This App")
    st.markdown("""
This Salary Prediction App is a **demo project** built using machine learning to estimate salaries based on:

- Age  
- Years of Experience  
- Education Level  
- Job Title  
- Gender

> ⚠️ **Disclaimer:** This app is for **testing and educational purposes only**.  
It does **not** reflect real-world compensation or provide financial advice.

Enter your details to explore how the model predicts salaries!
    """)

st.divider()
st.markdown("<h2 style='color:#f54242;'>Enter Employee Details Below</h2>", unsafe_allow_html=True)
st.divider()

# User Inputs
age = st.number_input("Age", min_value=18, max_value=65, step=1)
experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)

gender = st.selectbox("Gender", ["Male", "Female"])
education = st.selectbox("Education Level", [
    "Bachelor's",
    "Master's",
    "PhD"
])

job_title = st.selectbox("Job Title", [
    "Marketing",
    "Finance/Accounting",
    "Software Engineer",
    "Manager",
    "Analyst",
    "HR",
    "Sales",
    "Product Manager",
    "Project Manager",
    "Director",
    "Designer",
    "Data Scientist",
    "Data Analyst",
    "Scientist",
    "Other",
    "Coordinator",
    "IT Support",
    "Business Development",
    "Content/Writer",
    "Recruiter",
    "Consultant",
    "Executive",
    "Admin/Assistant",
    "Operations",
    "Researcher"
])

# Predict Button Styling
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #f54242 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        border: none !important;
        transition: background-color 0.3s ease;
        margin-top: 20px;
    }
    div.stButton > button:first-child:hover {
        background-color: #d63a3a !important;
    }
    </style>
""", unsafe_allow_html=True)

if st.button("Predict Salary"):
    with st.spinner('Predicting Salary...'):
        time.sleep(2)

        input_df = pd.DataFrame([{
            'Age': age,
            'Experience_Years': experience,
            'Gender': gender,
            'Education_Level': education,
            'Job_Title': job_title
        }])

        prediction = model.predict(input_df)[0]
        formatted_price = format_currency(prediction, 'INR', locale='en_IN')

        # Salary Result Box 
        st.markdown(
            f"""
            <div style='
                background-color: #214321;
                padding: 12px;
                border-radius: 5px;
                text-align: center;
                margin-top: 20px;
                color: white;
            '>
                <span style='font-size: 1.65em; font-weight: bold;'>📟 Estimated Salary: {formatted_price}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Disclaimer Box 
        st.markdown(
            """
            <style>
            .disclaimer {
                color: white;
                background-color: rgba(0, 0, 0, 0.6);
                padding: 1rem;
                border-radius: 8px;
                font-size: 16px;
                margin-top: 16px;
            }
            </style>

            <div class="disclaimer">
                ⚠️ <strong>Disclaimer:</strong><br>
                This prediction is generated by a machine learning model for <strong>educational and testing purposes only.</strong><br>
                It should not be used for real financial decisions or salary negotiations.
            </div>
            """,
            unsafe_allow_html=True
        )
