"""
Export module for generating study guides in various formats (PDF, HTML, Markdown, etc.)
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import asdict
import markdown
from jinja2 import Environment, FileSystemLoader, Template
from fpdf import FPDF
from datetime import datetime
import base64

class StudyGuideExporter:
    """Exports study guides to various formats."""
    
    def __init__(self, templates_dir: Optional[str] = None):
        self.templates_dir = templates_dir or "templates"
        self.ensure_templates_dir()
        self.setup_jinja_env()
        
    def ensure_templates_dir(self):
        """Ensure templates directory exists and create default templates."""
        os.makedirs(self.templates_dir, exist_ok=True)
        self.create_default_templates()
    
    def setup_jinja_env(self):
        """Set up Jinja2 environment for templates."""
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=True
        )
        # Add nl2br filter for converting newlines to HTML breaks
        self.jinja_env.filters['nl2br'] = lambda text: text.replace('\n', '<br>\n') if text else ''
    
    def create_default_templates(self):
        """Create default HTML and Markdown templates."""
        
        # HTML template
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ study_guide.title }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #2E86AB;
            border-bottom: 2px solid #DDE2E5;
            padding-bottom: 10px;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .metadata {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
        }
        .concept {
            background: #e3f2fd;
            margin: 10px 0;
            padding: 15px;
            border-left: 4px solid #2E86AB;
            border-radius: 5px;
        }
        .question {
            background: #fff3e0;
            margin: 15px 0;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ffcc02;
        }
        .flashcard {
            background: #f3e5f5;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #A23B72;
        }
        .summary {
            background: #e8f5e8;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .chapter {
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        ul, ol {
            padding-left: 25px;
        }
        .badge {
            display: inline-block;
            background: #F18F01;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin: 2px;
        }
        .difficulty-easy { background: #4CAF50; }
        .difficulty-medium { background: #FF9800; }
        .difficulty-hard { background: #F44336; }
        
        @media print {
            body { background: white; }
            .container { box-shadow: none; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ study_guide.title }}</h1>
            <div class="metadata">
                <strong>Subject:</strong> {{ study_guide.subject }} | 
                <strong>Level:</strong> {{ study_guide.level }} | 
                <strong>Generated:</strong> {{ generation_date }}
            </div>
        </div>

        <section>
            <h2>📋 Overview</h2>
            <div class="summary">
                {{ study_guide.summary }}
            </div>
        </section>

        {% if study_guide.key_concepts %}
        <section>
            <h2>🔑 Key Concepts</h2>
            {% for concept in study_guide.key_concepts %}
            <div class="concept">
                {% if concept.name is defined %}
                <h4>{{ concept.name }}</h4>
                <p><strong>Definition:</strong> {{ concept.definition }}</p>
                {% if concept.importance %}
                <p><strong>Why it matters:</strong> {{ concept.importance }}</p>
                {% endif %}
                {% if concept.relationships %}
                <p><strong>Related to:</strong> 
                {% for rel in concept.relationships %}
                <span class="badge">{{ rel }}</span>
                {% endfor %}
                </p>
                {% endif %}
                {% else %}
                <h4>{{ concept }}</h4>
                {% endif %}
            </div>
            {% endfor %}
        </section>
        {% endif %}

        {% if study_guide.chapter_summaries %}
        <section>
            <h2>📚 Chapter Summaries</h2>
            {% for chapter in study_guide.chapter_summaries %}
            <div class="chapter">
                <h3>{{ chapter.title }}</h3>
                <div>{{ chapter.summary | nl2br }}</div>
            </div>
            {% endfor %}
        </section>
        {% endif %}

        {% if study_guide.practice_questions %}
        <section>
            <h2>❓ Practice Questions</h2>
            {% for question in study_guide.practice_questions %}
            <div class="question">
                <h4>Question {{ loop.index }}</h4>
                <p><strong>{{ question.question }}</strong></p>
                {% if question.options %}
                <ul>
                {% for option in question.options %}
                <li>{{ option }}</li>
                {% endfor %}
                </ul>
                {% endif %}
                <p><strong>Answer:</strong> {{ question.correct_answer }}</p>
                {% if question.explanation %}
                <p><em>Explanation:</em> {{ question.explanation }}</p>
                {% endif %}
                <div>
                    <span class="badge difficulty-{{ question.difficulty or 'medium' }}">
                        {{ (question.difficulty or 'medium').title() }}
                    </span>
                    <span class="badge">{{ question.type or 'Question' }}</span>
                </div>
            </div>
            {% endfor %}
        </section>
        {% endif %}

        {% if study_guide.flashcards %}
        <section>
            <h2>📝 Flashcards</h2>
            {% for flashcard in study_guide.flashcards %}
            <div class="flashcard">
                <h4>Card {{ loop.index }}</h4>
                <p><strong>Front:</strong> {{ flashcard.front }}</p>
                <p><strong>Back:</strong> {{ flashcard.back }}</p>
                {% if flashcard.tags %}
                <div>
                {% for tag in flashcard.tags %}
                <span class="badge">{{ tag }}</span>
                {% endfor %}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </section>
        {% endif %}

        <footer style="margin-top: 40px; text-align: center; color: #666; font-size: 0.9em;">
            Generated by LangChain Study Guide Creator
        </footer>
    </div>
</body>
</html>
        """
        
        # Markdown template
        markdown_template = """# {{ study_guide.title }}

**Subject:** {{ study_guide.subject }}  
**Level:** {{ study_guide.level }}  
**Generated:** {{ generation_date }}

---

## 📋 Overview

{{ study_guide.summary }}

{% if study_guide.key_concepts %}
## 🔑 Key Concepts

{% for concept in study_guide.key_concepts %}
{% if concept.name is defined %}
### {{ concept.name }}

**Definition:** {{ concept.definition }}

{% if concept.importance %}
**Why it matters:** {{ concept.importance }}
{% endif %}

{% if concept.relationships %}
**Related concepts:** {{ concept.relationships | join(', ') }}
{% endif %}

{% else %}
### {{ concept }}

{% endif %}
{% endfor %}
{% endif %}

{% if study_guide.chapter_summaries %}
## 📚 Chapter Summaries

{% for chapter in study_guide.chapter_summaries %}
### {{ chapter.title }}

{{ chapter.summary }}

{% endfor %}
{% endif %}

{% if study_guide.practice_questions %}
## ❓ Practice Questions

{% for question in study_guide.practice_questions %}
### Question {{ loop.index }}

**{{ question.question }}**

{% if question.options %}
{% for option in question.options %}
- {{ option }}
{% endfor %}
{% endif %}

**Answer:** {{ question.correct_answer }}

{% if question.explanation %}
*Explanation:* {{ question.explanation }}
{% endif %}

*Difficulty:* {{ question.difficulty or 'medium' }} | *Type:* {{ question.type or 'Question' }}

---

{% endfor %}
{% endif %}

{% if study_guide.flashcards %}
## 📝 Flashcards

{% for flashcard in study_guide.flashcards %}
### Card {{ loop.index }}

**Front:** {{ flashcard.front }}

**Back:** {{ flashcard.back }}

{% if flashcard.tags %}
*Tags:* {{ flashcard.tags | join(', ') }}
{% endif %}

---

{% endfor %}
{% endif %}

---
*Generated by LangChain Study Guide Creator*
        """
        
        # Save templates
        with open(os.path.join(self.templates_dir, "study_guide.html"), "w", encoding='utf-8') as f:
            f.write(html_template)
            
        with open(os.path.join(self.templates_dir, "study_guide.md"), "w", encoding='utf-8') as f:
            f.write(markdown_template)
    
    def export_to_html(self, study_guide, output_path: str) -> str:
        """Export study guide to HTML format."""
        template = self.jinja_env.get_template("study_guide.html")
        
        # Add custom filter for line breaks
        def nl2br(value):
            return value.replace('\n', '<br>')
        
        self.jinja_env.filters['nl2br'] = nl2br
        
        html_content = template.render(
            study_guide=study_guide,
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def export_to_markdown(self, study_guide, output_path: str) -> str:
        """Export study guide to Markdown format."""
        template = self.jinja_env.get_template("study_guide.md")
        
        markdown_content = template.render(
            study_guide=study_guide,
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return output_path
    
    def export_to_pdf(self, study_guide, output_path: str) -> str:
        """Export study guide to PDF format."""
        
        class StudyGuidePDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 16)
                self.cell(0, 10, study_guide.title, 0, 1, 'C')
                self.ln(5)
            
            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()} - Generated by LangChain Study Guide Creator', 0, 0, 'C')
        
        pdf = StudyGuidePDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)
        
        # Title and metadata
        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 15, study_guide.title, 0, 1, 'C')
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"Subject: {study_guide.subject} | Level: {study_guide.level}", 0, 1, 'C')
        pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'C')
        pdf.ln(10)
        
        # Overview
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, "Overview", 0, 1)
        pdf.set_font('Arial', '', 11)
        
        # Split text into lines that fit the page width
        summary_lines = self._wrap_text(study_guide.summary, 80)
        for line in summary_lines:
            pdf.cell(0, 6, line.encode('latin-1', 'ignore').decode('latin-1'), 0, 1)
        pdf.ln(5)
        
        # Key Concepts
        if study_guide.key_concepts:
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, "Key Concepts", 0, 1)
            pdf.set_font('Arial', '', 11)
            
            for i, concept in enumerate(study_guide.key_concepts[:10]):  # Limit for PDF
                if isinstance(concept, dict):
                    pdf.set_font('Arial', 'B', 12)
                    pdf.cell(0, 8, f"{i+1}. {concept.get('name', '')}", 0, 1)
                    pdf.set_font('Arial', '', 11)
                    
                    definition = concept.get('definition', '')
                    def_lines = self._wrap_text(definition, 80)
                    for line in def_lines:
                        pdf.cell(0, 6, f"   {line}".encode('latin-1', 'ignore').decode('latin-1'), 0, 1)
                else:
                    pdf.set_font('Arial', 'B', 12)
                    pdf.cell(0, 8, f"{i+1}. {str(concept)}", 0, 1)
                pdf.ln(3)
        
        # Practice Questions
        if study_guide.practice_questions:
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, "Practice Questions", 0, 1)
            
            for i, question in enumerate(study_guide.practice_questions[:5]):  # Limit for PDF
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 8, f"Question {i+1}:", 0, 1)
                pdf.set_font('Arial', '', 11)
                
                # Question text
                q_lines = self._wrap_text(question.get('question', ''), 75)
                for line in q_lines:
                    pdf.cell(0, 6, line.encode('latin-1', 'ignore').decode('latin-1'), 0, 1)
                
                # Options
                if question.get('options'):
                    for option in question['options']:
                        opt_lines = self._wrap_text(option, 70)
                        for line in opt_lines:
                            pdf.cell(0, 6, f"  {line}".encode('latin-1', 'ignore').decode('latin-1'), 0, 1)
                
                # Answer
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(0, 6, f"Answer: {question.get('correct_answer', '')}", 0, 1)
                pdf.set_font('Arial', '', 11)
                pdf.ln(5)
        
        pdf.output(output_path)
        return output_path
    
    def export_to_json(self, study_guide, output_path: str) -> str:
        """Export study guide to JSON format."""
        # Convert dataclass to dict if needed
        if hasattr(study_guide, '__dict__'):
            guide_dict = asdict(study_guide) if hasattr(study_guide, '__dataclass_fields__') else study_guide.__dict__
        else:
            guide_dict = study_guide
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(guide_dict, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def export_flashcards_to_anki(self, study_guide, output_path: str) -> str:
        """Export flashcards to Anki-compatible format."""
        if not study_guide.flashcards:
            raise ValueError("No flashcards available to export")
        
        # Create Anki-compatible CSV format
        lines = []
        for flashcard in study_guide.flashcards:
            front = flashcard.get('front', '').replace('\n', '<br>').replace('"', '""')
            back = flashcard.get('back', '').replace('\n', '<br>').replace('"', '""')
            tags = ';'.join(flashcard.get('tags', []))
            
            lines.append(f'"{front}","{back}","{tags}"')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("Front,Back,Tags\n")
            f.write('\n'.join(lines))
        
        return output_path
    
    def export_quiz_to_json(self, quiz, output_path: str) -> str:
        """Export quiz to JSON format."""
        # Convert quiz object to dict
        if hasattr(quiz, '__dict__'):
            quiz_dict = asdict(quiz) if hasattr(quiz, '__dataclass_fields__') else quiz.__dict__
        else:
            quiz_dict = quiz
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(quiz_dict, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def create_study_package(self, study_guide, quiz=None, output_dir: str = "study_package") -> str:
        """Create a complete study package with multiple formats."""
        os.makedirs(output_dir, exist_ok=True)
        
        base_name = study_guide.title.replace(' ', '_').lower()
        
        # Export study guide in multiple formats
        html_path = self.export_to_html(study_guide, os.path.join(output_dir, f"{base_name}.html"))
        md_path = self.export_to_markdown(study_guide, os.path.join(output_dir, f"{base_name}.md"))
        pdf_path = self.export_to_pdf(study_guide, os.path.join(output_dir, f"{base_name}.pdf"))
        json_path = self.export_to_json(study_guide, os.path.join(output_dir, f"{base_name}.json"))
        
        # Export flashcards if available
        if study_guide.flashcards:
            anki_path = self.export_flashcards_to_anki(
                study_guide, os.path.join(output_dir, f"{base_name}_flashcards.csv")
            )
        
        # Export quiz if provided
        if quiz:
            quiz_path = self.export_quiz_to_json(
                quiz, os.path.join(output_dir, f"{base_name}_quiz.json")
            )
        
        # Create README
        readme_content = f"""# {study_guide.title} - Study Package

This package contains comprehensive study materials for {study_guide.subject}.

## Contents

- `{base_name}.html` - Interactive HTML study guide
- `{base_name}.md` - Markdown version for easy editing
- `{base_name}.pdf` - Printable PDF version
- `{base_name}.json` - Machine-readable data format
"""
        
        if study_guide.flashcards:
            readme_content += f"- `{base_name}_flashcards.csv` - Flashcards for Anki import\n"
        
        if quiz:
            readme_content += f"- `{base_name}_quiz.json` - Interactive quiz questions\n"
        
        readme_content += f"""
## Usage

1. **For studying:** Open the HTML file in your browser
2. **For printing:** Use the PDF version
3. **For editing:** Use the Markdown version
4. **For flashcards:** Import the CSV file into Anki
5. **For quizzes:** Use the quiz JSON with compatible applications

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        
        with open(os.path.join(output_dir, "README.md"), 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return output_dir
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Wrap text to specified width for PDF generation."""
        import textwrap
        return textwrap.wrap(text, width=width)
