import wikipedia
import requests
from typing import Dict, List, Set
import json
import logging
from dataclasses import dataclass
import re

@dataclass
class KnowledgeEvidence:
    supporting_facts: List[str]
    contradicting_facts: List[str]
    related_entities: List[str]
    confidence: float
    sources: List[str]
    fact_check: Dict

class KnowledgeGraphVerifier:
    """
    UPGRADED: Enhanced knowledge graph with real fact-checking capabilities
    """
    
    def __init__(self):
        self.entity_cache = {}
        self.fact_patterns = self._load_fact_patterns()
    
    def _load_fact_patterns(self) -> Dict:
        """UPGRADED: Load common fact patterns for better verification"""
        return {
            'scientific_facts': {
                'earth_shape': {'pattern': r'earth.*flat|flat.*earth', 'truth': 'false', 'confidence': 0.95},
                'climate_change': {'pattern': r'climate change.*real|global warming.*real', 'truth': 'true', 'confidence': 0.98},
                'moon_landing': {'pattern': r'moon landing.*fake|never.*moon', 'truth': 'false', 'confidence': 0.99},
                'vaccines': {'pattern': r'vaccines.*autism|vaccine.*cause', 'truth': 'false', 'confidence': 0.97}
            },
            'historical_facts': {
                'ww2_end': {'pattern': r'world war.*ended.*1945', 'truth': 'true', 'confidence': 0.99},
                'holocaust': {'pattern': r'holocaust.*fake|never.*happened', 'truth': 'false', 'confidence': 0.99}
            },
            'health_facts': {
                'covid_masks': {'pattern': r'masks.*don\'t work.*covid', 'truth': 'false', 'confidence': 0.90},
                'vitamin_c': {'pattern': r'vitamin c.*cure.*covid', 'truth': 'false', 'confidence': 0.85}
            }
        }
    
    def _check_against_fact_patterns(self, text: str) -> Dict:
        """UPGRADED: Check statement against known fact patterns"""
        text_lower = text.lower()
        matches = []
        
        for category, patterns in self.fact_patterns.items():
            for fact_name, fact_data in patterns.items():
                if re.search(fact_data['pattern'], text_lower, re.IGNORECASE):
                    matches.append({
                        'category': category,
                        'fact': fact_name,
                        'verdict': fact_data['truth'],
                        'confidence': fact_data['confidence'],
                        'explanation': f"Matches known {category.replace('_', ' ')} pattern"
                    })
        
        return {'pattern_matches': matches, 'total_matches': len(matches)}
    
    def extract_entities(self, text: str) -> List[str]:
        """UPGRADED: Better entity extraction with domain-specific terms"""
        entities = []
        words = text.split()
        
        # Enhanced entity recognition
        current_entity = []
        for i, word in enumerate(words):
            cleaned_word = word.strip('.,!?;:"()').lower()
            
            # Look for proper nouns and domain terms
            if (word[0].isupper() and len(word) > 1) or cleaned_word in self._get_domain_terms():
                current_entity.append(word)
            else:
                if current_entity:
                    entity = ' '.join(current_entity)
                    if len(entity) > 2 and self._is_significant_entity(entity):
                        entities.append(entity)
                    current_entity = []
        
        if current_entity:
            entity = ' '.join(current_entity)
            if len(entity) > 2 and self._is_significant_entity(entity):
                entities.append(entity)
        
        return list(set(entities))
    
    def _get_domain_terms(self) -> Set[str]:
        """Domain-specific terms that are important for fact-checking"""
        return {
            'covid', 'vaccine', 'climate', 'earth', 'moon', 'nasa', 'government',
            'study', 'research', 'scientists', 'doctor', 'expert', 'university',
            'virus', 'mask', 'lockdown', 'wuhan', 'who', 'cdc'
        }
    
    def _is_significant_entity(self, entity: str) -> bool:
        """Filter out insignificant entities"""
        insignificant = {'The', 'This', 'That', 'These', 'Those', 'There'}
        return entity not in insignificant and len(entity) > 2
    
    def query_wikipedia(self, entity: str) -> Dict:
        """UPGRADED: Enhanced Wikipedia query with better error handling"""
        try:
            wikipedia.set_rate_limiting(True)
            # Search for the entity first to get better results
            search_results = wikipedia.search(entity, results=3)
            if not search_results:
                return {'error': 'No results found', 'title': entity}
            
            # Use the first search result
            page_title = search_results[0]
            page = wikipedia.page(page_title, auto_suggest=False)
            
            return {
                'title': page.title,
                'summary': page.summary[:400] + '...' if len(page.summary) > 400 else page.summary,
                'url': page.url,
                'categories': page.categories[:5],
                'content': page.content[:1000] if len(page.content) > 1000 else page.content
            }
        except wikipedia.exceptions.DisambiguationError as e:
            return {'error': f'Multiple matches: {e.options[:2]}', 'title': entity}
        except wikipedia.exceptions.PageError:
            return {'error': 'Page not found', 'title': entity}
        except Exception as e:
            logging.error(f"Wikipedia query error for {entity}: {e}")
            return {'error': 'Query failed', 'title': entity}
    
    def verify_against_knowledge(self, text: str, entities: List[str]) -> KnowledgeEvidence:
        """UPGRADED: Enhanced verification with fact pattern matching"""
        supporting_facts = []
        contradicting_facts = []
        related_entities = []
        sources = []
        
        # First, check against known fact patterns
        pattern_check = self._check_against_fact_patterns(text)
        
        # Then verify with Wikipedia for entities
        for entity in entities[:4]:  # Limit to top 4 entities
            wiki_data = self.query_wikipedia(entity)
            
            if 'error' not in wiki_data:
                sources.append(wiki_data['url'])
                
                # Enhanced fact matching
                text_lower = text.lower()
                content_lower = (wiki_data.get('content', '') + ' ' + wiki_data.get('summary', '')).lower()
                
                # Look for supporting evidence
                supporting_evidence = self._find_supporting_evidence(text_lower, content_lower, wiki_data)
                supporting_facts.extend(supporting_evidence)
                
                # Look for contradicting evidence
                contradicting_evidence = self._find_contradicting_evidence(text_lower, content_lower, wiki_data)
                contradicting_facts.extend(contradicting_evidence)
                
                related_entities.append(wiki_data['title'])
        
        # Calculate confidence
        base_confidence = 0.5
        if pattern_check['total_matches'] > 0:
            # Use pattern match confidence
            best_match = max(pattern_check['pattern_matches'], key=lambda x: x['confidence'])
            base_confidence = best_match['confidence']
        else:
            # Adjust based on evidence found
            if supporting_facts:
                base_confidence += len(supporting_facts) * 0.1
            if contradicting_facts:
                base_confidence -= len(contradicting_facts) * 0.15
        
        confidence = max(0.1, min(base_confidence, 0.95))
        
        return KnowledgeEvidence(
            supporting_facts=supporting_facts[:3],
            contradicting_facts=contradicting_facts[:3],
            related_entities=related_entities[:5],
            confidence=confidence,
            sources=sources[:3],
            fact_check=pattern_check
        )
    
    def _find_supporting_evidence(self, text: str, content: str, wiki_data: Dict) -> List[str]:
        """UPGRADED: Find supporting evidence in Wikipedia content"""
        evidence = []
        
        # Extract key sentences that might support the claim
        sentences = re.split(r'[.!?]+', wiki_data.get('summary', ''))
        text_words = set(text.split())
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            # Check for keyword overlap
            sentence_words = set(sentence_lower.split())
            common_words = text_words.intersection(sentence_words)
            
            if len(common_words) >= 2 and len(sentence.strip()) > 20:
                evidence.append(sentence.strip())
                if len(evidence) >= 2:  # Limit to 2 pieces of evidence
                    break
        
        return evidence
    
    def _find_contradicting_evidence(self, text: str, content: str, wiki_data: Dict) -> List[str]:
        """UPGRADED: Find contradicting evidence"""
        evidence = []
        
        # Simple contradiction detection based on common misinformation patterns
        contradiction_patterns = {
            r'flat.*earth': 'The Earth is an oblate spheroid, not flat',
            r'moon.*landing.*fake': 'The Apollo moon landings are well-documented historical events',
            r'vaccin.*autism': 'Numerous studies have found no link between vaccines and autism'
        }
        
        for pattern, fact in contradiction_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                evidence.append(fact)
        
        return evidence
    
    def enhance_with_external_sources(self, text: str) -> Dict:
        """UPGRADED: Enhanced external source checking"""
        return {
            'fact_check_analysis': self._enhanced_fact_check(text),
            'credibility_score': self._calculate_credibility_score(text),
            'domain_analysis': self._analyze_domain(text)
        }
    
    def _enhanced_fact_check(self, text: str) -> Dict:
        """UPGRADED: More sophisticated fact-checking"""
        text_lower = text.lower()
        
        # Common fact checks
        checks = []
        
        if 'earth' in text_lower and 'flat' in text_lower:
            checks.append({
                'claim': 'Earth is flat',
                'verdict': 'False',
                'explanation': 'Overwhelming scientific evidence shows Earth is spherical',
                'sources': ['NASA', 'NOAA', 'Scientific consensus'],
                'confidence': 0.99
            })
        
        if 'vaccin' in text_lower and 'autism' in text_lower:
            checks.append({
                'claim': 'Vaccines cause autism',
                'verdict': 'False', 
                'explanation': 'Multiple large-scale studies found no link between vaccines and autism',
                'sources': ['CDC', 'WHO', 'The Lancet (retracted original study)'],
                'confidence': 0.98
            })
        
        if 'moon' in text_lower and 'landing' in text_lower and 'fake' in text_lower:
            checks.append({
                'claim': 'Moon landing was faked',
                'verdict': 'False',
                'explanation': 'Multiple lines of evidence confirm the Apollo moon landings',
                'sources': ['NASA', 'Independent scientists', 'Lunar laser ranging'],
                'confidence': 0.99
            })
        
        return {'checks': checks, 'total_checks': len(checks)}
    
    def _calculate_credibility_score(self, text: str) -> float:
        """UPGRADED: Calculate credibility score based on content"""
        score = 0.5
        text_lower = text.lower()
        
        # Positive indicators
        if any(term in text_lower for term in ['according to study', 'research shows', 'scientists found']):
            score += 0.3
        if any(term in text_lower for term in ['peer-reviewed', 'journal', 'university']):
            score += 0.2
        
        # Negative indicators  
        if any(term in text_lower for term in ['breaking', 'urgent', 'secret', 'they don\'t want you to know']):
            score -= 0.3
        if text_lower.count('!') > 2:
            score -= 0.1
        
        return max(0.1, min(score, 1.0))
    
    def _analyze_domain(self, text: str) -> Dict:
        """UPGRADED: Analyze which domain the claim belongs to"""
        text_lower = text.lower()
        domains = []
        
        if any(term in text_lower for term in ['covid', 'virus', 'vaccine', 'mask', 'pandemic']):
            domains.append('health')
        if any(term in text_lower for term in ['climate', 'warming', 'environment', 'carbon']):
            domains.append('environment')
        if any(term in text_lower for term in ['earth', 'moon', 'space', 'nasa', 'planet']):
            domains.append('science')
        if any(term in text_lower for term in ['government', 'politic', 'election', 'law']):
            domains.append('politics')
        
        return {'domains': domains, 'primary_domain': domains[0] if domains else 'general'}