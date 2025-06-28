#!/usr/bin/env python3
"""
Demo of Interactive Study Guide Creator
Shows how the interactive interface works with sample input
"""

import os
import tempfile
from study_guide_creator import StudyGuideCreator, StudyGuideRequest

def demo_interactive_creation():
    """Demonstrate interactive study guide creation."""
    
    print("🎓 INTERACTIVE STUDY GUIDE CREATOR DEMO")
    print("=" * 60)
    print("This demo shows how the interactive interface works!")
    print()
    
    # Sample user input
    sample_texts = {
        "Biology": """
Cell Biology Fundamentals

Cells are the basic units of life. There are two main types of cells:

1. Prokaryotic Cells:
   - No nucleus
   - Genetic material free in cytoplasm
   - Examples: bacteria, archaea

2. Eukaryotic Cells:
   - Have a nucleus
   - Membrane-bound organelles
   - Examples: plants, animals, fungi

Key organelles in eukaryotic cells:
- Nucleus: Contains DNA, controls cell activities
- Mitochondria: Powerhouse of the cell, produces ATP
- Ribosomes: Protein synthesis
- Endoplasmic Reticulum: Protein and lipid synthesis
- Golgi Apparatus: Modifies and packages proteins

Cell division occurs through mitosis, which produces two identical cells.
        """,
        
        "Physics": """
Introduction to Quantum Mechanics

Quantum mechanics is the branch of physics that describes matter and energy at the atomic scale.

Key Principles:
1. Wave-Particle Duality: Light and matter exhibit both wave and particle properties
2. Uncertainty Principle: Cannot simultaneously know exact position and momentum
3. Superposition: Particles can exist in multiple states simultaneously

Important Equations:
- Planck's equation: E = hf
- De Broglie wavelength: λ = h/p
- Schrödinger equation: describes quantum states

Applications:
- Lasers and LEDs
- Computer processors
- MRI machines
- Quantum computing
        """,
        
        "Mathematics": """
Calculus Fundamentals

Calculus is the study of continuous change, with two main branches:

1. Differential Calculus (Derivatives):
   - Measures rate of change
   - Slope of tangent lines
   - Key rules: power rule, product rule, chain rule
   - Applications: optimization, physics

2. Integral Calculus (Integrals):
   - Measures accumulation
   - Area under curves
   - Fundamental theorem connects derivatives and integrals
   - Applications: physics, engineering, economics

Important concepts:
- Limits: foundation of calculus
- Continuity: smooth functions
- Differentiation: finding derivatives
- Integration: finding antiderivatives
        """
    }
    
    for subject, content in sample_texts.items():
        print(f"📚 Creating study guide for: {subject}")
        print(f"📝 Sample content preview: {content[:100]}...")
        print("⏳ Processing...")
        
        try:
            # Create temporary file with content
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(content)
                temp_path = temp_file.name
            
            # Create study guide
            creator = StudyGuideCreator()
            output_dir = f"demo_{subject.lower()}_output"
            
            request = StudyGuideRequest(
                input_file=temp_path,
                subject=subject,
                level="undergraduate",
                title=f"{subject} Study Guide",
                output_dir=output_dir,
                export_formats=["html", "json"],
                include_quiz=True,
                include_visuals=True
            )
            
            result = creator.create_study_guide(request)
            
            print(f"✅ {subject} study guide created!")
            print(f"   📁 Output: {output_dir}")
            print(f"   🔑 Key concepts: {len(result.study_guide.key_concepts)}")
            
            if result.quiz:
                print(f"   ❓ Quiz questions: {len(result.quiz.questions)}")
                # Show sample question
                if result.quiz.questions:
                    q = result.quiz.questions[0]
                    print(f"   Sample Q: {q['question']}")
            
            # Clean up
            os.unlink(temp_path)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            try:
                os.unlink(temp_path)
            except:
                pass
        
        print()
    
    print("🎉 DEMO COMPLETE!")
    print("=" * 60)
    print("📋 How to use the interactive version:")
    print("1. Run: python interactive.py")
    print("2. Choose input method (file, text, or sample)")
    print("3. Enter your study material")
    print("4. Configure settings (subject, level, etc.)")
    print("5. Get your complete study guide!")
    print()
    print("📁 Generated demo files:")
    for subject in sample_texts.keys():
        output_dir = f"demo_{subject.lower()}_output"
        if os.path.exists(output_dir):
            print(f"   📚 {subject}: {output_dir}/")

if __name__ == "__main__":
    demo_interactive_creation()
