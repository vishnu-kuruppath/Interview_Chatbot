## Interview_Chatbot
#  AI Interviewer (GenAI Project)

An AI-powered Interview Simulator built using **Streamlit + Ollama (LLM)**.

##  Features
- Generates interview questions based on job role
- Takes user answers interactively
- Evaluates answers with AI
- Gives score (1–10) + feedback
- Final interview report with improvement tips

##  Tech Stack
- Python
- Streamlit
- Ollama (LLM - llama3.2:1b)

##  Project Flow
1. User enters name & job role
2. AI generates 5 interview questions
3. User answers each question
4. AI evaluates answers with score + feedback
5. Final report with average score & suggestions


```bash
pip install -r requirements.txt
streamlit run app.py
