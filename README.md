# LangChain Study Guide Creator

A comprehensive educational content generator that creates study guides from textbooks and lecture materials using LangChain and AI.

## Features

### Core Features

- **Content Processing**: PDF textbook parsing, lecture note extraction, concept identification
- **Study Guide Generation**: Chapter summaries, key concept lists, practice questions
- **Learning Features**: Flashcard creation, quiz generation, progress tracking, difficulty levels

### Bonus Features

- Interactive quizzes with Streamlit UI
- Mind map generation
- Visual diagrams and word clouds
- Export to multiple formats (PDF, HTML, Markdown)

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:

```bash
# Create a .env file and add:
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Web Interface (Streamlit)

```bash
streamlit run app.py
```

### Command Line Interface

```bash
python main.py --input "path/to/document.pdf" --subject "Mathematics" --level "undergraduate"
```

### Python API

```python
from study_guide_creator import StudyGuideCreator

creator = StudyGuideCreator()
guide = creator.create_study_guide("document.pdf", subject="Physics")
guide.export_pdf("physics_study_guide.pdf")
```

## Project Structure

```
├── app.py                    # Streamlit web interface
├── main.py                   # CLI interface
├── study_guide_creator.py    # Main StudyGuideCreator class
├── content_processor.py      # PDF and text processing
├── guide_generator.py        # Study guide generation
├── quiz_generator.py         # Quiz and flashcard creation
├── visualization.py          # Mind maps and diagrams
├── exporters.py             # Export to various formats
├── templates/               # Jinja2 templates
├── sample_materials/        # Sample textbooks and notes
├── generated_guides/        # Output directory
└── docs/                   # Documentation
```

## Examples

The project includes sample study guides for:

- Mathematics (Calculus)
- Physics (Quantum Mechanics)
- Biology (Cell Biology)
- Computer Science (Data Structures)
- Chemistry (Organic Chemistry)

## API Reference

See `docs/api.md` for detailed API documentation.

## License

MIT License
