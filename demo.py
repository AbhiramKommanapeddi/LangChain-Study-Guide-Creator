"""
Demo script showcasing all features of the LangChain Study Guide Creator.
This script demonstrates the complete workflow and creates sample study guides.
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from study_guide_creator import StudyGuideCreator, StudyGuideRequest
from quiz_generator import QuizGenerator
from visualization import EducationalVisualizer
from exporters import StudyGuideExporter

def create_demo_content():
    """Create demo content for different subjects."""
    
    demo_content = {
        "Mathematics": """
# Calculus Fundamentals

## Introduction to Derivatives

The derivative of a function represents the rate of change at any given point. 
It is fundamental to understanding motion, optimization, and many other mathematical concepts.

### Definition
The derivative of a function f(x) at point x is defined as:
f'(x) = lim(h→0) [f(x+h) - f(x)] / h

### Key Rules
1. Power Rule: d/dx[x^n] = nx^(n-1)
2. Product Rule: d/dx[f(x)g(x)] = f'(x)g(x) + f(x)g'(x)
3. Chain Rule: d/dx[f(g(x))] = f'(g(x)) × g'(x)

### Applications
- Finding slopes of tangent lines
- Optimization problems
- Related rates
- Motion analysis

## Introduction to Integrals

Integration is the reverse process of differentiation. It allows us to find areas under curves,
volumes of solids, and solve differential equations.

### Fundamental Theorem of Calculus
If F'(x) = f(x), then ∫[a to b] f(x)dx = F(b) - F(a)

### Integration Techniques
1. Substitution
2. Integration by parts
3. Partial fractions
4. Trigonometric substitution

### Applications
- Area under curves
- Volume calculations
- Center of mass
- Work problems
        """,
        
        "Physics": """
# Quantum Mechanics Principles

## Wave-Particle Duality

Light and matter exhibit both wave and particle characteristics. This fundamental concept
revolutionized our understanding of the microscopic world.

### Key Experiments
1. Double-slit experiment
2. Photoelectric effect
3. Compton scattering

### Implications
- Particles can behave like waves
- Waves can behave like particles
- Measurement affects the system

## Uncertainty Principle

Heisenberg's uncertainty principle states that certain pairs of properties cannot be
simultaneously measured with perfect precision.

### Mathematical Formulation
Δx × Δp ≥ ℏ/2

Where:
- Δx = uncertainty in position
- Δp = uncertainty in momentum
- ℏ = reduced Planck constant

### Applications
- Atomic structure
- Quantum tunneling
- Zero-point energy

## Schrödinger Equation

The Schrödinger equation describes how quantum systems evolve over time.

### Time-Dependent Form
iℏ ∂ψ/∂t = Ĥψ

### Applications
- Atomic orbitals
- Molecular bonding
- Quantum computing
        """,
        
        "Biology": """
# Cell Biology Fundamentals

## Cell Structure and Organization

Cells are the basic units of life. Understanding their structure is crucial for
comprehending all biological processes.

### Prokaryotic Cells
- No membrane-bound nucleus
- Genetic material freely floating
- Examples: bacteria, archaea

### Eukaryotic Cells
- Membrane-bound nucleus
- Complex organelles
- Examples: plants, animals, fungi

## Key Organelles

### Nucleus
- Contains genetic material (DNA)
- Controls cell activities
- Surrounded by nuclear envelope

### Mitochondria
- Powerhouse of the cell
- ATP production
- Double membrane structure

### Endoplasmic Reticulum
- Protein synthesis (rough ER)
- Lipid synthesis (smooth ER)
- Transport system

### Golgi Apparatus
- Protein modification
- Packaging and shipping
- Post-translational modifications

## Cellular Processes

### Cellular Respiration
Process of converting glucose to ATP:
1. Glycolysis (cytoplasm)
2. Krebs cycle (mitochondria)
3. Electron transport chain (mitochondria)

### Photosynthesis
Process of converting light energy to chemical energy:
1. Light reactions (thylakoids)
2. Calvin cycle (stroma)

