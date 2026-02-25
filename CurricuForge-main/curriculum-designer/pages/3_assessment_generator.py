import streamlit as st
from utils.openai_helper import generate_content, format_assessment
from utils.prompts import ASSESSMENT_PROMPTS
import re
from datetime import datetime

st.set_page_config(page_title="Assessment Generator 3D", page_icon="📊")

# 3D Custom CSS
st.markdown("""
<style>
    /* ===== 3D ASSESSMENT HEADER ===== */
    .assessment-header-3d {
        background: linear-gradient(135deg, rgba(255, 0, 170, 0.2) 0%, rgba(112, 0, 255, 0.2) 100%);
        padding: 3rem;
        border-radius: 30px;
        text-align: center;
        margin-bottom: 2rem;
        border: 2px solid #ff00aa;
        box-shadow: 0 0 30px rgba(255, 0, 170, 0.3);
        transform-style: preserve-3d;
        animation: headerPulse 4s ease-in-out infinite;
    }

    @keyframes headerPulse {
        0%, 100% { box-shadow: 0 0 30px rgba(255, 0, 170, 0.3); }
        50% { box-shadow: 0 0 60px rgba(112, 0, 255, 0.4); }
    }

    /* ===== 3D QUESTION CARD ===== */
    .question-card-3d {
        background: rgba(0, 0, 0, 0.8);
        border: 2px solid #ff00aa;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        position: relative;
        transform-style: preserve-3d;
        transition: all 0.3s ease;
        box-shadow: 0 0 30px rgba(255, 0, 170, 0.2);
        overflow: hidden;
    }

    .question-card-3d::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,0,170,0.1) 0%, transparent 70%);
        animation: rotate 10s linear infinite;
    }

    .question-card-3d:hover {
        transform: perspective(1000px) rotateX(3deg) translateZ(30px);
        border-color: #7000ff;
        box-shadow: 0 0 50px rgba(112, 0, 255, 0.4);
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* ===== 3D DIFFICULTY BADGE ===== */
    .difficulty-badge-3d {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-size: 1rem;
        font-weight: 600;
        margin: 0.5rem;
        border: 2px solid;
        transform-style: preserve-3d;
        animation: badgeSpin 3s ease-in-out infinite;
    }

    @keyframes badgeSpin {
        0%, 100% { transform: rotateY(0deg); }
        50% { transform: rotateY(180deg); }
    }

    .easy-3d { 
        background: rgba(0, 255, 0, 0.2); 
        border-color: #00ff00;
        color: #00ff00;
        box-shadow: 0 0 20px #00ff00;
    }
    .medium-3d { 
        background: rgba(255, 255, 0, 0.2); 
        border-color: #ffff00;
        color: #ffff00;
        box-shadow: 0 0 20px #ffff00;
    }
    .hard-3d { 
        background: rgba(255, 0, 0, 0.2); 
        border-color: #ff0000;
        color: #ff0000;
        box-shadow: 0 0 20px #ff0000;
    }

    /* ===== 3D RUBRIC TABLE ===== */
    .rubric-3d {
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid #ff00aa;
        border-radius: 20px;
        overflow: hidden;
        margin: 1rem 0;
        transform-style: preserve-3d;
        perspective: 1000px;
    }

    .rubric-3d table {
        width: 100%;
        border-collapse: collapse;
    }

    .rubric-3d th {
        background: linear-gradient(135deg, #ff00aa40, #7000ff40);
        color: #fff;
        padding: 1rem;
        text-align: left;
        border-bottom: 2px solid #ff00aa;
        font-size: 1.1rem;
    }

    .rubric-3d td {
        padding: 1rem;
        border-bottom: 1px solid rgba(255, 0, 170, 0.3);
        color: #fff;
    }

    .rubric-3d tr:hover {
        background: rgba(255, 0, 170, 0.1);
        transform: translateZ(10px);
    }

    /* ===== 3D STATS CARD ===== */
    .stats-card-3d {
        background: linear-gradient(135deg, rgba(255,0,170,0.2), rgba(112,0,255,0.2));
        border: 2px solid #ff00aa;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
        animation: statsGlow 3s ease-in-out infinite;
    }

    @keyframes statsGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(255,0,170,0.3); }
        50% { box-shadow: 0 0 40px rgba(112,0,255,0.4); }
    }

    .stat-number-3d {
        font-size: 3rem;
        font-weight: 800;
        color: #ff00aa;
        text-shadow: 0 0 20px #ff00aa;
        animation: numberFloat 2s ease-in-out infinite;
    }

    @keyframes numberFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    /* ===== 3D QUESTION BANK ===== */
    .bank-card-3d {
        background: rgba(0, 0, 0, 0.6);
        border: 2px solid #ff00aa;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .bank-card-3d:hover {
        transform: translateX(10px) translateZ(20px);
        border-color: #7000ff;
        box-shadow: 0 0 30px rgba(112,0,255,0.3);
    }

    /* ===== 3D PROGRESS RING ===== */
    .progress-ring-3d {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        border: 10px solid rgba(255,0,170,0.2);
        border-top-color: #ff00aa;
        border-right-color: #7000ff;
        border-bottom-color: #ff00aa;
        border-left-color: #7000ff;
        animation: ringSpin 3s linear infinite;
        margin: 20px auto;
        box-shadow: 0 0 30px rgba(255,0,170,0.3);
    }

    @keyframes ringSpin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* ===== 3D ANSWER KEY CARD ===== */
    .answer-key-3d {
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid #7000ff;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        position: relative;
        box-shadow: 0 0 30px rgba(112,0,255,0.3);
    }

    .answer-key-3d::after {
        content: '✓';
        position: absolute;
        bottom: 20px;
        right: 20px;
        font-size: 4rem;
        color: rgba(112,0,255,0.2);
        animation: checkPulse 2s ease-in-out infinite;
    }

    @keyframes checkPulse {
        0%, 100% { transform: scale(1); opacity: 0.2; }
        50% { transform: scale(1.2); opacity: 0.4; }
    }

    /* ===== 3D BLOOM'S TAXONOMY ===== */
    .blooms-level-3d {
        background: linear-gradient(135deg, #ff00aa20, #7000ff20);
        border: 2px solid #ff00aa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
        transform-style: preserve-3d;
        animation: levelFloat 3s ease-in-out infinite;
    }

    @keyframes levelFloat {
        0%, 100% { transform: translateZ(0); }
        50% { transform: translateZ(20px); }
    }

    /* ===== 3D PROGRESS BAR ===== */
    .progress-3d {
        width: 100%;
        height: 20px;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        border: 1px solid #ff00aa;
    }

    .progress-3d-fill {
        height: 100%;
        background: linear-gradient(90deg, #ff00aa, #7000ff);
        border-radius: 10px;
        animation: progressPulse 2s ease-in-out infinite;
        box-shadow: 0 0 20px #ff00aa;
    }

    @keyframes progressPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }

    /* ===== 3D CUBE LOADER ===== */
    .cube-loader {
        position: relative;
        width: 100px;
        height: 100px;
        margin: 50px auto;
        transform-style: preserve-3d;
        animation: cubeSpin 3s linear infinite;
    }

    .cube-loader div {
        position: absolute;
        width: 100%;
        height: 100%;
        border: 2px solid #ff00aa;
        box-shadow: 0 0 20px #ff00aa;
    }

    .cube-loader .front { transform: translateZ(50px); }
    .cube-loader .back { transform: rotateY(180deg) translateZ(50px); }
    .cube-loader .right { transform: rotateY(90deg) translateZ(50px); }
    .cube-loader .left { transform: rotateY(-90deg) translateZ(50px); }
    .cube-loader .top { transform: rotateX(90deg) translateZ(50px); }
    .cube-loader .bottom { transform: rotateX(-90deg) translateZ(50px); }

    @keyframes cubeSpin {
        from { transform: rotateX(0deg) rotateY(0deg); }
        to { transform: rotateX(360deg) rotateY(360deg); }
    }

    /* ===== 3D MODEL BADGE ===== */
    .model-badge-3d {
        background: linear-gradient(135deg, #ff00aa20, #7000ff20);
        border: 2px solid #ff00aa;
        color: #fff;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        display: inline-block;
        margin: 0.5rem 0;
        font-size: 1rem;
        font-weight: 500;
        box-shadow: 0 0 20px rgba(255, 0, 170, 0.3);
        animation: badgeGlow 3s ease-in-out infinite;
    }

    @keyframes badgeGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 0, 170, 0.3); }
        50% { box-shadow: 0 0 30px rgba(112, 0, 255, 0.4); }
    }

    /* ===== 3D SUCCESS MESSAGE ===== */
    .success-3d {
        background: linear-gradient(135deg, #ff00aa20, #ff00aa10);
        border: 2px solid #ff00aa;
        border-radius: 15px;
        padding: 1rem;
        color: #ff00aa;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 0 30px rgba(255, 0, 170, 0.3);
        animation: successPulse 2s ease-in-out infinite;
    }

    @keyframes successPulse {
        0%, 100% { box-shadow: 0 0 30px rgba(255, 0, 170, 0.3); }
        50% { box-shadow: 0 0 50px rgba(112, 0, 255, 0.4); }
    }

    /* ===== 3D ERROR MESSAGE ===== */
    .error-3d {
        background: linear-gradient(135deg, #ff000020, #ff000010);
        border: 2px solid #ff0000;
        border-radius: 15px;
        padding: 1rem;
        color: #ff6b6b;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.3);
    }

    /* ===== 3D TIPS CARD ===== */
    .tips-card-3d {
        background: linear-gradient(135deg, rgba(255, 0, 170, 0.2), rgba(112, 0, 255, 0.2));
        border: 2px solid #ff00aa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(255, 0, 170, 0.2);
        animation: tipsFloat 5s ease-in-out infinite;
    }

    @keyframes tipsFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="assessment-header-3d">
    <h1 style="color: #ff00aa;">📊 3D ASSESSMENT GENERATOR</h1>
    <p style="color: #fff; font-size: 1.2rem;">Create comprehensive 3D assessments with automatic answer keys and rubrics</p>
</div>
""", unsafe_allow_html=True)

