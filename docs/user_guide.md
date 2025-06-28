# User Guide

## Getting Started

### Installation

1. **Clone or download** the project files
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up API key** (optional but recommended):

   ```bash
   # Windows
   set OPENAI_API_KEY=your_api_key_here

   # Linux/Mac
   export OPENAI_API_KEY=your_api_key_here
   ```

### Quick Start

The easiest way to get started is with the web interface:

```bash
streamlit run app.py
```

This will open a web browser with the interactive interface.

## Usage Methods

### 1. Web Interface (Recommended)

The Streamlit web interface provides the most user-friendly experience:

1. **Start the app:** `streamlit run app.py`
2. **Upload a file** or paste text directly
3. **Configure settings** (subject, level, options)
4. **Generate study guide**
5. **Download results** in your preferred format

**Features:**

- File upload (PDF, DOCX, TXT)
- Real-time progress tracking
- Interactive quiz taking
- Progress analytics
- One-click downloads

### 2. Command Line Interface

For automation and scripting:

```bash
# Basic usage
python main.py --input textbook.pdf --subject "Mathematics"

# Advanced options
python main.py \
    --input lecture_notes.docx \
    --subject "Physics" \
    --level undergraduate \
    --title "Quantum Mechanics Guide" \
    --formats html pdf json \
    --output my_guides/
```

**CLI Options:**

- `--input`: Input file path
- `--subject`: Subject area
- `--level`: Education level (high_school, undergraduate, graduate, professional)
- `--title`: Custom title
- `--formats`: Export formats (html, pdf, markdown, json, anki)
- `--output`: Output directory
- `--no-quiz`: Skip quiz generation
- `--no-visuals`: Skip visualizations

### 3. Python API

For integration into other projects:

```python
from study_guide_creator import StudyGuideCreator, StudyGuideRequest

# Initialize
creator = StudyGuideCreator(api_key="your_key")

# Create from file
request = StudyGuideRequest(
    input_file="textbook.pdf",
    subject="Biology",
    level="undergraduate"
)
result = creator.create_study_guide(request)

# Create from text
result = creator.create_from_text(
    text="Your study material here...",
    subject="Chemistry",
    level="high_school"
)
```

## File Format Support

### Input Formats

| Format        | Extension       | Notes                         |
| ------------- | --------------- | ----------------------------- |
| PDF           | `.pdf`          | Best for textbooks and papers |
| Word Document | `.docx`, `.doc` | Good for lecture notes        |
| Text File     | `.txt`          | Simple text content           |

**Tips for best results:**

- Use clear, well-structured documents
- Ensure text is readable (not scanned images)
- Include headings and section breaks
- Avoid overly complex formatting

### Output Formats

| Format       | Best For          | Features                            |
| ------------ | ----------------- | ----------------------------------- |
| **HTML**     | Interactive study | Clickable, searchable, web-friendly |
| **PDF**      | Printing          | Professional layout, portable       |
| **Markdown** | Editing           | Easy to modify, version control     |
| **JSON**     | Data processing   | Machine-readable, API integration   |
| **Anki CSV** | Flashcards        | Import into Anki spaced repetition  |

## Features Guide

### Study Guide Generation

The AI analyzes your content and creates:

1. **Overview Summary**: High-level understanding of the material
2. **Key Concepts**: Important terms with definitions and relationships
3. **Chapter Summaries**: Structured breakdown of each section
4. **Practice Questions**: Multiple choice, true/false, and short answer
5. **Flashcards**: Front/back cards for active recall

### Interactive Quizzes

**Quiz Types:**

- **Standard Quiz**: Based on study guide content
- **Adaptive Quiz**: Adjusts to your performance
- **Custom Quiz**: Create your own questions

**Question Types:**

- Multiple choice (A, B, C, D)
- True/False
- Short answer
- Essay questions

**Features:**

- Immediate feedback
- Explanations for answers
- Progress tracking
- Performance analytics
- Study recommendations

### Visualizations

**Concept Maps:**

- Shows relationships between ideas
- Visual learning aid
- Interactive web version available

**Word Clouds:**

- Highlights important terms
- Visual term frequency
- Customizable colors and layouts

**Timelines:**

- Historical events
- Process flows
- Chronological learning

**Flow Charts:**

- Step-by-step processes
- Decision trees
- Problem-solving guides

### Progress Tracking

Monitor your learning with:

- Quiz score trends
- Time spent studying
- Weak area identification
- Improvement recommendations
- Achievement milestones

## Best Practices

### Content Preparation

1. **Use Quality Sources:**

   - Academic textbooks
   - Lecture slides
   - Scholarly articles
   - Official documentation

2. **Structure Your Content:**

   - Clear headings
   - Logical flow
   - Consistent formatting
   - Complete sentences

3. **Optimize Length:**
   - 1,000-10,000 words ideal
   - Break very long documents into chapters
   - Include all essential information

### Subject Configuration

**Subject Examples:**

