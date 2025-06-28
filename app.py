"""
Streamlit web application for the LangChain Study Guide Creator.
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
import zipfile
import base64
from io import BytesIO

from study_guide_creator import StudyGuideCreator, StudyGuideRequest
from quiz_generator import QuizResult

# Page configuration
st.set_page_config(
    page_title="LangChain Study Guide Creator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #2E86AB;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .quiz-question {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .flashcard {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'study_guide' not in st.session_state:
        st.session_state.study_guide = None
    if 'quiz' not in st.session_state:
        st.session_state.quiz = None
    if 'quiz_results' not in st.session_state:
        st.session_state.quiz_results = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False

def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📚 LangChain Study Guide Creator</h1>
        <p>Transform your textbooks and lecture materials into comprehensive study guides</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🚀 Getting Started")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key (optional)", 
            type="password",
            help="Enter your OpenAI API key for enhanced AI features. Leave blank to use basic features."
        )
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        st.markdown("---")
        
        # Navigation
        page = st.selectbox(
            "Navigate",
            ["📚 Create Study Guide", "❓ Take Quiz", "📊 Progress Tracking", "ℹ️ About"]
        )
    
    # Main content based on selected page
    if page == "📚 Create Study Guide":
        create_study_guide_page()
    elif page == "❓ Take Quiz":
        quiz_page()
    elif page == "📊 Progress Tracking":
        progress_page()
    elif page == "ℹ️ About":
        about_page()

def create_study_guide_page():
    """Study guide creation page."""
    st.header("📚 Create Your Study Guide")
    
    # Two-column layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📄 Upload Your Material")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'txt', 'docx'],
            help="Upload your textbook, lecture notes, or study material"
        )
        
        # Alternative: Text input
        st.subheader("📝 Or Enter Text Directly")
        text_input = st.text_area(
            "Paste your text here",
            height=200,
            placeholder="Enter your study material text here..."
        )
        
        # Configuration
        st.subheader("⚙️ Configuration")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            subject = st.text_input(
                "Subject", 
                placeholder="e.g., Mathematics, Physics, Biology"
            )
            
            level = st.selectbox(
                "Education Level",
                ["high_school", "undergraduate", "graduate", "professional"],
                index=1
            )
        
        with col_b:
            title = st.text_input(
                "Custom Title (optional)",
                placeholder="Leave blank for auto-generated title"
            )
            
            include_quiz = st.checkbox("Include Quiz", value=True)
            include_visuals = st.checkbox("Include Visualizations", value=True)
        
        # Export formats
        st.subheader("📁 Export Formats")
        export_formats = st.multiselect(
            "Select formats",
            ["html", "pdf", "markdown", "json", "anki"],
            default=["html", "pdf"]
        )
        
        # Generate button
        if st.button("🚀 Generate Study Guide", type="primary"):
            if not subject:
                st.error("Please enter a subject")
                return
            
            if not uploaded_file and not text_input.strip():
                st.error("Please upload a file or enter text")
                return
            
            # Show progress
            with st.spinner("Generating your study guide..."):
                try:
                    creator = StudyGuideCreator()
                    
                    if uploaded_file:
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                            tmp_file.write(uploaded_file.getbuffer())
                            tmp_file_path = tmp_file.name
                        
                        request = StudyGuideRequest(
                            input_file=tmp_file_path,
                            subject=subject,
                            level=level,
                            title=title if title else None,
                            include_quiz=include_quiz,
                            include_visuals=include_visuals,
                            export_formats=export_formats
                        )
                        
                        result = creator.create_study_guide(request)
                        
                        # Clean up temp file
                        os.unlink(tmp_file_path)
                        
                    else:
                        # Use text input
                        result = creator.create_from_text(text_input, subject, level)
                    
                    if result["success"]:
                        st.session_state.study_guide = result["study_guide"]
                        st.session_state.quiz = result.get("quiz")
                        
                        st.success("🎉 Study guide generated successfully!")
                        
                        # Show download links
                        display_download_links(result)
                        
                    else:
                        st.error("Failed to generate study guide")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        # Features overview
        st.subheader("✨ Features")
        
        features = [
            ("📖", "Content Processing", "PDF, DOCX, and text parsing"),
            ("🧠", "AI-Powered", "LangChain integration for smart analysis"),
            ("❓", "Interactive Quizzes", "Auto-generated practice questions"),
            ("📊", "Visual Learning", "Mind maps and concept diagrams"),
            ("📱", "Multiple Formats", "HTML, PDF, Markdown export"),
            ("🎯", "Adaptive Learning", "Personalized quiz recommendations")
        ]
        
        for icon, title, desc in features:
            st.markdown(f"""
            <div class="feature-box">
                <h4>{icon} {title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Sample materials
        st.subheader("📋 Sample Materials")
        if st.button("Create Sample Files"):
            creator = StudyGuideCreator()
            sample_dir = creator.create_sample_materials()
            st.success(f"Sample materials created in: {sample_dir}")
    
    # Display study guide if generated
    if st.session_state.study_guide:
        display_study_guide(st.session_state.study_guide)

def display_study_guide(study_guide):
    """Display the generated study guide."""
    st.markdown("---")
    st.header(f"📚 {study_guide.title}")
    
    # Tabs for different sections
    tabs = st.tabs(["📋 Overview", "🔑 Key Concepts", "📚 Chapters", "❓ Questions", "📝 Flashcards"])
    
    with tabs[0]:
        st.subheader("Overview")
        st.write(study_guide.summary)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Subject", study_guide.subject)
        with col2:
            st.metric("Level", study_guide.level.title())
        with col3:
            st.metric("Key Concepts", len(study_guide.key_concepts))
    
    with tabs[1]:
        st.subheader("🔑 Key Concepts")
        for i, concept in enumerate(study_guide.key_concepts):
            if isinstance(concept, dict):
                with st.expander(f"{i+1}. {concept.get('name', 'Concept')}"):
                    st.write(f"**Definition:** {concept.get('definition', 'No definition available')}")
                    if concept.get('importance'):
                        st.write(f"**Importance:** {concept.get('importance')}")
                    if concept.get('relationships'):
                        st.write(f"**Related to:** {', '.join(concept.get('relationships', []))}")
            else:
                st.write(f"{i+1}. {concept}")
    
    with tabs[2]:
        st.subheader("📚 Chapter Summaries")
        for chapter in study_guide.chapter_summaries:
            with st.expander(chapter['title']):
                st.write(chapter['summary'])
    
    with tabs[3]:
        st.subheader("❓ Practice Questions")
        for i, question in enumerate(study_guide.practice_questions):
            with st.expander(f"Question {i+1}"):
                st.write(f"**{question.get('question', '')}**")
                
                if question.get('options'):
                    for option in question['options']:
                        st.write(f"- {option}")
                
                st.write(f"**Answer:** {question.get('correct_answer', '')}")
                
                if question.get('explanation'):
                    st.write(f"*Explanation:* {question.get('explanation')}")
                
                # Badges
                difficulty = question.get('difficulty', 'medium')
                question_type = question.get('type', 'question')
                st.markdown(f"""
                <span style="background: #007bff; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; margin-right: 5px;">{difficulty}</span>
                <span style="background: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;">{question_type}</span>
                """, unsafe_allow_html=True)
    
    with tabs[4]:
        st.subheader("📝 Flashcards")
        
        # Flashcard viewer
        if study_guide.flashcards:
            flashcard_index = st.selectbox(
                "Select flashcard",
                range(len(study_guide.flashcards)),
                format_func=lambda x: f"Card {x+1}"
            )
            
            flashcard = study_guide.flashcards[flashcard_index]
            
            # Flip card functionality
            if 'show_back' not in st.session_state:
                st.session_state.show_back = False
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if not st.session_state.show_back:
                    st.markdown(f"""
                    <div class="flashcard">
                        <h4>Front</h4>
                        <p>{flashcard.get('front', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="flashcard">
                        <h4>Back</h4>
                        <p>{flashcard.get('back', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🔄 Flip Card"):
                    st.session_state.show_back = not st.session_state.show_back
                    st.experimental_rerun()

def quiz_page():
    """Interactive quiz page."""
    st.header("❓ Take a Quiz")
    
    if not st.session_state.quiz:
        st.info("📝 Generate a study guide first to access quizzes!")
        return
    
    quiz = st.session_state.quiz
    
    if not st.session_state.quiz_started:
        # Quiz introduction
        st.subheader(f"🎯 {quiz.title}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Questions", len(quiz.questions))
        with col2:
            st.metric("Time Limit", f"{quiz.time_limit} min")
        with col3:
            st.metric("Passing Score", f"{quiz.passing_score}%")
        
        if st.button("🚀 Start Quiz", type="primary"):
            st.session_state.quiz_started = True
            st.session_state.current_question = 0
            st.session_state.quiz_answers = {}
            st.experimental_rerun()
    
    else:
        # Quiz interface
        current_q = st.session_state.current_question
        total_q = len(quiz.questions)
        
        if current_q < total_q:
            question = quiz.questions[current_q]
            
            # Progress bar
            progress = (current_q + 1) / total_q
            st.progress(progress)
            st.write(f"Question {current_q + 1} of {total_q}")
            
            # Question
            st.markdown(f"""
            <div class="quiz-question">
                <h4>Question {current_q + 1}</h4>
                <p><strong>{question.get('question', '')}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Answer options
            answer = None
            if question.get('type') == 'multiple_choice':
                options = question.get('options', [])
                answer = st.radio(
                    "Select your answer:",
                    options,
                    key=f"q_{current_q}"
                )
            elif question.get('type') == 'true_false':
                answer = st.radio(
                    "Select your answer:",
                    ["True", "False"],
                    key=f"q_{current_q}"
                )
            else:
                answer = st.text_input(
                    "Enter your answer:",
                    key=f"q_{current_q}"
                )
            
            # Navigation
            col1, col2 = st.columns(2)
            
            with col1:
                if current_q > 0:
                    if st.button("⬅️ Previous"):
                        st.session_state.current_question -= 1
                        st.experimental_rerun()
            
            with col2:
                if answer:
                    st.session_state.quiz_answers[current_q + 1] = answer
                    
                    if current_q < total_q - 1:
                        if st.button("➡️ Next"):
                            st.session_state.current_question += 1
                            st.experimental_rerun()
                    else:
                        if st.button("✅ Submit Quiz", type="primary"):
                            # Evaluate quiz
                            result = evaluate_quiz_results(quiz, st.session_state.quiz_answers)
                            st.session_state.quiz_results.append(result)
                            st.session_state.quiz_started = False
                            st.experimental_rerun()
        
        else:
            # Show results
            if st.session_state.quiz_results:
                show_quiz_results(st.session_state.quiz_results[-1])

def evaluate_quiz_results(quiz, answers):
    """Evaluate quiz results."""
    from quiz_generator import QuizGenerator
    
    quiz_gen = QuizGenerator()
    result = quiz_gen.evaluate_quiz(quiz, answers)
    return result

def show_quiz_results(result):
    """Display quiz results."""
    st.subheader("🎯 Quiz Results")
    
    # Score overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Score", f"{result.score}/{result.total_questions}")
    with col2:
        st.metric("Percentage", f"{result.percentage:.1f}%")
    with col3:
        status = "✅ Passed" if result.percentage >= 70 else "❌ Failed"
        st.metric("Status", status)
    
    # Detailed results
    with st.expander("📊 Detailed Results"):
        for detail in result.detailed_results:
            correct_icon = "✅" if detail['correct'] else "❌"
            st.write(f"{correct_icon} **Question {detail['question_id']}:** {detail['question']}")
            st.write(f"Your answer: {detail['user_answer']}")
            if not detail['correct']:
                st.write(f"Correct answer: {detail['correct_answer']}")
            if detail['explanation']:
                st.write(f"*{detail['explanation']}*")
            st.write("---")
    
    # Recommendations
    if result.recommendations:
        st.subheader("💡 Recommendations")
        for rec in result.recommendations:
            st.write(f"• {rec}")
    
    # Retake button
    if st.button("🔄 Retake Quiz"):
        st.session_state.quiz_started = False
        st.session_state.current_question = 0
        st.session_state.quiz_answers = {}
        st.experimental_rerun()

def progress_page():
    """Progress tracking page."""
    st.header("📊 Progress Tracking")
    
    if not st.session_state.quiz_results:
        st.info("📝 Take some quizzes to see your progress!")
        return
    
    # Progress visualization
    results = st.session_state.quiz_results
    
    # Create progress chart
    import plotly.graph_objects as go
    
    scores = [r.percentage for r in results]
    quiz_numbers = list(range(1, len(scores) + 1))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=quiz_numbers,
        y=scores,
        mode='lines+markers',
        name='Quiz Scores',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_hline(y=70, line_dash="dash", line_color="red", 
                  annotation_text="Passing Score (70%)")
    
    fig.update_layout(
        title="Quiz Score Progress",
        xaxis_title="Quiz Number",
        yaxis_title="Score (%)",
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Quizzes", len(results))
    with col2:
        avg_score = sum(scores) / len(scores)
        st.metric("Average Score", f"{avg_score:.1f}%")
    with col3:
        best_score = max(scores)
        st.metric("Best Score", f"{best_score:.1f}%")
    with col4:
        improvement = scores[-1] - scores[0] if len(scores) > 1 else 0
        st.metric("Improvement", f"{improvement:+.1f}%")

def display_download_links(result):
    """Display download links for generated files."""
    st.subheader("📁 Download Files")
    
    exported_files = result.get("exported_files", {})
    
    for format_type, file_path in exported_files.items():
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            filename = os.path.basename(file_path)
            st.download_button(
                label=f"📄 Download {format_type.upper()}",
                data=file_data,
                file_name=filename,
                mime=get_mime_type(format_type)
            )

def get_mime_type(format_type):
    """Get MIME type for file format."""
    mime_types = {
        'html': 'text/html',
        'pdf': 'application/pdf',
        'markdown': 'text/markdown',
        'json': 'application/json',
        'anki': 'text/csv'
    }
    return mime_types.get(format_type, 'application/octet-stream')

def about_page():
    """About page with information and instructions."""
    st.header("ℹ️ About LangChain Study Guide Creator")
    
    st.markdown("""
    ## 🎯 Purpose
    
    The LangChain Study Guide Creator transforms your textbooks, lecture notes, and study materials 
    into comprehensive, interactive study guides using advanced AI technology.
    
    ## ✨ Features
    
    ### Core Features
    - **📖 Content Processing**: Parse PDF, DOCX, and text files
    - **🧠 AI-Powered Analysis**: Extract key concepts using LangChain
    - **📚 Study Guide Generation**: Create structured summaries and explanations
    - **❓ Interactive Quizzes**: Auto-generate practice questions
    - **📝 Flashcards**: Create digital flashcards for active recall
    - **🎨 Visualizations**: Generate mind maps and concept diagrams
    
    ### Export Options
    - **📄 HTML**: Interactive web-based study guides
    - **📑 PDF**: Printable study materials
    - **📝 Markdown**: Editable text format
    - **💾 JSON**: Machine-readable data
    - **🃏 Anki**: Flashcard import format
    
    ## 🚀 Getting Started
    
    1. **Upload Material**: Choose a PDF, DOCX, or text file
    2. **Configure Settings**: Set subject, education level, and options
    3. **Generate Guide**: Let AI create your comprehensive study guide
    4. **Study & Practice**: Use interactive features and take quizzes
    5. **Track Progress**: Monitor your learning with analytics
    
    ## 🔧 Technical Requirements
    
    - **Python 3.8+**
    - **LangChain Framework**
    - **OpenAI API Key** (optional, for enhanced features)
    - **Internet Connection** (for AI features)
    
    ## 💡 Tips for Best Results
    
    - **Use clear, well-structured documents**
    - **Provide specific subject areas**
    - **Include an OpenAI API key for best AI features**
    - **Review and customize generated content**
    
    ## 📞 Support
    
    For help and documentation, visit our [GitHub repository](https://github.com/your-repo/langchain-study-guide-creator).
    """)
    
    # System information
    with st.expander("🔧 System Information"):
        import sys
        import platform
        
        st.write(f"**Python Version:** {sys.version}")
        st.write(f"**Platform:** {platform.platform()}")
        st.write(f"**Streamlit Version:** {st.__version__}")
        
        # Check for API key
        if os.getenv("OPENAI_API_KEY"):
            st.success("✅ OpenAI API Key detected")
        else:
            st.warning("⚠️ No OpenAI API Key found - using fallback features")

if __name__ == "__main__":
    main()
