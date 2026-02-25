import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="AI Curriculum Designer 3D",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SIMPLIFIED 3D CSS (No Three.js - Pure CSS 3D)
st.markdown("""
<style>
    /* ===== 3D VARIABLES ===== */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #00ff9d;
        --secondary: #ff00aa;
        --tertiary: #7000ff;
        --dark-bg: #0a0a0f;
        --glass-bg: rgba(10, 10, 15, 0.8);
        --neon-shadow: 0 0 10px #00ff9d, 0 0 20px #00ff9d, 0 0 30px #00ff9d;
    }

    /* ===== GLOBAL STYLES ===== */
    .stApp {
        background: var(--dark-bg);
        color: #fff;
        font-family: 'Rajdhani', sans-serif;
    }

    /* ===== 3D TEXT EFFECTS ===== */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        animation: textGlow 2s ease-in-out infinite;
    }

    @keyframes textGlow {
        0%, 100% { text-shadow: 0 0 10px var(--primary); }
        50% { text-shadow: 0 0 20px var(--secondary); }
    }

    /* ===== 3D CARDS ===== */
    .card-3d {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 2px solid var(--primary);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        transform-style: preserve-3d;
        transform: perspective(1000px) rotateX(0deg);
        transition: all 0.3s ease;
        box-shadow: 0 0 20px var(--primary);
        animation: cardFloat 4s ease-in-out infinite;
    }

    .card-3d:hover {
        transform: perspective(1000px) rotateX(5deg) translateY(-10px);
        box-shadow: 0 0 30px var(--secondary);
        border-color: var(--secondary);
    }

    @keyframes cardFloat {
        0%, 100% { transform: perspective(1000px) rotateX(0deg) translateY(0); }
        50% { transform: perspective(1000px) rotateX(2deg) translateY(-10px); }
    }

    /* ===== 3D BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
        color: black !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 20px var(--primary) !important;
    }

    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 30px var(--secondary) !important;
    }

    /* ===== 3D INPUTS ===== */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 2px solid var(--primary) !important;
        border-radius: 10px !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--secondary) !important;
        box-shadow: 0 0 20px var(--secondary) !important;
        transform: translateY(-2px);
    }

    /* ===== 3D PROGRESS BAR ===== */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
        border-radius: 10px !important;
        height: 10px !important;
        animation: progressPulse 2s ease-in-out infinite;
    }

    @keyframes progressPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    /* ===== 3D METRIC CARDS ===== */
    .metric-3d {
        background: linear-gradient(135deg, rgba(0,255,157,0.2), rgba(255,0,170,0.2));
        border: 2px solid var(--primary);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        animation: metricFloat 3s ease-in-out infinite;
    }

    .metric-3d:hover {
        transform: translateY(-10px) scale(1.05);
        border-color: var(--secondary);
        box-shadow: 0 0 30px var(--secondary);
    }

    @keyframes metricFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }

    /* ===== 3D LOADER ===== */
    .loader-3d {
        width: 50px;
        height: 50px;
        border: 5px solid rgba(0,255,157,0.3);
        border-top-color: var(--primary);
        border-right-color: var(--secondary);
        border-radius: 50%;
        animation: spin3D 1s linear infinite;
        margin: 20px auto;
    }

    @keyframes spin3D {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* ===== 3D SUCCESS MESSAGE ===== */
    .success-3d {
        background: linear-gradient(135deg, rgba(0,255,157,0.2), rgba(0,255,157,0.1));
        border: 2px solid var(--primary);
        border-radius: 10px;
        padding: 1rem;
        color: var(--primary);
        text-align: center;
        animation: successGlow 2s ease-in-out infinite;
    }

    @keyframes successGlow {
        0%, 100% { box-shadow: 0 0 20px var(--primary); }
        50% { box-shadow: 0 0 30px var(--secondary); }
    }

    /* ===== 3D ERROR MESSAGE ===== */
    .error-3d {
        background: linear-gradient(135deg, rgba(255,0,0,0.2), rgba(255,0,0,0.1));
        border: 2px solid #ff0000;
        border-radius: 10px;
        padding: 1rem;
        color: #ff6b6b;
        text-align: center;
        animation: errorGlow 2s ease-in-out infinite;
    }

    @keyframes errorGlow {
        0%, 100% { box-shadow: 0 0 20px #ff0000; }
        50% { box-shadow: 0 0 30px #ff6b6b; }
    }

    /* ===== 3D HEADER ===== */
    .header-3d {
        background: linear-gradient(135deg, rgba(0,255,157,0.2), rgba(255,0,170,0.2));
        border: 2px solid var(--primary);
        border-radius: 30px;
        padding: 3rem;
        text-align: center;
        margin-bottom: 2rem;
        animation: headerFloat 5s ease-in-out infinite;
    }

    @keyframes headerFloat {
        0%, 100% { transform: perspective(1000px) rotateX(0deg); }
        50% { transform: perspective(1000px) rotateX(2deg); }
    }

    /* ===== 3D TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0,0,0,0.5) !important;
        border: 2px solid var(--primary) !important;
        border-radius: 50px !important;
        padding: 0.5rem !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: white !important;
        border-radius: 50px !important;
        transition: all 0.3s ease !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
        color: black !important;
    }

    /* ===== 3D EXPANDER ===== */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(0,255,157,0.2), rgba(255,0,170,0.2)) !important;
        border: 2px solid var(--primary) !important;
        border-radius: 10px !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }

    .streamlit-expanderHeader:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px var(--primary);
    }

    /* ===== BACKGROUND EFFECT ===== */
    .bg-effect {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: radial-gradient(circle at 20% 30%, rgba(0,255,157,0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 70%, rgba(255,0,170,0.1) 0%, transparent 50%);
        animation: bgMove 10s ease-in-out infinite;
    }

    @keyframes bgMove {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
</style>

<div class="bg-effect"></div>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv("OPENAI_API_KEY", "")
if 'client' not in st.session_state:
    st.session_state.client = None
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = {}
if 'model' not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.7

def initialize_openai():
    """Initialize OpenAI client"""
    try:
        if st.session_state.api_key:
            st.session_state.client = OpenAI(api_key=st.session_state.api_key)
            # Test connection
            test_response = st.session_state.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True
    except Exception as e:
        st.error(f"Error initializing OpenAI: {str(e)}")
        return False
    return False

def generate_openai_response(prompt, model="gpt-3.5-turbo", temperature=0.7):
    """Generate response using OpenAI"""
    try:
        response = st.session_state.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert curriculum designer and educator. Create detailed, professional educational content."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="card-3d">
        <h2 style="color: #00ff9d; text-align: center;">🎓 AI CURRICULUM<br>DESIGNER 3D</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input(
        "OpenAI API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-..."
    )
    
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        st.session_state.client = None
    
    st.markdown("### 🤖 Model Selection")
    model = st.selectbox(
        "Choose OpenAI Model",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
        index=0
    )
    st.session_state.model = model
    
    temperature = st.slider(
        "🌡️ Creativity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )
    st.session_state.temperature = temperature
    
    if st.button("🚀 Initialize OpenAI", type="primary", use_container_width=True):
        if initialize_openai():
            st.markdown("""
            <div class="success-3d">
                ✅ OpenAI initialized successfully!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="error-3d">
                ❌ Failed to initialize OpenAI
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🧭 Navigation")
    page = st.radio(
        "Go to",
        ["🏠 Home", "📝 Course Outline", "📅 Lesson Planner", "📊 Assessment"],
        index=0
    )

# Main content
if page == "🏠 Home":
    st.markdown("""
    <div class="header-3d">
        <h1 style="color: #00ff9d;">🎓 AI CURRICULUM DESIGNER 3D</h1>
        <p style="color: white; font-size: 1.2rem;">Welcome to the future of educational content creation</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.api_key:
        st.markdown("""
        <div class="card-3d">
            <h3 style="color: #ff00aa;">👋 Welcome!</h3>
            <p>Please enter your OpenAI API key in the sidebar to get started.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-3d">
                <h1 style="color: #00ff9d; font-size: 3rem;">📝</h1>
                <h3>Course Outlines</h3>
                <p>Create structured modules</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-3d">
                <h1 style="color: #ff00aa; font-size: 3rem;">📅</h1>
                <h3>Lesson Plans</h3>
                <p>Design timelines</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-3d">
                <h1 style="color: #7000ff; font-size: 3rem;">📊</h1>
                <h3>Assessments</h3>
                <p>Generate evaluations</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card-3d">
            <h3 style="color: #00ff9d;">✨ Welcome to 3D Curriculum Design</h3>
            <p>Navigate through our tools using the sidebar to create professional educational content.</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "📝 Course Outline":
    st.markdown("""
    <div class="header-3d">
        <h1 style="color: #00ff9d;">📝 3D COURSE OUTLINE</h1>
        <p>Create comprehensive course outlines</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.get('client'):
        st.markdown("""
        <div class="error-3d">
            ⚠️ Please initialize OpenAI in the sidebar first.
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.form("course_outline_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Course Title*", placeholder="e.g., Introduction to Python")
                subject = st.text_input("Subject Area*", placeholder="e.g., Computer Science")
                
            with col2:
                audience = st.text_input("Target Audience*", placeholder="e.g., College students")
                level = st.selectbox("Course Level", ["Beginner", "Intermediate", "Advanced"])
            
            duration = st.slider("Course Duration (weeks)", 1, 52, 8)
            additional = st.text_area("Additional Requirements", placeholder="Any specific topics?")
            
            if st.form_submit_button("🚀 GENERATE 3D OUTLINE", type="primary", use_container_width=True):
                if all([title, subject, audience]):
                    with st.spinner("Creating 3D outline..."):
                        # Show loader
                        st.markdown('<div class="loader-3d"></div>', unsafe_allow_html=True)
                        
                        prompt = f"Create a detailed {level} level course outline for {title} in {subject} for {audience} over {duration} weeks. Additional requirements: {additional}"
                        response = generate_openai_response(prompt, model=model, temperature=temperature)
                        
                        if response:
                            st.markdown("""
                            <div class="success-3d">
                                ✅ 3D Outline generated successfully!
                            </div>
                            """, unsafe_allow_html=True)
                            
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                            st.session_state.generated_content[f"Outline: {title}"] = {
                                'content': response,
                                'timestamp': timestamp
                            }
                            
                            st.markdown(f"""
                            <div class="card-3d">
                                <h2 style="color: #00ff9d;">{title}</h2>
                                <p><strong>Subject:</strong> {subject} | <strong>Level:</strong> {level}</p>
                                <hr>
                                {response}
                            </div>
                            """, unsafe_allow_html=True)

elif page == "📅 Lesson Planner":
    st.markdown("""
    <div class="header-3d">
        <h1 style="color: #00ff9d;">📅 3D LESSON PLANNER</h1>
        <p>Design engaging lesson plans</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.get('client'):
        st.markdown("""
        <div class="error-3d">
            ⚠️ Please initialize OpenAI in the sidebar first.
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.form("lesson_plan_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                lesson_title = st.text_input("Lesson Title*", placeholder="e.g., Introduction to Variables")
                course = st.text_input("Course Name*", placeholder="e.g., Python Programming 101")
                
            with col2:
                duration = st.number_input("Duration (minutes)*", min_value=15, value=60, step=15)
                objectives = st.text_area("Learning Objectives*", placeholder="What should students learn?", height=100)
            
            materials = st.text_input("Materials Needed", placeholder="e.g., Textbook, worksheets")
            
            if st.form_submit_button("🚀 GENERATE 3D LESSON", type="primary", use_container_width=True):
                if all([lesson_title, course, objectives]):
                    with st.spinner("Creating 3D lesson plan..."):
                        st.markdown('<div class="loader-3d"></div>', unsafe_allow_html=True)
                        
                        prompt = f"Create a detailed {duration} minute lesson plan for {lesson_title} in {course}. Learning objectives: {objectives}. Materials: {materials}"
                        response = generate_openai_response(prompt, model=model, temperature=temperature)
                        
                        if response:
                            st.markdown("""
                            <div class="success-3d">
                                ✅ 3D Lesson Plan generated successfully!
                            </div>
                            """, unsafe_allow_html=True)
                            
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                            st.session_state.generated_content[f"Lesson: {lesson_title}"] = {
                                'content': response,
                                'timestamp': timestamp
                            }
                            
                            st.markdown(f"""
                            <div class="card-3d">
                                <h2 style="color: #00ff9d;">{lesson_title}</h2>
                                <p><strong>Course:</strong> {course} | <strong>Duration:</strong> {duration} minutes</p>
                                <hr>
                                {response}
                            </div>
                            """, unsafe_allow_html=True)

elif page == "📊 Assessment":
    st.markdown("""
    <div class="header-3d">
        <h1 style="color: #ff00aa;">📊 3D ASSESSMENT GENERATOR</h1>
        <p>Create quizzes, tests, and assignments</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.get('client'):
        st.markdown("""
        <div class="error-3d">
            ⚠️ Please initialize OpenAI in the sidebar first.
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.form("assessment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                topic = st.text_input("Topic/Subject*", placeholder="e.g., Quadratic Equations")
                grade = st.text_input("Grade Level*", placeholder="e.g., 10th Grade")
                
            with col2:
                num_questions = st.number_input("Number of Questions", min_value=1, max_value=50, value=10)
                difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])
            
            assessment_type = st.selectbox("Assessment Type", ["Quiz", "Test", "Assignment", "Project"])
            objectives = st.text_area("Learning Objectives Tested*", placeholder="What should this assessment measure?")
            
            if st.form_submit_button("🚀 GENERATE 3D ASSESSMENT", type="primary", use_container_width=True):
                if all([topic, grade, objectives]):
                    with st.spinner("Creating 3D assessment..."):
                        st.markdown('<div class="loader-3d"></div>', unsafe_allow_html=True)
                        
                        prompt = f"Create a {difficulty} level {assessment_type} for {topic} for {grade} with {num_questions} questions. Learning objectives: {objectives}. Include a mix of question types and an answer key."
                        response = generate_openai_response(prompt, model=model, temperature=temperature)
                        
                        if response:
                            st.markdown("""
                            <div class="success-3d">
                                ✅ 3D Assessment generated successfully!
                            </div>
                            """, unsafe_allow_html=True)
                            
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                            st.session_state.generated_content[f"Assessment: {topic}"] = {
                                'content': response,
                                'timestamp': timestamp
                            }
                            
                            st.markdown(f"""
                            <div class="card-3d">
                                <h2 style="color: #ff00aa;">{topic} - {assessment_type}</h2>
                                <p><strong>Grade Level:</strong> {grade} | <strong>Difficulty:</strong> {difficulty}</p>
                                <hr>
                                {response}
                            </div>
                            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 3rem; border-top: 2px solid #00ff9d;">
    <p>Powered by OpenAI | Built with Streamlit 3D</p>
    <p style="opacity: 0.7;">© 2024 AI Curriculum Designer 3D</p>
</div>
""", unsafe_allow_html=True)