### Cell Division
- Mitosis: somatic cell division
- Meiosis: gamete formation
- DNA replication and segregation
        """
    }
    
    return demo_content

def demo_basic_functionality():
    """Demonstrate basic study guide creation without API key."""
    print("🎓 LangChain Study Guide Creator - Demo")
    print("=" * 50)
    print("This demo showcases the complete functionality of the study guide creator.")
    print("Note: Running without OpenAI API key - using fallback features.\n")
    
    # Create study guide creator
    creator = StudyGuideCreator()
    
    # Create sample materials
    print("📚 Creating sample materials...")
    sample_dir = creator.create_sample_materials()
    print(f"✅ Sample materials created in: {sample_dir}\n")
    
    # Get demo content
    demo_content = create_demo_content()
    
    # Demonstrate study guide creation for each subject
    subjects = ["Mathematics", "Physics", "Biology"]
    
    for subject in subjects:
        print(f"🔬 Creating {subject} study guide...")
        
        try:
            # Create study guide from text
            result = creator.create_from_text(
                text=demo_content[subject],
                subject=subject,
                level="undergraduate"
            )
            
            if result["success"]:
                study_guide = result["study_guide"]
                quiz = result.get("quiz")
                
                print(f"✅ {subject} study guide created successfully!")
                print(f"   - Key concepts: {len(study_guide.key_concepts)}")
                print(f"   - Practice questions: {len(study_guide.practice_questions)}")
                print(f"   - Flashcards: {len(study_guide.flashcards)}")
                if quiz:
                    print(f"   - Quiz questions: {len(quiz.questions)}")
                print(f"   - Package location: {result['package_directory']}")
                print()
                
                # Show some content examples
                print(f"📖 Sample content from {subject}:")
                if study_guide.key_concepts:
                    concept = study_guide.key_concepts[0]
                    concept_name = concept.get('name', 'Concept') if isinstance(concept, dict) else str(concept)
                    print(f"   First concept: {concept_name}")
                
                if study_guide.practice_questions:
                    question = study_guide.practice_questions[0]
                    print(f"   Sample question: {question.get('question', 'N/A')[:60]}...")
                
                print()
                
        except Exception as e:
            print(f"❌ Error creating {subject} study guide: {e}")
            print()
    
    print("🎉 Demo completed! Check the 'generated_guides' directory for output files.")
    return True

def demo_advanced_features():
    """Demonstrate advanced features if API key is available."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("⚠️  No OpenAI API key found. Skipping advanced AI features demo.")
        print("   Set OPENAI_API_KEY environment variable to see full AI capabilities.")
        return False
    
    print("🚀 Demonstrating advanced AI features...")
    
    try:
        # Create AI-powered study guide creator
        creator = StudyGuideCreator(openai_api_key=api_key)
        
        # Create enhanced study guide
        demo_content = create_demo_content()
        
        print("🧠 Creating AI-enhanced study guide...")
        result = creator.create_from_text(
            text=demo_content["Mathematics"],
            subject="Advanced Calculus",
            level="graduate"
        )
        
        if result["success"]:
            study_guide = result["study_guide"]
            print("✅ AI-enhanced study guide created!")
            print(f"   Enhanced with GPT-generated content and insights")
            
            # Demonstrate adaptive quiz
            if result.get("quiz"):
                print("🎯 Creating adaptive quiz...")
                quiz_gen = QuizGenerator(api_key=api_key)
                
                # Simulate previous results for adaptive quiz
                from quiz_generator import QuizResult
                fake_results = [
                    QuizResult(
                        quiz_title="Previous Quiz",
                        score=6,
                        total_questions=10,
                        percentage=60.0,
                        time_taken=300,
                        correct_answers=[1, 2, 3, 6, 7, 8],
                        incorrect_answers=[4, 5, 9, 10],
                        detailed_results=[],
                        recommendations=[]
                    )
                ]
                
                adaptive_quiz = quiz_gen.create_adaptive_quiz(
                    "Advanced Calculus",
                    fake_results,
                    num_questions=5
                )
                
                print("✅ Adaptive quiz created based on performance analysis!")
                print(f"   Focused on weak areas for personalized learning")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in advanced features demo: {e}")
        return False

