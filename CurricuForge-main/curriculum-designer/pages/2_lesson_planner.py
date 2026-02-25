import streamlit as st
from utils.openai_helper import generate_content, format_lesson_plan
from utils.prompts import LESSON_PLAN_PROMPTS
import re
from datetime import datetime

st.set_page_config(page_title="Lesson Planner 3D", page_icon="📅")

# 3D Custom CSS
st.markdown("""
<style>
    /* ===== 3D LESSON HEADER ===== */
    .lesson-header-3d {
        background: linear-gradient(135deg, rgba(0, 255, 157, 0.2) 0%, rgba(0, 255, 255, 0.2) 100%);
        padding: 3rem;
        border-radius: 30px;
        text-align: center;
        margin-bottom: 2rem;
        border: 2px solid #00ff9d;
        box-shadow: 0 0 30px rgba(0, 255, 157, 0.3);
        transform-style: preserve-3d;
        animation: lessonFloat 8s ease-in-out infinite;
    }

    @keyframes lessonFloat {
        0%, 100% { transform: perspective(1000px) rotateX(2deg) translateZ(0); }
        50% { transform: perspective(1000px) rotateX(0deg) translateZ(30px); }
    }

    /* ===== 3D TIMELINE STEPS ===== */
    .timeline-step-3d {
        background: linear-gradient(135deg, rgba(0, 255, 157, 0.2), rgba(0, 255, 255, 0.2));
        border: 2px solid #00ff9d;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        position: relative;
        transform-style: preserve-3d;
        transition: all 0.3s ease;
        box-shadow: 0 0 30px rgba(0, 255, 157, 0.2);
        animation: stepPulse 3s ease-in-out infinite;
    }

    @keyframes stepPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    .timeline-step-3d:hover {
        transform: perspective(1000px) rotateX(5deg) translateZ(40px);
        box-shadow: 0 0 50px rgba(0, 255, 255, 0.4);
    }

    .step-number {
        font-size: 4rem;
        font-weight: 800;
        color: rgba(0, 255, 157, 0.2);
        position: absolute;
        top: 10px;
        right: 20px;
        z-index: 0;
    }

    /* ===== 3D ACTIVITY CARD ===== */
    .activity-card-3d {
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid #00ff9d;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.2);
    }

    .activity-card-3d::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(0, 255, 157, 0.1) 50%,
            transparent 70%
        );
        transform: rotate(45deg);
        animation: shimmer 4s infinite;
    }

    .activity-card-3d:hover {
        transform: perspective(1000px) rotateX(3deg) translateZ(20px);
        border-color: #00ffff;
        box-shadow: 0 0 40px rgba(0, 255, 255, 0.3);
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }

    /* ===== 3D ENGAGEMENT TAG ===== */
    .engagement-tag-3d {
        background: rgba(0, 255, 157, 0.2);
        border: 1px solid #00ff9d;
        border-radius: 50px;
        padding: 0.5rem 1rem;
        display: inline-block;
        margin: 0.25rem;
        color: #fff;
        font-size: 0.9rem;
        box-shadow: 0 0 15px rgba(0, 255, 157, 0.2);
        transition: all 0.3s ease;
    }

    .engagement-tag-3d:hover {
        transform: translateY(-3px) translateZ(10px);
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.4);
        border-color: #00ffff;
    }

    /* ===== 3D TIME INDICATOR ===== */
    .time-indicator-3d {
        background: linear-gradient(135deg, #00ff9d20, #00ffff20);
        border: 2px solid #00ff9d;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: #00ff9d;
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.3);
        animation: timeGlow 2s ease-in-out infinite;
    }

    @keyframes timeGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 157, 0.3); }
        50% { box-shadow: 0 0 40px rgba(0, 255, 255, 0.4); }
    }

    /* ===== 3D DIFFERENTIATION CARD ===== */
    .diff-card-3d {
        background: linear-gradient(135deg, rgba(255, 0, 170, 0.1), rgba(112, 0, 255, 0.1));
        border: 2px solid #ff00aa;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #fff;
        transform-style: preserve-3d;
        transition: all 0.3s ease;
    }

    .diff-card-3d:hover {
        transform: translateX(10px) translateZ(10px);
        border-color: #7000ff;
        box-shadow: 0 0 30px rgba(255, 0, 170, 0.3);
    }

    /* ===== 3D CLOCK ANIMATION ===== */
    .clock-3d {
        width: 100px;
        height: 100px;
        border: 4px solid #00ff9d;
        border-radius: 50%;
        position: relative;
        margin: 20px auto;
        box-shadow: 0 0 30px #00ff9d;
        animation: clockPulse 2s ease-in-out infinite;
    }

    .clock-3d::before {
        content: '';
        position: absolute;
        width: 4px;
        height: 40px;
        background: #00ff9d;
        top: 10px;
        left: 48px;
        transform-origin: bottom center;
        animation: clockHand 6s linear infinite;
        box-shadow: 0 0 10px #00ff9d;
    }

    .clock-3d::after {
        content: '';
        position: absolute;
        width: 4px;
        height: 30px;
        background: #00ffff;
        top: 20px;
        left: 48px;
        transform-origin: bottom center;
        animation: clockHand 60s linear infinite;
        box-shadow: 0 0 10px #00ffff;
    }

    @keyframes clockHand {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    @keyframes clockPulse {
        0%, 100% { box-shadow: 0 0 30px #00ff9d; }
        50% { box-shadow: 0 0 50px #00ffff; }
    }

    /* ===== 3D PROGRESS BAR ===== */
    .progress-3d {
        width: 100%;
        height: 20px;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        border: 1px solid #00ff9d;
    }

    .progress-3d-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ff9d, #ff00aa);
        border-radius: 10px;
        animation: progressPulse 2s ease-in-out infinite;
        box-shadow: 0 0 20px #00ff9d;
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
        border: 2px solid #00ff9d;
        box-shadow: 0 0 20px #00ff9d;
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
        background: linear-gradient(135deg, #00ff9d20, #ff00aa20);
        border: 2px solid #00ff9d;
        color: #fff;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        display: inline-block;
        margin: 0.5rem 0;
        font-size: 1rem;
        font-weight: 500;
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.3);
        animation: badgeGlow 3s ease-in-out infinite;
    }

    @keyframes badgeGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 157, 0.3); }
        50% { box-shadow: 0 0 30px rgba(255, 0, 170, 0.4); }
    }

    /* ===== 3D SUCCESS MESSAGE ===== */
    .success-3d {
        background: linear-gradient(135deg, #00ff9d20, #00ff9d10);
        border: 2px solid #00ff9d;
        border-radius: 15px;
        padding: 1rem;
        color: #00ff9d;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 0 30px rgba(0, 255, 157, 0.3);
        animation: successPulse 2s ease-in-out infinite;
    }

    @keyframes successPulse {
        0%, 100% { box-shadow: 0 0 30px rgba(0, 255, 157, 0.3); }
        50% { box-shadow: 0 0 50px rgba(255, 0, 170, 0.4); }
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
        background: linear-gradient(135deg, rgba(0, 255, 157, 0.2), rgba(255, 0, 170, 0.2));
        border: 2px solid #00ff9d;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.2);
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
<div class="lesson-header-3d">
    <h1 style="color: #00ff9d;">📅 3D LESSON PLANNER</h1>
    <p style="color: #fff; font-size: 1.2rem;">Design engaging, interactive 3D lessons that captivate your students</p>
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
with st.form("lesson_plan_form"):
    st.markdown("### 📝 3D Lesson Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("Lesson Title*", placeholder="e.g., Introduction to Photosynthesis")
        course = st.text_input("Course Name*", placeholder="e.g., Biology 101")
        duration = st.slider("Lesson Duration (minutes)*", min_value=15, max_value=180, value=60, step=15)
        
    with col2:
        class_size = st.number_input("Class Size*", min_value=1, value=25, max_value=200)
        objectives = st.text_area(
            "Learning Objectives*",
            placeholder="What should students know or be able to do?",
            height=100
        )
    
    st.markdown("### 📚 3D Resources & Prerequisites")
    materials = st.text_input("Materials Needed", placeholder="e.g., Textbook, worksheets, projector")
    prerequisites = st.text_input("Prior Knowledge Required", placeholder="What should students already know?")
    
    # Teaching style
    st.markdown("### 🎯 3D Teaching Approach")
    teaching_style = st.selectbox(
        "Select teaching style",
        options=list(LESSON_PLAN_PROMPTS.keys()),
        format_func=lambda x: x.replace('_', ' ').title()
    )
    
    # Engagement features
    st.markdown("### ✨ 3D Engagement Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        group_work = st.checkbox("👥 Group Activities")
        technology = st.checkbox("💻 Technology Integration")
        brainstorming = st.checkbox("💡 Brainstorming")
    
    with col2:
        hands_on = st.checkbox("✋ Hands-on Exercises")
        discussion = st.checkbox("💬 Class Discussion")
        gamification = st.checkbox("🎮 Gamification")
    
    with col3:
        assessment = st.checkbox("📊 Formative Assessment")
        differentiation = st.checkbox("🎯 Differentiation")
        real_world = st.checkbox("🌍 Real-world Connections")
    
    # Advanced options
    with st.expander("⚙️ 3D Advanced Options"):
        col1, col2 = st.columns(2)
        with col1:
            use_streaming = st.checkbox("Enable 3D streaming output", value=True)
            include_timings = st.checkbox("Include detailed 3D timings", value=True)
        with col2:
            temperature_override = st.slider(
                "3D Temperature override",
                min_value=0.0,
                max_value=1.0,
                value=temperature,
                step=0.1
            )
            include_standards = st.checkbox("Include educational standards", value=False)
    
    submitted = st.form_submit_button("🚀 GENERATE 3D LESSON PLAN", type="primary", use_container_width=True)

if submitted:
    if not all([title, course, duration, objectives]):
        st.markdown("""
        <div class="error-3d">
            ❌ Please fill in all required fields (*)
        </div>
        """, unsafe_allow_html=True)
    else:
        # Collect engagement features
        engagement_features = []
        if group_work: engagement_features.append("group activities")
        if technology: engagement_features.append("technology integration")
        if hands_on: engagement_features.append("hands-on exercises")
        if discussion: engagement_features.append("class discussions")
        if assessment: engagement_features.append("formative assessment")
        if differentiation: engagement_features.append("differentiation strategies")
        if brainstorming: engagement_features.append("brainstorming")
        if gamification: engagement_features.append("gamification")
        if real_world: engagement_features.append("real-world connections")
        
        lesson_data = {
            'title': title,
            'course': course,
            'duration': duration,
            'class_size': class_size,
            'objectives': objectives,
            'materials': materials,
            'prerequisites': prerequisites,
            'include_timings': include_timings,
            'include_standards': include_standards,
            'engagement_features': engagement_features
        }
        
        base_prompt = format_lesson_plan(lesson_data)
        style_prompt = LESSON_PLAN_PROMPTS[teaching_style]
        
        if engagement_features:
            style_prompt += f"\n\n**3D ENGAGEMENT FEATURES:**\n"
            for feature in engagement_features:
                style_prompt += f"• {feature}\n"
        
        full_prompt = f"{base_prompt}\n\n{style_prompt}"
        
        if use_streaming:
            # Show 3D clock animation
            st.markdown('<div class="clock-3d"></div>', unsafe_allow_html=True)
            st.markdown("### ⏰ Generating your 3D lesson plan...")
            
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
            
            lesson_container = st.empty()
            full_response = ""
            
            with st.spinner("Crafting your lesson plan in 3D space..."):
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
                        
                        lesson_container.markdown(f"""
                        <div class="activity-card-3d">
                            <h2 style="color: #00ff9d;">{title}</h2>
                            <p><strong>Course:</strong> {course} | <strong>Duration:</strong> {duration} minutes</p>
                            <p><strong>Class Size:</strong> {class_size} students</p>
                            <div style="background: rgba(0,255,157,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                                <div class="progress-3d">
                                    <div class="progress-3d-fill" style="width: {progress}%"></div>
                                </div>
                                <p style="text-align: center; color: #00ff9d; margin-top: 0.5rem;">3D Generation Progress: {progress:.1f}%</p>
                            </div>
                            <hr style="border-color: #00ff9d;">
                            {full_response}
                        </div>
                        """, unsafe_allow_html=True)
            
            lesson_plan = full_response
        else:
            with st.spinner("🎨 Crafting your 3D lesson plan..."):
                lesson_plan = generate_content(
                    full_prompt, 
                    model=model, 
                    temperature=temperature_override
                )
        
        if lesson_plan:
            st.markdown("""
            <div class="success-3d">
                ✅ 3D Lesson plan generated successfully!
            </div>
            """, unsafe_allow_html=True)
            
            # Save to session state
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content_id = f"Lesson_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.session_state.generated_content[content_id] = {
                'content': lesson_plan,
                'timestamp': timestamp,
                'prompt': f"Lesson Plan: {title}",
                'model': model,
                'temperature': temperature_override
            }
            
            # Display engagement tags
            if engagement_features:
                st.markdown("### ✨ Selected 3D Features")
                tags_html = ""
                for feature in engagement_features:
                    tags_html += f'<span class="engagement-tag-3d">{feature}</span> '
                st.markdown(f'<div>{tags_html}</div>', unsafe_allow_html=True)
            
            # Interactive 3D timeline
            st.markdown("### ⏱️ 3D Lesson Timeline")
            
            cols = st.columns(4)
            timeline_segments = [
                ("🎯 OPENING", "5-10 min", "Hook & Objectives"),
                ("📚 INSTRUCTION", "15-20 min", "Content Delivery"),
                ("✋ PRACTICE", "15-20 min", "Guided & Independent"),
                ("🎉 CLOSING", "5-10 min", "Review & Assessment")
            ]
            
            for i, (col, (title_seg, duration_seg, desc)) in enumerate(zip(cols, timeline_segments)):
                with col:
                    st.markdown(f"""
                    <div class="timeline-step-3d">
                        <div class="step-number">{i+1}</div>
                        <h4 style="color: #00ff9d;">{title_seg}</h4>
                        <div class="time-indicator-3d" style="font-size: 1rem; padding: 0.5rem;">
                            {duration_seg}
                        </div>
                        <p style="color: #fff; margin-top: 0.5rem;">{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📄 3D LESSON", "⏰ 3D TIMELINE", "📋 3D ACTIVITIES", "💾 3D EXPORT"])
            
            with tab1:
                st.markdown(f"""
                <div class="activity-card-3d">
                    <h2 style="color: #00ff9d;">{title}</h2>
                    <p><strong>Course:</strong> {course} | <strong>Duration:</strong> {duration} minutes</p>
                    <p><strong>Class Size:</strong> {class_size} students</p>
                    <p><small>Generated with: {model} | 3D Temperature: {temperature_override}</small></p>
                    <hr style="border-color: #00ff9d;">
                    {lesson_plan}
                </div>
                """, unsafe_allow_html=True)
            
            with tab2:
                st.markdown("### ⏰ Detailed 3D Timeline")
                
                # Extract timeline items
                timeline_pattern = r'(\d+)[-–]\s*(\d+)?\s*minutes?[:\s]+([^\n]+)'
                timeline_items = re.findall(timeline_pattern, lesson_plan, re.IGNORECASE)
                
                if timeline_items:
                    for i, (start, end, activity) in enumerate(timeline_items):
                        duration_text = f"{start}-{end}" if end else f"{start}"
                        st.markdown(f"""
                        <div class="activity-card-3d">
                            <div style="display: flex; align-items: center;">
                                <div class="time-indicator-3d" style="width: 100px; margin-right: 1rem; font-size: 1rem;">
                                    {duration_text}m
                                </div>
                                <div style="flex: 1;">
                                    <strong style="color: #00ff9d;">Layer {i+1}:</strong> {activity}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    # Try alternative pattern
                    time_pattern = r'(\d+)\s*minutes?\s*[–-]?\s*(\d+)?\s*minutes?\s*[:\s]+([^\n]+)'
                    timeline_items = re.findall(time_pattern, lesson_plan, re.IGNORECASE)
                    
                    if timeline_items:
                        for i, (start, end, activity) in enumerate(timeline_items):
                            duration_text = f"{start}-{end}" if end else f"{start}"
                            st.markdown(f"""
                            <div class="activity-card-3d">
                                <div style="display: flex; align-items: center;">
                                    <div class="time-indicator-3d" style="width: 100px; margin-right: 1rem; font-size: 1rem;">
                                        {duration_text}m
                                    </div>
                                    <div style="flex: 1;">
                                        <strong style="color: #00ff9d;">Layer {i+1}:</strong> {activity}
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("3D Timeline details will be extracted from the generated lesson plan")
            
            with tab3:
                st.markdown("### 📋 3D Activities Breakdown")
                
                # Parse activities by section
                sections = [
                    ("Opening", r'(?:Opening|Hook|Warm-up|Introduction)[:\s]+([^\n]+)', "🎯"),
                    ("Instruction", r'(?:Direct Instruction|Lecture|Teaching)[:\s]+([^\n]+)', "📚"),
                    ("Guided Practice", r'(?:Guided Practice|Group Work|Collaborative)[:\s]+([^\n]+)', "🤝"),
                    ("Independent Practice", r'(?:Independent Practice|Individual Work|Application)[:\s]+([^\n]+)', "✋"),
                    ("Closing", r'(?:Closing|Assessment|Exit Ticket|Review)[:\s]+([^\n]+)', "🎉")
                ]
                
                activities_found = False
                for section_name, pattern, emoji in sections:
                    matches = re.findall(pattern, lesson_plan, re.IGNORECASE)
                    if matches:
                        activities_found = True
                        for match in matches:
                            st.markdown(f"""
                            <div class="activity-card-3d">
                                <h4 style="color: #00ff9d;">{emoji} {section_name} Layer</h4>
                                <p>{match}</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                if not activities_found:
                    # Try to extract any bullet points or numbered lists
                    lines = lesson_plan.split('\n')
                    activities = []
                    for line in lines:
                        if line.strip().startswith(('•', '-', '*', '1.', '2.', '3.')):
                            activities.append(line.strip())
                    
                    if activities:
                        for i, activity in enumerate(activities[:8]):
                            st.markdown(f"""
                            <div class="activity-card-3d">
                                <h4 style="color: #00ff9d;">Activity Layer {i+1}</h4>
                                <p>{activity}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("3D Activities breakdown will appear here")
            
            with tab4:
                st.markdown("### 💾 3D Export Options")
                
                # Prepare markdown content with 3D metadata
                markdown_content = f"""# {title} - 3D Lesson Plan

## Lesson Overview (Layer 1)
- **Course:** {course}
- **Duration:** {duration} minutes
- **Class Size:** {class_size} students
- **Teaching Style:** {teaching_style.replace('_', ' ').title()}
- **Generation Date:** {timestamp}
- **AI Model:** {model}
- **3D Temperature:** {temperature_override}

## Learning Objectives (Layer 2)
{objectives}

## Materials Needed (Layer 3)
{materials if materials else 'Standard classroom materials'}

## Prerequisites (Layer 4)
{prerequisites if prerequisites else 'None specified'}

## 3D Engagement Features (Layer 5)
{chr(10).join(['- ' + f for f in engagement_features]) if engagement_features else '- Standard engagement techniques'}

---

## 3D Lesson Content
{lesson_plan}

---
*Generated with OpenAI {model} in 3D mode on {timestamp}*
"""
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        label="📥 3D Markdown",
                        data=markdown_content,
                        file_name=f"{title.lower().replace(' ', '_')}_3d_lesson.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                with col2:
                    # Plain text version
                    plain_text = re.sub(r'[#*`]', '', markdown_content)
                    st.download_button(
                        label="📄 3D Plain Text",
                        data=plain_text,
                        file_name=f"{title.lower().replace(' ', '_')}_3d_lesson.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col3:
                    if st.button("📋 Copy 3D to Clipboard", use_container_width=True):
                        st.balloons()
                        st.success("✅ 3D Content copied!")

# Sidebar with 3D tips
with st.sidebar:
    st.markdown("""
    <div class="tips-card-3d">
        <h3 style="color: #00ff9d;">🎯 3D DIFFERENTIATION</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🤖 3D Configuration")
    st.info(f"""
    **Model:** {model}
    **Temperature:** {temperature}
    **3D Layers:** 5
    """)
    
    with st.expander("📚 For Different Learners"):
        st.markdown("""
        <div class="diff-card-3d">👁️ Visual Layer: Diagrams, charts, videos</div>
        <div class="diff-card-3d">👂 Auditory Layer: Discussions, recordings</div>
        <div class="diff-card-3d">✋ Kinesthetic Layer: Hands-on activities</div>
        """, unsafe_allow_html=True)
    
    with st.expander("⚡ For Quick Learners"):
        st.markdown("""
        <div class="diff-card-3d">📈 Extension Layer: Advanced activities</div>
        <div class="diff-card-3d">🔬 Research Layer: Independent projects</div>
        <div class="diff-card-3d">👥 Leadership Layer: Peer tutoring</div>
        """, unsafe_allow_html=True)
    
    with st.expander("🆘 For Struggling Learners"):
        st.markdown("""
        <div class="diff-card-3d">🪜 Scaffolding Layer: Step-by-step support</div>
        <div class="diff-card-3d">🔄 Practice Layer: Additional exercises</div>
        <div class="diff-card-3d">🤝 Support Layer: One-on-one assistance</div>
        """, unsafe_allow_html=True)
    
    # Show recent 3D lessons
    if st.session_state.generated_content:
        st.markdown("### 🕒 Recent 3D Lessons")
        recent = list(st.session_state.generated_content.items())[-3:]
        for key, value in reversed(recent):
            if "Lesson" in key or "lesson" in key.lower():
                st.markdown(f"""
                <div class="diff-card-3d" style="padding: 0.5rem;">
                    <p style="color: #00ff9d; margin: 0;">{key[:30]}...</p>
                    <p style="color: #666; font-size: 0.8rem; margin: 0;">{value.get('timestamp', '')}</p>
                </div>
                """, unsafe_allow_html=True)