"""
Command-line interface for the LangChain Study Guide Creator.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

from study_guide_creator import StudyGuideCreator, StudyGuideRequest

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="LangChain Study Guide Creator - Generate comprehensive study guides from textbooks and lecture materials",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input textbook.pdf --subject "Mathematics" --level undergraduate
  %(prog)s --input notes.txt --subject "Physics" --title "Quantum Mechanics Guide"
  %(prog)s --create-samples
  %(prog)s --input lecture.docx --subject "Biology" --no-quiz --formats html pdf
        """
    )
    
    # Input options
    parser.add_argument(
        "--input", "-i",
        type=str,
        help="Input file path (PDF, DOCX, or TXT)"
    )
    
    parser.add_argument(
        "--subject", "-s",
        type=str,
        help="Subject area (e.g., Mathematics, Physics, Biology)"
    )
    
    parser.add_argument(
        "--level", "-l",
        type=str,
        default="undergraduate",
        choices=["high_school", "undergraduate", "graduate", "professional"],
        help="Education level (default: undergraduate)"
    )
    
    parser.add_argument(
        "--title", "-t",
        type=str,
        help="Custom title for the study guide"
    )
    
    # Output options
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="generated_guides",
        help="Output directory (default: generated_guides)"
    )
    
    parser.add_argument(
        "--formats", "-f",
        nargs="+",
        default=["html", "pdf", "json"],
        choices=["html", "pdf", "markdown", "json", "anki"],
        help="Export formats (default: html pdf json)"
    )
    
    # Feature options
    parser.add_argument(
        "--no-quiz",
        action="store_true",
        help="Skip quiz generation"
    )
    
    parser.add_argument(
        "--no-visuals",
        action="store_true", 
        help="Skip visual diagram generation"
    )
    
    # Utility options
    parser.add_argument(
        "--create-samples",
        action="store_true",
        help="Create sample study materials for testing"
    )
    
    parser.add_argument(
        "--list-samples",
        action="store_true",
        help="List available sample materials"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        help="OpenAI API key (or set OPENAI_API_KEY environment variable)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Initialize the study guide creator
    try:
        creator = StudyGuideCreator(openai_api_key=args.api_key)
    except Exception as e:
        print(f"❌ Error initializing StudyGuideCreator: {e}")
        sys.exit(1)
    
    # Handle utility commands
    if args.create_samples:
        print("📚 Creating sample study materials...")
        sample_dir = creator.create_sample_materials()
        print(f"✅ Sample materials created in: {sample_dir}")
        print("Use --list-samples to see available files")
        return
    
    if args.list_samples:
        sample_dir = "sample_materials"
        if os.path.exists(sample_dir):
            print("📁 Available sample materials:")
            for file in os.listdir(sample_dir):
                if file.endswith(('.txt', '.pdf', '.docx')):
                    file_path = os.path.join(sample_dir, file)
                    print(f"  - {file_path}")
            print(f"\nTo use a sample: --input {sample_dir}/filename")
        else:
            print("No sample materials found. Use --create-samples to create them.")
        return
    
    # Validate required arguments
    if not args.input:
        print("❌ Error: --input is required")
        parser.print_help()
        sys.exit(1)
    
    if not args.subject:
        print("❌ Error: --subject is required")
        parser.print_help()
        sys.exit(1)
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file not found: {args.input}")
        sys.exit(1)
    
    # Create study guide request
    request = StudyGuideRequest(
        input_file=args.input,
        subject=args.subject,
        level=args.level,
        title=args.title,
        include_quiz=not args.no_quiz,
        include_visuals=not args.no_visuals,
        export_formats=args.formats,
        output_dir=args.output
    )
    
    # Generate study guide
    try:
        print("🚀 Starting study guide generation...")
        result = creator.create_study_guide(request)
        
        if result["success"]:
            print("\n🎉 Study guide generation completed successfully!")
            print(f"📁 Study package: {result['package_directory']}")
            
            if args.verbose:
                print("\n📊 Generation Summary:")
                study_guide = result["study_guide"]
                print(f"  - Title: {study_guide.title}")
                print(f"  - Subject: {study_guide.subject}")
                print(f"  - Level: {study_guide.level}")
                print(f"  - Key concepts: {len(study_guide.key_concepts)}")
                print(f"  - Practice questions: {len(study_guide.practice_questions)}")
                print(f"  - Flashcards: {len(study_guide.flashcards)}")
                
                if result["quiz"]:
                    quiz = result["quiz"]
                    print(f"  - Quiz questions: {len(quiz.questions)}")
                
                print(f"\n📁 Generated files:")
                for format_type, file_path in result["exported_files"].items():
                    print(f"  - {format_type.upper()}: {file_path}")
                
                if result["visual_files"]:
                    print(f"\n🎨 Visualizations:")
                    for visual_type, file_path in result["visual_files"].items():
                        print(f"  - {visual_type}: {file_path}")
        else:
            print("❌ Study guide generation failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Generation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def interactive_mode():
    """Interactive mode for the study guide creator."""
    print("🎓 LangChain Study Guide Creator - Interactive Mode")
    print("=" * 50)
    
    # Get input file
    while True:
        input_file = input("📄 Enter path to your document (PDF, DOCX, TXT): ").strip()
        if os.path.exists(input_file):
            break
        print("❌ File not found. Please enter a valid file path.")
    
    # Get subject
    subject = input("📚 Enter the subject area: ").strip()
    while not subject:
        subject = input("Subject cannot be empty. Please enter the subject: ").strip()
    
    # Get level
    print("\n📈 Education levels:")
    print("1. High School")
    print("2. Undergraduate (default)")
    print("3. Graduate")
    print("4. Professional")
    
    level_choice = input("Enter choice (1-4, default 2): ").strip()
    level_map = {
        "1": "high_school",
        "2": "undergraduate", 
        "3": "graduate",
        "4": "professional"
    }
    level = level_map.get(level_choice, "undergraduate")
    
    # Get title
    title = input("📝 Enter custom title (optional): ").strip() or None
    
    # Get options
    include_quiz = input("❓ Include quiz? (Y/n): ").strip().lower() not in ['n', 'no']
    include_visuals = input("🎨 Include visualizations? (Y/n): ").strip().lower() not in ['n', 'no']
    
    # Create request
    request = StudyGuideRequest(
        input_file=input_file,
        subject=subject,
        level=level,
        title=title,
        include_quiz=include_quiz,
        include_visuals=include_visuals,
        export_formats=["html", "pdf", "json"]
    )
    
    # Generate study guide
    print("\n🚀 Generating your study guide...")
    try:
        creator = StudyGuideCreator()
        result = creator.create_study_guide(request)
        
        if result["success"]:
            print(f"\n🎉 Success! Your study guide is ready: {result['package_directory']}")
        else:
            print("❌ Generation failed")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, run interactive mode
        interactive_mode()
    else:
        # Arguments provided, run CLI mode
        main()
