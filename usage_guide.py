#!/usr/bin/env python3
"""
Complete Usage Guide for Interactive Study Guide Creator
Shows all the ways users can interact with the system
"""

def show_usage_guide():
    print("🎓 LANGCHAIN STUDY GUIDE CREATOR - USER GUIDE")
    print("=" * 70)
    print("📚 Multiple ways to create study guides from your content!")
    print()
    
    print("🌟 INTERACTIVE OPTIONS:")
    print("-" * 30)
    
    print("\n1. 🚀 SUPER SIMPLE MODE (Recommended for beginners)")
    print("   Command: python user_interactive.py")
    print("   ✨ Just type your text and get a study guide!")
    print("   📝 Perfect for: Quick notes, lecture content, textbook chapters")
    print()
    
    print("2. 🎯 FULL INTERACTIVE MODE (Advanced features)")
    print("   Command: python interactive.py")
    print("   ✨ Complete control over all settings and options")
    print("   📝 Perfect for: Custom configurations, multiple formats")
    print()
    
    print("3. 💻 COMMAND LINE MODE (Direct control)")
    print("   Command: python main.py --input \"file.txt\" --subject \"Subject\"")
    print("   ✨ Batch processing and automation friendly")
    print("   📝 Perfect for: Multiple files, scripting, automation")
    print()
    
    print("4. 🌐 WEB INTERFACE MODE (Visual interface)")
    print("   Command: python local_server.py")
    print("   ✨ Browser-based interface with file upload")
    print("   📝 Perfect for: Visual learners, file uploads, sharing")
    print()
    
    print("📋 WHAT YOU CAN INPUT:")
    print("-" * 30)
    print("📄 File Types: PDF, DOCX, TXT files")
    print("✍️  Direct Text: Type or paste content directly")
    print("📚 Sample Materials: Use built-in examples")
    print("🔗 Any Subject: Math, Science, History, Languages, etc.")
    print()
    
    print("🎯 WHAT YOU GET:")
    print("-" * 30)
    print("📚 Comprehensive Study Guide with key concepts")
    print("❓ Interactive Quiz with multiple choice questions")
    print("🧠 Practice Questions for self-testing")
    print("📊 Visual aids (concept maps, word clouds)")
    print("📁 Multiple formats (HTML, PDF, JSON)")
    print("💡 Study recommendations and tips")
    print()
    
    print("🔥 EXAMPLE WORKFLOW:")
    print("-" * 30)
    print("1. Choose your preferred method above")
    print("2. Enter your study material (text, file, or sample)")
    print("3. Specify the subject (Biology, Math, etc.)")
    print("4. Configure options (level, formats, features)")
    print("5. Get your complete study package!")
    print("6. View in browser or share with others")
    print()
    
    print("💡 QUICK START EXAMPLES:")
    print("-" * 30)
    print("📝 For quick text input:")
    print("   python user_interactive.py")
    print()
    print("📄 For file processing:")
    print("   python main.py --input \"textbook.pdf\" --subject \"Biology\"")
    print()
    print("🌐 For web interface:")
    print("   python local_server.py")
    print("   Then visit: http://localhost:8080/demo_viewer.html")
    print()
    
    print("🎉 ALL METHODS WORK WITHOUT API KEYS!")
    print("   The system includes smart fallback templates")
    print("   Add OpenAI API key for enhanced AI features")
    print()
    
    print("📞 NEED HELP?")
    print("-" * 30)
    print("🔍 Run: python show_status.py (to see what's available)")
    print("🧪 Run: python demo_interactive.py (to see examples)")
    print("📚 Check: README.md for detailed documentation")

if __name__ == "__main__":
    show_usage_guide()
