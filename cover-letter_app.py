import streamlit as st
from groq import Groq

# Page config
st.set_page_config(page_title="AI Cover Letter Generator", page_icon="📝", layout="wide")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Groq API Key", type="password")
    tone = st.selectbox("Tone", ["formal", "friendly", "confident"])
    words = st.slider("Word limit", 150, 400, 250)
    st.divider()
    st.caption("Built with Streamlit + Groq + Llama 3")

# Session state
if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = ""

# Main UI
st.title("📝 AI Cover Letter Generator")
st.caption("Paste a job description, add your skills, get a personalised cover letter instantly.")

col1, col2 = st.columns(2)
with col1:
    jd = st.text_area("📋 Paste Job Description", height=250)
with col2:
    skills = st.text_area("🧠 Your Skills & Experience", height=250)

if st.button("✨ Generate Cover Letter", type="primary"):
    if not api_key:
        st.warning("Enter your Groq API key in the sidebar!")
    elif not jd or not skills:
        st.warning("Please fill in both fields!")
    else:
        with st.spinner("Writing your cover letter..."):
            client = Groq(api_key=api_key)
            prompt = f"""Write a {tone} cover letter in ~{words} words.

JOB DESCRIPTION:
{jd}

CANDIDATE SKILLS & EXPERIENCE:
{skills}

Requirements:
- Tailor it specifically to the job description
- Highlight the most relevant skills
- Include opening, body and closing paragraph
- Do not invent experience not provided
"""
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.cover_letter = res.choices[0].message.content

# Show output
if st.session_state.cover_letter:
    st.divider()
    st.subheader("Your Cover Letter")
    st.markdown(st.session_state.cover_letter)
    st.code(st.session_state.cover_letter, language=None)

    st.divider()
    changes = st.text_input("🔄 Want to refine? Describe what to change:")
    if st.button("Refine Cover Letter"):
        with st.spinner("Refining..."):
            client = Groq(api_key=api_key)
            res2 = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Rewrite this cover letter with these changes: {changes}\n\n{st.session_state.cover_letter}"}]
            )
            st.session_state.cover_letter = res2.choices[0].message.content
            st.rerun()