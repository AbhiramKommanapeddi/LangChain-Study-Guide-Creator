# API Documentation

## StudyGuideCreator Class

The main class for creating comprehensive study guides from educational materials.

### Constructor

```python
StudyGuideCreator(openai_api_key: Optional[str] = None)
```

**Parameters:**

- `openai_api_key`: OpenAI API key for enhanced AI features (optional)

**Example:**

```python
from study_guide_creator import StudyGuideCreator

# Basic usage (no API key)
creator = StudyGuideCreator()

# With API key for enhanced features
creator = StudyGuideCreator(api_key="your_openai_key")
```

### Methods

#### create_study_guide()

Creates a complete study guide from a document.

```python
create_study_guide(request: StudyGuideRequest) -> Dict[str, Any]
```

**Parameters:**

- `request`: StudyGuideRequest configuration object

**Returns:**

- Dictionary containing:
  - `study_guide`: Generated StudyGuide object
  - `quiz`: Generated Quiz object (if requested)
  - `exported_files`: Dictionary of exported file paths
  - `visual_files`: Dictionary of visualization file paths
  - `package_directory`: Path to complete study package
  - `success`: Boolean indicating success

**Example:**

```python
from study_guide_creator import StudyGuideRequest

request = StudyGuideRequest(
    input_file="textbook.pdf",
    subject="Mathematics",
    level="undergraduate",
    include_quiz=True,
    export_formats=["html", "pdf"]
)

result = creator.create_study_guide(request)
```

#### create_from_text()

Creates a study guide directly from text content.

```python
create_from_text(text: str, subject: str, level: str = "undergraduate") -> Dict[str, Any]
```

**Parameters:**

- `text`: Text content to process
- `subject`: Subject area
- `level`: Education level (default: "undergraduate")

**Returns:**

- Same as `create_study_guide()`

**Example:**

```python
text = "Calculus is the mathematical study of continuous change..."
result = creator.create_from_text(text, "Mathematics", "high_school")
```

## StudyGuideRequest Class

Configuration object for study guide generation.

### Constructor

```python
StudyGuideRequest(
    input_file: str,
    subject: str,
    level: str = "undergraduate",
    title: Optional[str] = None,
    include_quiz: bool = True,
    include_visuals: bool = True,
    export_formats: List[str] = None,
    output_dir: str = "generated_guides"
)
```

**Parameters:**

- `input_file`: Path to input document
- `subject`: Subject area (e.g., "Mathematics", "Physics")
- `level`: Education level ("high_school", "undergraduate", "graduate", "professional")
- `title`: Custom title (optional)
- `include_quiz`: Whether to generate quiz
- `include_visuals`: Whether to generate visualizations
- `export_formats`: List of export formats
- `output_dir`: Output directory

## StudyGuide Class

Container for a complete study guide.

### Attributes

- `title`: Study guide title
- `subject`: Subject area
- `level`: Education level
- `summary`: Overall summary
- `key_concepts`: List of key concepts
- `chapter_summaries`: List of chapter summaries
- `practice_questions`: List of practice questions
- `flashcards`: List of flashcards
- `visual_aids`: List of visual aids
- `metadata`: Additional metadata

### Example Usage

```python
# Access study guide content
study_guide = result["study_guide"]

print(f"Title: {study_guide.title}")
print(f"Subject: {study_guide.subject}")
print(f"Concepts: {len(study_guide.key_concepts)}")

# Iterate through concepts
for concept in study_guide.key_concepts:
    if isinstance(concept, dict):
        print(f"- {concept['name']}: {concept['definition']}")
    else:
        print(f"- {concept}")
```

## QuizGenerator Class

Generates interactive quizzes and assessments.

### Constructor

```python
QuizGenerator(api_key: Optional[str] = None)
```

### Methods

#### create_quiz_from_study_guide()

```python
create_quiz_from_study_guide(
    study_guide,
    difficulty: str = "medium",
    num_questions: int = 10,
    time_limit: Optional[int] = None,
    question_types: Optional[List[str]] = None
) -> Quiz
```

**Parameters:**

- `study_guide`: StudyGuide object
- `difficulty`: Quiz difficulty ("easy", "medium", "hard")
- `num_questions`: Number of questions
- `time_limit`: Time limit in minutes
- `question_types`: Types of questions to include

#### create_adaptive_quiz()

```python
create_adaptive_quiz(
    subject: str,
    previous_results: List[QuizResult],
    num_questions: int = 5
) -> Quiz
```

**Parameters:**

- `subject`: Subject area
- `previous_results`: List of previous quiz results
- `num_questions`: Number of questions

