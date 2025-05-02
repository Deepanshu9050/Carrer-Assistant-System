import streamlit as st
import cohere
import pandas as pd
import spacy
import os
from docx import Document
import fitz  # PyMuPDF for PDF extraction

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Access API Key from Streamlit secrets
cohere_api_key = st.secrets["COHERE_API_KEY"]
co = cohere.Client(cohere_api_key)

# Set Page Configuration
st.set_page_config(page_title="Career Counseling Assistant", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
body, .stApp { background-color: #f5f9ff; font-family: 'Segoe UI', sans-serif; color: #333; }
h1 { text-align: center; font-size: 40px; color: #2a7de1; font-weight: bold; margin-top: 20px; }
h2, .stHeader { color: #1b4f72; margin-top: 25px; }
.css-1d391kg { background-color: #2a7de1 !important; }
.stSelectbox label, .css-q8sbsg { color: white !important; }
.stButton > button { background-color: #2a7de1; color: white; padding: 10px 18px; border-radius: 8px; font-size: 16px; border: none; margin-top: 10px; transition: background-color 0.3s ease; }
.stButton > button:hover { background-color: #1a5dbb; }
.stTextInput input, .stTextArea textarea { background-color: #fff; border: 1px solid #ccc; border-radius: 8px; padding: 10px; }
.stSelectbox select { background-color: #fff; border: 1px solid #ccc; border-radius: 8px; padding: 10px; }
.stChatMessage { background-color: #eaf1fb; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
.stAlert-success { background-color: #d4edda; color: #155724; }
.stAlert-warning { background-color: #fff3cd; color: #856404; }
.stProgress > div > div { background-image: linear-gradient(to right, #2a7de1, #67b26f) !important; border-radius: 10px; }
.stDownloadButton > button { background-color: #28a745; color: white; border-radius: 8px; padding: 10px 16px; font-size: 16px; transition: background-color 0.3s ease; }
.stDownloadButton > button:hover { background-color: #218838; }
form { background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 12px; padding: 20px; margin-top: 20px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05); }
.css-1iy0h4s { background-color: #f9fbff; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.title("🎯 Career Counseling Assistant")

menu = st.sidebar.selectbox("Choose a service", [
    "Resume Analyzer", "Mock Interview", "Career Planner",
    "Resources Hub", "Job Search Tracker", "Career Counseling Chatbot"
])

# Job keywords for resume analysis
job_keywords = {
    "Data Scientist": ["machine learning", "python", "pandas", "data analysis", "statistics"],
    "Web Developer": ["html", "css", "javascript", "react", "frontend", "backend"],
    "Digital Marketer": ["seo", "content", "email marketing", "analytics", "social media"]
}

def extract_text_from_word(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(file):
    doc = fitz.open(file)
    return "\n".join([page.get_text() for page in doc])

# Resume Analyzer
if menu == "Resume Analyzer":
    st.header("📄 Resume Analyzer")
    uploaded_file = st.file_uploader("Upload your resume (.txt, .docx)", type=["txt", "docx"])

    if uploaded_file:
        ext = uploaded_file.name.split('.')[-1]
        resume_text = uploaded_file.read().decode("utf-8") if ext == "txt" else extract_text_from_word(uploaded_file)

        st.subheader("Resume Preview:")
        st.text_area("Text content", resume_text, height=200)

        role = st.selectbox("Select Target Role", list(job_keywords.keys()))
        keywords = job_keywords[role]
        doc = nlp(resume_text.lower())
        tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]

        matched = [kw for kw in keywords if kw in tokens]
        missing = [kw for kw in keywords if kw not in tokens]

        st.success(f"✅ Matched Keywords: {', '.join(matched)}")
        st.warning(f"❌ Missing Keywords: {', '.join(missing)}")
        score = int((len(matched) / len(keywords)) * 100)
        st.progress(score)
        st.info(f"Match Score: {score}%")

# Mock Interview Bot
elif menu == "Mock Interview":
    st.header("🎤 Mock Interview Bot")
    job_role = st.text_input("Target Job Role (e.g., Data Scientist)")
    user_question = st.text_area("Ask a mock interview question:")

    if st.button("Ask"):
        with st.spinner("Thinking..."):
            prompt = f"You are a professional interviewer for a {job_role} position. Answer the following question in a helpful and professional way:\n\n{user_question}"
            try:
                response = co.generate(model="command", prompt=prompt, max_tokens=300, temperature=0.8)
                st.success("Interviewer Response:")
                st.write(response.generations[0].text.strip())
            except Exception as e:
                st.error(f"Cohere API error: {e}")

# Career Planner
elif menu == "Career Planner":
    st.header("🧭 Career Planner")
    interest = st.text_input("What are your interests or favorite subjects?")
    skills = st.text_input("What skills do you have?")
    goal = st.text_input("What is your career goal?")

    if st.button("Generate Plan"):
        with st.spinner("Generating personalized career plan..."):
            prompt = (
                f"I am interested in: {interest}.\n"
                f"My skills are: {skills}.\n"
                f"My career goal is: {goal}.\n"
                "Suggest suitable career paths, skills I should develop, and recommended resources."
            )
            try:
                response = co.generate(model="command", prompt=prompt, max_tokens=300, temperature=0.7)
                st.markdown(response.generations[0].text.strip())
            except Exception as e:
                st.error(f"Cohere API error: {e}")

# Resources Hub
elif menu == "Resources Hub":
    st.header("📚 Career Resources Hub")
    topic = st.text_input("Enter Topic for Resources (e.g., Data Science, Machine Learning)")

    if st.button("Generate Resources") and topic:
        with st.spinner("Generating resources..."):
            prompt = f"""
            Please generate a detailed and in-depth guide on the topic: '{topic}'.
            The guide should include at least 5000 words covering:
            - Introduction
            - Core concepts
            - Real-world applications
            - Case studies
            - Diagrams (as descriptions)
            - Challenges
            - Future trends
            - Best practices
            """
            try:
                response = co.generate(model="command", prompt=prompt, max_tokens=8000, temperature=0.7)
                content = response.generations[0].text.strip()
                st.write(content)

                doc = Document()
                doc.add_heading(f"{topic} - Detailed Resources", 0)
                for para in content.split('\n'):
                    doc.add_paragraph(para)
                doc.add_heading("Tables and Diagrams", level=1)
                doc.add_paragraph("1. Diagram/Table on Core Concepts")
                doc.add_paragraph("2. Diagram/Table on Applications in the Real World")
                doc.add_paragraph("3. Future Trends Table")

                docx_filename = f"{topic}_resources.docx"
                doc.save(docx_filename)

                with open(docx_filename, "rb") as f:
                    st.download_button(
                        label="Download Detailed Resources as Word File",
                        data=f,
                        file_name=docx_filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            except Exception as e:
                st.error(f"Cohere API error: {e}")

# Job Search Tracker
elif menu == "Job Search Tracker":
    st.header("📋 Job Search Tracker")
    st.markdown("Keep track of jobs you've applied to.")

    if "job_data" not in st.session_state:
        st.session_state.job_data = []

    with st.form("job_form"):
        company = st.text_input("Company Name")
        position = st.text_input("Position")
        status = st.selectbox("Status", ["Applied", "Interview", "Offer", "Rejected"])
        submit = st.form_submit_button("Add Job")

        if submit:
            st.session_state.job_data.append({
                "Company": company,
                "Position": position,
                "Status": status
            })
            st.success("Job added!")

    if st.session_state.job_data:
        st.subheader("My Job Applications")
        st.dataframe(pd.DataFrame(st.session_state.job_data))

# Career Counseling Chatbot
elif menu == "Career Counseling Chatbot":
    st.header("🧠 AI Career Counseling Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["text"])

    user_input = st.chat_input("Ask anything about your career...")
    if user_input:
        st.chat_message("user").write(user_input)
        st.session_state.chat_history.append({"role": "user", "text": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chat_log = ''.join([
                    f"User: {m['text']}\n" if m["role"] == "user" else f"Assistant: {m['text']}\n"
                    for m in st.session_state.chat_history
                ])
                prompt = f"You are a professional career counselor. Here's a conversation:\n{chat_log}Assistant:"
                try:
                    response = co.generate(model="command", prompt=prompt, max_tokens=300, temperature=0.7)
                    reply = response.generations[0].text.strip()
                    st.write(reply)
                    st.session_state.chat_history.append({"role": "assistant", "text": reply})
                except Exception as e:
                    st.error(f"Cohere API error: {e}")
