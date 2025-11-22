import streamlit as st
import PyPDF2
from docx import Document
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Criticizer", page_icon="📝", layout="centered")

# Styling
st.markdown("""
    <style>
        .loading-container {
        font-size: 18px;
        font-weight: 600;
        margin-top: 1rem;
    }

    .loading-dots span {
        display: inline-block;
        font-weight: 900;
        animation-duration: 1.5s;
        animation-iteration-count: infinite;
        animation-timing-function: steps(1, end);
    }

    /* Dot 1: always visible */
    .loading-dots span:nth-child(1) {
        animation-name: dot1;
    }

    /* Dot 2: on except during the "1 dot" phase */
    .loading-dots span:nth-child(2) {
        animation-name: dot2;
    }

    /* Dot 3: only on during "3 dots" phases */
    .loading-dots span:nth-child(3) {
        animation-name: dot3;
    }

    @keyframes dot1 {
        0%, 100% { opacity: 1; }
    }

    /* 3 → 2 → 1 → 2 → 3 pattern */
    @keyframes dot2 {
        0%, 39%   { opacity: 1; }  /* 3 and 2 dots */
        40%, 59%  { opacity: 0; }  /* 1 dot */
        60%, 100% { opacity: 1; }  /* 2 and 3 dots */
    }

    @keyframes dot3 {
        0%, 19%   { opacity: 1; }  /* 3 dots */
        20%, 79%  { opacity: 0; }  /* 2 and 1 and 2 dots */
        80%, 100% { opacity: 1; }  /* 3 dots */
    }        
    </style>
""", unsafe_allow_html=True)
# END of styling 

st.title("AI Resume Criticizer 📝")
st.markdown("Upload your Resume to get AI-Powered Feedback tailored to your Dream Job! ☁️✨")
st.markdown("Don't have a Dream Job? We'll find you one! Make sure to leave the Text Box below Empty. 💡✨")

OPEN_API_KEY = os.getenv("OPEN_API_KEY")

uploaded_file = st.file_uploader("Upload your Resume (PDF, TEXT, DOCX or MD)", type=["pdf", "txt", "docx", "md"])

col1 , col2 = st.columns([3, 1])
with col1:
    job_role = st.text_input("Enter your Dream Job or Role (Optional)")
with col2:
    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
    analyze = st.button("Analyze Resume", icon="🔎", type="primary")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = []
    for page in pdf_reader.pages:
        text.append(page.extract_text())
    return "\n".join(text)

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = []
    for paragraph in doc.paragraphs:
        style = paragraph.style.name.lower()
        if "list" in style or "bullet" in style:
            line = f"• {paragraph.text}"
        else:
            line = paragraph.text
        text.append(line)
    return "\n".join(text)

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))  #Converts PDF to Bytes Object 
    return uploaded_file.read().decode("utf-8")                         #Runs if file is .txt

if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("File does not have any content")
            st.stop()

        job_role_prompt = f"""Please analyze this resume and provide constructive feedback.
        Focus on the following aspects:
        1. Content clarity and quantified impact
        2. Skills Presentation
        3. Experience Descriptions
        4. Specific improvement for {job_role}
        5. Provide 5 Companies that resume closely algins with so that the reader may apply.

        Resume Content:
        {file_content}

        Please provide your analysis in a clear, structured format with specific recommendations. Be sure to add emojis to help catch the reader's eye."""

        no_role_prompt = f"""Please analyze this resume and provide constructive feedback.
        Focus on the following aspects:
        1. Content clarity and quantified impact
        2. Skills Presentation
        3. Experience Descriptions
        4. List 5 suggestions on roles the resume closely aligns with.
        5. Specific improvement for the job role the following resume closely algins with.
        6. Provide 5 Companies that resume closely algins with so that the reader may apply.

        Resume Content:
        {file_content}

        Please provide your analysis in a clear, structured format with specific recommendations. Be sure to add emojis to help catch the reader's eye."""

        client = OpenAI(api_key=OPEN_API_KEY)

        # Creates a Loading Placeholder Text
        loading_text = st.empty()
        loading_text.markdown("""
            <div class="loading-container">
                Your Analysis is Loading
                <span class="loading-dots">
                    <span>.</span><span>.</span><span>.</span>
                </span>
            </div>
        """, unsafe_allow_html=True)

        # Sets the gpt Model 
        response = client.chat.completions.create(
            model='gpt-4.1-mini',
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer with years of experience in Human Resources and Recruitment"},
                {"role": "user", "content": job_role_prompt if job_role else no_role_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        #Removes Loading Text
        loading_text.empty()

        # Returns Response
        st.markdown("### Your Analysis Results: ")
        st.markdown(response.choices[0].message.content)    #Returns the first Response (You could get multiple responses)
    
    except Exception as e:
        st.error(f"An error has occurred: {str(e)}")