#### evaluate_quiz()

```python
evaluate_quiz(
    quiz: Quiz,
    answers: Dict[int, str],
    time_taken: Optional[int] = None
) -> QuizResult
```

**Parameters:**

- `quiz`: Quiz object
- `answers`: Dictionary mapping question IDs to answers
- `time_taken`: Time taken in seconds

## EducationalVisualizer Class

Creates educational visualizations and diagrams.

### Methods

#### create_concept_map()

```python
create_concept_map(
    concepts: List[Dict],
    title: str = "Concept Map",
    save_path: Optional[str] = None
) -> str
```

**Parameters:**

- `concepts`: List of concept dictionaries
- `title`: Title for the map
- `save_path`: Path to save image

**Returns:**

- Path to saved image or base64 encoded image

#### create_word_cloud()

```python
create_word_cloud(
    text: str,
    title: str = "Key Terms",
    save_path: Optional[str] = None
) -> str
```

#### create_timeline_diagram()

```python
create_timeline_diagram(
    events: List[Dict],
    title: str = "Timeline",
    save_path: Optional[str] = None
) -> str
```

#### create_flowchart()

```python
create_flowchart(
    steps: List[str],
    title: str = "Process Flow",
    save_path: Optional[str] = None
) -> str
```

## StudyGuideExporter Class

Exports study guides to various formats.

### Methods

#### export_to_html()

```python
export_to_html(study_guide, output_path: str) -> str
```

#### export_to_pdf()

```python
export_to_pdf(study_guide, output_path: str) -> str
```

#### export_to_markdown()

```python
export_to_markdown(study_guide, output_path: str) -> str
```

#### export_to_json()

```python
export_to_json(study_guide, output_path: str) -> str
```

#### export_flashcards_to_anki()

```python
export_flashcards_to_anki(study_guide, output_path: str) -> str
```

#### create_study_package()

```python
create_study_package(
    study_guide,
    quiz=None,
    output_dir: str = "study_package"
) -> str
```

## Error Handling

All methods include error handling and will gracefully degrade when certain features are unavailable:

```python
try:
    result = creator.create_study_guide(request)
    if result["success"]:
        print("Study guide created successfully!")
    else:
        print("Failed to create study guide")
except Exception as e:
    print(f"Error: {e}")
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for enhanced features
- `LANGCHAIN_TRACING_V2`: Enable LangChain tracing
- `LANGCHAIN_API_KEY`: LangChain API key for tracing

### File Support

Supported input formats:

- **PDF**: `.pdf` files
- **Word**: `.docx`, `.doc` files
- **Text**: `.txt` files

### Export Formats

Available export formats:

- **HTML**: Interactive web format
- **PDF**: Printable format
- **Markdown**: Editable text format
- **JSON**: Machine-readable format
- **Anki**: Flashcard import format

## Examples

### Complete Workflow

```python
from study_guide_creator import StudyGuideCreator, StudyGuideRequest

# Initialize creator
creator = StudyGuideCreator(api_key="your_key")

# Create request
request = StudyGuideRequest(
    input_file="physics_textbook.pdf",
    subject="Physics",
    level="undergraduate",
    title="Quantum Mechanics Study Guide",
    include_quiz=True,
    include_visuals=True,
    export_formats=["html", "pdf", "anki"]
)

# Generate study guide
result = creator.create_study_guide(request)

if result["success"]:
    study_guide = result["study_guide"]
    quiz = result["quiz"]

    print(f"Created: {study_guide.title}")
    print(f"Concepts: {len(study_guide.key_concepts)}")
    print(f"Questions: {len(quiz.questions)}")
    print(f"Package: {result['package_directory']}")
```

### Quiz Taking

```python
from quiz_generator import QuizGenerator

# Take quiz
quiz = result["quiz"]
answers = {
    1: "A",
    2: "True",
    3: "The speed of light"
}

quiz_gen = QuizGenerator()
quiz_result = quiz_gen.evaluate_quiz(quiz, answers)

print(f"Score: {quiz_result.percentage}%")
for rec in quiz_result.recommendations:
    print(f"- {rec}")
```

### Custom Visualizations

```python
from visualization import EducationalVisualizer

visualizer = EducationalVisualizer()

# Create concept map
concepts = [
    {"name": "Force", "definition": "Push or pull", "relationships": ["Motion"]},
    {"name": "Motion", "definition": "Change in position", "relationships": ["Force"]}
]

concept_map = visualizer.create_concept_map(
    concepts,
    title="Physics Concepts",
    save_path="physics_map.png"
)
```
