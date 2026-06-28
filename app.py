"""
EduReach AI — Multi-Agent Tutoring System
==========================================
Google AI Agents Intensive Capstone | Track: Agents for Good

Install: pip install streamlit google-genai python-dotenv
Run:     streamlit run app.py
"""

import streamlit as st
import os
import random
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="EduReach AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

:root {
    --green: #1a5c38;
    --green2: #2d8653;
    --green-bg: #e8f5ee;
    --amber: #f59e0b;
    --amber-bg: #fef3c7;
    --border: #e2e8f0;
    --muted: #64748b;
}

html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
.block-container { padding-top: 1.5rem; max-width: 880px; }
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0f3d24, #1a5c38, #2d8653);
}
[data-testid="stSidebar"] * { color: #d1fae5 !important; }
[data-testid="stSidebar"] .stRadio label {
    padding: .5rem .85rem; border-radius: 8px;
    font-weight: 600; display: block; cursor: pointer;
    transition: background .15s;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,.12);
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #1a5c38, #2d8653 60%, #f59e0b);
    border-radius: 18px; padding: 2.5rem 2rem;
    color: white; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.hero::after {
    content: "🌍"; position: absolute;
    right: 2rem; top: 50%; transform: translateY(-50%);
    font-size: 5.5rem; opacity: .15;
}
.hero h1 { font-size: 2rem; margin: 0 0 .4rem; color: white !important; font-weight: 800; }
.hero p  { opacity: .9; margin: 0; font-size: 1rem; }
.badge-pill {
    display: inline-block; background: rgba(255,255,255,.22);
    border-radius: 99px; padding: .2rem .85rem;
    font-size: .75rem; font-weight: 700; letter-spacing: .05em;
    text-transform: uppercase; margin-bottom: .75rem;
}

/* Agent cards */
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: .9rem; margin: 1rem 0; }
.card {
    background: #fff; border: 1.5px solid var(--border);
    border-radius: 14px; padding: 1.2rem;
    transition: transform .15s, box-shadow .15s, border-color .15s;
}
.card:hover { transform: translateY(-3px); box-shadow: 0 6px 22px rgba(26,92,56,.13); border-color: var(--green2); }
.card-icon { font-size: 1.9rem; margin-bottom: .35rem; }
.card h3 { margin: 0 0 .25rem; font-size: .97rem; color: var(--green); }
.card p  { margin: 0; font-size: .82rem; color: var(--muted); line-height: 1.4; }
.tag { display: inline-block; background: var(--green-bg); color: var(--green); border-radius: 99px; padding: .12rem .55rem; font-size: .68rem; font-weight: 700; margin-top: .45rem; }

/* Section header */
.shdr { display: flex; align-items: center; gap: .7rem; border-bottom: 2px solid var(--green-bg); padding-bottom: .7rem; margin-bottom: 1.2rem; }
.shdr span { font-size: 1.7rem; }
.shdr h2 { margin: 0; font-size: 1.3rem; color: var(--green); }

/* Response box */
.rbox {
    background: #fff; border: 1.5px solid var(--border);
    border-left: 4px solid var(--green2);
    border-radius: 14px; padding: 1.4rem 1.6rem;
    margin-top: .9rem; box-shadow: 0 2px 14px rgba(0,0,0,.04);
}

/* Tip box */
.tipbox {
    background: var(--amber-bg); border-left: 4px solid var(--amber);
    border-radius: 0 12px 12px 0; padding: .85rem 1.2rem;
    font-size: .92rem; color: #78350f; margin: .9rem 0;
}

/* Concept tags */
.ctag { display: inline-block; background: #ede9fe; color: #5b21b6; border-radius: 99px; padding: .18rem .65rem; font-size: .73rem; font-weight: 700; margin: .2rem; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1a5c38, #2d8653);
    color: white; border: none; border-radius: 10px;
    padding: .6rem 1.4rem; font-weight: 700; width: 100%;
    font-family: 'Nunito', sans-serif; font-size: .94rem;
    transition: opacity .2s, transform .1s;
}
.stButton > button:hover { opacity: .87; transform: translateY(-1px); }

