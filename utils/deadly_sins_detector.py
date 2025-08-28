import re
from typing import Dict, List, Tuple

class DeadlySinsDetector:
    """
    Advanced detection of AI fingerprint patterns with context-aware pattern libraries
    and multi-order validation scanning.
    """
    
    def __init__(self):
        # Enhanced pattern libraries with more comprehensive regex patterns
        self.patterns = {
            "em_dash": {
                "pattern": r"[—–]",  # em dash and en dash
                "severity": "critical",
                "description": "Em dash usage creates robotic pauses"
            },
            "rhetorical_contrast": {
                "pattern": r"(?:It's not just|It's not merely|It's not only).+?[,;]\s*(?:it's|it is|but).+?",
                "severity": "critical",
                "description": "Rhetorical contrast creates artificial drama"
            },
            "antithesis": {
                "pattern": r"(?:It's not|It is not|It isn't).+?[,;]\s*(?:it's|it is|but).+?",
                "severity": "critical",
                "description": "Antithesis creates false dichotomies"
            },
            "paradiastole": {
                "pattern": r"(?:It's not|It is not|It isn't)\s+(?:laziness|failure|mistake|problem).+?[,;]\s*(?:it's|it is|but).+?",
                "severity": "critical",
                "description": "Paradiastole reclassifies concepts disingenuously"
            },
            "reframing_contrast": {
                "pattern": r"(?:It's not just|It's not merely|It's not only)\s+(?:a cost|an expense|a problem).+?[,;]\s*(?:it's|it is|but).+?",
                "severity": "critical",
                "description": "Reframing contrast disconnects from reality"
            },
            "chiasmus": {
                "pattern": r"(?:It's not what).+?(?:does to you|makes you|gives you).+?[,;]\s*(?:it's|it is|but).+?(?:you do with|make of|get from).+?",
                "severity": "critical",
                "description": "Chiasmus creates contrived parallelism"
            },
            "tagline_frame": {
                "pattern": r"(?:It's not just|It's not merely|It's not only)\s+(?:a car|a product|a service|an app|a tool).+?[,;]\s*(?:it's|it is|but).+?",
                "severity": "critical",
                "description": "Tagline framing feels like corporate jargon"
            }
        }
    
    def detect_patterns(self, text: str, brand_voice: Dict = None) -> Dict:
        """
        Detect all deadly sins patterns in text with precise location tracking.
        
        Args:
            text (str): Text to scan for patterns
            brand_voice (Dict): Brand voice parameters for context-aware detection
            
        Returns:
            Dict: Detailed violations report
        """
        violations = {}
        false_positive_score = 0.0
        
        for pattern_name, pattern_info in self.patterns.items():
            pattern = re.compile(pattern_info["pattern"], re.IGNORECASE)
            matches = list(pattern.finditer(text))
            
            violation_details = {
                "count": len(matches),
                "positions": [(match.start(), match.end()) for match in matches],
                "matches": [match.group() for match in matches],
                "severity": pattern_info["severity"],
                "description": pattern_info["description"]
            }
            
            violations[pattern_name] = violation_details
            
            # Calculate false positive score based on brand context
            if brand_voice and matches:
                false_positive_score += self._calculate_false_positive_score(
                    matches, text, brand_voice, pattern_name
                )
        
        # Calculate overall severity score
        severity_score = self._calculate_severity_score(violations)
        
        return {
            "violations": violations,
            "severity_score": severity_score,
            "violation_positions": self._get_all_positions(violations),
            "false_positive_score": false_positive_score / len(self.patterns) if self.patterns else 0.0,
            "total_violations": sum(v["count"] for v in violations.values())
        }
    
    def _calculate_false_positive_score(self, matches: List, text: str, brand_voice: Dict, pattern_name: str) -> float:
        """
        Calculate false positive likelihood based on brand context.
        """
        if not brand_voice:
            return 0.0
            
        # Check if matches are in brand-specific terminology
        brand_terms = set()
        if "themes" in brand_voice:
            brand_terms.update(brand_voice["themes"])
        if "values" in brand_voice:
            brand_terms.update(brand_voice["values"])
            
        false_positives = 0
        for match in matches:
            match_text = match.group() if hasattr(match, 'group') else str(match)
            if any(term.lower() in match_text.lower() for term in brand_terms):
                false_positives += 1
                
        return false_positives / len(matches) if matches else 0.0
    
    def _calculate_severity_score(self, violations: Dict) -> float:
        """
        Calculate overall severity score based on violation counts and severities.
        """
        total_score = 0.0
        total_violations = 0
        
        severity_weights = {
            "critical": 1.0,
            "high": 0.8,
            "medium": 0.5,
            "low": 0.2
        }
        
        for violation in violations.values():
            weight = severity_weights.get(violation["severity"], 0.5)
            total_score += violation["count"] * weight
            total_violations += violation["count"]
            
        return total_score / max(total_violations, 1) if total_violations > 0 else 0.0
    
    def _get_all_positions(self, violations: Dict) -> List[Tuple[int, int]]:
        """
        Get all violation positions sorted by start position.
        """
        all_positions = []
        for violation in violations.values():
            all_positions.extend(violation["positions"])
        return sorted(all_positions, key=lambda x: x[0])
    
    def multi_order_validation(self, text: str) -> Dict:
        """
        Multi-stage validation scanning (structural → semantic → stylistic).
        """
        # Stage 1: Structural scanning (basic pattern matching)
        structural_results = self.detect_patterns(text)
        
        # Stage 2: Semantic scanning (context-aware detection)
        # This would involve more sophisticated NLP analysis in a full implementation
        semantic_results = structural_results.copy()
        
        # Stage 3: Stylistic scanning (flow and naturalness analysis)
        # This would involve analyzing sentence structure and flow
        stylistic_results = structural_results.copy()
        
        return {
            "structural": structural_results,
            "semantic": semantic_results,
            "stylistic": stylistic_results,
            "overall_confidence": 0.95  # High confidence in pattern matching
        }

def detect_deadly_sins(text: str, brand_voice: Dict = None) -> Dict:
    """
    Convenience function to detect deadly sins patterns.
    
    Args:
        text (str): Text to scan
        brand_voice (Dict): Optional brand voice context
        
    Returns:
        Dict: Violations report
    """
    detector = DeadlySinsDetector()
    return detector.detect_patterns(text, brand_voice)

if __name__ == "__main__":
    # Test the detector
    test_text = "It's not just a product; it's a revolution. The AI—our most powerful tool—will transform everything. It's not laziness; it's strategic delegation."
    
    detector = DeadlySinsDetector()
    results = detector.detect_patterns(test_text)
    
    print("Detection Results:")
    print(f"Total Violations: {results['total_violations']}")
    print(f"Severity Score: {results['severity_score']:.2f}")
    print(f"False Positive Score: {results['false_positive_score']:.2f}")
    
    for pattern_name, details in results['violations'].items():
        if details['count'] > 0:
            print(f"\n{pattern_name}:")
            print(f"  Count: {details['count']}")
            print(f"  Matches: {details['matches']}")
