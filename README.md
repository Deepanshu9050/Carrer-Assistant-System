# Career Counseling Assistant

## Overview

The **Career Counseling Assistant** is a web application built using Streamlit that provides various career-related services to users. It includes features such as **Resume Analyzer**, **Mock Interview**, **Career Planner**, **Resources Hub**, **Job Search Tracker**, and **Career Counseling Chatbot**. This application uses the Cohere API for natural language generation and the spaCy library for text processing.

## Features

### 1. **Resume Analyzer**

* Upload your resume (in `.txt` or `.docx` format).
* Select a target role (e.g., Data Scientist, Web Developer, etc.).
* The system analyzes your resume and matches it with job-specific keywords.
* Shows a "match score" based on the presence of relevant keywords.

### 2. **Mock Interview**

* Input a target job role (e.g., Software Engineer, Data Scientist).
* Ask mock interview questions.
* The application responds with a professional interviewer's answer using the Cohere API.

### 3. **Career Planner**

* Input your interests, skills, and career goals.
* The system generates a personalized career plan and suggests suitable career paths based on your input.

### 4. **Resources Hub**

* Input a topic of interest (e.g., "Data Science").
* The system generates a detailed guide on the topic, including core concepts, applications, case studies, future trends, and best practices.
* You can download the generated content as a Word document.

### 5. **Job Search Tracker**

* Track job applications, interviews, offers, and rejections.
* Add job details such as company, position, and application status.
* View all tracked job data in a table.

### 6. **Career Counseling Chatbot**

* Engage in a conversation with an AI career counselor.
* Ask any career-related questions.
* The system responds with personalized career advice and guidance.

## Requirements

* Python 3.7+
* Streamlit
* Cohere Python Client
* spaCy
* PyMuPDF (for PDF extraction)
* docx (for DOCX file processing)
* pandas

### Installation

1. Clone this repository to your local machine.

2. Install the required libraries:

```bash
pip install streamlit cohere pandas spacy python-docx PyMuPDF
```

3. Download the spaCy model:

```bash
python -m spacy download en_core_web_sm
```

4. Set up the Cohere API key:

   * Create an account on [Cohere](https://cohere.ai/).
   * Get your API key and save it in the `streamlit secrets` file. You can store it as:

```yaml
COHERE_API_KEY: "your-cohere-api-key"
```

5. Run the app with:

```bash
streamlit run app.py
```

## File Structure

```
Career-Counseling-Assistant/
│
├── app.py                  # Main Streamlit application
├── en_core_web_sm/         # Local folder containing the spaCy model
│   └── (model files)
├── requirements.txt        # List of dependencies
└── README.md               # This README file
```

## Code Explanation

### Main Libraries Used

* **Streamlit**: Provides the framework for building the interactive web application.
* **Cohere**: Used for natural language generation (AI responses).
* **spaCy**: Used for text processing and analysis (e.g., extracting keywords from resumes).
* **PyMuPDF (fitz)**: Extracts text from PDF files (though this feature is not currently implemented in the code, it can be added for future improvements).
* **docx**: Processes DOCX files to extract text content for resume analysis.

### Key Components

* **`extract_text_from_word(file)`**: A helper function that extracts text from DOCX files.
* **Resume Analyzer**: Analyzes resumes by checking if the text contains relevant keywords based on the selected job role.
* **Mock Interview**: Allows users to simulate a mock interview for a specific job role, using AI-generated responses.
* **Career Planner**: Creates a personalized career plan based on the user's interests, skills, and career goals.
* **Resources Hub**: Generates detailed guides on a given topic and allows the user to download them as Word documents.
* **Job Search Tracker**: Lets users track their job search process by saving and displaying job application statuses.
* **Career Counseling Chatbot**: A conversational assistant powered by the Cohere API, providing personalized career advice.

## Usage

1. **Resume Analyzer**:

   * Upload a resume file (either `.txt` or `.docx`).
   * Choose a job role and view the matching keywords and score.

2. **Mock Interview**:

   * Type in a job role and ask a mock interview question.
   * The bot responds with an interviewer's answer.

3. **Career Planner**:

   * Provide information about your interests, skills, and career goals.
   * Get a personalized career plan.

4. **Resources Hub**:

   * Enter a career-related topic, and get a detailed guide.
   * Download the guide as a Word document.

5. **Job Search Tracker**:

   * Add and track job applications.
   * View your job search status in a table format.

6. **Career Counseling Chatbot**:

   * Engage in a conversation with the AI chatbot about career guidance.

## Contributing

Feel free to open issues or pull requests if you'd like to contribute to this project. Some potential improvements include:

* Adding PDF resume parsing functionality.
* Enhancing the career plan with more personalized recommendations.
* Improving chatbot capabilities with more extensive conversational context.


Happy coding and best of luck with your career journey! 🎯