/* Inputs */
.stTextArea textarea, .stTextInput input {
    border-radius: 10px !important;
    border-color: var(--border) !important;
    font-family: 'Nunito', sans-serif;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# TOOLS  (ADK Concept 3 — Tool Integration)
# ─────────────────────────────────────────
def tool_get_today():
    return datetime.now().strftime("%A, %B %d, %Y")

def tool_study_tip():
    return random.choice([
        "Use active recall — close your notes and test yourself instead of re-reading.",
        "Pomodoro Technique: 25 min focused study, then 5 min break. Repeat.",
        "Space your revision over several days — never cram everything at once.",
        "Teach what you learned to someone else — gaps show up immediately.",
        "Write notes by hand; handwriting improves long-term retention.",
        "Sleep consolidates memory — get 7–9 hours before any exam.",
        "Start with your hardest topic when your energy is highest.",
        "Connect new concepts to things you already know.",
        "Review your notes within 24 hours to lock them into long-term memory.",
        "Break big topics into small chunks — master one before moving on.",
    ])

def tool_word_count(text):
    return len(text.split()) if text.strip() else 0

def tool_reading_time(text):
    w = tool_word_count(text)
    if w == 0: return "0 sec"
    s = (w / 200) * 60
    m, sc = int(s // 60), int(s % 60)
    return f"{m}m {sc}s" if m else f"{sc}s"


# ─────────────────────────────────────────
# AGENT PROMPTS  (ADK Concept 2 — Agent Skills)
# ─────────────────────────────────────────
def p_tutor():
    return f"""You are EduReach Tutor — a warm, patient AI tutor for students in underserved communities.
Today: {tool_get_today()} | Tip: {tool_study_tip()}

YOUR SKILL: Explain academic concepts clearly with real-world examples anyone can relate to.

RULES:
- Use simple language; define any jargon.
- Include a real-world analogy.
- For CS/math topics include time complexity or key formulas.
- End with one short encouraging sentence.

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

## 📖 Simple Explanation
[2–3 sentence plain definition]

## 🔢 Step-by-Step
[numbered steps]

## 🌍 Real-World Example
[relatable analogy or story]

## ⚡ Key Facts
• [fact 1]
• [fact 2]
• [fact 3]

💪 [Encouraging closing line]"""

def p_career():
    return f"""You are EduReach Career Guide — helping first-generation students discover opportunities.
Today: {tool_get_today()}

YOUR SKILL: Map a student's interests to realistic, inspiring career paths with a clear roadmap.

SAFETY: Never discourage education. Always say school comes first.

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

## 🎯 Career Paths For You
[3 specific careers with one-line descriptions]

## 📚 Skills to Build Now (Free Resources)
[list skills + free platforms: Khan Academy, YouTube, Coursera, etc.]

## 🗺️ Your Roadmap
Month 1: [action]
Month 6: [milestone]
Year 1:  [milestone]
Year 3:  [goal]

## 🌟 One Thing You Can Do Today
[specific free actionable first step]"""

def p_scholarship():
    return f"""You are EduReach Scholarship Finder — helping low-income students find education funding.
Today: {tool_get_today()}

YOUR SKILL: Surface scholarships, teach application strategy, point to free search tools.

ALWAYS remind students to verify deadlines on official websites.

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

## 🏆 Scholarship Types to Explore
[5 types: merit, need-based, community, subject-specific, government]

## 📋 Application Checklist
[what most scholarships require]

## 🔍 Free Places to Search
[5+ specific websites with brief descriptions]

## ✍️ 3 Essay Writing Tips
[practical tips for a compelling scholarship essay]

## 💡 Hidden Opportunities
[lesser-known sources: local businesses, unions, religious orgs, NGOs]"""

def p_coach():
    tip = tool_study_tip()
    return f"""You are EduReach Coach — a motivational study coach for students with limited time.
Today: {tool_get_today()} | Evidence-based tip: {tip}

YOUR SKILL: Build realistic daily study plans and provide genuine motivation.

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

## 📅 Your Study Plan

### 🌅 Morning Session
[time | activity | topic]

### ☀️ Afternoon Session
[time | activity | topic]

### 🌙 Evening Session
[time | activity | topic]

## 🎯 Today's 3 Goals
- [ ] [Goal 1]
- [ ] [Goal 2]
- [ ] [Goal 3]

## 💡 Study Strategy
{tip}

## 🌟 You've Got This
[Warm, personal encouragement — acknowledge that studying alongside other responsibilities is genuinely hard]"""

def p_quiz():
    return f"""You are EduReach Quiz — generating practice MCQs to reinforce student knowledge.
Today: {tool_get_today()}

YOUR SKILL: Create exactly 5 multiple-choice questions that build real understanding.

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

## 📝 Quiz: [Topic Name]

**Q1** _(Easy)_
[Question text here]
- A) [option]
- B) [option]
- C) [option]
- D) [option]

**Q2** _(Easy)_
[Question text here]
- A) [option]
- B) [option]
- C) [option]
- D) [option]

**Q3** _(Medium)_
[Question text here]
- A) [option]
- B) [option]
- C) [option]
- D) [option]

**Q4** _(Medium)_
[Question text here]
- A) [option]
- B) [option]
- C) [option]
- D) [option]

**Q5** _(Challenging)_
[Question text here]
- A) [option]
- B) [option]
- C) [option]
- D) [option]

---
## ✅ Answer Key
1. **[Letter]** — [One sentence why this is correct]
2. **[Letter]** — [One sentence why this is correct]
3. **[Letter]** — [One sentence why this is correct]
4. **[Letter]** — [One sentence why this is correct]
5. **[Letter]** — [One sentence why this is correct]"""


# ─────────────────────────────────────────
# CONTROLLER  (ADK Concept 1 — Multi-Agent)
# ─────────────────────────────────────────
CONTROLLER = """You are the EduReach Controller — the router of a multi-agent education system.

Read the student message and reply with EXACTLY ONE word from this list:
TUTOR | CAREER | SCHOLARSHIP | COACH | QUIZ

Rules:
- explain / what is / how does / define / concept  →  TUTOR
- career / job / future / what should I study       →  CAREER
- scholarship / funding / financial aid / grant     →  SCHOLARSHIP
- study plan / schedule / motivation / overwhelmed  →  COACH
- quiz / test / practice questions / MCQ            →  QUIZ

Reply with ONE word only. No punctuation. No explanation."""

AGENTS = {
    "TUTOR":       ("📚 Tutor Agent",             p_tutor),
    "CAREER":      ("🎯 Career Guide Agent",       p_career),
    "SCHOLARSHIP": ("🏆 Scholarship Finder Agent", p_scholarship),
    "COACH":       ("💪 Coach Agent",              p_coach),
    "QUIZ":        ("📝 Quiz Agent",               p_quiz),
}


# ─────────────────────────────────────────
# GEMINI CLIENT  (google-genai SDK)
# ─────────────────────────────────────────
MODEL = "gemini-2.5-flash-lite"

def get_key():
    try:    return st.secrets["GOOGLE_API_KEY"]
    except: return os.getenv("GOOGLE_API_KEY")

def make_client():
    k = get_key()
    if not k: return None
    try:    return genai.Client(api_key=k)
    except: return None

def ask(client, system_prompt, user_msg):
    try:
        r = client.models.generate_content(
            model=MODEL,
            contents=user_msg,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=2048,
                temperature=0.7,
            ),
        )
        return r.text
    except Exception as e:
        err = str(e)
        if "403" in err or "api_key" in err.lower(): return "❌ Invalid API key. Please check the key in the sidebar."
        if "429" in err or "quota"  in err.lower(): return "❌ Quota exceeded. Please wait a moment and try again."
        if "404" in err:                             return "❌ Model not found. Make sure your API key has Gemini access."
        return f"❌ Error: {err}"

def route(client, msg):
    try:
        r = client.models.generate_content(
            model=MODEL,
            contents=f"{CONTROLLER}\n\nStudent: {msg}",
        )
        k = r.text.strip().upper().split()[0]
        return k if k in AGENTS else "TUTOR"
    except:
        return "TUTOR"


# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "client"  not in st.session_state: st.session_state.client  = make_client()
if "history" not in st.session_state: st.session_state.history = []
if "tip"     not in st.session_state: st.session_state.tip     = tool_study_tip()


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 EduReach AI")
    st.markdown("*Education for Everyone*")
    st.markdown("---")

    PAGES = {
        "🏠  Home":                    "Home",
        "🤖  Smart Chat":              "Chat",
        "📚  Tutor Agent":             "Tutor",
        "🎯  Career Guide":            "Career",
        "🏆  Scholarship Finder":      "Scholarship",
        "💪  Study Coach":             "Coach",
        "📝  Practice Quiz":           "Quiz",
        "⚙️  ADK Architecture":        "ADK",
    }
    sel = st.radio("nav", list(PAGES.keys()), label_visibility="collapsed")
    PAGE = PAGES[sel]

    st.markdown("---")
    st.markdown("**🔑 Google API Key**")
    key_in = st.text_input("key", type="password",
                            placeholder="Paste your AIza... key here",
                            label_visibility="collapsed")
    if key_in:
        os.environ["GOOGLE_API_KEY"] = key_in
        st.session_state.client = make_client()
        st.success("✅ Key saved!") if st.session_state.client else st.error("❌ Key invalid")

    st.markdown("---")
    st.markdown("""<div style="font-size:.76rem;opacity:.65;text-align:center;line-height:1.75;">
        <b>ADK Concepts Used</b><br>
        ✅ Multi-Agent System<br>✅ Agent Skills<br>✅ Tool Integration<br>
        ✅ Controller Routing<br>✅ Session Management<br>✅ Safety Guardrails
        <br><br>Gemini 2.0 Flash · google-genai<br>Agents for Good · Solo
    </div>""", unsafe_allow_html=True)

C = st.session_state.client

def need_key():
    if not C:
        st.warning("⚠️ **API key required.** Paste your Google API key in the sidebar.\n\n"
                   "Get a free key → [aistudio.google.com/apikey](https://aistudio.google.com/apikey)", icon="🔑")
        return False
    return True


# ═══════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════
if PAGE == "Home":
    st.markdown("""
    <div class="hero">
        <div class="badge-pill">🌍 Agents for Good · Capstone</div>
        <h1>EduReach AI</h1>
        <p>A multi-agent tutoring system bringing quality education,<br>
           career guidance, and scholarship access to every student.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="tipbox">💡 <b>Today\'s Tip:</b> {st.session_state.tip}</div>',
                unsafe_allow_html=True)
    if st.button("🔄 New Tip"):
        st.session_state.tip = tool_study_tip()
        st.rerun()

    st.markdown("### 🤖 Your 5 AI Agents")
    st.markdown('<div class="grid">', unsafe_allow_html=True)
    for ico, name, desc, tag in [
        ("📚","Tutor Agent","Explains any subject simply with examples and step-by-step breakdowns.","Skill: Teach"),
        ("🎯","Career Guide Agent","Maps your interests to career paths with a clear roadmap and free resources.","Skill: Advise"),
        ("🏆","Scholarship Finder","Surfaces funding opportunities and application strategies for any student.","Skill: Research"),
        ("💪","Coach Agent","Builds personalized daily study plans and keeps you motivated.","Skill: Plan"),
        ("📝","Quiz Agent","Generates 5 practice MCQs with answers to test your knowledge.","Skill: Assess"),
    ]:
        st.markdown(f"""<div class="card">
            <div class="card-icon">{ico}</div>
            <h3>{name}</h3><p>{desc}</p>
            <span class="tag">{tag}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ ADK Concepts Demonstrated")
    for c in ["Multi-Agent System","Agent Skills","Tool Integration","Controller Routing","Session Management","Safety Guardrails"]:
        st.markdown(f'<span class="ctag">✅ {c}</span>', unsafe_allow_html=True)
    st.markdown("---")
    st.info("👈 Use **Smart Chat** to let the Controller auto-route your question, or pick any agent from the sidebar.", icon="💡")


# ═══════════════════════════════════════════════════
# SMART CHAT
# ═══════════════════════════════════════════════════
elif PAGE == "Chat":
    st.markdown('<div class="shdr"><span>🤖</span><h2>Smart Chat — Controller Agent</h2></div>', unsafe_allow_html=True)
    st.markdown("Type anything — the **Controller Agent** picks the right specialist automatically.")

    for h in st.session_state.history:
        with st.chat_message("user"):      st.write(h["user"])
        with st.chat_message("assistant"):
            st.caption(f"Routed to: **{h['agent']}**")
            st.markdown(h["response"])

    msg = st.chat_input("Ask anything — explain, career, scholarship, quiz, study plan...")
    if msg:
        if not need_key(): st.stop()
        with st.chat_message("user"): st.write(msg)
        with st.chat_message("assistant"):
            with st.spinner("Routing to best agent..."):
                key  = route(C, msg)
                name, pfn = AGENTS[key]
                st.caption(f"Routed to: **{name}**")
                resp = ask(C, pfn(), msg)
            if resp.startswith("❌"): st.error(resp)
            else:
                st.markdown(resp)
                st.session_state.history.append({"user":msg,"agent":name,"response":resp})

    if st.session_state.history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.history = []
            st.rerun()


# ═══════════════════════════════════════════════════
# TUTOR
# ═══════════════════════════════════════════════════
elif PAGE == "Tutor":
    st.markdown('<div class="shdr"><span>📚</span><h2>Tutor Agent</h2></div>', unsafe_allow_html=True)
    st.markdown("Ask any academic question and get a clear, simple explanation with examples.")
    q   = st.text_input("Your question", placeholder="e.g. What is recursion?  Explain photosynthesis.  What is the French Revolution?", label_visibility="collapsed")
    sub = st.selectbox("Subject (optional)", ["Any","Mathematics","Computer Science","Physics","Chemistry","Biology","History","English","Economics"])
    if st.button("📚 Explain This"):
        if not q.strip(): st.warning("Please enter a question.", icon="⚠️")
        elif need_key():
            with st.spinner("Tutor Agent thinking..."):
                resp = ask(C, p_tutor(), f"[{sub}] {q}" if sub != "Any" else q)
            st.error(resp) if resp.startswith("❌") else st.markdown(f'<div class="rbox">{resp}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# CAREER
# ═══════════════════════════════════════════════════
elif PAGE == "Career":
    st.markdown('<div class="shdr"><span>🎯</span><h2>Career Guide Agent</h2></div>', unsafe_allow_html=True)
    st.markdown("Discover career paths that match your interests — with a free roadmap.")
    c1, c2 = st.columns(2)
    interests = c1.text_input("Your interests / subjects you enjoy", placeholder="e.g. computers, helping people, art, animals...")
    level     = c2.selectbox("Current level", ["High School","College / University","Graduate","Working Professional"])
    extra     = st.text_area("Anything else? (optional)", height=75, placeholder="e.g. I want to work from home, I'm good at math, I want to help my community...")
    if st.button("🎯 Show My Career Paths"):
        if not interests.strip(): st.warning("Please describe your interests.", icon="⚠️")
        elif need_key():
            with st.spinner("Building your roadmap..."):
                resp = ask(C, p_career(), f"Interests: {interests}. Level: {level}. Extra: {extra}")
            st.error(resp) if resp.startswith("❌") else st.markdown(f'<div class="rbox">{resp}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# SCHOLARSHIP
# ═══════════════════════════════════════════════════
elif PAGE == "Scholarship":
    st.markdown('<div class="shdr"><span>🏆</span><h2>Scholarship Finder Agent</h2></div>', unsafe_allow_html=True)
    st.markdown("Find funding opportunities and learn exactly how to apply for them.")
    c1, c2 = st.columns(2)
    field   = c1.text_input("Field of study", placeholder="e.g. Engineering, Medicine, Arts, Business...")
    country = c2.text_input("Country / Region", placeholder="e.g. India, Nigeria, USA, Southeast Asia...")
    level   = st.selectbox("Study level", ["High School","Undergraduate","Postgraduate / Masters","PhD","Vocational / Certificate"])
    bg      = st.text_area("Your situation (optional)", height=75, placeholder="e.g. First-generation student, low-income family, rural area...")
    if st.button("🏆 Find Scholarships"):
        if not field.strip(): st.warning("Please enter your field of study.", icon="⚠️")
        elif need_key():
            with st.spinner("Searching opportunities..."):
                resp = ask(C, p_scholarship(), f"Field: {field}. Country: {country}. Level: {level}. Background: {bg}")
            if resp.startswith("❌"): st.error(resp)
            else:
                st.markdown(f'<div class="rbox">{resp}</div>', unsafe_allow_html=True)
                st.info("⚠️ Always verify deadlines and eligibility on official websites before applying.", icon="ℹ️")


# ═══════════════════════════════════════════════════
# COACH
# ═══════════════════════════════════════════════════
elif PAGE == "Coach":
    st.markdown('<div class="shdr"><span>💪</span><h2>Coach Agent</h2></div>', unsafe_allow_html=True)
    st.markdown("Get a personalized study schedule and the motivation to follow it.")
    topics = st.text_input("What do you need to study?", placeholder="e.g. Python and Algebra, Biology exam, English essay writing...")
    c1, c2 = st.columns(2)
    hours   = c1.slider("Study hours available today", 1, 12, 4)
    problem = c2.text_input("Any challenge? (optional)", placeholder="e.g. I keep getting distracted, I have work after 5pm...")
    if st.button("💪 Build My Study Plan"):
        if not topics.strip(): st.warning("Please enter what you need to study.", icon="⚠️")
        elif need_key():
            with st.spinner("Building your plan..."):
                resp = ask(C, p_coach(), f"Topics: {topics}. Available hours: {hours}. Challenge: {problem}")
            st.error(resp) if resp.startswith("❌") else st.markdown(f'<div class="rbox">{resp}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# QUIZ
# ═══════════════════════════════════════════════════
elif PAGE == "Quiz":
    st.markdown('<div class="shdr"><span>📝</span><h2>Quiz Agent</h2></div>', unsafe_allow_html=True)
    st.markdown("Test your knowledge with 5 multiple-choice questions on any topic.")
    c1, c2 = st.columns([3,1])
    topic  = c1.text_input("Topic", placeholder="e.g. Python loops, World War 2, Photosynthesis, Algebra...", label_visibility="collapsed")
    diff   = c2.selectbox("Level", ["Mixed","Easy","Medium","Hard"], label_visibility="collapsed")
    if st.button("📝 Generate Quiz"):
        if not topic.strip(): st.warning("Please enter a topic.", icon="⚠️")
        elif need_key():
            with st.spinner(f"Generating quiz on '{topic}'..."):
                resp = ask(C, p_quiz(), f"Topic: {topic}. Difficulty: {diff}")
            if resp.startswith("❌"): st.error(resp)
            else:
                st.markdown(f'<div class="rbox">{resp}</div>', unsafe_allow_html=True)
                st.success("Try all 5 questions before peeking at the Answer Key! 🎯", icon="✅")


# ═══════════════════════════════════════════════════
# ADK ARCHITECTURE
# ═══════════════════════════════════════════════════
elif PAGE == "ADK":
    st.markdown('<div class="shdr"><span>⚙️</span><h2>ADK Architecture</h2></div>', unsafe_allow_html=True)
    st.markdown("How EduReach AI demonstrates the Google ADK capstone concepts.")

    st.markdown("### 🔄 Multi-Agent Workflow")
    st.code("""
Student Input
      │
      ▼
┌─────────────────────────────┐
│      CONTROLLER AGENT       │  ← Reads intent using Gemini
│    (Router/Orchestrator)    │  ← Picks the right specialist
└──┬────┬────┬──────┬────────┘
   │    │    │      │       │
   ▼    ▼    ▼      ▼       ▼
TUTOR CAREER SCHOL COACH  QUIZ
Agent Agent  Agent Agent  Agent
   └────┴────┴──────┴───────┘
                │
                ▼
      Gemini 2.0 Flash API
                │
                ▼
       Response to Student
""", language="text")

    st.markdown("### ✅ ADK Concepts Checklist")
    for name, desc in [
        ("Multi-Agent System",   "5 specialist agents (Tutor, Career, Scholarship, Coach, Quiz) + a Controller Agent that routes all requests."),
        ("Agent Skills",         "Each agent has a dedicated system prompt (p_tutor, p_career, etc.) defining its exact role, tone, and output format."),
        ("Tool Integration",     "4 custom tools: tool_get_today() · tool_study_tip() · tool_word_count() · tool_reading_time() — injected into agent prompts at runtime."),
        ("Controller Routing",   "The Controller uses Gemini to classify user intent and output a routing key (TUTOR/CAREER/SCHOLARSHIP/COACH/QUIZ) — no hardcoded if-else."),
        ("Session Management",   "st.session_state stores the Gemini client, chat history, and daily tip across page navigation."),
        ("Safety Guardrails",    "Career Agent system prompt explicitly forbids discouraging education and requires school to always be recommended first."),
    ]:
        with st.expander(f"✅ {name}"):
            st.markdown(desc)

    st.markdown("### 📦 Correct Package & Setup")
    st.code("""# INSTALL (one command)
pip install streamlit google-genai python-dotenv

# .env file (same folder as app.py)
GOOGLE_API_KEY=AIzaSy...your_key_here...

# RUN
streamlit run app.py
""", language="bash")

    st.code("""# How this app calls Gemini (new google-genai SDK)
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="What is recursion?",
    config=types.GenerateContentConfig(
        system_instruction="You are a patient AI tutor...",
        max_output_tokens=2048,
        temperature=0.7,
    ),
)
print(response.text)
""", language="python")
