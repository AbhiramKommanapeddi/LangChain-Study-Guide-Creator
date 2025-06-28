"""
Visualization module for creating mind maps, word clouds, and educational diagrams.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import networkx as nx
import numpy as np
from wordcloud import WordCloud
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import List, Dict, Tuple, Optional
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import textwrap
import colorsys

class EducationalVisualizer:
    """Creates various educational visualizations and diagrams."""
    
    def __init__(self):
        self.color_scheme = {
            'primary': '#2E86AB',
            'secondary': '#A23B72', 
            'accent': '#F18F01',
            'background': '#F5F5F5',
            'text': '#2D3436',
            'light': '#DDE2E5'
        }
        
        # Set matplotlib style
        plt.style.use('default')
        plt.rcParams['font.family'] = 'Arial'
        plt.rcParams['font.size'] = 10
    
    def create_concept_map(self, concepts: List[Dict], 
                          title: str = "Concept Map",
                          save_path: Optional[str] = None) -> str:
        """
        Create a visual concept map showing relationships between concepts.
        
        Args:
            concepts: List of concept dictionaries with names and relationships
            title: Title for the concept map
            save_path: Optional path to save the image
            
        Returns:
            Path to the generated image or base64 encoded image
        """
        
        # Create networkx graph
        G = nx.Graph()
        
        # Add nodes (concepts)
        for concept in concepts:
            concept_name = concept.get('name', '') if isinstance(concept, dict) else str(concept)
            if concept_name:
                G.add_node(concept_name)
        
        # Add edges (relationships)
        for concept in concepts:
            if isinstance(concept, dict):
                concept_name = concept.get('name', '')
                relationships = concept.get('relationships', [])
                for related in relationships:
                    if related in [c.get('name', '') if isinstance(c, dict) else str(c) for c in concepts]:
                        G.add_edge(concept_name, related)
        
        # If no relationships found, create a hub layout
        if G.number_of_edges() == 0 and len(concepts) > 1:
            main_concept = concepts[0].get('name', '') if isinstance(concepts[0], dict) else str(concepts[0])
            for concept in concepts[1:]:
                concept_name = concept.get('name', '') if isinstance(concept, dict) else str(concept)
                if concept_name:
                    G.add_edge(main_concept, concept_name)
        
        # Create the visualization
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        fig.patch.set_facecolor(self.color_scheme['background'])
        ax.set_facecolor(self.color_scheme['background'])
        
        # Position nodes
        if G.number_of_nodes() > 0:
            if G.number_of_edges() > 0:
                pos = nx.spring_layout(G, k=3, iterations=50)
            else:
                # Single node - center it
                pos = {list(G.nodes())[0]: (0, 0)}
        else:
            pos = {}
        
        # Draw edges
        if G.number_of_edges() > 0:
            nx.draw_networkx_edges(G, pos, edge_color=self.color_scheme['light'], 
                                 width=2, alpha=0.6, ax=ax)
        
        # Draw nodes
        if G.number_of_nodes() > 0:
            node_sizes = [3000 + len(node) * 100 for node in G.nodes()]
            nx.draw_networkx_nodes(G, pos, node_color=self.color_scheme['primary'],
                                 node_size=node_sizes, alpha=0.8, ax=ax)
            
            # Draw labels with text wrapping
            labels = {}
            for node in G.nodes():
                wrapped_text = '\n'.join(textwrap.wrap(node, 15))
                labels[node] = wrapped_text
            
            nx.draw_networkx_labels(G, pos, labels, font_size=9, 
                                  font_color='white', font_weight='bold', ax=ax)
        
        ax.set_title(title, fontsize=16, fontweight='bold', 
                    color=self.color_scheme['text'], pad=20)
        ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor=self.color_scheme['background'])
            plt.close()
            return save_path
        else:
            # Return base64 encoded image
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                       facecolor=self.color_scheme['background'])
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            return f"data:image/png;base64,{image_base64}"
    
    def create_word_cloud(self, text: str, 
                         title: str = "Key Terms",
                         save_path: Optional[str] = None) -> str:
        """
        Create a word cloud from text content.
        
        Args:
            text: Text content to generate word cloud from
            title: Title for the word cloud
            save_path: Optional path to save the image
            
        Returns:
            Path to the generated image or base64 encoded image
        """
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=800, 
            height=400,
            background_color=self.color_scheme['background'],
            colormap='viridis',
            max_words=50,
            relative_scaling=0.5,
            min_font_size=10
        ).generate(text)
        
        # Create plot
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        fig.patch.set_facecolor(self.color_scheme['background'])
        
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_title(title, fontsize=16, fontweight='bold', 
                    color=self.color_scheme['text'], pad=20)
        ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight',
                       facecolor=self.color_scheme['background'])
            plt.close()
            return save_path
        else:
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                       facecolor=self.color_scheme['background'])
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            return f"data:image/png;base64,{image_base64}"
    
    def create_timeline_diagram(self, events: List[Dict],
                              title: str = "Timeline",
                              save_path: Optional[str] = None) -> str:
        """
        Create a timeline diagram for historical or process events.
        
        Args:
            events: List of event dictionaries with 'name', 'date', 'description'
            title: Title for the timeline
            save_path: Optional path to save the image
            
        Returns:
            Path to the generated image or base64 encoded image
        """
        
        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        fig.patch.set_facecolor(self.color_scheme['background'])
        ax.set_facecolor(self.color_scheme['background'])
        
        if not events:
            events = [{"name": "Start", "date": "Beginning", "description": "Timeline start"}]
        
        y_pos = 0.5
        x_positions = np.linspace(0.1, 0.9, len(events))
        
        # Draw timeline line
        ax.plot([0.05, 0.95], [y_pos, y_pos], color=self.color_scheme['primary'], 
               linewidth=3, alpha=0.7)
        
        # Add events
        for i, (event, x_pos) in enumerate(zip(events, x_positions)):
            # Event marker
            ax.scatter(x_pos, y_pos, s=200, color=self.color_scheme['accent'], 
                      zorder=5, edgecolors=self.color_scheme['primary'], linewidth=2)
            
            # Event details
            event_name = event.get('name', f'Event {i+1}')
            event_date = event.get('date', '')
            event_desc = event.get('description', '')
            
            # Alternate text position (above/below)
            text_y = y_pos + 0.15 if i % 2 == 0 else y_pos - 0.15
            
            # Event name
            ax.text(x_pos, text_y, event_name, ha='center', va='center',
                   fontsize=11, fontweight='bold', color=self.color_scheme['text'],
                   bbox=dict(boxstyle="round,pad=0.3", facecolor=self.color_scheme['light'], 
                           edgecolor=self.color_scheme['primary'], alpha=0.8))
            
            # Date
            if event_date:
                date_y = text_y + 0.08 if i % 2 == 0 else text_y - 0.08
                ax.text(x_pos, date_y, event_date, ha='center', va='center',
                       fontsize=9, color=self.color_scheme['text'], style='italic')
            
            # Connection line
            line_y = y_pos + 0.05 if i % 2 == 0 else y_pos - 0.05
            ax.plot([x_pos, x_pos], [y_pos, line_y], color=self.color_scheme['primary'], 
                   linewidth=2, alpha=0.7)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(title, fontsize=16, fontweight='bold', 
                    color=self.color_scheme['text'], pad=20)
        ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight',
                       facecolor=self.color_scheme['background'])
            plt.close()
            return save_path
        else:
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                       facecolor=self.color_scheme['background'])
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            return f"data:image/png;base64,{image_base64}"
    
    def create_flowchart(self, steps: List[str],
                        title: str = "Process Flow",
                        save_path: Optional[str] = None) -> str:
        """
        Create a flowchart diagram for processes or procedures.
        
        Args:
            steps: List of step descriptions
            title: Title for the flowchart
            save_path: Optional path to save the image
            
        Returns:
            Path to the generated image or base64 encoded image
        """
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        fig.patch.set_facecolor(self.color_scheme['background'])
        ax.set_facecolor(self.color_scheme['background'])
        
        if not steps:
            steps = ["Step 1", "Step 2", "Step 3"]
        
        # Calculate positions
        num_steps = len(steps)
        y_positions = np.linspace(0.9, 0.1, num_steps)
        x_center = 0.5
        
        # Draw steps
        for i, (step, y_pos) in enumerate(zip(steps, y_positions)):
            # Step box
            box = FancyBboxPatch((x_center - 0.2, y_pos - 0.05), 0.4, 0.08,
                               boxstyle="round,pad=0.01",
                               facecolor=self.color_scheme['primary'],
                               edgecolor=self.color_scheme['text'],
                               linewidth=2)
            ax.add_patch(box)
            
            # Step text
            wrapped_step = '\n'.join(textwrap.wrap(step, 30))
            ax.text(x_center, y_pos, wrapped_step, ha='center', va='center',
                   fontsize=10, color='white', fontweight='bold')
            
            # Arrow to next step
            if i < num_steps - 1:
                arrow_start_y = y_pos - 0.05
                arrow_end_y = y_positions[i + 1] + 0.05
                ax.annotate('', xy=(x_center, arrow_end_y), xytext=(x_center, arrow_start_y),
                           arrowprops=dict(arrowstyle='->', lw=2, 
                                         color=self.color_scheme['accent']))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(title, fontsize=16, fontweight='bold',
                    color=self.color_scheme['text'], pad=20)
        ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight',
                       facecolor=self.color_scheme['background'])
            plt.close()
            return save_path
        else:
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                       facecolor=self.color_scheme['background'])
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            return f"data:image/png;base64,{image_base64}"
    
    def create_interactive_concept_map(self, concepts: List[Dict], 
                                     title: str = "Interactive Concept Map") -> str:
        """
        Create an interactive concept map using Plotly.
        
        Args:
            concepts: List of concept dictionaries
            title: Title for the concept map
            
        Returns:
            HTML string of the interactive plot
        """
        
        # Create graph structure
        nodes = []
        edges = []
        
        for i, concept in enumerate(concepts):
            concept_name = concept.get('name', '') if isinstance(concept, dict) else str(concept)
            concept_def = concept.get('definition', '') if isinstance(concept, dict) else ''
            
            nodes.append({
                'id': i,
                'name': concept_name,
                'definition': concept_def,
                'size': len(concept_name) + 20
            })
            
            # Add relationships as edges
            if isinstance(concept, dict):
                relationships = concept.get('relationships', [])
                for related in relationships:
                    related_idx = None
                    for j, other_concept in enumerate(concepts):
                        other_name = other_concept.get('name', '') if isinstance(other_concept, dict) else str(other_concept)
                        if other_name == related:
                            related_idx = j
                            break
                    
                    if related_idx is not None:
                        edges.append({'source': i, 'target': related_idx})
        
        # Generate positions using a simple circular layout
        n = len(nodes)
        positions = []
        for i in range(n):
            angle = 2 * np.pi * i / n
            x = np.cos(angle)
            y = np.sin(angle)
            positions.append((x, y))
        
        # Create traces for edges
        edge_trace = go.Scatter(x=[], y=[], line=dict(width=2, color='#888'), 
                              hoverinfo='none', mode='lines')
        
        for edge in edges:
            x0, y0 = positions[edge['source']]
            x1, y1 = positions[edge['target']]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])
        
        # Create trace for nodes
        node_trace = go.Scatter(x=[], y=[], mode='markers+text',
                              hoverinfo='text', text=[], textposition="middle center",
                              marker=dict(size=[], color=[], line=dict(width=2)))
        
        for i, node in enumerate(nodes):
            x, y = positions[i]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
            node_trace['text'] += tuple([node['name']])
            node_trace['marker']['size'] += tuple([node['size']])
            node_trace['marker']['color'] += tuple([self.color_scheme['primary']])
        
        # Create hover text
        hover_text = []
        for node in nodes:
            hover_text.append(f"<b>{node['name']}</b><br>{node['definition']}")
        node_trace['hovertext'] = hover_text
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(title=title,
                                       titlefont_size=16,
                                       showlegend=False,
                                       hovermode='closest',
                                       margin=dict(b=20,l=5,r=5,t=40),
                                       annotations=[dict(text="", showarrow=False,
                                                        xref="paper", yref="paper",
                                                        x=0.005, y=-0.002,
                                                        xanchor='left', yanchor='bottom',
                                                        font=dict(color="black", size=12))],
                                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
        
        return fig.to_html(include_plotlyjs=True, div_id="concept-map")
    
    def create_progress_chart(self, quiz_results: List[Dict],
                            title: str = "Learning Progress",
                            save_path: Optional[str] = None) -> str:
        """
        Create a progress chart showing quiz performance over time.
        
        Args:
            quiz_results: List of quiz result dictionaries
            title: Title for the chart
            save_path: Optional path to save the image
            
        Returns:
            Path to the generated image or base64 encoded image
        """
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.patch.set_facecolor(self.color_scheme['background'])
        
        if not quiz_results:
            quiz_results = [
                {"quiz_title": "Quiz 1", "percentage": 60, "date": "2024-01-01"},
                {"quiz_title": "Quiz 2", "percentage": 75, "date": "2024-01-08"},
                {"quiz_title": "Quiz 3", "percentage": 85, "date": "2024-01-15"}
            ]
        
        # Extract data
        quiz_names = [result.get('quiz_title', f'Quiz {i+1}') for i, result in enumerate(quiz_results)]
        scores = [result.get('percentage', 0) for result in quiz_results]
        
        # Progress line chart
        ax1.plot(range(len(scores)), scores, marker='o', linewidth=3, 
                markersize=8, color=self.color_scheme['primary'])
        ax1.fill_between(range(len(scores)), scores, alpha=0.3, color=self.color_scheme['primary'])
        ax1.set_ylabel('Score (%)', fontsize=12, color=self.color_scheme['text'])
        ax1.set_title('Score Progression', fontsize=14, fontweight='bold', 
                     color=self.color_scheme['text'])
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 100)
        ax1.set_xticks(range(len(quiz_names)))
        ax1.set_xticklabels(quiz_names, rotation=45, ha='right')
        
        # Add target line at 80%
        ax1.axhline(y=80, color=self.color_scheme['accent'], linestyle='--', 
                   alpha=0.7, label='Target (80%)')
        ax1.legend()
        
        # Score distribution bar chart
        colors = [self.color_scheme['accent'] if score >= 80 else 
                 self.color_scheme['primary'] if score >= 70 else 
                 self.color_scheme['secondary'] for score in scores]
        
        bars = ax2.bar(range(len(scores)), scores, color=colors, alpha=0.8, 
                      edgecolor=self.color_scheme['text'], linewidth=1)
        ax2.set_ylabel('Score (%)', fontsize=12, color=self.color_scheme['text'])
        ax2.set_title('Individual Quiz Scores', fontsize=14, fontweight='bold',
                     color=self.color_scheme['text'])
        ax2.set_ylim(0, 100)
        ax2.set_xticks(range(len(quiz_names)))
        ax2.set_xticklabels(quiz_names, rotation=45, ha='right')
        
        # Add score labels on bars
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{score:.1f}%', ha='center', va='bottom', 
                    color=self.color_scheme['text'], fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight',
                       facecolor=self.color_scheme['background'])
            plt.close()
            return save_path
        else:
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                       facecolor=self.color_scheme['background'])
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            return f"data:image/png;base64,{image_base64}"
