import streamlit as st
from openai import OpenAI
import time
from datetime import datetime

def generate_content(prompt, model="gpt-3.5-turbo", temperature=0.7, max_retries=3, streaming=False):
    """Generate content using OpenAI with retry logic and 3D streaming support"""
    
    if not st.session_state.client:
        st.error("OpenAI client not initialized. Please check your API key.")
        return None
    
    for attempt in range(max_retries):
        try:
            if streaming:
                # Streaming mode for 3D effects
                stream = st.session_state.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an expert curriculum designer and educator. Create detailed, professional, and pedagogically sound educational content with clear 3D layered structure and formatting."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=4000,
                    stream=True
                )
                
                full_response = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        yield content
                
                # Save to session state
                if full_response:
                    content_id = f"Content_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    st.session_state.generated_content[content_id] = {
                        'content': full_response,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'prompt': prompt[:100] + '...' if len(prompt) > 100 else prompt,
                        'model': model,
                        'temperature': temperature
                    }
                return full_response
                
            else:
                # Non-streaming mode
                response = st.session_state.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an expert curriculum designer and educator. Create detailed, professional, and pedagogically sound educational content with clear 3D layered structure."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=4000
                )
                
                if response and response.choices[0].message.content:
                    content = response.choices[0].message.content
                    
                    # Save to session state
                    content_id = f"Content_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    st.session_state.generated_content[content_id] = {
                        'content': content,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'prompt': prompt[:100] + '...' if len(prompt) > 100 else prompt,
                        'model': model,
                        'temperature': temperature
                    }
                    return content
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                st.error(f"Failed after {max_retries} attempts: {str(e)}")
                return None
    
    return None

def format_course_outline(course_data):
    """Format course outline data for prompt with 3D structure"""
    return f"""
    Create a comprehensive course outline with 3D layered structure:
    
    Course Title: {course_data['title']}
    Subject Area: {course_data['subject']}
    Target Audience: {course_data['audience']}
    Duration: {course_data['duration']} {course_data['duration_unit']}
    Level: {course_data['level']}
    
    Additional Requirements:
    - {course_data.get('additional_reqs', 'None specified')}
    - Include real-world examples: {course_data.get('include_examples', True)}
    
    Structure with 3D layers:
    
    LAYER 1: COURSE DESCRIPTION
    Write a compelling 2-3 paragraph overview that captures the essence of the course.
    
    LAYER 2: LEARNING OBJECTIVES
    List 5-7 specific, measurable learning objectives using action verbs.
    
    LAYER 3: PREREQUISITES
    List any required prior knowledge, skills, or completed courses.
    
    LAYER 4: COURSE OUTLINE (3D MODULE STRUCTURE)
    For each module/week, include:
    - Module title (3D Layer A)
    - Key topics covered (3D Layer B)
    - Learning activities (3D Layer C)
    - Time commitment (3D Layer D)
    - Resources needed (3D Layer E)
    
    LAYER 5: ASSESSMENT METHODS
    - Formative assessments (ongoing checks)
    - Summative assessments (final evaluations)
    - Grading criteria and weight distribution
    
    LAYER 6: REQUIRED MATERIALS
    List textbooks, software, tools, and other resources.
    
    LAYER 7: COURSE POLICIES
    - Attendance requirements
    - Late work policy
    - Academic integrity guidelines
    - Communication protocols
    """

def format_lesson_plan(lesson_data):
    """Format lesson plan data for prompt with 3D timeline"""
    return f"""
    Create a detailed lesson plan with 3D timeline visualization:
    
    Lesson Title: {lesson_data['title']}
    Course: {lesson_data['course']}
    Duration: {lesson_data['duration']} minutes
    Class Size: {lesson_data['class_size']} students
    
    Learning Objectives:
    {lesson_data['objectives']}
    
    Materials Needed:
    {lesson_data.get('materials', 'Standard classroom materials')}
    
    Prior Knowledge:
    {lesson_data.get('prerequisites', 'None specified')}
    
    Engagement Features:
    {', '.join(lesson_data.get('engagement_features', ['Standard engagement']))}
    
    Structure with 3D timeline layers:
    
    LAYER 1: OPENING (5-10 minutes)
    - Hook/Attention Grabber: Creative way to engage students
    - Review Connection: Link to previous learning
    - Objectives Introduction: Clear statement of goals
    
    LAYER 2: DIRECT INSTRUCTION (15-20 minutes)
    - Key Concept 1: Clear explanation with examples
    - Key Concept 2: Building on previous concept
    - Check for Understanding: Embedded questions
    
    LAYER 3: GUIDED PRACTICE (15-20 minutes)
    - Activity 1: Step-by-step instructions
    - Activity 2: Collaborative element
    - Scaffolding Strategies: Support for learners
    
    LAYER 4: INDEPENDENT PRACTICE (10-15 minutes)
    - Task: Clear expectations and success criteria
    - Differentiation: Options for varied learners
    - Monitoring: How to check progress
    
    LAYER 5: CLOSING (5-10 minutes)
    - Summary: Key takeaways
    - Formative Check: Exit ticket or quick assessment
    - Preview: Connection to next lesson
    
    LAYER 6: DIFFERENTIATION STRATEGIES
    - For struggling learners: Specific supports
    - For English language learners: Language supports
    - For advanced learners: Extension opportunities
    
    LAYER 7: ASSESSMENT AND FEEDBACK
    - Formative checks throughout
    - Success criteria for each activity
    - Feedback methods and timing
    """

def format_assessment(assessment_data):
    """Format assessment data for prompt with 3D structure"""
    return f"""
    Create a comprehensive assessment with 3D layered structure:
    
    Assessment Type: {assessment_data['type']}
    Topic: {assessment_data['topic']}
    Grade Level: {assessment_data['grade_level']}
    Number of Questions: {assessment_data['num_questions']}
    Difficulty Level: {assessment_data['difficulty']}
    Time Limit: {assessment_data.get('time_limit', 60)} minutes
    
    Learning Objectives:
    {assessment_data['objectives']}
    
    Requirements:
    {assessment_data.get('requirements', 'Include variety of question types')}
    Include Bloom's Taxonomy: {assessment_data.get('include_blooms', False)}
    
    Structure with 3D layers:
    
    LAYER 1: STUDENT INSTRUCTIONS
    - Time allowed
    - Total points
    - Format requirements
    - Academic integrity reminder
    
    LAYER 2: MULTIPLE CHOICE SECTION
    For each question:
    - Clear question stem
    - 4 plausible options
    - Indicate correct answer in key
    
    LAYER 3: SHORT ANSWER SECTION
    For each question:
    - Specific prompt
    - Expected length
    - Key points to include
    
    LAYER 4: ESSAY/EXTENDED RESPONSE
    For each prompt:
    - Detailed question
    - Required elements
    - Scoring criteria
    
    LAYER 5: ANSWER KEY
    - Correct answers for objective questions
    - Model answers for subjective questions
    - Point values for each question
    
    LAYER 6: SCORING RUBRIC
    - Grading criteria by section
    - Performance level descriptors
    - Total points calculation
    
    LAYER 7: ASSESSMENT ANALYSIS
    - Skills assessed
    - Difficulty distribution
    - Recommendations for remediation
    """

def initialize_openai_client(api_key):
    """Initialize OpenAI client with error handling"""
    try:
        client = OpenAI(api_key=api_key)
        # Test connection with minimal request
        test_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        return client
    except Exception as e:
        st.error(f"Failed to initialize OpenAI: {str(e)}")
        return None