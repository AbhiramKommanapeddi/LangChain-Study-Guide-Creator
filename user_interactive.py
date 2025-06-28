#!/usr/bin/env python3
"""
Super Simple Interactive Study Guide Creator
Just enter your text and get a study guide!
"""

import os
import tempfile
import json
from study_guide_creator import StudyGuideCreator, StudyGuideRequest

def create_study_guide_from_text():
    """Simple function to create study guide from user text."""
    
    print("🎓 SIMPLE STUDY GUIDE CREATOR")
    print("=" * 50)
    print("Enter your study material and get an instant study guide!")
    print()
    
    # Get text from user
    print("📝 Enter your study text (press Enter twice when done):")
    print("-" * 50)
    
    lines = []
    empty_count = 0
    
    while True:
        try:
            line = input()
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
            lines.append(line)
        except KeyboardInterrupt:
            print("\nExiting...")
            return
    
    content = "\n".join(lines).strip()
    
    if not content:
        print("❌ No content provided!")
        return
    
    # Get subject
    subject = input("\n📚 What subject is this? ").strip()
    if not subject:
        subject = "General Studies"
    
    print(f"\n⏳ Creating study guide for {subject}...")
    
    try:
        # Save to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_path = f.name
        
        # Create study guide
        creator = StudyGuideCreator()
        output_dir = f"user_study_guide_{subject.lower().replace(' ', '_')}"
        
        request = StudyGuideRequest(
            input_file=temp_path,
            subject=subject,
            level="undergraduate",
            title=f"{subject} Study Guide",
            output_dir=output_dir,
            export_formats=["html", "json"]
        )
        
        result = creator.create_study_guide(request)
        
        print(f"\n✅ SUCCESS! Your study guide is ready!")
        print("=" * 50)
        
        # Load and display the JSON result
        json_file = os.path.join(output_dir, f"{subject.lower().replace(' ', '_')}_study_guide.json")
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            print(f"📚 Title: {data.get('title', 'N/A')}")
            print(f"🎓 Subject: {data.get('subject', 'N/A')}")
            print(f"📝 Summary: {data.get('summary', 'N/A')}")
            
            print(f"\n🔑 Key Concepts Found:")
            for concept in data.get('key_concepts', [])[:5]:
                if isinstance(concept, dict):
                    print(f"   • {concept.get('name', 'N/A')}")
                else:
                    print(f"   • {concept}")
            
            print(f"\n❓ Practice Questions:")
            for q in data.get('practice_questions', [])[:3]:
                print(f"   • {q.get('question', 'N/A')}")
        
        # Show quiz if available
        quiz_file = os.path.join(output_dir, f"{subject.lower().replace(' ', '_')}_study_guide_quiz.json")
        if os.path.exists(quiz_file):
            with open(quiz_file, 'r') as f:
                quiz_data = json.load(f)
            
            print(f"\n🧠 Quiz Generated ({len(quiz_data.get('questions', []))} questions)")
            if quiz_data.get('questions'):
                q = quiz_data['questions'][0]
                print(f"\nSample Question:")
                print(f"   Q: {q.get('question', 'N/A')}")
                if q.get('options'):
                    for opt in q['options'][:2]:
                        print(f"      {opt}")
                print(f"   ✅ Answer: {q.get('correct_answer', 'N/A')}")
        
        print(f"\n📁 Files saved to: {output_dir}")
        
        # Show HTML file
        html_files = [f for f in os.listdir(output_dir) if f.endswith('.html')]
        if html_files:
            html_path = os.path.join(output_dir, html_files[0])
            print(f"🌐 View in browser: file:///{os.path.abspath(html_path)}")
        
        os.unlink(temp_path)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        try:
            os.unlink(temp_path)
        except:
            pass

if __name__ == "__main__":
    while True:
        create_study_guide_from_text()
        
        print(f"\n🔄 Create another study guide? (y/n): ", end="")
        if input().lower() != 'y':
            break
        print("\n" + "="*50)
    
    print("\n👋 Thanks for using the Study Guide Creator!")