- Mathematics (Calculus, Algebra, Statistics)
- Physics (Mechanics, Thermodynamics, Quantum)
- Biology (Cell Biology, Genetics, Ecology)
- Chemistry (Organic, Inorganic, Physical)
- Computer Science (Algorithms, Data Structures)
- History (World History, American History)
- Literature (Poetry, Prose, Drama)

**Level Guidelines:**

- **High School**: Basic concepts, introductory level
- **Undergraduate**: Intermediate depth, some prerequisites
- **Graduate**: Advanced topics, specialized knowledge
- **Professional**: Industry-specific, practical applications

### Study Strategies

1. **Active Learning:**

   - Take the generated quizzes
   - Review flashcards regularly
   - Create concept maps

2. **Spaced Repetition:**

   - Export flashcards to Anki
   - Review at increasing intervals
   - Focus on weak areas

3. **Multi-Modal Learning:**

   - Read the HTML version
   - Print the PDF for notes
   - View visualizations

4. **Progress Monitoring:**
   - Track quiz scores
   - Identify improvement areas
   - Adjust study focus

## Troubleshooting

### Common Issues

**"API Key Error"**

- Solution: Set your OpenAI API key in environment variables
- Workaround: Use without API key (basic features only)

**"File Not Found"**

- Check file path is correct
- Ensure file exists and is readable
- Verify file format is supported

**"Import Error"**

- Install missing dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

**"PDF Processing Failed"**

- Try converting to text file first
- Check if PDF has selectable text (not scanned image)
- Reduce file size if very large

**"Memory Error"**

- Use smaller input files
- Close other applications
- Increase virtual memory

### Performance Tips

1. **Optimize File Size:**

   - Remove unnecessary images
   - Use text files when possible
   - Split large documents

2. **Internet Connection:**

   - Stable connection needed for AI features
   - Download dependencies in advance
   - Use offline mode for basic features

3. **Hardware Requirements:**
   - 4GB+ RAM recommended
   - 1GB+ free disk space
   - Modern CPU for faster processing

### Getting Help

1. **Check Documentation:**

   - API documentation: `docs/api.md`
   - User guide: `docs/user_guide.md`
   - README file

2. **Run Demo:**

   ```bash
   python demo.py
   ```

3. **Test with Samples:**

   ```bash
   python main.py --create-samples
   python main.py --list-samples
   ```

4. **Verbose Output:**
   ```bash
   python main.py --input file.pdf --subject Math --verbose
   ```

## Advanced Usage

### Custom Templates

Modify HTML/Markdown templates in the `templates/` directory:

1. Edit `study_guide.html` for HTML output
2. Edit `study_guide.md` for Markdown output
3. Restart application to apply changes

### Batch Processing

Process multiple files:

```python
from study_guide_creator import StudyGuideCreator

creator = StudyGuideCreator()
files = ["ch1.pdf", "ch2.pdf", "ch3.pdf"]

for file in files:
    result = creator.create_study_guide(
        StudyGuideRequest(input_file=file, subject="Physics")
    )
    print(f"Processed: {file}")
```

### Integration with LMS

Export study guides for Learning Management Systems:

```python
# Export for Canvas, Blackboard, etc.
exporter = StudyGuideExporter()
html_content = exporter.export_to_html(study_guide, "guide.html")

# Create SCORM package
package = exporter.create_study_package(study_guide, output_dir="scorm_package")
```

### Custom Visualizations

Create custom visualizations:

```python
from visualization import EducationalVisualizer

visualizer = EducationalVisualizer()

# Custom concept map
concepts = [
    {"name": "Photosynthesis", "relationships": ["Light", "CO2", "Water"]},
    {"name": "Respiration", "relationships": ["Glucose", "Oxygen"]}
]

visualizer.create_concept_map(concepts, save_path="biology_map.png")
```

## Sample Workflows

### Textbook Study Guide

1. Upload PDF textbook chapter
2. Set subject (e.g., "Organic Chemistry")
3. Set level to "undergraduate"
4. Include quiz and visuals
5. Export as HTML and PDF
6. Study HTML version online
7. Print PDF for offline review
8. Take quizzes for practice
9. Export flashcards to Anki

### Lecture Notes Processing

1. Upload DOCX lecture slides
2. Set specific topic (e.g., "Protein Synthesis")
3. Generate focused study guide
4. Create concept map
5. Take adaptive quiz
6. Review weak areas
7. Export Markdown for editing

### Exam Preparation

1. Process multiple chapters
2. Generate comprehensive quiz
3. Track performance over time
4. Focus on identified weak areas
5. Use spaced repetition with flashcards
6. Monitor progress to exam date

## Tips for Educators

### Creating Course Materials

1. **Process textbook chapters** to create supplementary guides
2. **Generate quizzes** for class activities
3. **Create concept maps** for visual learners
4. **Export flashcards** for student review
5. **Track student progress** with analytics

### Curriculum Development

1. **Analyze content coverage** with concept extraction
2. **Identify knowledge gaps** in materials
3. **Create learning objectives** from key concepts
4. **Develop assessment items** from practice questions
5. **Design visual aids** from generated diagrams

This completes the user guide! The system provides comprehensive tools for transforming educational content into interactive study materials.
