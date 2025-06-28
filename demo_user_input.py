#!/usr/bin/env python3
"""
Quick demo of the user interactive mode
Simulates user input for demonstration
"""

import subprocess
import sys

def demo_user_interaction():
    """Demonstrate the user interactive mode with sample input."""
    
    print("🎯 DEMO: User Interactive Study Guide Creation")
    print("=" * 60)
    print("This shows how a user would interact with the system:")
    print()
    
    # Sample user input
    sample_content = """Photosynthesis in Plants

Photosynthesis is the process by which plants convert light energy into chemical energy.

The equation for photosynthesis is:
6CO2 + 6H2O + light energy → C6H12O6 + 6O2

Key stages:
1. Light-dependent reactions (in thylakoids)
   - Chlorophyll absorbs light
   - Water molecules split
   - Oxygen released as byproduct
   - ATP and NADPH produced

2. Light-independent reactions (Calvin cycle)
   - CO2 fixed into organic molecules
   - Uses ATP and NADPH from first stage
   - Produces glucose

Importance:
- Provides food for plants
- Produces oxygen for atmosphere
- Foundation of food chains
- Removes CO2 from atmosphere"""

    print("📝 Sample user input:")
    print("-" * 40)
    print(sample_content)
    print("-" * 40)
    print()
    
    print("📚 Subject: Biology")
    print("⏳ Processing...")
    print()
    
    # Create a temporary file with the content
    import tempfile
    import os
    from study_guide_creator import StudyGuideCreator, StudyGuideRequest
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(sample_content)
            temp_path = f.name
        
        creator = StudyGuideCreator()
        output_dir = "demo_user_photosynthesis"
        
        request = StudyGuideRequest(
            input_file=temp_path,
            subject="Biology",
            level="undergraduate",
            title="Photosynthesis Study Guide",
            output_dir=output_dir,
            export_formats=["html", "json"]
        )
        
        result = creator.create_study_guide(request)
        
        print("✅ STUDY GUIDE CREATED!")
        print("=" * 40)
        
        # Show generated content
        import json
        json_file = os.path.join(output_dir, "photosynthesis_study_guide.json")
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            print(f"📚 Title: {data.get('title', 'N/A')}")
            print(f"📖 Subject: {data.get('subject', 'N/A')}")
            print(f"📝 Summary: {data.get('summary', 'N/A')}")
            
            print(f"\n🔑 Key Concepts:")
            for concept in data.get('key_concepts', [])[:4]:
                if isinstance(concept, dict):
                    print(f"   • {concept.get('name', 'N/A')}")
        
        # Show quiz
        quiz_file = os.path.join(output_dir, "photosynthesis_study_guide_quiz.json")
        if os.path.exists(quiz_file):
            with open(quiz_file, 'r') as f:
                quiz_data = json.load(f)
            
            print(f"\n❓ Sample Quiz Question:")
            if quiz_data.get('questions'):
                q = quiz_data['questions'][0]
                print(f"   {q.get('question', 'N/A')}")
                if q.get('options'):
                    for opt in q['options'][:2]:
                        print(f"      {opt}")
                print(f"   ✅ Answer: {q.get('correct_answer', 'N/A')}")
        
        print(f"\n📁 Generated files in: {output_dir}")
        
        os.unlink(temp_path)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        try:
            os.unlink(temp_path)
        except:
            pass
    
    print(f"\n🎯 This is how users interact with your system!")
    print("They simply enter text and get comprehensive study materials.")

if __name__ == "__main__":
    demo_user_interaction()
