import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List
import numpy as np

class AdvancedDashboard:
    """
    Advanced analytics dashboard for truth verification
    """
    
    def create_verdict_gauge(self, confidence: float, verdict: str) -> go.Figure:
        """Create a verdict confidence gauge"""
        if verdict == 'true':
            color = '#00ff9d'
            ranges = [(0, 0.5, 'red'), (0.5, 0.8, 'yellow'), (0.8, 1, 'green')]
        elif verdict == 'false':
            color = '#ff0080'
            ranges = [(0, 0.5, 'red'), (0.5, 0.8, 'yellow'), (0.8, 1, 'red')]
        else:
            color = '#ffff00'
            ranges = [(0, 0.5, 'red'), (0.5, 0.8, 'yellow'), (0.8, 1, 'yellow')]
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=confidence * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"CONFIDENCE: {verdict.upper()}", 'font': {'size': 24}},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': color},
                'steps': [
                    {'range': [r[0]*100, r[1]*100], 'color': r[2]} for r in ranges
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': confidence * 100
                }
            }
        ))
        
        fig.update_layout(height=300, margin=dict(t=50, b=10))
        return fig
    
    def create_model_comparison(self, probabilities: Dict) -> go.Figure:
        """Create model comparison visualization - FIXED VERSION"""
        # Handle case where probabilities might be None or empty
        if not probabilities:
            # Create demo data for empty case
            models = ['deberta', 'roberta', 'electra', 'bert']
            verdicts = ['true', 'false', 'misleading', 'unverifiable']
            
            # Create random probabilities for demo
            data = np.random.dirichlet(np.ones(4), size=4).tolist()
        else:
            # Use actual probabilities with safe access
            models = list(probabilities.keys())
            verdicts = ['true', 'false', 'misleading', 'unverifiable']
            
            data = []
            for verdict in verdicts:
                row = []
                for model in models:
                    # Safe probability access
                    model_probs = probabilities.get(model, {})
                    if isinstance(model_probs, dict):
                        prob_value = model_probs.get(verdict, 0)
                    else:
                        prob_value = 0  # Default if not a dict
                    row.append(prob_value)
                data.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=data,
            x=models,
            y=verdicts,
            colorscale='Viridis',
            hoverongaps=False,
            text=[[f"{val:.3f}" for val in row] for row in data],
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title="Model Probability Distribution",
            xaxis_title="Models",
            yaxis_title="Verdicts",
            height=400
        )
        
        return fig
    
    def create_feature_analysis(self, features: Dict) -> go.Figure:
        """Create feature analysis visualization"""
        if not features:
            # Demo features if none provided
            features = {
                'char_length': 150,
                'word_count': 25,
                'avg_word_length': 6.0,
                'exclamation_count': 1,
                'question_count': 0,
                'uppercase_ratio': 0.1,
                'sensational_score': 2
            }
        
        feature_names = list(features.keys())
        feature_values = list(features.values())
        
        fig = go.Figure(go.Bar(
            x=feature_values,
            y=feature_names,
            orientation='h',
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title="Text Feature Analysis",
            xaxis_title="Feature Value",
            yaxis_title="Features",
            height=400
        )
        
        return fig
    
    def create_timeline_analysis(self, historical_data: List) -> go.Figure:
        """Create timeline analysis of similar claims"""
        # Mock data for demonstration
        dates = pd.date_range('2023-01-01', periods=12, freq='M')
        claims_count = [5, 8, 12, 7, 15, 20, 18, 22, 25, 30, 28, 32]
        accuracy_trend = [0.6, 0.65, 0.7, 0.68, 0.72, 0.75, 0.78, 0.8, 0.82, 0.85, 0.83, 0.87]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Claims count
        fig.add_trace(
            go.Scatter(x=dates, y=claims_count, name="Similar Claims", line=dict(color='blue')),
            secondary_y=False,
        )
        
        # Accuracy trend
        fig.add_trace(
            go.Scatter(x=dates, y=accuracy_trend, name="Accuracy Trend", line=dict(color='green')),
            secondary_y=True,
        )
        
        fig.update_layout(
            title="Historical Analysis of Similar Claims",
            xaxis_title="Date",
            height=400
        )
        
        fig.update_yaxes(title_text="Number of Claims", secondary_y=False)
        fig.update_yaxes(title_text="Accuracy", secondary_y=True)
        
        return fig