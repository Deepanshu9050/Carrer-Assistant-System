import streamlit as st
import cohere
import pandas as pd
import spacy
import os
from docx import Document
import fitz  # PyMuPDF for PDF extraction

# Load spaCy model from local folder
LOCAL_SPACY_MODEL_PATH = os.path.join(os.path.dirname(__file__), "en_core_web_sm", "en_core_web_sm-3.8.0")
nlp = spacy.load(LOCAL_SPACY_MODEL_PATH)

# Access Cohere API Key from Streamlit secrets
cohere_api_key = st.secrets["COHERE_API_KEY"]
co = cohere.Client(cohere_api_key)

# Set Streamlit page configuration
st.set_page_config(page_title="Career Counselling Assistant", layout="wide")

# Custom styling
st.markdown("""
<style>
body, .stApp { background-color: #f5f9ff; font-family: 'Segoe UI', sans-serif; color: #333; }
h1 { text-align: center; font-size: 40px; color: #2a7de1; font-weight: bold; margin-top: 20px; }
h2, .stHeader { color: #1b4f72; margin-top: 25px; }
.stButton > button { background-color: #2a7de1; color: white; padding: 10px 18px; border-radius: 8px; font-size: 16px; border: none; }
.stButton > button:hover { background-color: #1a5dbb; }
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background-color: #fff; border: 1px solid #ccc; border-radius: 8px; padding: 10px;
}
.stChatMessage { background-color: #eaf1fb; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
.stDownloadButton > button { background-color: #28a745; color: white; border-radius: 8px; padding: 10px 16px; font-size: 16px; }
.stDownloadButton > button:hover { background-color: #218838; }
</style>
""", unsafe_allow_html=True)

st.title("🎯 Career Counselling Assistant")

menu = st.sidebar.selectbox("Choose a service", [
    "Resume Analyzer", "Mock Interview", "Career Planner",
    "Resources Hub", "Job Search Tracker", "Career Counselling Chatbot"
])

job_keywords = {
    "Data Scientist": ["machine learning", "python", "pandas", "data analysis", "statistics"],
    "Web Developer": ["html", "css", "javascript", "react", "frontend", "backend"],
    "Digital Marketer": ["seo", "content", "email marketing", "analytics", "social media"]
}

def extract_text_from_word(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

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

# Mock Interview
elif menu == "Mock Interview":
    st.header("🎤 Mock Interview Bot")
    job_role = st.text_input("Target Job Role")
    user_question = st.text_area("Ask a mock interview question:")
    if st.button("Ask"):
        with st.spinner("Thinking..."):
            prompt = f"You are a professional interviewer for a {job_role} position. Answer the following question:\n\n{user_question}"
            try:
                response = co.generate(model="command", prompt=prompt, max_tokens=300, temperature=0.8)
                st.success("Interviewer Response:")
                st.write(response.generations[0].text.strip())
            except Exception as e:
                st.error(f"Cohere API error: {e}")

# Career Planner
elif menu == "Career Planner":
    st.header("🧭 Career Planner")
    interest = st.text_input("What are your interests?")
    skills = st.text_input("What skills do you have?")
    goal = st.text_input("What is your career goal?")
    if st.button("Generate Plan"):
        with st.spinner("Generating career plan..."):
            prompt = (
                f"I am interested in: {interest}.\n"
                f"My skills are: {skills}.\n"
                f"My career goal is: {goal}.\n"
                "Suggest suitable career paths and resources."
            )
            try:
                response = co.generate(model="command", prompt=prompt, max_tokens=300, temperature=0.7)
                st.markdown(response.generations[0].text.strip())
            except Exception as e:
                st.error(f"Cohere API error: {e}")

# Resources Hub
elif menu == "Resources Hub":
    st.header("📚 Career Resources Hub")
    topic = st.text_input("Enter Topic")
    if st.button("Generate Resources") and topic:
        with st.spinner("Generating resources..."):
            prompt = f"""
            Generate a 5000-word guide on: {topic}. Include:
            - Introduction
            - Core concepts
            - Applications
            - Case studies
            - Diagrams (as text descriptions)
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
                docx_filename = f"{topic}_resources.docx"
                doc.save(docx_filename)
                with open(docx_filename, "rb") as f:
                    st.download_button("Download as Word File", f, file_name=docx_filename)
            except Exception as e:
                st.error(f"Cohere API error: {e}")

# Job Tracker
elif menu == "Job Search Tracker":
    st.header("📋 Job Search Tracker")
    if "job_data" not in st.session_state:
        st.session_state.job_data = []
    with st.form("job_form"):
        company = st.text_input("Company")
        position = st.text_input("Position")
        status = st.selectbox("Status", ["Applied", "Interview", "Offer", "Rejected"])
        if st.form_submit_button("Add Job"):
            st.session_state.job_data.append({
                "Company": company, "Position": position, "Status": status
            })
            st.success("Job added!")
    if st.session_state.job_data:
        st.dataframe(pd.DataFrame(st.session_state.job_data))

# Career Counseling Chatbot
elif menu == "Career Counselling Chatbot":
    st.header("🧠 Career Counselling Chatbot")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["text"])
    user_input = st.chat_input("Ask anything...")
    if user_input:
        st.chat_message("user").write(user_input)
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chat_log = ''.join([
                    f"{m['role'].capitalize()}: {m['text']}\n" for m in st.session_state.chat_history
                ])
                prompt = f"You are a professional career counselor. Here's the conversation:\n{chat_log}Assistant:"
                try:
                    response = co.generate(model="command", prompt=prompt, max_tokens=300, temperature=0.7)
                    reply = response.generations[0].text.strip()
                    st.write(reply)
                    st.session_state.chat_history.append({"role": "assistant", "text": reply})
                except Exception as e:
                    st.error(f"Cohere API error: {e}")
