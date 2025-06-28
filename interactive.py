#!/usr/bin/env python3
"""
Interactive LangChain Study Guide Creator
User-friendly interface for creating study guides from user input
"""

import os
import tempfile
import json
from pathlib import Path
import webbrowser
import time

from study_guide_creator import StudyGuideCreator, StudyGuideRequest

class InteractiveStudyGuideCreator:
    """Interactive interface for study guide creation."""
    
    def __init__(self):
        self.creator = StudyGuideCreator()
        self.session_dir = None
        
    def print_banner(self):
        """Print welcome banner."""
        print("\n" + "="*70)
        print("🎓 INTERACTIVE LANGCHAIN STUDY GUIDE CREATOR 🎓")
        print("="*70)
        print("📚 Transform your educational content into comprehensive study guides!")
        print("✨ Features: Study guides, quizzes, flashcards, and visualizations")
        print("="*70 + "\n")
    
    def get_user_input(self):
        """Get study material input from user."""
        print("📝 STEP 1: PROVIDE YOUR STUDY MATERIAL")
        print("-" * 40)
        
        while True:
            print("\nHow would you like to provide your study material?")
            print("1. 📄 Upload a file (PDF, DOCX, TXT)")
            print("2. ✍️  Type/paste text directly")
            print("3. 📚 Use sample material")
            print("4. 🚪 Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                return self.handle_file_upload()
            elif choice == "2":
                return self.handle_text_input()
            elif choice == "3":
                return self.handle_sample_selection()
            elif choice == "4":
                print("👋 Goodbye! Thanks for using the Study Guide Creator!")
                return None, None
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
    
    def handle_file_upload(self):
        """Handle file upload option."""
        print("\n📄 FILE UPLOAD")
        print("Supported formats: PDF, DOCX, TXT")
        
        while True:
            file_path = input("Enter the full path to your file: ").strip().strip('"')
            
            if not file_path:
                print("❌ Please enter a file path.")
                continue
                
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                retry = input("Would you like to try again? (y/n): ").lower()
                if retry != 'y':
                    return None, None
                continue
            
            if not file_path.lower().endswith(('.pdf', '.docx', '.txt')):
                print("❌ Unsupported file format. Please use PDF, DOCX, or TXT.")
                continue
            
            return file_path, "file"
    
    def handle_text_input(self):
        """Handle direct text input option."""
        print("\n✍️  DIRECT TEXT INPUT")
        print("Enter your study material (press Enter twice when finished):")
        print("-" * 50)
        
        lines = []
        empty_line_count = 0
        
        while True:
            line = input()
            if line.strip() == "":
                empty_line_count += 1
                if empty_line_count >= 2:
                    break
            else:
                empty_line_count = 0
            lines.append(line)
        
        content = "\n".join(lines).strip()
        
        if not content:
            print("❌ No content provided.")
            return None, None
        
        if len(content) < 50:
            print("⚠️  Content seems quite short. Consider adding more detail for better results.")
            proceed = input("Continue anyway? (y/n): ").lower()
            if proceed != 'y':
                return None, None
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
        temp_file.write(content)
        temp_file.close()
        
        return temp_file.name, "text"
    
    def handle_sample_selection(self):
        """Handle sample material selection."""
        print("\n📚 SAMPLE MATERIALS")
        
        sample_dir = "sample_materials"
        if not os.path.exists(sample_dir):
            print("❌ No sample materials found.")
            return None, None
        
        samples = [f for f in os.listdir(sample_dir) if f.endswith('.txt')]
        
        if not samples:
            print("❌ No sample text files found.")
            return None, None
        
        print("Available sample materials:")
        for i, sample in enumerate(samples, 1):
            # Create readable names
            name = sample.replace('.txt', '').replace('_', ' ').title()
            print(f"{i}. 📖 {name}")
        
        while True:
            try:
                choice = int(input(f"\nSelect a sample (1-{len(samples)}): "))
                if 1 <= choice <= len(samples):
                    selected_file = os.path.join(sample_dir, samples[choice - 1])
                    subject = samples[choice - 1].replace('.txt', '').replace('_', ' ').title()
                    print(f"✅ Selected: {subject}")
                    return selected_file, "sample"
                else:
                    print(f"❌ Please enter a number between 1 and {len(samples)}")
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def get_study_guide_config(self, input_type, file_path):
        """Get study guide configuration from user."""
        print("\n⚙️  STEP 2: CONFIGURE YOUR STUDY GUIDE")
        print("-" * 40)
        
        # Subject
        if input_type == "sample":
            suggested_subject = Path(file_path).stem.replace('_', ' ').title()
            subject = input(f"Subject (suggested: {suggested_subject}): ").strip()
            if not subject:
                subject = suggested_subject
        else:
            subject = input("Enter the subject area (e.g., Mathematics, Biology, Physics): ").strip()
            if not subject:
                subject = "General Studies"
        
        # Education level
        print("\nEducation Level:")
        print("1. 🎓 High School")
        print("2. 🏫 Undergraduate") 
        print("3. 🎓 Graduate")
        print("4. 👨‍💼 Professional")
        
        level_map = {"1": "high_school", "2": "undergraduate", "3": "graduate", "4": "professional"}
        
        while True:
            level_choice = input("Select education level (1-4, default: 2): ").strip()
            if not level_choice:
                level_choice = "2"
            
            if level_choice in level_map:
                level = level_map[level_choice]
                break
            else:
                print("❌ Please enter 1, 2, 3, or 4.")
        
        # Title
        default_title = f"{subject} Study Guide"
        title = input(f"Study guide title (default: {default_title}): ").strip()
        if not title:
            title = default_title
        
        # Features
        print("\n🎯 FEATURES TO INCLUDE:")
        
        include_quiz = input("Include interactive quiz? (Y/n): ").strip().lower()
        include_quiz = include_quiz != 'n'
        
        include_visuals = input("Include visualizations (concept maps, word clouds)? (Y/n): ").strip().lower()
        include_visuals = include_visuals != 'n'
        
        # Export formats
        print("\n📁 EXPORT FORMATS:")
        print("Available: HTML, PDF, JSON, Markdown")
        formats_input = input("Select formats (comma-separated, default: html,pdf,json): ").strip()
        
        if not formats_input:
            formats = ["html", "pdf", "json"]
        else:
            available_formats = ["html", "pdf", "json", "markdown"]
            formats = [f.strip().lower() for f in formats_input.split(",")]
            formats = [f for f in formats if f in available_formats]
            if not formats:
                formats = ["html", "pdf", "json"]
        
        return {
            "subject": subject,
            "level": level,
            "title": title,
            "include_quiz": include_quiz,
            "include_visuals": include_visuals,
            "formats": formats
        }
    
    def create_study_guide(self, file_path, config):
        """Create the study guide with user configuration."""
        print("\n🚀 STEP 3: GENERATING YOUR STUDY GUIDE")
        print("-" * 40)
        print("⏳ Processing your content...")
        
        try:
            # Create output directory
            safe_subject = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in config['subject'])
            safe_subject = safe_subject.replace(' ', '_').lower()
            self.session_dir = f"interactive_output_{safe_subject}_{int(time.time())}"
            
            # Create request
            request = StudyGuideRequest(
                input_file=file_path,
                subject=config['subject'],
                level=config['level'],
                title=config['title'],
                output_dir=self.session_dir,
                export_formats=config['formats'],
                include_quiz=config['include_quiz'],
                include_visuals=config['include_visuals']
            )
            
            print(f"📁 Output directory: {self.session_dir}")
            print("🧠 Analyzing content and extracting key concepts...")
            
            # Generate study guide
            result = self.creator.create_study_guide(request)
            
            print("\n✅ STUDY GUIDE CREATED SUCCESSFULLY!")
            return result
            
        except Exception as e:
            print(f"\n❌ Error creating study guide: {e}")
            return None
    
    def display_results(self, result, config):
        """Display the results to the user."""
        if not result:
            return
        
        print("\n🎉 GENERATION COMPLETE!")
        print("=" * 50)
        
        print(f"📚 Title: {result.study_guide.title}")
        print(f"🎓 Subject: {result.study_guide.subject}")
        print(f"📊 Level: {result.study_guide.level}")
        print(f"🔑 Key Concepts: {len(result.study_guide.key_concepts)}")
        print(f"❓ Practice Questions: {len(result.study_guide.practice_questions)}")
        
        if result.quiz:
            print(f"🧠 Quiz Questions: {len(result.quiz.questions)}")
        
        print(f"\n📁 Generated Files:")
        if os.path.exists(self.session_dir):
            for file in os.listdir(self.session_dir):
                if os.path.isfile(os.path.join(self.session_dir, file)):
                    file_path = os.path.join(self.session_dir, file)
                    size = os.path.getsize(file_path)
                    print(f"   ✅ {file} ({size:,} bytes)")
        
        # Show sample content
        self.show_sample_content(result)
        
        # Offer to view results
        self.offer_view_options()
    
    def show_sample_content(self, result):
        """Show sample content from the generated study guide."""
        print(f"\n📋 SAMPLE CONTENT:")
        print("-" * 30)
        
        # Show first few key concepts
        if result.study_guide.key_concepts:
            print("🔑 Key Concepts:")
            for i, concept in enumerate(result.study_guide.key_concepts[:3]):
                if isinstance(concept, dict):
                    print(f"   • {concept.get('name', 'N/A')}: {concept.get('definition', 'N/A')}")
                else:
                    print(f"   • {concept}")
        
        # Show sample quiz question
        if result.quiz and result.quiz.questions:
            print(f"\n❓ Sample Quiz Question:")
            q = result.quiz.questions[0]
            print(f"   Q: {q['question']}")
            if q.get('options'):
                for option in q['options'][:2]:  # Show first 2 options
                    print(f"      {option}")
                if len(q['options']) > 2:
                    print(f"      ... and {len(q['options']) - 2} more options")
            print(f"   ✅ Answer: {q['correct_answer']}")
    
    def offer_view_options(self):
        """Offer options to view the generated content."""
        print(f"\n🖥️  VIEW YOUR STUDY GUIDE:")
        print("-" * 30)
        print("1. 🌐 Open in web browser (HTML)")
        print("2. 📁 Open output folder")
        print("3. 🖨️  Show file paths")
        print("4. ↩️  Return to main menu")
        print("5. 🚪 Exit")
        
        while True:
            choice = input("\nWhat would you like to do? (1-5): ").strip()
            
            if choice == "1":
                self.open_in_browser()
                break
            elif choice == "2":
                self.open_output_folder()
                break
            elif choice == "3":
                self.show_file_paths()
                break
            elif choice == "4":
                return True  # Continue to main menu
            elif choice == "5":
                return False  # Exit
            else:
                print("❌ Please enter a number between 1 and 5.")
        
        return True
    
    def open_in_browser(self):
        """Open the HTML study guide in browser."""
        if not self.session_dir:
            print("❌ No output directory found.")
            return
        
        html_files = [f for f in os.listdir(self.session_dir) if f.endswith('.html')]
        
        if not html_files:
            print("❌ No HTML file found.")
            return
        
        html_path = os.path.join(self.session_dir, html_files[0])
        full_path = os.path.abspath(html_path)
        
        try:
            webbrowser.open(f'file:///{full_path}')
            print(f"🌐 Opening in browser: {html_files[0]}")
        except Exception as e:
            print(f"❌ Could not open browser: {e}")
            print(f"📁 File location: {full_path}")
    
    def open_output_folder(self):
        """Open the output folder in file explorer."""
        if not self.session_dir or not os.path.exists(self.session_dir):
            print("❌ Output directory not found.")
            return
        
        try:
            os.startfile(self.session_dir)  # Windows
            print(f"📁 Opened folder: {self.session_dir}")
        except AttributeError:
            try:
                os.system(f'open "{self.session_dir}"')  # macOS
                print(f"📁 Opened folder: {self.session_dir}")
            except:
                try:
                    os.system(f'xdg-open "{self.session_dir}"')  # Linux
                    print(f"📁 Opened folder: {self.session_dir}")
                except:
                    print(f"📁 Output folder: {os.path.abspath(self.session_dir)}")
    
    def show_file_paths(self):
        """Show all generated file paths."""
        if not self.session_dir or not os.path.exists(self.session_dir):
            print("❌ Output directory not found.")
            return
        
        print(f"\n📁 Generated Files in {self.session_dir}:")
        for file in sorted(os.listdir(self.session_dir)):
            file_path = os.path.join(self.session_dir, file)
            if os.path.isfile(file_path):
                full_path = os.path.abspath(file_path)
                print(f"   📄 {file}")
                print(f"      {full_path}")
    
    def run_interactive_session(self):
        """Run a complete interactive session."""
        while True:
            # Get input
            file_path, input_type = self.get_user_input()
            if not file_path:
                break
            
            # Get configuration
            config = self.get_study_guide_config(input_type, file_path)
            
            # Create study guide
            result = self.create_study_guide(file_path, config)
            
            # Display results and get next action
            continue_session = self.display_results(result, config)
            
            # Clean up temporary files
            if input_type == "text" and file_path.startswith(tempfile.gettempdir()):
                try:
                    os.unlink(file_path)
                except:
                    pass
            
            if not continue_session:
                break
            
            print("\n" + "="*70)
            print("🔄 READY FOR NEXT STUDY GUIDE")
            print("="*70)
    
    def run(self):
        """Main entry point."""
        self.print_banner()
        
        try:
            self.run_interactive_session()
        except KeyboardInterrupt:
            print("\n\n🛑 Process interrupted by user.")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        
        print("\n👋 Thank you for using the LangChain Study Guide Creator!")
        print("🎓 Happy studying!")

def main():
    """Main function."""
    creator = InteractiveStudyGuideCreator()
    creator.run()

if __name__ == "__main__":
    main()
