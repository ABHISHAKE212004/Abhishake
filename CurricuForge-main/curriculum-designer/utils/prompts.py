# Pre-defined prompts for different educational scenarios with 3D structure

COURSE_OUTLINE_PROMPTS = {
    "beginner": """
    Create a beginner-friendly course outline with 3D progressive structure:
    
    LAYER 1 (Foundation): Start with fundamental concepts, basic terminology, and core principles
    - Use simple, clear language
    - Include plenty of examples
    - Break complex ideas into digestible chunks
    
    LAYER 2 (Building): Introduce simple applications and basic problem-solving
    - Step-by-step instructions
    - Guided practice opportunities
    - Frequent checkpoints
    
    LAYER 3 (Practice): Include guided exercises and step-by-step activities
    - Scaffolded worksheets
    - Peer learning activities
    - Immediate feedback loops
    
    LAYER 4 (Connection): Connect concepts to real-world examples
    - Relevant case studies
    - Practical applications
    - Student-relevant scenarios
    
    LAYER 5 (Confidence): Review and practice with simple assessments
    - Low-stakes quizzes
    - Self-assessment tools
    - Progress tracking
    
    Additional 3D elements:
    - Visual learning suggestions
    - Confidence-building checkpoints
    - Common misconceptions to address
    - Scaffolding for struggling learners
    """,
    
    "intermediate": """
    Create an intermediate-level course outline with 3D interconnected structure:
    
    LAYER 1 (Foundation): Review and connect prior knowledge with new concepts
    - Knowledge activation activities
    - Bridging concepts
    - Prerequisite review
    
    LAYER 2 (Depth): Introduce complex concepts with real-world connections
    - Theoretical frameworks
    - Industry examples
    - Current research
    
    LAYER 3 (Application): Explore practical applications and case studies
    - Real-world problems
    - Authentic scenarios
    - Project-based learning
    
    LAYER 4 (Analysis): Develop critical thinking through analysis and evaluation
    - Case study analysis
    - Problem-solving frameworks
    - Evaluation criteria
    
    LAYER 5 (Synthesis): Synthesize learning through projects and presentations
    - Integration projects
    - Collaborative work
    - Presentation skills
    
    Additional 3D elements:
    - Cross-topic connections
    - Problem-solving scenarios
    - Collaborative elements
    - Reflection points
    """,
    
    "advanced": """
    Create an advanced course outline with 3D deep-dive structure:
    
    LAYER 1 (Theory): Cutting-edge theory, current research, and emerging trends
    - Research papers
    - Theoretical debates
    - Future directions
    
    LAYER 2 (Complexity): Complex problem-solving with multiple variables
    - Multi-step problems
    - Systems thinking
    - Uncertainty management
    
    LAYER 3 (Innovation): Creative application and innovation challenges
    - Design thinking
    - Innovation frameworks
    - Creative solutions
    
    LAYER 4 (Expertise): Professional applications and industry standards
    - Professional practices
    - Industry certifications
    - Expert insights
    
    LAYER 5 (Mastery): Original research or complex project development
    - Research proposals
    - Capstone projects
    - Publication opportunities
    
    Additional 3D elements:
    - Research opportunities
    - Mentorship components
    - Leadership development
    - Professional networking
    """
}