# Check if OpenAI client is initialized
if not st.session_state.get('client'):
    st.markdown("""
    <div class="error-3d">
        ⚠️ Please initialize OpenAI in the main page first to enter 3D mode.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Get model configuration
model = st.session_state.get('model', 'gpt-3.5-turbo')
temperature = st.session_state.get('temperature', 0.7)

# Display current model info
st.markdown(f"""
<div class="model-badge-3d">
    🤖 Current Model: {model} | 🌡️ Temperature: {temperature}
</div>
""", unsafe_allow_html=True)

# Main form
with st.form("assessment_form"):
    st.markdown("### 📝 3D Assessment Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        assessment_type = st.selectbox(
            "Assessment Type*",
            ["Quiz", "Test", "Exam", "Assignment", "Project", "Worksheet"],
            format_func=lambda x: f"📌 {x}"
        )
        topic = st.text_input("Topic/Subject*", placeholder="e.g., Quadratic Equations")
        grade_level = st.text_input("Grade Level*", placeholder="e.g., 10th Grade, College")
        
    with col2:
        num_questions = st.number_input("Number of Questions*", min_value=1, max_value=50, value=10)
        difficulty = st.select_slider(
            "Difficulty Level*",
            options=["Very Easy", "Easy", "Medium", "Hard", "Very Hard"],
            value="Medium"
        )
        time_limit = st.number_input("Time Limit (minutes)", min_value=5, max_value=180, value=60, step=5)
    
    objectives = st.text_area(
        "Learning Objectives Tested*",
        placeholder="What specific knowledge or skills should this assessment measure?",
        height=100
    )
    
    requirements = st.text_area(
        "Additional Requirements",
        placeholder="e.g., Include real-world problems, require written explanations, etc.",
        height=80
    )
    
    # Assessment purpose
    st.markdown("### 🎯 3D Assessment Purpose")
    assessment_style = st.radio(
        "Select the main purpose",
        options=list(ASSESSMENT_PROMPTS.keys()),
        format_func=lambda x: x.title(),
        horizontal=True
    )
    
    # Question types
    st.markdown("### 📋 3D Question Types")
    q_col1, q_col2, q_col3 = st.columns(3)
    
    with q_col1:
        multiple_choice = st.checkbox("🔘 Multiple Choice", value=True)
        true_false = st.checkbox("✅ True/False")
        
    with q_col2:
        short_answer = st.checkbox("📝 Short Answer", value=True)
        essay = st.checkbox("📄 Essay")
        
    with q_col3:
        matching = st.checkbox("🔗 Matching")
        fill_blank = st.checkbox("✏️ Fill in the Blank", value=True)
        diagram = st.checkbox("📊 Diagram/Label")
    
    # Advanced options
    with st.expander("⚙️ 3D Advanced Options"):
        col1, col2 = st.columns(2)
        with col1:
            use_streaming = st.checkbox("Enable 3D streaming output", value=True)
            include_answer_key = st.checkbox("Include 3D answer key", value=True)
            include_rubric = st.checkbox("Include 3D grading rubric", value=True)
        with col2:
            temperature_override = st.slider(
                "3D Temperature override",
                min_value=0.0,
                max_value=1.0,
                value=temperature,
                step=0.1
            )
            include_blooms = st.checkbox("Include Bloom's Taxonomy levels", value=False)
    
    submitted = st.form_submit_button("🚀 GENERATE 3D ASSESSMENT", type="primary", use_container_width=True)

if submitted:
    if not all([topic, grade_level, objectives]):
        st.markdown("""
        <div class="error-3d">
            ❌ Please fill in all required fields (*)
        </div>
        """, unsafe_allow_html=True)
    else:
        # Compile question types
        question_types = []
        if multiple_choice: question_types.append("multiple choice")
        if true_false: question_types.append("true/false")
        if short_answer: question_types.append("short answer")
        if essay: question_types.append("essay")
        if matching: question_types.append("matching")
        if fill_blank: question_types.append("fill in the blank")
        if diagram: question_types.append("diagram labeling")
        
        assessment_data = {
            'type': assessment_type,
            'topic': topic,
            'grade_level': grade_level,
            'num_questions': num_questions,
            'difficulty': difficulty,
            'time_limit': time_limit,
            'objectives': objectives,
            'requirements': f"{requirements}\nQuestion types: {', '.join(question_types)}",
            'include_blooms': include_blooms
        }
        
        base_prompt = format_assessment(assessment_data)
        style_prompt = ASSESSMENT_PROMPTS[assessment_style]
        full_prompt = f"{base_prompt}\n\n{style_prompt}"
        
        if use_streaming:
            # Show 3D progress ring
            st.markdown('<div class="progress-ring-3d"></div>', unsafe_allow_html=True)
            st.markdown("### 📝 Generating your 3D assessment...")
            
            # Show 3D cube loader
            st.markdown("""
            <div class="cube-loader">
                <div class="front"></div>
                <div class="back"></div>
                <div class="right"></div>
                <div class="left"></div>
                <div class="top"></div>
                <div class="bottom"></div>
            </div>
            """, unsafe_allow_html=True)
            
            assessment_container = st.empty()
            full_response = ""
            
            with st.spinner("Creating assessment questions in 3D space..."):
                for chunk in generate_content(
                    full_prompt, 
                    model=model, 
                    temperature=temperature_override,
                    streaming=True
                ):
                    if chunk:
                        full_response += chunk
                        
                        # Calculate progress
                        progress = min(len(full_response) / 50, 100)
                        
                        # Determine difficulty class
                        diff_class = "easy-3d" if difficulty in ["Very Easy", "Easy"] else "medium-3d" if difficulty == "Medium" else "hard-3d"
                        
                        assessment_container.markdown(f"""
                        <div class="question-card-3d">
                            <h2 style="color: #ff00aa;">{topic} - {assessment_type}</h2>
                            <p><strong>Grade Level:</strong> {grade_level} | <strong>Time:</strong> {time_limit} min</p>
                            <p>
                                <span class="difficulty-badge-3d {diff_class}">
                                    {difficulty}
                                </span>
                            </p>
                            <div style="background: rgba(255,0,170,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                                <div class="progress-3d">
                                    <div class="progress-3d-fill" style="width: {progress}%"></div>
                                </div>
                                <p style="text-align: center; color: #ff00aa; margin-top: 0.5rem;">3D Generation Progress: {progress:.1f}%</p>
                            </div>
                            <hr style="border-color: #ff00aa;">
                            {full_response}
                        </div>
                        """, unsafe_allow_html=True)
            
            assessment = full_response
        else:
            with st.spinner("📝 Generating your 3D assessment..."):
                assessment = generate_content(
                    full_prompt, 
                    model=model, 
                    temperature=temperature_override
                )
        
        if assessment:
            st.markdown("""
            <div class="success-3d">
                ✅ 3D Assessment generated successfully!
            </div>
            """, unsafe_allow_html=True)
            
            # Save to session state
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content_id = f"Assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.session_state.generated_content[content_id] = {
                'content': assessment,
                'timestamp': timestamp,
                'prompt': f"Assessment: {topic}",
                'model': model,
                'temperature': temperature_override
            }
            
            # Determine difficulty class
            diff_class = "easy-3d" if difficulty in ["Very Easy", "Easy"] else "medium-3d" if difficulty == "Medium" else "hard-3d"
            
            # Display assessment in tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 3D ASSESSMENT", "🔑 3D ANSWER KEY", "📊 3D RUBRIC", "📈 3D ANALYSIS", "💾 3D EXPORT"])
            
            with tab1:
                st.markdown(f"""
                <div class="question-card-3d">
                    <h2 style="color: #ff00aa;">{topic} - {assessment_type}</h2>
                    <p><strong>Grade Level:</strong> {grade_level} | <strong>Time Limit:</strong> {time_limit} minutes</p>
                    <p><strong>Questions:</strong> {num_questions}</p>
                    <p>
                        <span class="difficulty-badge-3d {diff_class}">
                            {difficulty}
                        </span>
                    </p>
                    <p><small>Generated with: {model} | 3D Temperature: {temperature_override}</small></p>
                    <hr style="border-color: #ff00aa;">
                    {assessment}
                </div>
                """, unsafe_allow_html=True)
            
            with tab2:
                if include_answer_key:
                    with st.spinner("🔑 Generating 3D answer key..."):
                        answer_key_prompt = f"""Create a detailed answer key for this {assessment_type} on {topic} with 3D layered structure:

{assessment}

Format with 3D layers:
Layer 1: Correct answers for multiple choice, true/false
Layer 2: Model answers for short answer
Layer 3: Sample responses for essay questions
Layer 4: Point values and grading criteria
Layer 5: Explanations for correct answers"""
                        
                        if use_streaming:
                            answer_container = st.empty()
                            answer_full = ""
                            for chunk in generate_content(answer_key_prompt, model=model, temperature=0.3, streaming=True):
                                if chunk:
                                    answer_full += chunk
                                    answer_container.markdown(f"""
                                    <div class="answer-key-3d">
                                        <h3 style="color: #7000ff;">🔑 3D Answer Key</h3>
                                        {answer_full}
                                    </div>
                                    """, unsafe_allow_html=True)
                            answer_key = answer_full
                        else:
                            answer_key = generate_content(answer_key_prompt, model=model, temperature=0.3)
                            if answer_key:
                                st.markdown(f"""
                                <div class="answer-key-3d">
                                    <h3 style="color: #7000ff;">🔑 3D Answer Key</h3>
                                    {answer_key}
                                </div>
                                """, unsafe_allow_html=True)
                else:
                    st.info("3D Answer key generation was disabled")
            
            with tab3:
                if include_rubric:
                    with st.spinner("📊 Generating 3D rubric..."):
                        rubric_prompt = f"""Create a detailed scoring rubric for this {assessment_type} on {topic} with 3D layered structure:

{assessment}

Include 3D layers:
Layer 1: Grading criteria for each question type
Layer 2: Point distribution by section
Layer 3: Performance levels (Excellent, Good, Satisfactory, Needs Improvement)
Layer 4: Specific descriptors for each level
Layer 5: Total points and grade calculation"""
                        
                        if use_streaming:
                            rubric_container = st.empty()
                            rubric_full = ""
                            for chunk in generate_content(rubric_prompt, model=model, temperature=0.3, streaming=True):
                                if chunk:
                                    rubric_full += chunk
                                    rubric_container.markdown(f"""
                                    <div class="rubric-3d">
                                        <h3 style="padding: 1rem; color: #ff00aa;">📊 3D Scoring Rubric</h3>
                                        {rubric_full}
                                    </div>
                                    """, unsafe_allow_html=True)
                            rubric = rubric_full
                        else:
                            rubric = generate_content(rubric_prompt, model=model, temperature=0.3)
                            if rubric:
                                st.markdown(f"""
                                <div class="rubric-3d">
                                    <h3 style="padding: 1rem; color: #ff00aa;">📊 3D Scoring Rubric</h3>
                                    {rubric}
                                </div>
                                """, unsafe_allow_html=True)
                else:
                    st.info("3D Rubric generation was disabled")
            
            with tab4:
                st.markdown("### 📈 3D Assessment Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 3D Difficulty Distribution")
                    
                    difficulty_map = {
                        "Very Easy": 10,
                        "Easy": 20,
                        "Medium": 40,
                        "Hard": 20,
                        "Very Hard": 10
                    }
                    
                    for level, percentage in difficulty_map.items():
                        level_class = "easy-3d" if level in ["Very Easy", "Easy"] else "medium-3d" if level == "Medium" else "hard-3d"
                        st.markdown(f"""
                        <div style="margin: 1rem 0;">
                            <span class="difficulty-badge-3d {level_class}" style="font-size: 0.8rem;">{level}</span>
                            <div class="progress-3d">
                                <div class="progress-3d-fill" style="width: {percentage}%; background: {'#00ff00' if level in ['Very Easy','Easy'] else '#ffff00' if level == 'Medium' else '#ff0000'};"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("#### 3D Question Statistics")
                    
                    st.markdown(f"""
                    <div class="stats-card-3d">
                        <div class="stat-number-3d">{num_questions}</div>
                        <p>Total Questions</p>
                        <div class="stat-number-3d" style="font-size: 2rem;">{time_limit}</div>
                        <p>Minutes Allowed</p>
                        <div class="stat-number-3d" style="font-size: 2rem;">{(num_questions/time_limit):.1f}</div>
                        <p>Questions per Minute</p>
                        <div class="stat-number-3d" style="font-size: 2rem;">{len(question_types)}</div>
                        <p>Question Types</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                if include_blooms:
                    st.markdown("#### 🧠 3D Bloom's Taxonomy Distribution")
                    blooms_levels = {
                        "Remember": 15,
                        "Understand": 25,
                        "Apply": 30,
                        "Analyze": 15,
                        "Evaluate": 10,
                        "Create": 5
                    }
                    
                    for level, percentage in blooms_levels.items():
                        st.markdown(f"""
                        <div class="blooms-level-3d">
                            <strong>{level}</strong>
                            <div class="progress-3d" style="margin-top: 0.5rem;">
                                <div class="progress-3d-fill" style="width: {percentage}%; background: linear-gradient(90deg, #ff00aa, #7000ff);"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            with tab5:
                st.markdown("### 💾 3D Export Options")
                
                # Prepare markdown content
                markdown_content = f"""# {topic} - {assessment_type} (3D Assessment)

## Assessment Overview (Layer 1)
- **Grade Level:** {grade_level}
- **Time Limit:** {time_limit} minutes
- **Total Questions:** {num_questions}
- **Difficulty:** {difficulty}
- **Question Types:** {', '.join(question_types)}
- **Generation Date:** {timestamp}
- **AI Model:** {model}
- **3D Temperature:** {temperature_override}

## Learning Objectives (Layer 2)
{objectives}

## Additional Requirements (Layer 3)
{requirements if requirements else 'None specified'}

---

## Assessment Content (Layer 4)
{assessment}

---
*Generated with OpenAI {model} in 3D mode on {timestamp}*
"""
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        label="📥 3D Markdown",
                        data=markdown_content,
                        file_name=f"{topic.lower().replace(' ', '_')}_3d_assessment.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                with col2:
                    # Plain text version
                    plain_text = re.sub(r'[#*`]', '', markdown_content)
                    st.download_button(
                        label="📄 3D Plain Text",
                        data=plain_text,
                        file_name=f"{topic.lower().replace(' ', '_')}_3d_assessment.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col3:
                    if st.button("📋 Copy 3D to Clipboard", use_container_width=True):
                        st.balloons()
                        st.success("✅ 3D Content copied!")

# Sidebar with question bank
with st.sidebar:
    st.markdown("""
    <div class="tips-card-3d">
        <h3 style="color: #ff00aa;">📚 3D QUESTION BANK</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🤖 3D Configuration")
    st.info(f"""
    **Model:** {model}
    **Temperature:** {temperature}
    **3D Layers:** 5
    """)
    
    if 'question_bank' not in st.session_state:
        st.session_state.question_bank = []
    
    # Quick question generator
    with st.expander("➕ Add 3D Question"):
        q_topic = st.text_input("Topic", key="q_topic")
        q_type = st.selectbox("Type", ["Multiple Choice", "Short Answer", "Essay", "True/False"])
        q_difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])
        
        if st.button("Generate 3D Question", use_container_width=True):
            if q_topic:
                with st.spinner("Generating 3D question..."):
                    q_prompt = f"Generate one {q_difficulty} {q_type} question about {q_topic} with clear formatting"
                    question = generate_content(q_prompt, model=model, temperature=0.5)
                    
                    if question:
                        st.session_state.question_bank.append({
                            'question': question,
                            'topic': q_topic,
                            'type': q_type,
                            'difficulty': q_difficulty,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                        st.markdown("""
                        <div class="success-3d" style="padding: 0.5rem;">
                            ✅ 3D Question added!
                        </div>
                        """, unsafe_allow_html=True)
                        st.rerun()
    
    # Display question bank
    if st.session_state.question_bank:
        st.markdown("### 📌 Saved 3D Questions")
        for i, q in enumerate(reversed(st.session_state.question_bank[-5:])):
            diff_class = "easy-3d" if q['difficulty'] == "Easy" else "medium-3d" if q['difficulty'] == "Medium" else "hard-3d"
            st.markdown(f"""
            <div class="bank-card-3d">
                <span class="difficulty-badge-3d {diff_class}" style="font-size: 0.7rem; padding: 0.25rem 0.75rem;">{q['difficulty']}</span>
                <span style="color: #ff00aa;">{q['type']}</span>
                <p style="color: #fff; margin-top: 0.5rem; font-size: 0.9rem;">{q['topic']}</p>
                <p style="color: #666; font-size: 0.7rem;">{q.get('timestamp', '')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if len(st.session_state.question_bank) > 5:
            st.caption(f"... and {len(st.session_state.question_bank) - 5} more 3D questions")
        
        if st.button("🗑️ Clear 3D Bank", use_container_width=True):
            st.session_state.question_bank = []
            st.rerun()
    else:
        st.info("No 3D questions saved yet")