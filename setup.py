"""
Setup script to verify and install dependencies for the LangChain Study Guide Creator.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True

def install_requirements():
    """Install required packages."""
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ Requirements file not found: {requirements_file}")
        return False
    
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_imports():
    """Check if all required modules can be imported."""
    required_modules = [
        ("PyPDF2", "PyPDF2"),
        ("docx", "python-docx"),
        ("matplotlib", "matplotlib"),
        ("nltk", "nltk"),
        ("sklearn", "scikit-learn"),
        ("wordcloud", "wordcloud"),
        ("plotly", "plotly"),
        ("streamlit", "streamlit"),
        ("fpdf", "fpdf2"),
        ("jinja2", "jinja2"),
        ("markdown", "markdown")
    ]
    
    print("🔍 Checking imports...")
    success = True
    
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - OK")
        except ImportError:
            print(f"❌ {module_name} - Missing (install: pip install {package_name})")
            success = False
    
    # Optional modules
    optional_modules = [
        ("langchain", "langchain"),
        ("langchain_openai", "langchain-openai"),
        ("openai", "openai")
    ]
    
    print("\n🔍 Checking optional imports...")
    for module_name, package_name in optional_modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - OK (enhanced features available)")
        except ImportError:
            print(f"⚠️  {module_name} - Missing (install: pip install {package_name})")
    
    return success

def download_nltk_data():
    """Download required NLTK data."""
    print("📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        print("✅ NLTK data downloaded")
        return True
    except Exception as e:
        print(f"⚠️  Could not download NLTK data: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    dirs = [
        "generated_guides",
        "sample_materials", 
        "templates",
        "docs"
    ]
    
    print("📁 Creating directories...")
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✅ {dir_name}/")
    
    return True

def check_api_key():
    """Check for API key configuration."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    print("🔑 Checking API configuration...")
    if api_key:
        print("✅ OPENAI_API_KEY found in environment")
        return True
    else:
        print("⚠️  OPENAI_API_KEY not found")
        print("   Set your API key for enhanced features:")
        print("   Windows: set OPENAI_API_KEY=your_key")
        print("   Linux/Mac: export OPENAI_API_KEY=your_key")
        return False

def run_basic_test():
    """Run a basic test to verify the system works."""
    print("🧪 Running basic functionality test...")
    
    try:
        # Import main classes without API dependencies
        from content_processor import ContentProcessor
        from exporters import StudyGuideExporter
        from visualization import EducationalVisualizer
        
        # Test content processor
        processor = ContentProcessor()
        
        # Test exporter
        exporter = StudyGuideExporter()
        
        # Test visualizer  
        visualizer = EducationalVisualizer()
        
        print("✅ Basic functionality test passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🎓 LangChain Study Guide Creator - Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("⚠️  Continuing with existing packages...")
    
    # Check imports
    if not check_imports():
        print("\n❌ Some dependencies are missing.")
        print("Run: pip install -r requirements.txt")
        
        choice = input("\nContinue anyway? (y/N): ").lower()
        if choice != 'y':
            sys.exit(1)
    
    # Download NLTK data
    download_nltk_data()
    
    # Create directories
    create_directories()
    
    # Check API key
    api_available = check_api_key()
    
    # Run basic test
    if not run_basic_test():
        print("❌ Setup incomplete - some components failed")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n🚀 Next steps:")
    print("1. Run demo: python demo.py")
    print("2. Start web app: streamlit run app.py")
    print("3. Use CLI: python main.py --help")
    
    if not api_available:
        print("\n💡 For enhanced AI features:")
        print("Set your OpenAI API key and run setup again")
    
    print("\n📚 Documentation:")
    print("- User guide: docs/user_guide.md")
    print("- API docs: docs/api.md")
    print("- README: README.md")

if __name__ == "__main__":
    main()