LESSON_PLAN_PROMPTS = {
    "interactive": """
    Design an interactive lesson with 3D engagement layers:
    
    LAYER 1 - HOOK (0-5 min): Capture attention
    - Surprising fact or demonstration
    - Provocative question
    - Quick activity
    
    LAYER 2 - EXPLORE (5-15 min): Hands-on discovery
    - Group investigation
    - Guided inquiry
    - Experimentation
    
    LAYER 3 - EXPLAIN (15-25 min): Concept development
    - Student explanations
    - Teacher clarification
    - Visual representations
    
    LAYER 4 - ELABORATE (25-35 min): Application
    - Real-world problems
    - Creative projects
    - Technology integration
    
    LAYER 5 - EVALUATE (35-45 min): Assessment
    - Formative checks
    - Peer feedback
    - Self-reflection
    
    Engagement strategies:
    - Think-pair-share
    - Movement activities
    - Digital tools
    - Games and simulations
    """,
    
    "lecture_based": """
    Design a lecture-based lesson with 3D presentation structure:
    
    LAYER 1 - PRE-LECTURE (0-5 min): Set the stage
    - Guiding questions
    - Prior knowledge activation
    - Learning objectives
    
    LAYER 2 - CORE CONTENT (5-25 min): Main presentation
    - Clear structure
    - Visual aids
    - Key examples
    
    LAYER 3 - INTERACTION (25-35 min): Student engagement
    - Quick activities
    - Discussion breaks
    - Concept checks
    
    LAYER 4 - APPLICATION (35-45 min): Practice
    - Guided problems
    - Case studies
    - Group work
    
    LAYER 5 - REVIEW (45-50 min): Closure
    - Summary
    - Exit ticket
    - Preview
    
    Enhancement strategies:
    - Storytelling
    - Analogies
    - Humor
    - Vocal variety
    """,
    
    "project_based": """
    Design a project-based lesson with 3D project layers:
    
    LAYER 1 - LAUNCH (0-15 min): Project introduction
    - Driving question
    - Real-world context
    - Success criteria
    
    LAYER 2 - RESEARCH (15-30 min): Information gathering
    - Guided research
    - Resource collection
    - Expert input
    
    LAYER 3 - PLAN (30-40 min): Project planning
    - Timeline creation
    - Role assignment
    - Resource allocation
    
    LAYER 4 - CREATE (40-70 min): Project development
    - Milestone work
    - Peer collaboration
    - Teacher check-ins
    
    LAYER 5 - PRESENT (70-90 min): Sharing and reflection
    - Presentations
    - Feedback
    - Reflection
    
    Project scaffolding:
    - Checkpoints
    - Rubrics
    - Templates
    - Peer review
    """
}

ASSESSMENT_PROMPTS = {
    "formative": """
    Create formative assessments with 3D diagnostic layers:
    
    LAYER 1 - QUICK CHECKS (1-2 min each)
    - Entrance tickets
    - Thumbs up/down
    - Mini whiteboards
    - Poll questions
    
    LAYER 2 - DURING INSTRUCTION (3-5 min each)
    - Think-pair-share
    - Concept questions
    - Observation checklists
    - Digital response systems
    
    LAYER 3 - APPLICATION (5-10 min each)
    - Problem-solving demos
    - Skill practice
    - Group work observations
    - Peer assessment
    
    LAYER 4 - END OF LESSON (3-5 min)
    - Exit tickets
    - Summary writing
    - Concept maps
    - Self-assessment
    
    LAYER 5 - CUMULATIVE (10-15 min)
    - Weekly quizzes
    - Progress checks
    - Portfolio reviews
    - Student conferences
    
    For each assessment include:
    - Purpose and timing
    - Success criteria
    - Feedback method
    - Follow-up actions
    """,
    
    "summative": """
    Create summative assessments with 3D evaluation layers:
    
    LAYER 1 - KNOWLEDGE (30% of assessment)
    - Multiple choice questions
    - True/false with explanations
    - Matching exercises
    - Fill-in-the-blank
    
    LAYER 2 - COMPREHENSION (25% of assessment)
    - Short answer questions
    - Summaries
    - Explanations
    - Comparisons
    
    LAYER 3 - APPLICATION (25% of assessment)
    - Problem-solving
    - Case studies
    - Real-world scenarios
    - Data interpretation
    
    LAYER 4 - ANALYSIS (20% of assessment)
    - Essay questions
    - Research analysis
    - Critical evaluation
    - Synthesis tasks
    
    LAYER 5 - COMPREHENSIVE
    - Answer key with explanations
    - Scoring guidelines
    - Rubrics
    - Grade calculation
    
    Include:
    - Clear instructions
    - Point distributions
    - Time allocations
    - Accommodation notes
    """,
    
    "diagnostic": """
    Create diagnostic assessments with 3D discovery layers:
    
    LAYER 1 - PRIOR KNOWLEDGE
    - Prerequisite concept checks
    - Related topic questions
    - Experience surveys
    - Skill self-ratings
    
    LAYER 2 - MISCONCEPTIONS
    - Common error questions
    - Distractor analysis
    - Explanation tasks
    - Concept comparison
    
    LAYER 3 - READINESS
    - Basic skill checks
    - Vocabulary assessment
    - Foundational knowledge
    - Learning preferences
    
    LAYER 4 - LEARNING PROFILE
    - Strengths identification
    - Challenge areas
    - Learning preferences
    - Interest surveys
    
    LAYER 5 - RECOMMENDATIONS
    - Learning paths
    - Interventions
    - Enrichment
    - Goal setting
    
    Analysis templates:
    - Score interpretation
    - Pattern identification
    - Action planning
    - Progress tracking
    """
}