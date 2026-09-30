import streamlit as st
import ollama

st.set_page_config(page_title="AI Interviewer", page_icon="🎤")

st.title("🎤 AI Interviewer")


if "step" not in st.session_state:
    st.session_state.step = 1

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "scores" not in st.session_state:
    st.session_state.scores = []

if "feedback" not in st.session_state:
    st.session_state.feedback = []


if st.session_state.step == 1:
    name = st.text_input("Enter your name:")
    if st.button("Next"):
        if name:
            st.session_state.name = name
            st.session_state.step = 2
        else:
            st.warning("Please enter your name")

elif st.session_state.step == 2:
    role = st.text_input("Enter job role:")
    if st.button("Generate Questions"):
        if role:
            st.session_state.role = role

            prompt = f"""
            Generate 5 interview questions for a {role} role.
            Only list questions.
            """

            response = ollama.chat(model="llama3.2:1b",messages=[{"role": "user", "content": prompt}])

            questions = response["message"]["content"].split("\n")
            questions = [q for q in questions if q.strip()!=""]

            st.session_state.questions = questions[:5]
            st.session_state.current_q = 0
            st.session_state.step = 3
        else:
            st.warning("Enter a job role")

elif st.session_state.step == 3:

    q_index = st.session_state.current_q
    questions = st.session_state.questions

    if q_index < len(questions):

        st.subheader(f"Question {q_index+1}")
        st.write(questions[q_index])

        answer = st.text_area("Your Answer")

        if st.button("Submit Answer"):

            if answer:
                st.session_state.answers.append(answer)

                eval_prompt = f"""
                Question: {questions[q_index]}
                Answer: {answer}
                Give:
                1. Score (1-10)
                2. Feedback (short)"""

                eval_response = ollama.chat(model="llama3.2:1b",messages=[{"role": "user", "content": eval_prompt}])
                result = eval_response["message"]["content"]
                st.session_state.feedback.append(result)

                import re
                score_match = re.search(r'\b([1-9]|10)\b', result)
                score = int(score_match.group()) if score_match else 5
                st.session_state.scores.append(score)
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.warning("Please enter your answer")
    else:
        st.session_state.step = 4
elif st.session_state.step == 4:
    st.subheader("📊 Interview Report")
    total_score = sum(st.session_state.scores)
    avg_score = total_score / len(st.session_state.scores)

    st.write(f"👤 Name: {st.session_state.name}")
    st.write(f"💼 Role: {st.session_state.role}")
    st.write(f"⭐ Average Score: {avg_score:.2f}/10")

    st.markdown("---")

    for i in range(len(st.session_state.questions)):
        st.write(f"**Q{i+1}: {st.session_state.questions[i]}**")
        st.write(f"Answer: {st.session_state.answers[i]}")
        st.write(f"Feedback: {st.session_state.feedback[i]}")
        st.write(f"Score: {st.session_state.scores[i]}")
        st.markdown("---")

    final_prompt = f"""
    Candidate: {st.session_state.name}
    Role: {st.session_state.role}
    Average Score: {avg_score}
    Give a final interview summary and improvement tips.
    """
    final_response = ollama.chat(model="llama3.2:1b",messages=[{"role": "user", "content": final_prompt}])
    st.subheader("📝 Final Feedback")
    st.write(final_response["message"]["content"])