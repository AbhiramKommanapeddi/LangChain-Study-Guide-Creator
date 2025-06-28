"""
Simple test to verify project structure and basic functionality.
This test runs without external dependencies.
"""

import os
import sys
from pathlib import Path

def test_project_structure():
    """Test that all required files exist."""
    print("📁 Testing project structure...")
    
    required_files = [
        "README.md",
        "requirements.txt",
        "main.py",
        "app.py",
        "demo.py",
        "setup.py",
        "study_guide_creator.py",
        "content_processor.py",
        "guide_generator.py",
        "quiz_generator.py",
        "visualization.py",
        "exporters.py",
        ".env.example"
    ]
    
    required_dirs = [
        "docs",
        "templates"
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
        else:
            print(f"✅ {dir_name}/")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    print("✅ Project structure complete")
    return True

def test_python_syntax():
    """Test Python syntax of all Python files."""
    print("\n🐍 Testing Python syntax...")
    
    python_files = [
        "main.py",
        "app.py", 
        "demo.py",
        "setup.py",
        "study_guide_creator.py",
        "content_processor.py",
        "guide_generator.py",
        "quiz_generator.py",
        "visualization.py",
        "exporters.py"
    ]
    
    for file in python_files:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    compile(content, file, 'exec')
                print(f"✅ {file} - syntax OK")
            except SyntaxError as e:
                print(f"❌ {file} - syntax error: {e}")
                return False
            except Exception as e:
                print(f"⚠️  {file} - warning: {e}")
    
    print("✅ Python syntax check passed")
    return True

def test_documentation():
    """Test that documentation files exist and are readable."""
    print("\n📚 Testing documentation...")
    
    doc_files = [
        "README.md",
        "docs/user_guide.md",
        "docs/api.md"
    ]
    
    for file in doc_files:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if len(content) > 100:  # Basic content check
                        print(f"✅ {file} - content OK")
                    else:
                        print(f"⚠️  {file} - minimal content")
            except Exception as e:
                print(f"❌ {file} - error: {e}")
                return False
        else:
            print(f"❌ {file} - missing")
            return False
    
    print("✅ Documentation check passed")
    return True

def test_requirements():
    """Test requirements.txt format."""
    print("\n📦 Testing requirements...")
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt missing")
        return False
    
    try:
        with open("requirements.txt", 'r') as f:
            lines = f.readlines()
            
        if len(lines) < 5:
            print("⚠️  requirements.txt seems minimal")
        
        # Check for key packages
        required_packages = [
            "matplotlib",
            "streamlit", 
            "PyPDF2",
            "jinja2"
        ]
        
        content = " ".join(lines)
        missing_packages = []
        
        for pkg in required_packages:
            if pkg.lower() not in content.lower():
                missing_packages.append(pkg)
        
        if missing_packages:
            print(f"⚠️  Missing packages: {missing_packages}")
        else:
            print("✅ Key packages found in requirements")
        
        print("✅ Requirements file format OK")
        return True
        
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def test_templates():
    """Test template structure."""
    print("\n📄 Testing templates...")
    
    if not os.path.exists("templates"):
        print("⚠️  templates directory will be created on first run")
        return True
    
    # Templates are created dynamically, so this is optional
    print("✅ Templates directory ready")
    return True

def create_sample_content():
    """Create a simple test file for demonstration."""
    print("\n📝 Creating sample content...")
    
    sample_dir = "sample_materials"
    os.makedirs(sample_dir, exist_ok=True)
    
    sample_content = """
# Mathematics Study Material

## Introduction to Calculus

Calculus is the mathematical study of continuous change. It has two main branches:
derivatives and integrals.

### Derivatives
The derivative measures the rate of change of a function. For a function f(x),
the derivative f'(x) represents the slope at any point.

Key formulas:
- Power rule: d/dx[x^n] = nx^(n-1)
- Product rule: d/dx[fg] = f'g + fg'
- Chain rule: d/dx[f(g(x))] = f'(g(x)) × g'(x)

### Integrals
Integration is the reverse of differentiation. It finds the area under curves
and solves accumulation problems.

Fundamental theorem: ∫f'(x)dx = f(x) + C

Applications:
- Finding areas under curves
- Calculating volumes of solids
- Solving differential equations
- Physics applications (motion, work, etc.)
    """
    
    try:
        with open(os.path.join(sample_dir, "sample_calculus.txt"), 'w', encoding='utf-8') as f:
            f.write(sample_content)
        print(f"✅ Sample content created in {sample_dir}/")
        return True
    except Exception as e:
        print(f"❌ Error creating sample content: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 LangChain Study Guide Creator - Basic Tests")
    print("=" * 55)
    
    tests = [
        test_project_structure,
        test_python_syntax,
        test_documentation,
        test_requirements,
        test_templates,
        create_sample_content
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All basic tests passed!")
        print("\n🚀 Ready to install dependencies and run:")
        print("1. python setup.py")
        print("2. python demo.py")
        print("3. streamlit run app.py")
    else:
        print("⚠️  Some tests failed - check the output above")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
