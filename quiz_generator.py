"""
Quiz generator for creating interactive quizzes and assessments.
"""

import random
import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains.llm import LLMChain
from langchain.schema import HumanMessage, SystemMessage

@dataclass
class Quiz:
    """Container for a quiz with questions and metadata."""
    title: str
    subject: str
    difficulty: str
    questions: List[Dict]
    time_limit: Optional[int]
    passing_score: int
    metadata: Dict

@dataclass
class QuizResult:
    """Container for quiz results and analytics."""
    quiz_title: str
    score: int
    total_questions: int
    percentage: float
    time_taken: Optional[int]
    correct_answers: List[int]
    incorrect_answers: List[int]
    detailed_results: List[Dict]
    recommendations: List[str]

class QuizGenerator:
    """Generates interactive quizzes and assessments."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        if self.api_key:
            self.llm = ChatOpenAI(
                openai_api_key=self.api_key,
                model_name="gpt-3.5-turbo",
                temperature=0.7
            )
            self._setup_prompts()
    
    def _setup_prompts(self):
        """Set up prompt templates for quiz generation."""
        
        self.quiz_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert quiz creator. Create engaging, 
            educational quizzes that test understanding at the appropriate level."""),
            HumanMessage(content="""
            Create a quiz based on the following study guide content.
            
            Subject: {subject}
            Difficulty: {difficulty}
            Topic: {topic}
            Content: {content}
            Number of Questions: {num_questions}
            
            Create questions with these requirements:
            - Mix of question types (multiple choice, true/false, short answer)
            - Progressive difficulty within the chosen level
            - Clear, unambiguous questions
            - Realistic distractors for multiple choice
            - Educational explanations for answers
            
            Return as JSON with this exact structure:
            [
                {{
                    "id": 1,
                    "question": "question text",
                    "type": "multiple_choice|true_false|short_answer",
                    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                    "correct_answer": "A",
                    "explanation": "detailed explanation of why this is correct",
                    "points": 1,
                    "time_estimate": 60,
                    "tags": ["concept1", "concept2"],
                    "difficulty_level": "easy|medium|hard"
                }}
            ]
            
            Quiz Questions:""")
        ])
        
        self.adaptive_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are creating adaptive quiz questions that adjust 
            to student performance. Focus on areas where improvement is needed."""),
            HumanMessage(content="""
            Create follow-up questions based on quiz performance.
            
            Subject: {subject}
            Weak Areas: {weak_areas}
            Student Level: {student_level}
            Previous Scores: {previous_scores}
            
            Create {num_questions} questions that:
            1. Target identified weak areas
            2. Match the student's learning level
            3. Provide scaffolding for improvement
            4. Include hints or guided questions
            
            Return in the same JSON format as regular quizzes.
            
            Adaptive Questions:""")
        ])
    
    def create_quiz_from_study_guide(self, 
                                   study_guide,
                                   difficulty: str = "medium",
                                   num_questions: int = 10,
                                   time_limit: Optional[int] = None,
                                   question_types: Optional[List[str]] = None) -> Quiz:
        """
        Create a quiz from a study guide.
        
        Args:
            study_guide: StudyGuide object
            difficulty: Quiz difficulty level
            num_questions: Number of questions to generate
            time_limit: Time limit in minutes
            question_types: Types of questions to include
            
        Returns:
            Quiz object
        """
        
        # Prepare content for quiz generation
        content_parts = []
        content_parts.append(study_guide.summary)
        
        # Add key concepts
        if study_guide.key_concepts:
            concepts_text = "Key Concepts:\n"
            for concept in study_guide.key_concepts[:10]:
                if isinstance(concept, dict):
                    concepts_text += f"- {concept.get('name', '')}: {concept.get('definition', '')}\n"
                else:
                    concepts_text += f"- {concept}\n"
            content_parts.append(concepts_text)
        
        # Add chapter summaries
        if study_guide.chapter_summaries:
            for chapter in study_guide.chapter_summaries[:3]:
                content_parts.append(f"Chapter: {chapter['title']}\n{chapter['summary']}")
        
        content = "\n\n".join(content_parts)
        
        # Generate questions using AI if available
        if hasattr(self, 'llm'):
            questions = self._generate_ai_questions(
                content, study_guide.subject, difficulty, num_questions
            )
        else:
            # Fallback to template-based generation
            questions = self._generate_template_questions(
                study_guide, difficulty, num_questions
            )
        
        # Calculate time limit if not provided
        if not time_limit:
            time_limit = max(10, len(questions) * 2)  # 2 minutes per question minimum
        
        # Create metadata
        metadata = {
            "created_at": datetime.now().isoformat(),
            "source_guide": study_guide.title,
            "generated_by": "QuizGenerator",
            "question_count": len(questions),
            "estimated_time": sum(q.get('time_estimate', 60) for q in questions) // 60
        }
        
        return Quiz(
            title=f"{study_guide.subject} Quiz - {difficulty.title()} Level",
            subject=study_guide.subject,
            difficulty=difficulty,
            questions=questions,
            time_limit=time_limit,
            passing_score=70,
            metadata=metadata
        )
    
    def _generate_ai_questions(self, content: str, subject: str, difficulty: str, num_questions: int) -> List[Dict]:
        """Generate questions using AI."""
        try:
            # Truncate content if too long
            if len(content) > 3500:
                content = content[:3500] + "..."
            
            chain = LLMChain(llm=self.llm, prompt=self.quiz_prompt)
            result = chain.run(
                subject=subject,
                difficulty=difficulty,
                topic="General",
                content=content,
                num_questions=num_questions
            )
            
            # Try to parse JSON result
            try:
                questions = json.loads(result.strip())
                if isinstance(questions, list) and len(questions) > 0:
                    return questions
            except json.JSONDecodeError:
                pass
            
            # Fallback if parsing fails
            return self._create_fallback_questions(subject, difficulty, num_questions)
            
        except Exception as e:
            print(f"Error generating AI questions: {e}")
            return self._create_fallback_questions(subject, difficulty, num_questions)
    
    def _generate_template_questions(self, study_guide, difficulty: str, num_questions: int) -> List[Dict]:
        """Generate questions using templates."""
        questions = []
        question_id = 1
        
        # Multiple choice questions from concepts
        if study_guide.key_concepts:
            for i, concept in enumerate(study_guide.key_concepts[:num_questions//2]):
                if isinstance(concept, dict):
                    concept_name = concept.get('name', '')
                    concept_def = concept.get('definition', '')
                else:
                    concept_name = str(concept)
                    concept_def = f"Important concept in {study_guide.subject}"
                
                question = {
                    "id": question_id,
                    "question": f"What is {concept_name}?",
                    "type": "multiple_choice",
                    "options": [
                        f"A) {concept_def}",
                        f"B) A different concept entirely",
                        f"C) An unrelated term",
                        f"D) None of the above"
                    ],
                    "correct_answer": "A",
                    "explanation": f"{concept_name} is defined as: {concept_def}",
                    "points": 1,
                    "time_estimate": 60,
                    "tags": [concept_name],
                    "difficulty_level": difficulty
                }
                questions.append(question)
                question_id += 1
        
        # True/False questions from practice questions
        if study_guide.practice_questions and len(questions) < num_questions:
            for pq in study_guide.practice_questions[:num_questions-len(questions)]:
                if pq.get('type') == 'true_false':
                    question = {
                        "id": question_id,
                        "question": pq['question'],
                        "type": "true_false",
                        "options": ["True", "False"],
                        "correct_answer": pq.get('correct_answer', 'True'),
                        "explanation": pq.get('explanation', 'See study materials'),
                        "points": 1,
                        "time_estimate": 45,
                        "tags": pq.get('concepts_tested', []),
                        "difficulty_level": pq.get('difficulty', difficulty)
                    }
                    questions.append(question)
                    question_id += 1
        
        # Fill remaining slots with generic questions
        while len(questions) < num_questions:
            question = {
                "id": question_id,
                "question": f"Which of the following is a key concept in {study_guide.subject}?",
                "type": "multiple_choice",
                "options": [
                    "A) Fundamental principle",
                    "B) Basic theory",
                    "C) Core concept",
                    "D) All of the above"
                ],
                "correct_answer": "D",
                "explanation": f"All options represent important aspects of {study_guide.subject}",
                "points": 1,
                "time_estimate": 60,
                "tags": ["general"],
                "difficulty_level": difficulty
            }
            questions.append(question)
            question_id += 1
        
        return questions
    
    def _create_fallback_questions(self, subject: str, difficulty: str, num_questions: int) -> List[Dict]:
        """Create basic questions when other methods fail."""
        questions = []
        
        for i in range(num_questions):
            question = {
                "id": i + 1,
                "question": f"Question {i + 1}: What is an important concept in {subject}?",
                "type": "multiple_choice",
                "options": [
                    "A) Fundamental principle",
                    "B) Basic theory", 
                    "C) Core methodology",
                    "D) All of the above"
                ],
                "correct_answer": "D",
                "explanation": f"All options are important in {subject}",
                "points": 1,
                "time_estimate": 60,
                "tags": [subject.lower()],
                "difficulty_level": difficulty
            }
            questions.append(question)
        
        return questions
    
    def create_adaptive_quiz(self, 
                           subject: str,
                           previous_results: List[QuizResult],
                           num_questions: int = 5) -> Quiz:
        """
        Create an adaptive quiz based on previous performance.
        
        Args:
            subject: Subject area
            previous_results: List of previous quiz results
            num_questions: Number of questions to generate
            
        Returns:
            Adaptive Quiz object
        """
        
        # Analyze weak areas from previous results
        weak_areas = self._analyze_weak_areas(previous_results)
        student_level = self._determine_student_level(previous_results)
        
        # Generate adaptive questions if AI is available
        if hasattr(self, 'llm'):
            questions = self._generate_adaptive_ai_questions(
                subject, weak_areas, student_level, previous_results, num_questions
            )
        else:
            questions = self._generate_adaptive_template_questions(
                subject, weak_areas, num_questions
            )
        
        metadata = {
            "created_at": datetime.now().isoformat(),
            "type": "adaptive",
            "weak_areas": weak_areas,
            "student_level": student_level,
            "based_on_results": len(previous_results)
        }
        
        return Quiz(
            title=f"Adaptive {subject} Quiz",
            subject=subject,
            difficulty="adaptive",
            questions=questions,
            time_limit=num_questions * 3,  # 3 minutes per question
            passing_score=60,
            metadata=metadata
        )
    
    def _analyze_weak_areas(self, results: List[QuizResult]) -> List[str]:
        """Analyze quiz results to identify weak areas."""
        weak_areas = []
        
        for result in results[-3:]:  # Look at last 3 results
            if result.percentage < 70:
                # Add topics from incorrect answers
                for detail in result.detailed_results:
                    if not detail.get('correct', False):
                        tags = detail.get('tags', [])
                        weak_areas.extend(tags)
        
        # Return most common weak areas
        from collections import Counter
        common_weak = Counter(weak_areas).most_common(5)
        return [area for area, count in common_weak]
    
    def _determine_student_level(self, results: List[QuizResult]) -> str:
        """Determine student level from performance."""
        if not results:
            return "beginner"
        
        recent_scores = [r.percentage for r in results[-3:]]
        avg_score = sum(recent_scores) / len(recent_scores)
        
        if avg_score >= 85:
            return "advanced"
        elif avg_score >= 70:
            return "intermediate"
        else:
            return "beginner"
    
    def _generate_adaptive_ai_questions(self, subject: str, weak_areas: List[str], 
                                      student_level: str, previous_results: List[QuizResult],
                                      num_questions: int) -> List[Dict]:
        """Generate adaptive questions using AI."""
        try:
            previous_scores = [r.percentage for r in previous_results[-5:]]
            
            chain = LLMChain(llm=self.llm, prompt=self.adaptive_prompt)
            result = chain.run(
                subject=subject,
                weak_areas=", ".join(weak_areas),
                student_level=student_level,
                previous_scores=previous_scores,
                num_questions=num_questions
            )
            
            try:
                questions = json.loads(result.strip())
                if isinstance(questions, list):
                    return questions
            except json.JSONDecodeError:
                pass
            
            return self._generate_adaptive_template_questions(subject, weak_areas, num_questions)
            
        except Exception as e:
            print(f"Error generating adaptive AI questions: {e}")
            return self._generate_adaptive_template_questions(subject, weak_areas, num_questions)
    
    def _generate_adaptive_template_questions(self, subject: str, weak_areas: List[str], 
                                           num_questions: int) -> List[Dict]:
        """Generate adaptive questions using templates."""
        questions = []
        
        for i, area in enumerate(weak_areas[:num_questions]):
            question = {
                "id": i + 1,
                "question": f"Let's review {area} in {subject}. What is the key principle?",
                "type": "multiple_choice",
                "options": [
                    f"A) Basic definition of {area}",
                    f"B) Advanced application of {area}",
                    f"C) Related concept to {area}",
                    f"D) All aspects of {area}"
                ],
                "correct_answer": "D",
                "explanation": f"Understanding {area} requires knowledge of all these aspects",
                "points": 2,  # Higher points for remediation
                "time_estimate": 90,
                "tags": [area],
                "difficulty_level": "remedial"
            }
            questions.append(question)
        
        # Fill remaining questions with general review
        while len(questions) < num_questions:
            i = len(questions)
            question = {
                "id": i + 1,
                "question": f"Review question for {subject}: Which concept needs more practice?",
                "type": "short_answer",
                "options": [],
                "correct_answer": "Any concept that was previously answered incorrectly",
                "explanation": "Focus on areas where you scored lowest",
                "points": 1,
                "time_estimate": 120,
                "tags": ["review"],
                "difficulty_level": "review"
            }
            questions.append(question)
        
        return questions
    
    def evaluate_quiz(self, quiz: Quiz, answers: Dict[int, str], 
                     time_taken: Optional[int] = None) -> QuizResult:
        """
        Evaluate quiz answers and provide detailed results.
        
        Args:
            quiz: Quiz object
            answers: Dictionary mapping question IDs to answers
            time_taken: Time taken in seconds
            
        Returns:
            QuizResult with detailed analysis
        """
        
        correct_answers = []
        incorrect_answers = []
        detailed_results = []
        total_points = 0
        earned_points = 0
        
        for question in quiz.questions:
            q_id = question['id']
            user_answer = answers.get(q_id, "")
            correct_answer = question['correct_answer']
            points = question.get('points', 1)
            total_points += points
            
            is_correct = self._check_answer(user_answer, correct_answer, question['type'])
            
            if is_correct:
                correct_answers.append(q_id)
                earned_points += points
            else:
                incorrect_answers.append(q_id)
            
            detailed_results.append({
                'question_id': q_id,
                'question': question['question'],
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'correct': is_correct,
                'points_earned': points if is_correct else 0,
                'points_possible': points,
                'explanation': question.get('explanation', ''),
                'tags': question.get('tags', []),
                'difficulty': question.get('difficulty_level', 'medium')
            })
        
        percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(detailed_results, percentage)
        
        return QuizResult(
            quiz_title=quiz.title,
            score=earned_points,
            total_questions=len(quiz.questions),
            percentage=percentage,
            time_taken=time_taken,
            correct_answers=correct_answers,
            incorrect_answers=incorrect_answers,
            detailed_results=detailed_results,
            recommendations=recommendations
        )
    
    def _check_answer(self, user_answer: str, correct_answer: str, question_type: str) -> bool:
        """Check if user answer is correct."""
        if question_type == "multiple_choice":
            return user_answer.upper().strip() == correct_answer.upper().strip()
        elif question_type == "true_false":
            user_bool = user_answer.lower().strip() in ['true', 't', 'yes', 'y', '1']
            correct_bool = correct_answer.lower().strip() in ['true', 't', 'yes', 'y', '1']
            return user_bool == correct_bool
        elif question_type == "short_answer":
            # Simple keyword matching for short answers
            user_words = set(user_answer.lower().split())
            correct_words = set(correct_answer.lower().split())
            # Consider correct if at least 50% of key words match
            overlap = len(user_words.intersection(correct_words))
            return overlap >= len(correct_words) * 0.5
        else:
            return user_answer.lower().strip() == correct_answer.lower().strip()
    
    def _generate_recommendations(self, detailed_results: List[Dict], percentage: float) -> List[str]:
        """Generate study recommendations based on performance."""
        recommendations = []
        
        # Overall performance
        if percentage >= 90:
            recommendations.append("Excellent work! You have mastered this material.")
        elif percentage >= 80:
            recommendations.append("Good job! Review the missed concepts to achieve mastery.")
        elif percentage >= 70:
            recommendations.append("Solid understanding. Focus on the areas you missed.")
        elif percentage >= 60:
            recommendations.append("You're on the right track. Additional study is recommended.")
        else:
            recommendations.append("Consider reviewing the fundamental concepts before retaking.")
        
        # Specific weak areas
        incorrect_tags = []
        for result in detailed_results:
            if not result['correct']:
                incorrect_tags.extend(result['tags'])
        
        if incorrect_tags:
            from collections import Counter
            common_weak = Counter(incorrect_tags).most_common(3)
            for tag, count in common_weak:
                recommendations.append(f"Focus additional study on: {tag}")
        
        # Difficulty-based recommendations
        hard_questions_missed = [r for r in detailed_results 
                               if not r['correct'] and r['difficulty'] == 'hard']
        if hard_questions_missed:
            recommendations.append("Practice more advanced problems to improve on difficult concepts.")
        
        easy_questions_missed = [r for r in detailed_results 
                               if not r['correct'] and r['difficulty'] == 'easy']
        if easy_questions_missed:
            recommendations.append("Review fundamental concepts - focus on basic understanding first.")
        
        return recommendations
