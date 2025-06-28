#!/usr/bin/env python3
"""
Quick test of the quiz functionality
"""

import json
from quiz_generator import QuizGenerator

def test_quiz_functionality():
    """Test the quiz generator and evaluation."""
    
    print("🧪 Testing Quiz Generator")
    print("=" * 40)
    
    # Load the generated quiz
    with open("calculus_output/calculus_study_guide_quiz.json", "r") as f:
        quiz_data = json.load(f)
    
    print(f"📚 Quiz Title: {quiz_data['title']}")
    print(f"📖 Subject: {quiz_data['subject']}")
    print(f"🎯 Difficulty: {quiz_data['difficulty']}")
    print(f"❓ Number of Questions: {len(quiz_data['questions'])}")
    print()
    
    # Show first few questions
    print("📝 Sample Questions:")
    print("-" * 20)
    
    for i, question in enumerate(quiz_data['questions'][:3]):
        print(f"\n{i+1}. {question['question']}")
        print(f"   Type: {question['type']}")
        
        if question['options']:
            for option in question['options']:
                print(f"   {option}")
        
        print(f"   ✅ Correct Answer: {question['correct_answer']}")
        print(f"   💡 Explanation: {question['explanation']}")
    
    print("\n" + "=" * 40)
    print("✅ Quiz functionality test completed!")
    
    # Test quiz evaluation
    quiz_gen = QuizGenerator()
    
    # Create a mock quiz object from the data
    class MockQuiz:
        def __init__(self, data):
            self.title = data['title']
            self.subject = data['subject']
            self.difficulty = data['difficulty']
            self.questions = data['questions']
            self.time_limit = data.get('time_limit', 30)
            self.passing_score = data.get('passing_score', 70)
    
    quiz = MockQuiz(quiz_data)
    
    # Simulate some answers (mix of correct and incorrect)
    answers = {}
    for i, question in enumerate(quiz_data['questions'][:5]):
        if i % 2 == 0:  # Every other question correct
            answers[question['id']] = question['correct_answer']
        else:
            # Give a wrong answer
            if question['type'] == 'multiple_choice':
                # Pick a different option
                options = ['A', 'B', 'C', 'D']
                wrong_answers = [opt for opt in options if opt != question['correct_answer']]
                answers[question['id']] = wrong_answers[0] if wrong_answers else 'B'
            else:
                answers[question['id']] = 'Wrong answer'
    
    print("\n🎯 Testing Quiz Evaluation")
    print("-" * 30)
    
    result = quiz_gen.evaluate_quiz(quiz, answers, time_taken=600)
    
    print(f"📊 Quiz Results:")
    print(f"   Score: {result.score}/{len(result.detailed_results)}")
    print(f"   Percentage: {result.percentage:.1f}%")
    print(f"   Correct Answers: {len(result.correct_answers)}")
    print(f"   Incorrect Answers: {len(result.incorrect_answers)}")
    print(f"   Time Taken: {result.time_taken} seconds")
    
    print(f"\n💡 Recommendations:")
    for recommendation in result.recommendations:
        print(f"   • {recommendation}")
    
    print("\n✅ Quiz evaluation test completed!")

if __name__ == "__main__":
    test_quiz_functionality()
