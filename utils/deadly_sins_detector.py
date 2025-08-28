import re
from typing import Dict, List, Tuple

class DeadlySinsDetector:
    """
    Basic detection of AI fingerprint patterns using simpler matching techniques.
    This implementation serves as a foundation we can build upon in future iterations.
    """
    
    def __init__(self):
        # Core patterns with basic matching
        self.patterns = {
            "em_dash": {
                "detect": lambda text: text.count("—"),  # Count number of em dashes
                "severity": "critical",
                "description": "Em dash usage creates robotic pauses"
            },
            "rhetorical_contrast": {
                "detect": lambda text: 1 if (
                    any(phrase in text.lower() for phrase in ["not just", "not only"]) 
                    and any(phrase in text.lower() for phrase in ["it's", "it is", "it’s"])
                ) else 0,
                "severity": "critical",
                "description": "Rhetorical contrast creates artificial drama"
            },
            "antithesis": {
                "detect": lambda text: 1 if (
                    any(phrase in text.lower() for phrase in [" not ", " isn't", "isn't ", " not,"]) 
                    and any(phrase in text.lower() for phrase in ["it's", "it is", "it’s", "he is", "she is", "they are"])
                ) else 0,
                "severity": "critical",
                "description": "Antithesis creates false dichotomies"
            },
            # More patterns can be added here as we refine the detection
        }
    
    def detect_patterns(self, text: str, brand_voice: Dict = None) -> Dict:
        """
        Detect basic deadly sins patterns in text.
        
        Args:
            text (str): Text to scan for patterns
            brand_voice (Dict): Brand voice parameters for context-aware detection
            
        Returns:
            Dict: Basic violations report
        """
        violations = {}
        total_violations = 0
        
        for pattern_name, pattern_info in self.patterns.items():
            count = pattern_info["detect"](text)
            violation_details = {
                "count": count,
                "positions": [(0, len(text))] if count else [],
                "matches": [pattern_name] if count else [],
                "severity": pattern_info["severity"],
                "description": pattern_info["description"]
            }
            violations[pattern_name] = violation_details
            total_violations += count
        
        return {
            "violations": violations,
            "severity_score": 1.0 if total_violations else 0.0,
            "total_violations": total_violations,
            "violation_positions": [(0, len(text))] if total_violations else [],
            "false_positive_score": 0.0  # Placeholder for now
        }
    
    def multi_order_validation(self, text: str) -> Dict:
        """Simplified validation scanning"""
        structural_results = self.detect_patterns(text)
        return {
            "structural": structural_results,
            "overall_confidence": 0.7
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
    test_text = "It's not just a product; it's a revolution."
    
    detector = DeadlySinsDetector()
    results = detector.detect_patterns(test_text)
    
    print("Detection Results:")
    print(f"Total Violations: {results['total_violations']}")
    
    for pattern_name, details in results['violations'].items():
        print(f"\n{pattern_name}:")
        print(f"  Description: {details['description']}")