def demo_visualization_features():
    """Demonstrate visualization capabilities."""
    print("🎨 Demonstrating visualization features...")
    
    try:
        visualizer = EducationalVisualizer()
        
        # Sample concepts for visualization
        sample_concepts = [
            {"name": "Derivatives", "definition": "Rate of change", "relationships": ["Integrals", "Limits"]},
            {"name": "Integrals", "definition": "Area under curve", "relationships": ["Derivatives"]},
            {"name": "Limits", "definition": "Approaching value", "relationships": ["Derivatives", "Continuity"]},
            {"name": "Continuity", "definition": "Unbroken function", "relationships": ["Limits"]}
        ]
        
        # Create concept map
        concept_map_path = "demo_concept_map.png"
        visualizer.create_concept_map(
            sample_concepts,
            title="Mathematics Concept Map",
            save_path=concept_map_path
        )
        
        if os.path.exists(concept_map_path):
            print(f"✅ Concept map created: {concept_map_path}")
        
        # Create word cloud
        sample_text = "calculus derivatives integrals limits functions mathematics analysis optimization rates change areas volumes"
        word_cloud_path = "demo_word_cloud.png"
        visualizer.create_word_cloud(
            sample_text,
            title="Mathematics Terms",
            save_path=word_cloud_path
        )
        
        if os.path.exists(word_cloud_path):
            print(f"✅ Word cloud created: {word_cloud_path}")
        
        # Create timeline
        events = [
            {"name": "Newton", "date": "1665", "description": "Developed calculus"},
            {"name": "Leibniz", "date": "1684", "description": "Published calculus notation"},
            {"name": "Euler", "date": "1748", "description": "Systematized calculus"}
        ]
        
        timeline_path = "demo_timeline.png"
        visualizer.create_timeline_diagram(
            events,
            title="History of Calculus",
            save_path=timeline_path
        )
        
        if os.path.exists(timeline_path):
            print(f"✅ Timeline diagram created: {timeline_path}")
        
        print("🎨 Visualization demo completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error in visualization demo: {e}")
        return False

def demo_export_features():
    """Demonstrate export capabilities."""
    print("📁 Demonstrating export features...")
    
    try:
        # Create a sample study guide for export
        creator = StudyGuideCreator()
        demo_content = create_demo_content()
        
        result = creator.create_from_text(
            text=demo_content["Mathematics"][:500],  # Truncate for demo
            subject="Export Demo",
            level="undergraduate"
        )
        
        if result["success"]:
            study_guide = result["study_guide"]
            exporter = StudyGuideExporter()
            
            # Demonstrate different export formats
            formats = ["html", "pdf", "markdown", "json"]
            
            for fmt in formats:
                try:
                    output_path = f"demo_export.{fmt}"
                    
                    if fmt == "html":
                        exporter.export_to_html(study_guide, output_path)
                    elif fmt == "pdf":
                        exporter.export_to_pdf(study_guide, output_path)
                    elif fmt == "markdown":
                        exporter.export_to_markdown(study_guide, output_path)
                    elif fmt == "json":
                        exporter.export_to_json(study_guide, output_path)
                    
                    if os.path.exists(output_path):
                        print(f"✅ Exported to {fmt.upper()}: {output_path}")
                        
                except Exception as e:
                    print(f"⚠️  Could not export to {fmt}: {e}")
            
            # Create complete study package
            package_dir = exporter.create_study_package(
                study_guide,
                result.get("quiz"),
                "demo_study_package"
            )
            
            print(f"✅ Complete study package created: {package_dir}")
            
        print("📁 Export demo completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error in export demo: {e}")
        return False

def main():
    """Run the complete demo."""
    print("🎓 LangChain Study Guide Creator - Complete Demo")
    print("=" * 60)
    print()
    
    # Check requirements
    print("🔍 Checking requirements...")
    try:
        import langchain
        print("✅ LangChain available")
    except ImportError:
        print("⚠️  LangChain not installed - some features may be limited")
    
    try:
        import matplotlib
        print("✅ Matplotlib available for visualizations")
    except ImportError:
        print("⚠️  Matplotlib not installed - visualizations disabled")
    
    try:
        import streamlit
        print("✅ Streamlit available for web interface")
    except ImportError:
        print("⚠️  Streamlit not installed - web interface disabled")
    
    print()
    
    # Run demo sections
    success_count = 0
    
    # Basic functionality
    if demo_basic_functionality():
        success_count += 1
    
    # Advanced AI features
    if demo_advanced_features():
        success_count += 1
    
    # Visualization features
    if demo_visualization_features():
        success_count += 1
    
    # Export features  
    if demo_export_features():
        success_count += 1
    
    # Summary
    print()
    print("📊 Demo Summary")
    print("=" * 30)
    print(f"✅ Successfully demonstrated {success_count}/4 feature sets")
    print()
    
    print("🚀 Next Steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set OpenAI API key: export OPENAI_API_KEY=your_key")
    print("3. Run web interface: streamlit run app.py")
    print("4. Use CLI: python main.py --help")
    print()
    
    print("📚 Generated Files:")
    print("- Check 'generated_guides/' for study guides")
    print("- Check 'sample_materials/' for sample inputs")
    print("- Check current directory for demo visualizations")
    print()
    
    print("🎉 Demo completed successfully!")

if __name__ == "__main__":
    main()
