#!/usr/bin/env python3
"""
Simple Interactive Study Guide Creator
Quick and easy interface for generating study guides from user text
"""

import os
import tempfile
import json
from study_guide_creator import StudyGuideCreator, StudyGuideRequest

def main():
    print("🎓 INTERACTIVE STUDY GUIDE CREATOR")
    print("=" * 50)
    print("Transform your text into comprehensive study guides!")
    print()
    
    while True:
        print("📝 Enter your study material below:")
        print("(Type your content and press Enter twice when finished)")
        print("-" * 50)
        
        # Collect user input
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
            print("❌ No content provided. Please try again.\n")
            continue
        
        # Get subject
        subject = input("\n📚 Enter the subject (e.g., Biology, Physics): ").strip()
        if not subject:
            subject = "General Studies"
        
        # Get title
        title = input(f"📖 Enter title (default: {subject} Study Guide): ").strip()
        if not title:
            title = f"{subject} Study Guide"
        
        print(f"\n⏳ Generating study guide for: {title}")
        print("🧠 Processing your content...")
        
        try:
            # Save content to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(content)
                temp_path = temp_file.name
            
            # Create study guide
            creator = StudyGuideCreator()
            
            # Create output directory
            output_dir = f"interactive_output_{subject.lower().replace(' ', '_')}"
            os.makedirs(output_dir, exist_ok=True)
            
            request = StudyGuideRequest(
                input_file=temp_path,
                subject=subject,
                level="undergraduate",
                title=title,
                output_dir=output_dir,
                export_formats=["html", "json"],
                include_quiz=True,
                include_visuals=True
            )
            
            result = creator.create_study_guide(request)
            
            print("\n✅ STUDY GUIDE CREATED SUCCESSFULLY!")
            print("=" * 50)
            print(f"📚 Title: {result.study_guide.title}")
            print(f"🎓 Subject: {result.study_guide.subject}")
            print(f"🔑 Key Concepts: {len(result.study_guide.key_concepts)}")
            
            if result.quiz:
                print(f"❓ Quiz Questions: {len(result.quiz.questions)}")
            
            print(f"\n📁 Files saved to: {output_dir}")
            
            # Show sample content
            if result.study_guide.key_concepts:
                print(f"\n🔑 Sample Key Concepts:")
                for concept in result.study_guide.key_concepts[:3]:
                    if isinstance(concept, dict):
                        print(f"   • {concept.get('name', 'N/A')}")
                    else:
                        print(f"   • {concept}")
            
            if result.quiz and result.quiz.questions:
                print(f"\n❓ Sample Quiz Question:")
                q = result.quiz.questions[0]
                print(f"   {q['question']}")
                print(f"   Answer: {q['correct_answer']}")
            
            # Clean up
            os.unlink(temp_path)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            try:
                os.unlink(temp_path)
            except:
                pass
        
        # Ask to continue
        print(f"\n🔄 Create another study guide? (y/n): ", end="")
        if input().lower() != 'y':
            break
        
        print("\n" + "="*50)
    
    print("\n👋 Thank you for using the Study Guide Creator!")

if __name__ == "__main__":
    main()
