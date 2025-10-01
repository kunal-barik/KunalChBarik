import numpy as np
from typing import Dict, List
import logging

class ExplainableAI:
    """
    Advanced Explainable AI system for model interpretability
    """
    
    def __init__(self):
        self.feature_descriptions = {
            'char_length': 'Total character count in the text',
            'word_count': 'Total number of words',
            'avg_word_length': 'Average length of words',
            'exclamation_count': 'Number of exclamation marks',
            'question_count': 'Number of question marks', 
            'uppercase_ratio': 'Percentage of uppercase letters',
            'sensational_score': 'Count of sensational words'
        }
    
    def generate_explanation(self, prediction_result, text: str) -> Dict:
        """Generate comprehensive explanation for the prediction"""
        
        explanation = {
            'verdict_explanation': self._explain_verdict(prediction_result.verdict, prediction_result.confidence),
            'confidence_breakdown': self._explain_confidence(prediction_result.confidence, prediction_result.features),
            'feature_analysis': self._analyze_features(prediction_result.features),
            'key_factors': self._identify_key_factors(prediction_result.features),
            'recommendations': self._generate_recommendations(prediction_result),
            'counterfactuals': self._generate_counterfactuals(text, prediction_result.verdict)
        }
        
        return explanation
    
    def _explain_verdict(self, verdict: str, confidence: float) -> str:
        """Explain the verdict in natural language"""
        confidence_level = "high" if confidence > 0.8 else "medium" if confidence > 0.6 else "low"
        
        explanations = {
            'true': f"The statement appears to be factually accurate with {confidence_level} confidence.",
            'false': f"The statement contains factual inaccuracies with {confidence_level} confidence.",
            'misleading': f"The statement is partially true but contains misleading elements with {confidence_level} confidence.",
            'unverifiable': f"The statement cannot be reliably verified with available information."
        }
        
        return explanations.get(verdict, "Unable to determine statement veracity.")
    
    def _explain_confidence(self, confidence: float, features: Dict) -> List[str]:
        """Explain factors affecting confidence"""
        factors = []
        
        if features.get('word_count', 0) < 10:
            factors.append("Low confidence due to very short text length")
        
        if features.get('sensational_score', 0) > 3:
            factors.append("Reduced confidence due to sensational language")
        
        if features.get('exclamation_count', 0) > 2:
            factors.append("Multiple exclamation marks may indicate emotional bias")
        
        if features.get('uppercase_ratio', 0) > 0.3:
            factors.append("High uppercase ratio may indicate sensationalism")
        
        if confidence > 0.8:
            factors.append("High confidence due to clear linguistic patterns")
        elif confidence < 0.5:
            factors.append("Low confidence suggests ambiguous or contradictory information")
        
        return factors
    
    def _analyze_features(self, features: Dict) -> List[Dict]:
        """Analyze and explain each feature"""
        analysis = []
        
        for feature, value in features.items():
            description = self.feature_descriptions.get(feature, 'Unknown feature')
            
            # Provide interpretation
            if feature == 'sensational_score':
                interpretation = "High" if value > 2 else "Medium" if value > 1 else "Low"
                interpretation += " sensational language detected"
            elif feature == 'word_count':
                interpretation = "Too short" if value < 15 else "Adequate" if value < 100 else "Very detailed"
            elif feature == 'uppercase_ratio':
                interpretation = "Normal" if value < 0.1 else "Elevated" if value < 0.3 else "Very high"
            else:
                interpretation = "Within normal range"
            
            analysis.append({
                'feature': feature,
                'value': value,
                'description': description,
                'interpretation': interpretation
            })
        
        return analysis
    
    def _identify_key_factors(self, features: Dict) -> List[str]:
        """Identify the most influential factors in the decision"""
        key_factors = []
        
        # Define thresholds for key factors
        if features.get('sensational_score', 0) >= 2:
            key_factors.append("Sensational language usage")
        
        if features.get('exclamation_count', 0) >= 2:
            key_factors.append("Multiple exclamation marks")
        
        if features.get('word_count', 0) < 10:
            key_factors.append("Very short statement length")
        
        if features.get('uppercase_ratio', 0) > 0.2:
            key_factors.append("High uppercase letter ratio")
        
        return key_factors if key_factors else ["Standard linguistic patterns"]
    
    def _generate_recommendations(self, prediction_result) -> List[str]:
        """Generate recommendations based on the analysis"""
        recommendations = []
        
        if prediction_result.confidence < 0.7:
            recommendations.append("Verify with additional reliable sources")
        
        if prediction_result.verdict in ['false', 'misleading']:
            recommendations.append("Be cautious about sharing this information")
            recommendations.append("Check official sources for confirmation")
        
        if prediction_result.features.get('sensational_score', 0) > 2:
            recommendations.append("Sensational language often indicates unreliable claims")
        
        recommendations.append("Consider the source and context of the information")
        
        return recommendations
    
    def _generate_counterfactuals(self, text: str, current_verdict: str) -> List[Dict]:
        """Generate counterfactual explanations - FIXED VERSION"""
        counterfactuals = []
        
        # Define all possible verdicts
        all_verdicts = ['true', 'false', 'misleading', 'unverifiable']
        
        # Create a copy of the list and safely remove current verdict
        target_verdicts = all_verdicts.copy()
        
        # Safe removal - only remove if it exists in the list
        if current_verdict in target_verdicts:
            target_verdicts.remove(current_verdict)
        else:
            # If current verdict is not in the list, use all verdicts except the first one
            target_verdicts = all_verdicts[1:]
        
        # Limit to 2 counterfactuals to avoid clutter
        for target_verdict in target_verdicts[:2]:
            modification = self._suggest_modification(text, target_verdict)
            counterfactuals.append({
                'target_verdict': target_verdict,
                'modification_suggestion': modification,
                'explanation': f"To be considered {target_verdict}, the statement might need:"
            })
        
        return counterfactuals
    
    def _suggest_modification(self, text: str, target_verdict: str) -> str:
        """Suggest modifications to change verdict"""
        suggestions = {
            'true': "More specific, verifiable details and credible sources. Include factual evidence and remove sensational language.",
            'false': "Removal of sensational language, exaggeration, and unverified claims. Add specific factual inaccuracies.",
            'misleading': "Clearer context, less ambiguous wording, and balanced presentation of facts without omission of key information.",
            'unverifiable': "More specific claims that can be checked against reliable sources, or removal of speculative elements."
        }
        
        return suggestions.get(target_verdict, "Different wording, structure, and evidence presentation.")