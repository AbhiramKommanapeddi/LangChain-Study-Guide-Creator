"""
Study guide generator using LangChain for creating comprehensive educational content.
"""

import os
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import json

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains.llm import LLMChain
from langchain.schema import HumanMessage, SystemMessage
from content_processor import ProcessedContent

@dataclass
class StudyGuide:
    """Container for a complete study guide."""
    title: str
    subject: str
    level: str
    summary: str
    key_concepts: List[str]
    chapter_summaries: List[Dict]
    practice_questions: List[Dict]
    flashcards: List[Dict]
    visual_aids: List[Dict]
    metadata: Dict

class GuideGenerator:
    """Generates comprehensive study guides using LangChain."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.llm = ChatOpenAI(
            openai_api_key=self.api_key,
            model_name=model,
            temperature=0.7
        )
        
        self._setup_prompts()
    
    def _setup_prompts(self):
        """Set up prompt templates for different generation tasks."""
        
        # Summary generation prompt
        self.summary_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert educational content creator. 
            Create clear, comprehensive summaries that help students understand key concepts."""),
            HumanMessage(content="""
            Create a comprehensive summary of the following educational content.
            Focus on the main concepts, key ideas, and important relationships.
            
            Subject: {subject}
            Level: {level}
            Content: {content}
            
            Provide a well-structured summary that includes:
            1. Main topic overview
            2. Key concepts and definitions
            3. Important relationships and connections
            4. Critical points students should remember
            
            Summary:""")
        ])
        
        # Chapter summary prompt
        self.chapter_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert educator creating chapter summaries.
            Make complex topics accessible and highlight the most important information."""),
            HumanMessage(content="""
            Create a detailed chapter summary for the following content.
            
            Chapter Title: {title}
            Subject: {subject}
            Level: {level}
            Content: {content}
            
            Provide:
            1. Chapter overview (2-3 sentences)
            2. Key learning objectives (3-5 points)
            3. Main concepts with brief explanations
            4. Important formulas, equations, or processes
            5. Real-world applications or examples
            6. Connection to other chapters/topics
            
            Chapter Summary:""")
        ])
        
        # Concept extraction prompt
        self.concept_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert at identifying and explaining key concepts
            in educational material. Focus on the most important ideas students need to master."""),
            HumanMessage(content="""
            Extract and explain the key concepts from this educational content.
            
            Subject: {subject}
            Level: {level}
            Content: {content}
            
            For each concept, provide:
            1. Concept name
            2. Clear definition (1-2 sentences)
            3. Why it's important
            4. How it relates to other concepts
            
            Return as a JSON list with this structure:
            [
                {{
                    "name": "concept name",
                    "definition": "clear definition",
                    "importance": "why it matters",
                    "relationships": ["related concept 1", "related concept 2"]
                }}
            ]
            
            Key Concepts:""")
        ])
        
        # Practice questions prompt
        self.questions_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert educator creating practice questions.
            Design questions that test understanding at different cognitive levels."""),
            HumanMessage(content="""
            Create practice questions based on this educational content.
            Include a mix of question types and difficulty levels.
            
            Subject: {subject}
            Level: {level}
            Content: {content}
            Key Concepts: {concepts}
            
            Create questions for each difficulty level:
            
            EASY (Knowledge/Comprehension):
            - Multiple choice questions
            - True/False questions
            - Fill in the blank
            
            MEDIUM (Application/Analysis):
            - Short answer questions
            - Problem-solving questions
            - Compare and contrast
            
            HARD (Synthesis/Evaluation):
            - Essay questions
            - Case study analysis
            - Creative applications
            
            Return as JSON with this structure:
            [
                {{
                    "question": "question text",
                    "type": "multiple_choice|true_false|short_answer|essay",
                    "difficulty": "easy|medium|hard",
                    "options": ["option1", "option2"] (for multiple choice),
                    "correct_answer": "answer",
                    "explanation": "why this is correct",
                    "concepts_tested": ["concept1", "concept2"]
                }}
            ]
            
            Practice Questions:""")
        ])
        
        # Flashcards prompt
        self.flashcards_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are creating educational flashcards for active recall.
            Make cards that test key facts, concepts, and relationships."""),
            HumanMessage(content="""
            Create flashcards based on this educational content.
            Focus on key terms, concepts, formulas, and important facts.
            
            Subject: {subject}
            Level: {level}
            Content: {content}
            Key Terms: {key_terms}
            
            Create flashcards that include:
            1. Term/concept cards (front: term, back: definition)
            2. Question cards (front: question, back: answer)
            3. Formula cards (front: when to use, back: formula + example)
            4. Process cards (front: process name, back: steps)
            
            Return as JSON:
            [
                {{
                    "front": "front text",
                    "back": "back text",
                    "type": "term|question|formula|process",
                    "difficulty": "easy|medium|hard",
                    "tags": ["tag1", "tag2"]
                }}
            ]
            
            Flashcards:""")
        ])
    
    def generate_study_guide(self, 
                           processed_content: ProcessedContent,
                           subject: str,
                           level: str = "undergraduate",
                           title: Optional[str] = None) -> StudyGuide:
        """
        Generate a comprehensive study guide from processed content.
        
        Args:
            processed_content: Processed document content
            subject: Subject area (e.g., "Mathematics", "Physics")
            level: Education level (e.g., "high_school", "undergraduate")
            title: Optional title for the study guide
            
        Returns:
            Complete StudyGuide object
        """
        
        if not title:
            title = f"{subject} Study Guide"
        
        print(f"Generating study guide: {title}")
        
        # Generate overall summary
        print("Creating overall summary...")
        summary = self._generate_summary(processed_content.text, subject, level)
        
        # Generate chapter summaries
        print("Creating chapter summaries...")
        chapter_summaries = self._generate_chapter_summaries(
            processed_content.sections, subject, level
        )
        
        # Extract and explain key concepts
        print("Extracting key concepts...")
        key_concepts = self._generate_concepts(processed_content.text, subject, level)
        
        # Generate practice questions
        print("Creating practice questions...")
        practice_questions = self._generate_questions(
            processed_content.text, subject, level, processed_content.concepts
        )
        
        # Generate flashcards
        print("Creating flashcards...")
        flashcards = self._generate_flashcards(
            processed_content.text, subject, level, processed_content.key_terms
        )
        
        # Create visual aids descriptions
        visual_aids = self._create_visual_aids_descriptions(key_concepts)
        
        # Create metadata
        metadata = {
            "generated_by": "LangChain Study Guide Creator",
            "source_file": processed_content.metadata.get("file_path"),
            "word_count": processed_content.metadata.get("word_count"),
            "concepts_count": len(key_concepts),
            "questions_count": len(practice_questions),
            "flashcards_count": len(flashcards)
        }
        
        return StudyGuide(
            title=title,
            subject=subject,
            level=level,
            summary=summary,
            key_concepts=key_concepts,
            chapter_summaries=chapter_summaries,
            practice_questions=practice_questions,
            flashcards=flashcards,
            visual_aids=visual_aids,
            metadata=metadata
        )
    
    def _generate_summary(self, content: str, subject: str, level: str) -> str:
        """Generate overall summary of the content."""
        try:
            # Truncate content if too long
            max_content_length = 4000
            if len(content) > max_content_length:
                content = content[:max_content_length] + "..."
            
            chain = LLMChain(llm=self.llm, prompt=self.summary_prompt)
            result = chain.run(
                subject=subject,
                level=level,
                content=content
            )
            return result.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"Summary for {subject} content covering key concepts and principles."
    
    def _generate_chapter_summaries(self, sections: List[Dict], subject: str, level: str) -> List[Dict]:
        """Generate summaries for each chapter/section."""
        chapter_summaries = []
        
        for section in sections[:5]:  # Limit to first 5 sections
            try:
                # Truncate section content if too long
                content = section['content']
                if len(content) > 3000:
                    content = content[:3000] + "..."
                
                chain = LLMChain(llm=self.llm, prompt=self.chapter_prompt)
                result = chain.run(
                    title=section['title'],
                    subject=subject,
                    level=level,
                    content=content
                )
                
                chapter_summaries.append({
                    'title': section['title'],
                    'summary': result.strip(),
                    'start_line': section.get('start_line', 0),
                    'end_line': section.get('end_line', 0)
                })
            except Exception as e:
                print(f"Error generating chapter summary for {section['title']}: {e}")
                chapter_summaries.append({
                    'title': section['title'],
                    'summary': f"Summary for {section['title']} - key concepts and principles.",
                    'start_line': section.get('start_line', 0),
                    'end_line': section.get('end_line', 0)
                })
        
        return chapter_summaries
    
    def _generate_concepts(self, content: str, subject: str, level: str) -> List[Dict]:
        """Extract and explain key concepts."""
        try:
            # Truncate content if too long
            if len(content) > 3500:
                content = content[:3500] + "..."
            
            chain = LLMChain(llm=self.llm, prompt=self.concept_prompt)
            result = chain.run(
                subject=subject,
                level=level,
                content=content
            )
            
            # Try to parse JSON result
            try:
                concepts = json.loads(result.strip())
                if isinstance(concepts, list):
                    return concepts
            except json.JSONDecodeError:
                pass
            
            # Fallback: create basic concepts
            return self._create_fallback_concepts(content)
            
        except Exception as e:
            print(f"Error generating concepts: {e}")
            return self._create_fallback_concepts(content)
    
    def _generate_questions(self, content: str, subject: str, level: str, concepts: List[str]) -> List[Dict]:
        """Generate practice questions."""
        try:
            # Truncate content if too long
            if len(content) > 3000:
                content = content[:3000] + "..."
            
            concepts_str = ", ".join(concepts[:10])
            
            chain = LLMChain(llm=self.llm, prompt=self.questions_prompt)
            result = chain.run(
                subject=subject,
                level=level,
                content=content,
                concepts=concepts_str
            )
            
            # Try to parse JSON result
            try:
                questions = json.loads(result.strip())
                if isinstance(questions, list):
                    return questions
            except json.JSONDecodeError:
                pass
            
            # Fallback: create basic questions
            return self._create_fallback_questions(concepts)
            
        except Exception as e:
            print(f"Error generating questions: {e}")
            return self._create_fallback_questions(concepts)
    
    def _generate_flashcards(self, content: str, subject: str, level: str, key_terms: List[str]) -> List[Dict]:
        """Generate flashcards."""
        try:
            # Truncate content if too long
            if len(content) > 3000:
                content = content[:3000] + "..."
            
            terms_str = ", ".join(key_terms[:15])
            
            chain = LLMChain(llm=self.llm, prompt=self.flashcards_prompt)
            result = chain.run(
                subject=subject,
                level=level,
                content=content,
                key_terms=terms_str
            )
            
            # Try to parse JSON result
            try:
                flashcards = json.loads(result.strip())
                if isinstance(flashcards, list):
                    return flashcards
            except json.JSONDecodeError:
                pass
            
            # Fallback: create basic flashcards
            return self._create_fallback_flashcards(key_terms)
            
        except Exception as e:
            print(f"Error generating flashcards: {e}")
            return self._create_fallback_flashcards(key_terms)
    
    def _create_visual_aids_descriptions(self, concepts: List[Dict]) -> List[Dict]:
        """Create descriptions for visual aids that could be generated."""
        visual_aids = []
        
        if concepts:
            # Concept map
            visual_aids.append({
                'type': 'concept_map',
                'title': 'Key Concepts Mind Map',
                'description': 'A visual representation showing relationships between key concepts',
                'concepts': [c.get('name', '') for c in concepts[:10] if isinstance(c, dict)]
            })
            
            # Word cloud
            visual_aids.append({
                'type': 'word_cloud',
                'title': 'Important Terms Cloud',
                'description': 'Visual representation of the most important terms sized by relevance',
                'terms': [c.get('name', '') for c in concepts[:20] if isinstance(c, dict)]
            })
            
            # Process diagram
            visual_aids.append({
                'type': 'process_diagram',
                'title': 'Key Processes Flow Chart',
                'description': 'Step-by-step visualization of important processes and procedures',
                'processes': []
            })
        
        return visual_aids
    
    def _create_fallback_concepts(self, content: str) -> List[Dict]:
        """Create basic concepts when AI generation fails."""
        # Extract potential concepts from content
        words = content.split()
        important_words = [w for w in words if len(w) > 6 and w.istitle()]
        
        concepts = []
        for word in important_words[:10]:
            concepts.append({
                'name': word,
                'definition': f'Important concept: {word}',
                'importance': 'Key term in the subject matter',
                'relationships': []
            })
        
        return concepts
    
    def _create_fallback_questions(self, concepts: List[str]) -> List[Dict]:
        """Create basic questions when AI generation fails."""
        questions = []
        
        for i, concept in enumerate(concepts[:5]):
            questions.append({
                'question': f'What is {concept}?',
                'type': 'short_answer',
                'difficulty': 'easy',
                'correct_answer': f'Definition and explanation of {concept}',
                'explanation': 'Basic concept understanding',
                'concepts_tested': [concept]
            })
        
        return questions
    
    def _create_fallback_flashcards(self, key_terms: List[str]) -> List[Dict]:
        """Create basic flashcards when AI generation fails."""
        flashcards = []
        
        for term in key_terms[:10]:
            flashcards.append({
                'front': term,
                'back': f'Definition and explanation of {term}',
                'type': 'term',
                'difficulty': 'medium',
                'tags': ['key_term']
            })
        
        return flashcards
