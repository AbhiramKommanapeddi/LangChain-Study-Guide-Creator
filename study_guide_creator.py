"""
Main StudyGuideCreator class that orchestrates the entire study guide creation process.
"""

import os
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import json

from content_processor import ContentProcessor, ProcessedContent
from guide_generator import GuideGenerator, StudyGuide
from quiz_generator import QuizGenerator, Quiz
from visualization import EducationalVisualizer
from exporters import StudyGuideExporter

@dataclass
class StudyGuideRequest:
    """Configuration for study guide generation."""
    input_file: str
    subject: str
    level: str = "undergraduate"
    title: Optional[str] = None
    include_quiz: bool = True
    include_visuals: bool = True
    export_formats: List[str] = None
    output_dir: str = "generated_guides"

class StudyGuideCreator:
    """Main class for creating comprehensive study guides."""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the StudyGuideCreator.
        
        Args:
            openai_api_key: OpenAI API key for LangChain integration
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        # Initialize components
        self.content_processor = ContentProcessor()
        self.guide_generator = GuideGenerator(api_key=self.openai_api_key) if self.openai_api_key else None
        self.quiz_generator = QuizGenerator(api_key=self.openai_api_key) if self.openai_api_key else None
        self.visualizer = EducationalVisualizer()
        self.exporter = StudyGuideExporter()
        
        # Ensure output directory exists
        os.makedirs("generated_guides", exist_ok=True)
        os.makedirs("sample_materials", exist_ok=True)
        
    def create_study_guide(self, request: StudyGuideRequest) -> Dict[str, Any]:
        """
        Create a complete study guide from a document.
        
        Args:
            request: StudyGuideRequest with configuration
            
        Returns:
            Dictionary with created study guide and associated files
        """
        
        print(f"📚 Creating study guide for: {request.input_file}")
        print(f"Subject: {request.subject} | Level: {request.level}")
        
        # Step 1: Process the input document
        print("📖 Processing document...")
        try:
            processed_content = self.content_processor.process_document(
                request.input_file, document_type="auto"
            )
            print(f"✅ Processed {processed_content.metadata['word_count']} words")
        except Exception as e:
            print(f"❌ Error processing document: {e}")
            # Create fallback content
            processed_content = self._create_fallback_content(request)
        
        # Step 2: Generate the study guide
        print("🧠 Generating study guide...")
        try:
            if self.guide_generator:
                study_guide = self.guide_generator.generate_study_guide(
                    processed_content, 
                    request.subject, 
                    request.level,
                    request.title
                )
                print(f"✅ Generated guide with {len(study_guide.key_concepts)} concepts")
            else:
                study_guide = self._create_fallback_study_guide(processed_content, request)
                print("⚠️ Generated fallback study guide (no API key)")
        except Exception as e:
            print(f"❌ Error generating study guide: {e}")
            study_guide = self._create_fallback_study_guide(processed_content, request)
        
        # Step 3: Create quiz if requested
        quiz = None
        if request.include_quiz:
            print("❓ Creating quiz...")
            try:
                if self.quiz_generator:
                    quiz = self.quiz_generator.create_quiz_from_study_guide(
                        study_guide, difficulty="medium", num_questions=10
                    )
                    print(f"✅ Created quiz with {len(quiz.questions)} questions")
                else:
                    quiz = self._create_fallback_quiz(study_guide)
                    print("⚠️ Created fallback quiz (no API key)")
            except Exception as e:
                print(f"❌ Error creating quiz: {e}")
                quiz = self._create_fallback_quiz(study_guide)
        
        # Step 4: Create visualizations if requested
        visual_files = {}
        if request.include_visuals:
            print("🎨 Creating visualizations...")
            try:
                visual_files = self._create_visualizations(study_guide, request.output_dir)
                print(f"✅ Created {len(visual_files)} visualizations")
            except Exception as e:
                print(f"❌ Error creating visualizations: {e}")
        
        # Step 5: Export to requested formats
        print("📁 Exporting files...")
        export_formats = request.export_formats or ["html", "pdf", "json"]
        exported_files = self._export_study_guide(study_guide, quiz, export_formats, request.output_dir)
        print(f"✅ Exported to {len(exported_files)} formats")
        
        # Step 6: Create complete study package
        package_dir = self.exporter.create_study_package(
            study_guide, 
            quiz, 
            os.path.join(request.output_dir, study_guide.title.replace(' ', '_').lower())
        )
        
        result = {
            "study_guide": study_guide,
            "quiz": quiz,
            "processed_content": processed_content,
            "exported_files": exported_files,
            "visual_files": visual_files,
            "package_directory": package_dir,
            "success": True
        }
        
        print(f"🎉 Study guide creation complete! Package saved to: {package_dir}")
        return result
    
    def create_from_text(self, text: str, subject: str, level: str = "undergraduate") -> Dict[str, Any]:
        """
        Create a study guide directly from text content.
        
        Args:
            text: Text content to process
            subject: Subject area
            level: Education level
            
        Returns:
            Dictionary with created study guide
        """
        
        # Create temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(text)
            temp_file = f.name
        
        try:
            request = StudyGuideRequest(
                input_file=temp_file,
                subject=subject,
                level=level,
                title=f"{subject} Study Guide"
            )
            
            result = self.create_study_guide(request)
            return result
        finally:
            # Clean up temporary file
            os.unlink(temp_file)
    
    def _create_fallback_content(self, request: StudyGuideRequest) -> ProcessedContent:
        """Create fallback content when document processing fails."""
        fallback_text = f"""
        This is a study guide for {request.subject} at the {request.level} level.
        
        Key topics in {request.subject} include fundamental concepts, theories, and applications.
        Students should focus on understanding core principles and their practical applications.
        
        Important areas of study:
        - Basic principles and definitions
        - Key theories and models
        - Practical applications
        - Problem-solving techniques
        - Real-world examples
        """
        
        return ProcessedContent(
            text=fallback_text,
            chunks=[fallback_text],
            concepts=[request.subject, "principles", "applications"],
            key_terms=["concepts", "theories", "applications", "principles"],
            metadata={"fallback": True, "word_count": len(fallback_text.split())},
            sections=[{"title": f"{request.subject} Overview", "content": fallback_text}]
        )
    
    def _create_fallback_study_guide(self, processed_content: ProcessedContent, request: StudyGuideRequest) -> StudyGuide:
        """Create a basic study guide when AI generation is not available."""
        
        # Create basic concepts
        key_concepts = []
        for concept in processed_content.concepts[:5]:
            key_concepts.append({
                "name": concept,
                "definition": f"Important concept in {request.subject}",
                "importance": "Key for understanding the subject",
                "relationships": []
            })
        
        # Create basic questions
        practice_questions = []
        for i, concept in enumerate(processed_content.concepts[:3]):
            practice_questions.append({
                "question": f"What is {concept}?",
                "type": "short_answer",
                "difficulty": "medium",
                "correct_answer": f"Definition and explanation of {concept}",
                "explanation": f"{concept} is an important concept in {request.subject}",
                "concepts_tested": [concept]
            })
        
        # Create basic flashcards
        flashcards = []
        for term in processed_content.key_terms[:5]:
            flashcards.append({
                "front": term,
                "back": f"Definition and explanation of {term}",
                "type": "term",
                "difficulty": "medium",
                "tags": [request.subject.lower()]
            })
        
        return StudyGuide(
            title=request.title or f"{request.subject} Study Guide",
            subject=request.subject,
            level=request.level,
            summary=f"Comprehensive study guide for {request.subject} covering key concepts and principles.",
            key_concepts=key_concepts,
            chapter_summaries=[{
                "title": section["title"],
                "summary": section["content"][:500] + "..."
            } for section in processed_content.sections[:3]],
            practice_questions=practice_questions,
            flashcards=flashcards,
            visual_aids=[],
            metadata={"generated_by": "StudyGuideCreator (fallback mode)"}
        )
    
    def _create_fallback_quiz(self, study_guide: StudyGuide) -> Quiz:
        """Create a basic quiz when AI generation is not available."""
        
        questions = []
        for i, concept in enumerate(study_guide.key_concepts[:5]):
            concept_name = concept.get('name', f'Concept {i+1}') if isinstance(concept, dict) else str(concept)
            
            questions.append({
                "id": i + 1,
                "question": f"What is {concept_name}?",
                "type": "multiple_choice",
                "options": [
                    f"A) A key concept in {study_guide.subject}",
                    f"B) An unrelated term",
                    f"C) A different subject area",
                    f"D) None of the above"
                ],
                "correct_answer": "A",
                "explanation": f"{concept_name} is indeed a key concept in {study_guide.subject}",
                "points": 1,
                "time_estimate": 60,
                "tags": [concept_name],
                "difficulty_level": "medium"
            })
        
        from datetime import datetime
        return Quiz(
            title=f"{study_guide.subject} Quiz",
            subject=study_guide.subject,
            difficulty="medium",
            questions=questions,
            time_limit=15,
            passing_score=70,
            metadata={
                "created_at": datetime.now().isoformat(),
                "generated_by": "StudyGuideCreator (fallback mode)"
            }
        )
    
    def _create_visualizations(self, study_guide: StudyGuide, output_dir: str) -> Dict[str, str]:
        """Create educational visualizations."""
        visual_files = {}
        
        try:
            # Create concept map
            concept_map_path = os.path.join(output_dir, "concept_map.png")
            self.visualizer.create_concept_map(
                study_guide.key_concepts,
                title=f"{study_guide.subject} Concept Map",
                save_path=concept_map_path
            )
            visual_files["concept_map"] = concept_map_path
        except Exception as e:
            print(f"Warning: Could not create concept map: {e}")
        
        try:
            # Create word cloud
            text_for_cloud = " ".join([
                study_guide.summary,
                " ".join([c.get('name', '') if isinstance(c, dict) else str(c) for c in study_guide.key_concepts])
            ])
            
            word_cloud_path = os.path.join(output_dir, "word_cloud.png")
            self.visualizer.create_word_cloud(
                text_for_cloud,
                title=f"{study_guide.subject} Key Terms",
                save_path=word_cloud_path
            )
            visual_files["word_cloud"] = word_cloud_path
        except Exception as e:
            print(f"Warning: Could not create word cloud: {e}")
        
        return visual_files
    
    def _export_study_guide(self, study_guide: StudyGuide, quiz: Optional[Quiz], 
                           formats: List[str], output_dir: str) -> Dict[str, str]:
        """Export study guide to specified formats."""
        exported_files = {}
        base_name = study_guide.title.replace(' ', '_').lower()
        
        os.makedirs(output_dir, exist_ok=True)
        
        for format_type in formats:
            try:
                if format_type == "html":
                    path = os.path.join(output_dir, f"{base_name}.html")
                    self.exporter.export_to_html(study_guide, path)
                    exported_files["html"] = path
                
                elif format_type == "pdf":
                    path = os.path.join(output_dir, f"{base_name}.pdf")
                    self.exporter.export_to_pdf(study_guide, path)
                    exported_files["pdf"] = path
                
                elif format_type == "markdown":
                    path = os.path.join(output_dir, f"{base_name}.md")
                    self.exporter.export_to_markdown(study_guide, path)
                    exported_files["markdown"] = path
                
                elif format_type == "json":
                    path = os.path.join(output_dir, f"{base_name}.json")
                    self.exporter.export_to_json(study_guide, path)
                    exported_files["json"] = path
                
                elif format_type == "anki" and study_guide.flashcards:
                    path = os.path.join(output_dir, f"{base_name}_flashcards.csv")
                    self.exporter.export_flashcards_to_anki(study_guide, path)
                    exported_files["anki"] = path
                
            except Exception as e:
                print(f"Warning: Could not export to {format_type}: {e}")
        
        # Export quiz if available
        if quiz:
            try:
                quiz_path = os.path.join(output_dir, f"{base_name}_quiz.json")
                self.exporter.export_quiz_to_json(quiz, quiz_path)
                exported_files["quiz"] = quiz_path
            except Exception as e:
                print(f"Warning: Could not export quiz: {e}")
        
        return exported_files
    
    def create_sample_materials(self):
        """Create sample study materials for demonstration."""
        
        sample_subjects = [
            ("Mathematics", "calculus", "Calculus fundamentals including derivatives, integrals, and limits."),
            ("Physics", "quantum_mechanics", "Quantum mechanics principles including wave functions and uncertainty."),
            ("Biology", "cell_biology", "Cell structure, organelles, and cellular processes."),
            ("Computer Science", "data_structures", "Arrays, linked lists, trees, and algorithm complexity."),
            ("Chemistry", "organic_chemistry", "Organic compounds, reactions, and molecular structures.")
        ]
        
        sample_dir = "sample_materials"
        os.makedirs(sample_dir, exist_ok=True)
        
        for subject, filename, content in sample_subjects:
            # Create sample text file
            sample_text = f"""
# {subject} Study Material

## Introduction
{content}

## Key Concepts

### Fundamental Principles
Understanding the basic principles of {subject} is crucial for mastering advanced topics.

### Important Theories
Several key theories form the foundation of {subject}:
- Core theory 1: Explains fundamental relationships
- Core theory 2: Describes advanced interactions
- Core theory 3: Provides practical applications

### Applications
{subject} has numerous real-world applications:
- Application 1: Used in technology and engineering
- Application 2: Important for research and development  
- Application 3: Essential for problem-solving

## Examples and Problems

### Example 1
Basic example demonstrating key concepts in {subject}.

### Example 2
Intermediate example showing practical applications.

### Example 3
Advanced example requiring synthesis of multiple concepts.

## Summary
This material covers the essential concepts needed to understand {subject} at an introductory level.
Students should focus on mastering these fundamentals before proceeding to advanced topics.
            """
            
            with open(os.path.join(sample_dir, f"{filename}.txt"), 'w') as f:
                f.write(sample_text)
        
        print(f"✅ Created sample materials in {sample_dir}/")
        return sample_dir
