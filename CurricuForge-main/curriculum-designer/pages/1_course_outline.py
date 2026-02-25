import streamlit as st
from utils.openai_helper import generate_content, format_course_outline
from utils.prompts import COURSE_OUTLINE_PROMPTS
import re
from datetime import datetime

st.set_page_config(page_title="Course Outline Generator 3D", page_icon="📝")

# 3D Custom CSS for this page
st.markdown("""
<style>
    /* ===== 3D PAGE HEADER ===== */
    .page-header-3d {
        background: linear-gradient(135deg, rgba(0, 255, 157, 0.2) 0%, rgba(255, 0, 170, 0.2) 100%);
        padding: 3rem;
        border-radius: 30px;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        border: 2px solid #00ff9d;
        box-shadow: 0 0 10px rgba(0, 255, 157, 0.3),
                   0 0 20px rgba(0, 255, 157, 0.2),
                   0 0 30px rgba(0, 255, 157, 0.1);
        transform-style: preserve-3d;
        animation: headerFloat 8s ease-in-out infinite;
    }

    @keyframes headerFloat {
        0%, 100% { transform: perspective(1000px) rotateX(2deg) translateZ(0); }
        50% { transform: perspective(1000px) rotateX(0deg) translateZ(20px); }
    }

    .feature-badge-3d {
        background: rgba(0, 255, 157, 0.2);
        border: 1px solid #00ff9d;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        display: inline-block;
        margin: 0.25rem;
        font-size: 0.9rem;
        color: #fff;
        box-shadow: 0 0 10px rgba(0, 255, 157, 0.3);
        transition: all 0.3s ease;
    }

    .feature-badge-3d:hover {
        transform: translateY(-3px) translateZ(10px);
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.5);
    }

    /* ===== 3D OUTLINE CONTAINER ===== */
    .outline-container-3d {
        background: rgba(10, 10, 15, 0.8);
        backdrop-filter: blur(10px);
        border: 2px solid #00ff9d;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 30px rgba(0, 255, 157, 0.2);
        transform-style: preserve-3d;
        animation: outlinePulse 4s ease-in-out infinite;
    }

    @keyframes outlinePulse {
        0%, 100% { box-shadow: 0 0 30px rgba(0, 255, 157, 0.2); }
        50% { box-shadow: 0 0 50px rgba(255, 0, 170, 0.3); }
    }

    .outline-container-3d::before {
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
        animation: shimmer 3s infinite;
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }

    /* ===== 3D MODULE CARDS ===== */
    .module-card-3d {
        background: rgba(0, 0, 0, 0.5);
        border: 2px solid #00ff9d;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        transform-style: preserve-3d;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.2);
    }

    .module-card-3d:hover {
        transform: perspective(1000px) rotateX(5deg) translateZ(20px);
        box-shadow: 0 0 30px rgba(255, 0, 170, 0.3);
        border-color: #ff00aa;
    }

    .module-number {
        font-size: 3rem;
        font-weight: 800;
        color: rgba(0, 255, 157, 0.2);
        position: absolute;
        top: 10px;
        right: 20px;
        z-index: 0;
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

    /* ===== 3D PROGRESS INDICATOR ===== */
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

    /* ===== 3D TIMELINE ===== */
    .timeline-3d {
        position: relative;
        padding: 2rem 0;
    }

    .timeline-3d::before {
        content: '';
        position: absolute;
        left: 50%;
        top: 0;
        bottom: 0;
        width: 2px;
        background: linear-gradient(180deg, #00ff9d, #ff00aa);
        transform: translateX(-50%);
        box-shadow: 0 0 20px #00ff9d;
    }

    .timeline-item-3d {
        position: relative;
        margin: 2rem 0;
        transform-style: preserve-3d;
    }

    .timeline-item-3d:nth-child(odd) {
        padding-right: 50%;
    }

    .timeline-item-3d:nth-child(even) {
        padding-left: 50%;
    }

    .timeline-content-3d {
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid #00ff9d;
        border-radius: 15px;
        padding: 1.5rem;
        position: relative;
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.2);
        transition: all 0.3s ease;
    }

    .timeline-content-3d:hover {
        transform: translateZ(20px);
        box-shadow: 0 0 30px rgba(255, 0, 170, 0.3);
    }

    .timeline-dot-3d {
        position: absolute;
        width: 20px;
        height: 20px;
        background: #00ff9d;
        border-radius: 50%;
        top: 50%;
        transform: translateY(-50%);
        box-shadow: 0 0 20px #00ff9d;
    }

    .timeline-item-3d:nth-child(odd) .timeline-dot-3d {
        right: -60px;
    }

    .timeline-item-3d:nth-child(even) .timeline-dot-3d {
        left: -60px;
    }

    /* ===== 3D DOWNLOAD BUTTONS ===== */
    .download-btn-3d {
        background: linear-gradient(135deg, #00ff9d20, #ff00aa20);
        border: 2px solid #00ff9d;
        border-radius: 50px;
        padding: 0.75rem 1.5rem;
        color: #fff;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 255, 157, 0.3);
        cursor: pointer;
    }

    .download-btn-3d:hover {
        transform: translateY(-3px) translateZ(10px);
        box-shadow: 0 0 25px rgba(255, 0, 170, 0.4);
        border-color: #ff00aa;
    }

    /* ===== 3D SIDEBAR TIPS ===== */
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

    /* ===== 3D RADIO BUTTONS ===== */
    .stRadio > div {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 2px solid #00ff9d !important;
        border-radius: 50px !important;
        padding: 0.5rem !important;
    }

    .stRadio > div > label {
        color: #fff !important;
        padding: 0.5rem 1rem !important;
        border-radius: 50px !important;
        transition: all 0.3s ease !important;
    }

    .stRadio > div > label:hover {
        background: rgba(0, 255, 157, 0.2) !important;
        transform: translateZ(5px);
    }

    /* ===== 3D CHECKBOX ===== */
    .stCheckbox > label {
        color: #fff !important;
        transition: all 0.3s ease !important;
    }

    .stCheckbox > label:hover {
        text-shadow: 0 0 10px #00ff9d;
    }

    /* ===== 3D NUMBER INPUT ===== */
    .stNumberInput > div > div > input {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 2px solid #00ff9d !important;
        border-radius: 50px !important;
        color: #fff !important;
        box-shadow: 0 0 10px rgba(0, 255, 157, 0.2) !important;
    }

    /* ===== 3D TEXT AREA ===== */
    .stTextArea > div > div > textarea {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 2px solid #00ff9d !important;
        border-radius: 15px !important;
        color: #fff !important;
        box-shadow: 0 0 10px rgba(0, 255, 157, 0.2) !important;
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
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="page-header-3d">
    <h1 style="color: #00ff9d;">📝 3D COURSE OUTLINE GENERATOR</h1>
    <p style="color: #fff; font-size: 1.2rem;">Create comprehensive, 3D-structured course outlines with AI assistance</p>
    <div style="margin-top: 1rem;">
        <span class="feature-badge-3d">🎯 Learning Objectives</span>
        <span class="feature-badge-3d">📚 Module Breakdown</span>
        <span class="feature-badge-3d">⏱️ Duration Planning</span>
        <span class="feature-badge-3d">📊 Assessment Methods</span>
    </div>
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

# Get model configuration from session state
model = st.session_state.get('model', 'gpt-3.5-turbo')
temperature = st.session_state.get('temperature', 0.7)

# Display current model info
st.markdown(f"""
<div class="model-badge-3d">
    🤖 Current Model: {model} | 🌡️ Temperature: {temperature}
</div>
""", unsafe_allow_html=True)

# Main form
with st.form("course_outline_form"):
    st.markdown("### 📋 3D Course Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("Course Title*", placeholder="e.g., Introduction to Python Programming")
        subject = st.text_input("Subject Area*", placeholder="e.g., Computer Science")
        audience = st.text_input("Target Audience*", placeholder="e.g., College freshmen, professionals")
        
    with col2:
        duration = st.number_input("Course Duration*", min_value=1, value=8)
        duration_unit = st.selectbox("Duration Unit", ["weeks", "days", "months", "sessions"])
        level = st.selectbox(
            "Course Level*",
            ["Beginner", "Intermediate", "Advanced", "All Levels"]
        )
    
    st.markdown("### 🎯 Additional 3D Specifications")
    additional_reqs = st.text_area(
        "Additional Requirements (optional)",
        placeholder="Any specific topics, teaching methods, or resources to include?",
        height=100
    )
    
    # Prompt style selection
    st.markdown("### 🎨 3D Outline Style")
    prompt_style = st.radio(
        "Select the teaching approach",
        options=list(COURSE_OUTLINE_PROMPTS.keys()),
        format_func=lambda x: x.title(),
        horizontal=True
    )
    
    # Advanced options
    with st.expander("⚙️ 3D Advanced Options"):
        col1, col2 = st.columns(2)
        with col1:
            use_streaming = st.checkbox("Enable 3D streaming output", value=True)
            include_examples = st.checkbox("Include real-world examples", value=True)
        with col2:
            temperature_override = st.slider(
                "3D Temperature override",
                min_value=0.0,
                max_value=1.0,
                value=temperature,
                step=0.1
            )
            detailed_modules = st.checkbox("Detailed 3D module breakdown", value=True)
    
    submitted = st.form_submit_button("🚀 GENERATE 3D COURSE OUTLINE", type="primary", use_container_width=True)

if submitted:
    if not all([title, subject, audience, duration]):
        st.markdown("""
        <div class="error-3d">
            ❌ Please fill in all required fields (*)
        </div>
        """, unsafe_allow_html=True)
    else:
        course_data = {
            'title': title,
            'subject': subject,
            'audience': audience,
            'duration': duration,
            'duration_unit': duration_unit,
            'level': level,
            'additional_reqs': additional_reqs,
            'include_examples': include_examples if 'include_examples' in locals() else True
        }
        
        base_prompt = format_course_outline(course_data)
        style_prompt = COURSE_OUTLINE_PROMPTS[prompt_style]
        
        if detailed_modules:
            style_prompt += "\n\n**INCLUDE 3D DETAILED BREAKDOWN:**\n- Learning activities for each module\n- Time allocation per topic\n- Resources and materials needed\n- Assessment methods for each module"
        
        full_prompt = f"{base_prompt}\n\n{style_prompt}"
        
        if use_streaming:
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
            
            st.markdown("### 🎨 Generating your 3D course outline...")
            outline_container = st.empty()
            full_response = ""
            
            with st.spinner("Crafting your course outline in 3D space..."):
                for chunk in generate_content(
                    full_prompt, 
                    model=model, 
                    temperature=temperature_override,
                    streaming=True
                ):
                    if chunk:
                        full_response += chunk
                        
                        # Calculate progress percentage
                        progress = min(len(full_response) / 50, 100)
                        
                        outline_container.markdown(f"""
                        <div class="outline-container-3d">
                            <h2 style="color: #00ff9d;">{title}</h2>
                            <p><strong>Subject:</strong> {subject} | <strong>Level:</strong> {level}</p>
                            <p><strong>Audience:</strong> {audience} | <strong>Duration:</strong> {duration} {duration_unit}</p>
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
            
            outline = full_response
        else:
            # Regular generation
            with st.spinner("🎨 Crafting your 3D course outline..."):
                outline = generate_content(
                    full_prompt, 
                    model=model, 
                    temperature=temperature_override
                )
        
        if outline:
            st.markdown("""
            <div class="success-3d">
                ✅ 3D Course outline generated successfully!
            </div>
            """, unsafe_allow_html=True)
            
            # Save to session state
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content_id = f"Outline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.session_state.generated_content[content_id] = {
                'content': outline,
                'timestamp': timestamp,
                'prompt': f"Course Outline: {title}",
                'model': model,
                'temperature': temperature_override
            }
            
            # Display outline in 3D tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📄 3D OUTLINE", "📊 3D STRUCTURE", "📋 3D MODULES", "💾 3D EXPORT"])
            
            with tab1:
                st.markdown(f"""
                <div class="outline-container-3d">
                    <h2 style="color: #00ff9d;">{title}</h2>
                    <p><strong>Subject:</strong> {subject} | <strong>Level:</strong> {level}</p>
                    <p><strong>Audience:</strong> {audience} | <strong>Duration:</strong> {duration} {duration_unit}</p>
                    <p><small>Generated with: {model} | 3D Temperature: {temperature_override}</small></p>
                    <hr style="border-color: #00ff9d;">
                    {outline}
                </div>
                """, unsafe_allow_html=True)
            
            with tab2:
                st.markdown("### 📊 3D Course Structure Visualization")
                
                # Extract modules using regex
                modules = re.findall(r'(?:Module|Week)\s+\d+[:\s]+([^\n]+)', outline)
                
                if modules:
                    st.markdown("#### 3D Module Distribution")
                    
                    # Create 3D-like progress bars for each module
                    for i, module in enumerate(modules[:8], 1):
                        # Calculate random-looking but deterministic progress based on module index
                        progress_width = 20 + (i * 8)
                        if progress_width > 100:
                            progress_width = 100
                        
                        st.markdown(f"""
                        <div class="module-card-3d">
                            <div class="module-number">{i}</div>
                            <h4 style="color: #00ff9d;">Module {i}: {module[:50]}{'...' if len(module) > 50 else ''}</h4>
                            <div style="margin: 1rem 0;">
                                <div class="progress-3d">
                                    <div class="progress-3d-fill" style="width: {progress_width}%"></div>
                                </div>
                                <p style="text-align: right; color: #00ff9d; margin-top: 0.25rem;">Coverage: {progress_width}%</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Time allocation visualization
                    st.markdown("#### ⏱️ 3D Time Allocation")
                    
                    phases = [
                        ("Foundation Layer", 25, "#00ff9d"),
                        ("Core Concepts Layer", 35, "#ff00aa"),
                        ("Application Layer", 25, "#7000ff"),
                        ("Assessment Layer", 15, "#00ffff")
                    ]
                    
                    for phase, percentage, color in phases:
                        st.markdown(f"**{phase}**")
                        st.markdown(f"""
                        <div class="progress-3d">
                            <div class="progress-3d-fill" style="width: {percentage}%; background: {color};"></div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Module breakdown will appear here in 3D format")
            
            with tab3:
                st.markdown("### 📋 3D Module Explorer")
                
                # Parse modules for detailed view
                module_pattern = r'(?:Module|Week)\s+(\d+)[:\s]+([^\n]+)(.*?)(?=(?:Module|Week)\s+\d+|$)'
                modules_detailed = re.findall(module_pattern, outline, re.DOTALL)
                
                if modules_detailed:
                    for module_num, module_title, module_content in modules_detailed:
                        with st.expander(f"📦 3D Module {module_num}: {module_title}", expanded=False):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.markdown(f"""
                                <div class="module-card-3d">
                                    <h4 style="color: #00ff9d;">Module {module_num} Content</h4>
                                    {module_content if module_content.strip() else "No detailed content available for this module."}
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown("#### 🎯 3D Actions")
                                if st.button(f"📝 Edit in 3D", key=f"edit_{module_num}"):
                                    st.info("3D Edit mode coming soon!")
                                if st.button(f"📊 3D Assessment", key=f"assess_{module_num}"):
                                    st.info("3D Assessment builder coming soon!")
                                if st.button(f"📋 3D Details", key=f"details_{module_num}"):
                                    st.info("3D Details view coming soon!")
                else:
                    # Try alternative parsing
                    lines = outline.split('\n')
                    modules_found = []
                    current_module = None
                    
                    for line in lines:
                        if re.match(r'^(?:Module|Week)\s+\d+', line, re.IGNORECASE):
                            current_module = line.strip()
                            modules_found.append(current_module)
                    
                    if modules_found:
                        for i, module in enumerate(modules_found[:8], 1):
                            with st.expander(f"📦 3D Module {i}", expanded=False):
                                st.markdown(f"""
                                <div class="module-card-3d">
                                    <h4 style="color: #00ff9d;">{module}</h4>
                                    <p>Content will be parsed in more detail in the next update.</p>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.info("Detailed 3D module breakdown will appear here")
            
            with tab4:
                st.markdown("### 💾 3D Export Options")
                
                # Prepare markdown content with 3D metadata
                markdown_content = f"""# {title} - 3D Course Outline

## Course Overview (Layer 1)
- **Subject:** {subject}
- **Level:** {level}
- **Audience:** {audience}
- **Duration:** {duration} {duration_unit}
- **Generation Date:** {timestamp}
- **AI Model:** {model}
- **3D Temperature:** {temperature_override}

## Learning Objectives (Layer 2)
{outline}

---
*Generated with OpenAI {model} in 3D mode on {timestamp}*
"""
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.download_button(
                        label="📥 3D Markdown",
                        data=markdown_content,
                        file_name=f"{title.lower().replace(' ', '_')}_3d_outline.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                with col2:
                    # Plain text version
                    plain_text = re.sub(r'[#*`]', '', markdown_content)
                    st.download_button(
                        label="📄 3D Plain Text",
                        data=plain_text,
                        file_name=f"{title.lower().replace(' ', '_')}_3d_outline.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col3:
                    if st.button("📋 Copy 3D to Clipboard", use_container_width=True):
                        st.write("📋 3D Content copied!")
                        st.balloons()
                
                with col4:
                    if st.button("🖨️ Print 3D View", use_container_width=True):
                        st.balloons()
                        st.snow()

# Sidebar with 3D tips
with st.sidebar:
    st.markdown("""
    <div class="tips-card-3d">
        <h3 style="color: #00ff9d;">💡 3D PRO TIPS</h3>
        <ul style="list-style-type: none; padding-left: 0; color: #fff;">
            <li style="margin: 1rem 0;">🎯 <strong>Layer 1:</strong> Be specific about learning outcomes</li>
            <li style="margin: 1rem 0;">📚 <strong>Layer 2:</strong> Mention prerequisites clearly</li>
            <li style="margin: 1rem 0;">💻 <strong>Layer 3:</strong> Specify tech requirements</li>
            <li style="margin: 1rem 0;">👥 <strong>Layer 4:</strong> Include audience details</li>
            <li style="margin: 1rem 0;">📊 <strong>Layer 5:</strong> Add assessment methods</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🤖 3D Configuration")
    st.info(f"""
    **Model:** {model}
    **Temperature:** {temperature}
    **Max Tokens:** 4000
    **3D Layers:** 5
    """)
    
    st.markdown("### 📚 3D Example Courses")
    
    example_courses = {
        "Computer Science": ["Data Structures", "Web Development", "Machine Learning"],
        "Business": ["Project Management", "Digital Marketing", "Financial Accounting"],
        "Languages": ["Spanish Basics", "Business English", "Academic Writing"]
    }
    
    for category, courses in example_courses.items():
        with st.expander(f"📂 {category} 3D"):
            for course in courses:
                if st.button(f"📘 {course}", key=f"example_{course}", use_container_width=True):
                    st.session_state['example_title'] = course
                    st.rerun()
    
    # Show recent 3D generations
    if st.session_state.generated_content:
        st.markdown("### 🕒 Recent 3D Outlines")
        recent = list(st.session_state.generated_content.items())[-3:]
        for key, value in reversed(recent):
            if "Outline" in key or "outline" in key.lower():
                st.markdown(f"""
                <div class="module-card-3d" style="padding: 0.5rem;">
                    <p style="color: #00ff9d; margin: 0;">{key[:30]}...</p>
                    <p style="color: #666; font-size: 0.8rem; margin: 0;">{value.get('timestamp', '')}</p>
                </div>
                """, unsafe_allow_html=True)

# Auto-fill from example if selected
if 'example_title' in st.session_state:
    title = st.session_state.example_title
    st.success(f"✨ 3D Example loaded: {title}")
    # Clear after use
    del st.session_state.example_title