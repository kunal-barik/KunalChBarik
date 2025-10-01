import time
from typing import Dict, List
import logging
from dataclasses import dataclass

@dataclass
class SourceResult:
    source: str
    verdict: str
    confidence: float
    evidence: List[str]
    url: str

class MultiSourceVerifier:
    """
    Multi-source fact verification system - SYNCHRONOUS VERSION
    """
    
    def __init__(self):
        self.sources = {
            'wikipedia': self.query_wikipedia,
            'news': self.query_news,
            'fact_check': self.query_fact_check
        }
    
    def verify_claim(self, claim: str) -> Dict:
        """Verify claim across multiple sources - SYNCHRONOUS VERSION"""
        results = []
        
        for source_name, query_func in self.sources.items():
            try:
                result = query_func(claim)
                results.append(SourceResult(
                    source=source_name,
                    verdict=result.get('verdict', 'unknown'),
                    confidence=result.get('confidence', 0.5),
                    evidence=result.get('evidence', []),
                    url=result.get('url', '')
                ))
            except Exception as e:
                logging.error(f"Error querying {source_name}: {e}")
                results.append(SourceResult(
                    source=source_name,
                    verdict='error',
                    confidence=0.0,
                    evidence=[],
                    url=''
                ))
        
        return self._aggregate_results(results, claim)
    
    def query_wikipedia(self, claim: str) -> Dict:
        """Query Wikipedia for claim verification"""
        # Simulate API call delay
        time.sleep(0.2)
        
        # Mock implementation - analyze claim content
        claim_lower = claim.lower()
        
        if any(word in claim_lower for word in ['earth', 'round', 'planet', 'science']):
            return {
                'verdict': 'supported',
                'confidence': 0.8,
                'evidence': ['Scientific consensus supports this claim'],
                'url': 'https://en.wikipedia.org/wiki/Earth'
            }
        elif any(word in claim_lower for word in ['breaking', 'secret', 'urgent', 'shocking']):
            return {
                'verdict': 'contradicted',
                'confidence': 0.7,
                'evidence': ['No reliable sources support this sensational claim'],
                'url': 'https://en.wikipedia.org'
            }
        else:
            return {
                'verdict': 'mixed',
                'confidence': 0.5,
                'evidence': ['Insufficient information for definitive verification'],
                'url': 'https://en.wikipedia.org'
            }
    
    def query_news(self, claim: str) -> Dict:
        """Query news sources"""
        time.sleep(0.1)
        
        claim_lower = claim.lower()
        
        if any(word in claim_lower for word in ['covid', 'vaccine', 'health']):
            return {
                'verdict': 'supported',
                'confidence': 0.75,
                'evidence': ['Multiple reputable health organizations confirm this'],
                'url': 'https://newsapi.org'
            }
        elif any(word in claim_lower for word in ['conspiracy', 'secret', 'government']):
            return {
                'verdict': 'contradicted',
                'confidence': 0.8,
                'evidence': ['Fact-checkers have debunked similar claims'],
                'url': 'https://reuters.com'
            }
        else:
            return {
                'verdict': 'unknown',
                'confidence': 0.4,
                'evidence': ['Limited news coverage on this specific claim'],
                'url': 'https://newsapi.org'
            }
    
    def query_fact_check(self, claim: str) -> Dict:
        """Query fact-checking websites"""
        time.sleep(0.1)
        
        claim_lower = claim.lower()
        
        if any(word in claim_lower for word in ['true', 'real', 'fact']):
            return {
                'verdict': 'supported',
                'confidence': 0.85,
                'evidence': ['Verified by multiple independent fact-checking organizations'],
                'url': 'https://snopes.com'
            }
        elif any(word in claim_lower for word in ['false', 'fake', 'hoax']):
            return {
                'verdict': 'contradicted',
                'confidence': 0.9,
                'evidence': ['This claim has been rated false by fact-checkers'],
                'url': 'https://factcheck.org'
            }
        else:
            return {
                'verdict': 'mixed',
                'confidence': 0.6,
                'evidence': ['Some sources support, others contradict this claim'],
                'url': 'https://snopes.com'
            }
    
    def _aggregate_results(self, results: List[SourceResult], claim: str) -> Dict:
        """Aggregate results from multiple sources"""
        valid_results = [r for r in results if r.verdict != 'error']
        
        if not valid_results:
            return {
                'final_verdict': 'unverifiable',
                'confidence': 0.5,
                'sources_checked': 0,
                'source_breakdown': []
            }
        
        # Weighted aggregation
        verdict_weights = {
            'supported': 1.0, 
            'contradicted': -1.0, 
            'mixed': 0.0, 
            'unknown': 0.0,
            'true': 1.0,
            'false': -1.0
        }
        
        total_weight = 0
        weighted_sum = 0
        
        for result in valid_results:
            weight = result.confidence
            verdict_weight = verdict_weights.get(result.verdict, 0.0)
            
            weighted_sum += verdict_weight * weight
            total_weight += weight
        
        if total_weight == 0:
            final_confidence = 0.5
            final_verdict = 'unverifiable'
        else:
            normalized_score = weighted_sum / total_weight
            
            if normalized_score > 0.3:
                final_verdict = 'supported'
            elif normalized_score < -0.3:
                final_verdict = 'contradicted'
            else:
                final_verdict = 'mixed'
            
            final_confidence = min(abs(normalized_score) * 1.5, 1.0)  # Boost confidence
        
        return {
            'final_verdict': final_verdict,
            'confidence': final_confidence,
            'sources_checked': len(valid_results),
            'source_breakdown': [
                {
                    'source': r.source,
                    'verdict': r.verdict,
                    'confidence': r.confidence,
                    'evidence': r.evidence
                } for r in valid_results
            ]
        }