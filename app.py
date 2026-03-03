import streamlit as st
import json
import time
import re
from groq import Groq

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="TalentScout x PG-AGI", page_icon="🤖", layout="wide")

# --- 2. ADVANCED ANIMATED CSS (PG-AGI STYLE) ---
st.markdown("""
    <style>
    /* Main Background: Deep Space Black */
    .stApp {
        background-color: #020617 !important;
    }

    /* Typography: Inter UI */
    h1, h2, h3, p, span, div, label {
        color: #F8FAFC !important;
        font-family: 'Inter', sans-serif;
    }

    /* 1. Cyber Pulse Animation for Header */
    @keyframes cyber-pulse {
        0% { border-bottom-color: #38BDF8; box-shadow: 0 0 5px rgba(56, 189, 248, 0.1); }
        50% { border-bottom-color: #0EA5E9; box-shadow: 0 0 15px rgba(14, 165, 233, 0.4); }
        100% { border-bottom-color: #38BDF8; box-shadow: 0 0 5px rgba(56, 189, 248, 0.1); }
    }

    .pg-header {
        border-bottom: 1px solid #38BDF8;
        padding-bottom: 10px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        animation: cyber-pulse 3s infinite ease-in-out;
    }

    /* 2. System Online Blinking Dot */
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }
    .online-dot {
        height: 10px; width: 10px;
        background-color: #38BDF8;
        border-radius: 50%;
        display: inline-block;
        margin-left: 8px;
        animation: blink 1.5s infinite;
        box-shadow: 0 0 8px #38BDF8;
    }

    /* 3. Bento-Style Sidebar Cards with Hover Effect */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }
    
    .bento-card {
        background: #1E293B;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
        margin-bottom: 10px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .bento-card:hover {
        transform: translateX(5px);
        border-color: #38BDF8;
    }
    .bento-label { color: #38BDF8; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; }

    /* 4. Chat Messages: Fade-In Animation */
    @keyframes fade-in {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    [data-testid="stChatMessage"] {
        background-color: #0F172A !important;
        border: 1px solid #1E293B !important;
        border-radius: 12px !important;
        margin-bottom: 15px;
        animation: fade-in 0.5s ease-out forwards;
    }

    /* 5. Cyber Primary Button */
    .stButton>button {
        background-color: #38BDF8 !important;
        color: #020617 !important;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px #38BDF8 !important;
        transform: translateY(-2px);
    }

    /* Exit Screen */
    .exit-header {
        color: #F43F5E !important;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-top: 20vh;
    }
            .agent-header {
        border: 1px solid #38BDF8; /* The Box Border */
        padding: 15px 25px;
        border-radius: 10px;
        margin-bottom: 30px;
        display: flex;
        justify-content: center; /* Centers horizontally */
        align-items: center;     /* Centers vertically */
        background: rgba(15, 23, 42, 0.5); /* Subtle dark fill */
        animation: cyber-pulse 3s infinite ease-in-out;
    }

    .agent-header h4 {
        margin: 0;
        letter-spacing: 2px;
        color: #38BDF8 !important; /* Cyber Blue text */
        font-weight: bold;
    }
            /* Blue Fire Animation */
    @keyframes blue-fire {
        0% { text-shadow: 0 -2px 4px #fff, 0 -4px 10px #38BDF8, 0 -10px 20px #0EA5E9, 0 -18px 40px #020617; }
        25% { text-shadow: 0 -2px 1px #fff, 0 -4px 15px #38BDF8, 0 -12px 25px #0EA5E9, 0 -20px 50px #020617; }
        50% { text-shadow: 0 -2px 6px #fff, 0 -6px 12px #38BDF8, 0 -10px 30px #0EA5E9, 0 -15px 35px #020617; }
        75% { text-shadow: 0 -2px 2px #fff, 0 -4px 18px #38BDF8, 0 -14px 28px #0EA5E9, 0 -22px 55px #020617; }
        100% { text-shadow: 0 -2px 4px #fff, 0 -4px 10px #38BDF8, 0 -10px 20px #0EA5E9, 0 -18px 40px #020617; }
    }

    .fire-title {
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        color: #F8FAFC !important; /* White text looks better with blue fire behind it */
        text-align: center;
        margin-bottom: 0px;
        animation: blue-fire 1.5s infinite alternate;
        letter-spacing: 4px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC FUNCTIONS ---


# Initialize Groq client (In Streamlit Cloud, we use st.secrets for safety)
# For local testing, you can paste your key here, but don't upload the key to GitHub!
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_ollama_response(messages):
    """Updated to use the latest supported Groq model"""
    try:
        completion = client.chat.completions.create(
            # llama3-8b-8192 is dead. Use this version instead:
            model="llama-3.1-8b-instant", 
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"System error: {str(e)}"

def validate_input(text, step_name):
    text = text.strip()
    if step_name == "Full Name":
        return bool(re.match(r"^[a-zA-Z\s\-]+$", text)), "Full Name: ONLY include alphabets."
    elif step_name == "Email Address":
        return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", text)), "Invalid! Write a valid email."
    elif step_name == "Phone Number":
        return bool(re.match(r"^\d{10}$", text)), "Must be 10 numerical digits."
    elif step_name == "Years of Experience":
        return text.replace('.', '', 1).isdigit(), "ONLY numerical values allowed."
    elif step_name in ["Desired Position", "Current Location", "Tech Stack"]:
        return bool(re.search(r"[a-zA-Z]", text)), f"{step_name}: Should be alphabetic."
    return True, ""

import re

import re

import random
import re

def get_questions_for_stack(user_tech_input):
    # 1. Clean the input and turn it into a list
    # Replaces commas with spaces and splits into words
    stack_list = re.split(r'[,\s]+', user_tech_input.strip())
    stack_list = [tech for tech in stack_list if tech] # remove empty strings
    
    # 2. Randomly pick up to 3 technologies
    num_to_select = min(len(stack_list), 3)
    selected_techs = random.sample(stack_list, num_to_select)
    tech_string = ", ".join(selected_techs)

    # 3. Strict Prompt for selected techs
    prompt = f"""
    TASK: Generate exactly {num_to_select} technical interview questions.
    TECHNOLOGIES TO FOCUS ON: {tech_string}
    
    STRICT RULES:
    - Output ONLY the questions.
    - One question per line.
    - No introductions, no "Question 1", no "Sure thing".
    - Focus on practical, senior-level knowledge.
    """
    
    return prompt

def clean_questions(raw_text):
    # Split by lines and remove empty ones/intro chatter
    lines = [l.strip() for l in raw_text.split('\n') if len(l.strip()) > 15]
    
    # Filter out common AI intro phrases
    forbidden = ["here are", "i selected", "sure", "technical question"]
    clean_qs = [line for line in lines if not any(f in line.lower() for f in forbidden)]
    
    # Clean off numbering (1., 2., etc)
    final_qs = [re.sub(r'^\d+[\s\.\)-]+', '', q) for q in clean_qs]
    
    return final_qs[:3]

# --- 4. SESSION STATE ---
if "step" not in st.session_state: st.session_state.step = 0
if "messages" not in st.session_state: st.session_state.messages = []
if "candidate_data" not in st.session_state: st.session_state.candidate_data = {}
if "tech_questions" not in st.session_state: st.session_state.tech_questions = []
if "current_q_idx" not in st.session_state: st.session_state.current_q_idx = 0
if "is_finished" not in st.session_state: st.session_state.is_finished = False

INFO_STEPS = ["Full Name", "Email Address", "Phone Number", "Years of Experience", "Desired Position", "Current Location", "Tech Stack"]
EXIT_KEYWORDS = ["exit", "bye", "quit", "done", "terminate"]

# --- 5. SIDEBAR (BENTO DESIGN) ---
with st.sidebar:
    # This creates the Blue Fire Title
    st.markdown("<h1 class='fire-title'>TalentScout</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#38BDF8; font-size:0.8rem; margin-top:-10px;'>RECRUITMENT INTERFACE</p>", unsafe_allow_html=True)
    # ... rest of your sidebar code
    st.markdown("---")
    if st.session_state.candidate_data:
        for k, v in st.session_state.candidate_data.items():
            st.markdown(f"""<div class="bento-card"><div class="bento-label">{k}</div><b>{v}</b></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("TERMINATE SESSION"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- 6. MAIN APP LOGIC ---

if st.session_state.is_finished:
    st.markdown('<h1 class="exit-header">CONVERSATION ENDED</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#94A3B8;"> Data secure. we will be in touch shortly Thanks :)</p>', unsafe_allow_html=True)
    st.chat_input("START NEW CONVERSATION", disabled=True)
else:
    # Animated Header
   # Inside the "else" block of Section 6
    st.markdown("""<div class="agent-header"><h4>AGENT SCOUT</h4></div>""", unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if st.session_state.step == 0 and not st.session_state.messages:
        welcome = f"Welcome I am Scout, let me guide you through the recruitment process.\n\n Please provide your **{INFO_STEPS[0]}**."
        st.session_state.messages.append({"role": "assistant", "content": welcome})
        st.rerun()

    if prompt := st.chat_input("Input command..."):
        if any(key in prompt.lower() for key in EXIT_KEYWORDS):
            st.session_state.is_finished = True
            st.rerun()

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            if st.session_state.step < len(INFO_STEPS):
                current_label = INFO_STEPS[st.session_state.step]
                is_valid, error_msg = validate_input(prompt, current_label)
                
                if not is_valid:
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                else:
                    st.session_state.candidate_data[current_label] = prompt
                    st.session_state.step += 1
                    if st.session_state.step < len(INFO_STEPS):
                        next_q = f"Got it, Requesting: **{INFO_STEPS[st.session_state.step]}**."
                        st.session_state.messages.append({"role": "assistant", "content": next_q})
                    else:
                        # --- UPDATE THIS SECTION IN YOUR CODE ---
                        with st.status("⚙️ Generating Assessment Sequence...", expanded=False) as status:
                            stack = st.session_state.candidate_data.get("Tech Stack")
                            yoe = st.session_state.candidate_data.get("Years of Experience")
                            
                            # We tell the AI to be a 'Senior Technical Interviewer' for better quality
                            ai_prompt = [{
                                "role": "system", 
                                "content": f"""You are a Senior Technical Interviewer. 
                                The candidate has listed these skills: {stack}.
                                
                                TASK:
                                1. Select 3 different technologies from that list.
                                2. Create ONE deep-dive technical question for each of the 3 selected skills.
                                3. The questions must be suitable for {yoe} years of experience.
                                
                                FORMAT RULES:
                                - Return ONLY the questions.
                                - Do NOT use prefixes like 'Question 1:' or 'Q1:'.
                                - Start each question on a new line.
                                - Do NOT provide answers or introductory text."""
                            },
                            {"role": "user", "content": "Generate the 3 questions now."}]
                            
                            raw_qs = get_ollama_response(ai_prompt)
                            st.session_state.tech_questions = clean_questions(raw_qs)[:3]
                            status.update(label="Questions Verified", state="complete")
                        
                        first_tq = f"### Technical Sequence Active\n\n**Q1:** {st.session_state.tech_questions[0]}"
                        st.session_state.messages.append({"role": "assistant", "content": first_tq})
                st.rerun()

          # STAGE 2: Technical Assessment Answers
            elif st.session_state.current_q_idx < 3:
                # 1. SAVE the current answer before moving to the next question
                current_question_text = st.session_state.tech_questions[st.session_state.current_q_idx]
                save_key = f"Technical Question {st.session_state.current_q_idx + 1}"
                answer_key = f"Technical Answer {st.session_state.current_q_idx + 1}"
                
                # Store both the question asked and the answer given
                st.session_state.candidate_data[save_key] = current_question_text
                st.session_state.candidate_data[answer_key] = prompt
                
                # 2. Increment the index to move to the next question
                st.session_state.current_q_idx += 1
                
                if st.session_state.current_q_idx < 3:
                    # Ask the next question from the generated list
                    next_tq = f"**Question {st.session_state.current_q_idx+1}:** {st.session_state.tech_questions[st.session_state.current_q_idx]}"
                    st.session_state.messages.append({"role": "assistant", "content": next_tq})
                else:
                    # Final Conclusion
                    st.session_state.is_finished = True
                    st.session_state.messages.append({"role": "assistant", "content": "Analysis complete. All technical responses have been logged and secured."})
                    # --- ADD THIS TO SAVE TO VS CODE ---
                    # 1. Prepare the data
                    file_name = "database.json"

                    # 2. Read existing data so we don't delete previous candidates
                    import os
                    existing_data = []
                    if os.path.exists(file_name):
                        try:
                            with open(file_name, "r") as f:
                                existing_data = json.load(f)
                        except:
                            existing_data = []

                    # 3. Add the new candidate to the list
                    existing_data.append(st.session_state.candidate_data)

                    # 4. Save it back to your VS Code folder
                    with open(file_name, "w") as f:
                        json.dump(existing_data, f, indent=4)
                    # -----------------------------------
                st.rerun()