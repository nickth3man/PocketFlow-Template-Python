import re
from typing import Dict, List, Tuple
from utils.deadly_sins_detector import DeadlySinsDetector

class ContentSanitizer:
    """
    Deterministic content sanitizer that removes AI fingerprint patterns
    while preserving brand voice and ensuring no side effects.
    """
    
    def __init__(self):
        self.detector = DeadlySinsDetector()
    
    def sanitize_content(self, text: str, violations: Dict, brand_voice: Dict = None) -> Tuple[str, Dict]:
        """
        Remove deadly sins patterns from text using deterministic transformations.
        
        Args:
            text (str): Text to sanitize
            violations (Dict): Violations report from detector
            brand_voice (Dict): Brand voice parameters for preservation
            
        Returns:
            Tuple[str, Dict]: (sanitized_text, transformation_log)
        """
        sanitized_text = text
        transformation_log = {
            "original_length": len(text),
            "transformations_applied": [],
            "patterns_removed": {},
            "brand_preservation_score": 1.0
        }
        
        # Apply transformations in order of severity and impact
        # Start with the most disruptive patterns
        
        # 1. Remove em dashes (simple replacement)
        if violations.get("em_dash", {}).get("count", 0) > 0:
            sanitized_text, em_dash_changes = self._remove_em_dashes(sanitized_text, violations["em_dash"])
            transformation_log["transformations_applied"].append("em_dash_removal")
            transformation_log["patterns_removed"]["em_dash"] = em_dash_changes
        
        # 2. Fix rhetorical contrasts and similar patterns
        pattern_fixes = [
            ("rhetorical_contrast", self._fix_rhetorical_contrast),
            ("antithesis", self._fix_antithesis),
            ("paradiastole", self._fix_paradiastole),
            ("reframing_contrast", self._fix_reframing_contrast),
            ("chiasmus", self._fix_chiasmus),
            ("tagline_frame", self._fix_tagline_frame)
        ]
        
        for pattern_name, fix_function in pattern_fixes:
            if violations.get(pattern_name, {}).get("count", 0) > 0:
                sanitized_text, changes = fix_function(sanitized_text, violations[pattern_name], brand_voice)
                if changes > 0:
                    transformation_log["transformations_applied"].append(f"{pattern_name}_fix")
                    transformation_log["patterns_removed"][pattern_name] = changes
        
        # Final validation to ensure no new patterns were introduced
        final_violations = self.detector.detect_patterns(sanitized_text, brand_voice)
        transformation_log["final_violations"] = final_violations["total_violations"]
        transformation_log["final_length"] = len(sanitized_text)
        
        return sanitized_text, transformation_log
    
    def _remove_em_dashes(self, text: str, em_dash_violations: Dict) -> Tuple[str, int]:
        """
        Remove em dashes and replace with appropriate punctuation.
        """
        changes = 0
        # Replace em dashes with commas, periods, or remove based on context
        # This is a simple approach - in practice, more sophisticated context analysis would be used
        
        # Replace with comma and space for mid-sentence pauses
        text = re.sub(r'\s*[—–]\s*', ', ', text)
        changes = em_dash_violations["count"]
        
        # Clean up double commas
        text = re.sub(r',\s*,', ',', text)
        # Clean up comma before period
        text = re.sub(r',\s*\.', '.', text)
        
        return text, changes
    
    def _fix_rhetorical_contrast(self, text: str, violations: Dict, brand_voice: Dict = None) -> Tuple[str, int]:
        """
        Fix rhetorical contrast patterns by making them more natural.
        """
        changes = 0
        pattern = re.compile(r"(?:It's not just|It's not merely|It's not only)\s+(.+?)\s*[,;]\s*(?:it's|it is|but)\s+(.+?)\.", re.IGNORECASE)
        
        def replacement_func(match):
            nonlocal changes
            changes += 1
            first_part = match.group(1)
            second_part = match.group(2)
            
            # Make it more natural and conversational
            if brand_voice and "tone" in brand_voice:
                if brand_voice["tone"] == "conversational":
                    return f"Beyond {first_part}, {second_part.lower()}."
                elif brand_voice["tone"] == "professional":
                    return f"While {first_part} is important, {second_part.lower()}."
                else:
                    return f"{first_part} and {second_part.lower()}."
            else:
                return f"{first_part} and {second_part.lower()}."
        
        text = pattern.sub(replacement_func, text)
        return text, changes
    
    def _fix_antithesis(self, text: str, violations: Dict, brand_voice: Dict = None) -> Tuple[str, int]:
        """
        Fix antithesis patterns by making them more balanced.
        """
        changes = 0
        pattern = re.compile(r"(?:It's not|It is not|It isn't)\s+(.+?)\s*[,;]\s*(?:it's|it is|but)\s+(.+?)\.", re.IGNORECASE)
        
        def replacement_func(match):
            nonlocal changes
            changes += 1
            first_part = match.group(1)
            second_part = match.group(2)
            
            # Make it more natural
            return f"Rather than {first_part}, {second_part.lower()}."
        
        text = pattern.sub(replacement_func, text)
        return text, changes
    
    def _fix_paradiastole(self, text: str, violations: Dict, brand_voice: Dict = None) -> Tuple[str, int]:
        """
        Fix paradiastole patterns by being more direct.
        """
        changes = 0
        pattern = re.compile(r"(?:It's not|It is not|It isn't)\s+(?:laziness|failure|mistake|problem|error)\s+(.+?)\s*[,;]\s*(?:it's|it is|but)\s+(.+?)\.", re.IGNORECASE)
        
        def replacement_func(match):
            nonlocal changes
            changes += 1
            first_part = match.group(1)
            second_part = match.group(2)
            
            # Be more direct and honest
            return f"This isn't {first_part}; instead, {second_part.lower()}."
        
        text = pattern.sub(replacement_func, text)
        return text, changes
    
    def _fix_reframing_contrast(self, text: str, violations: Dict, brand_voice: Dict = None) -> Tuple[str, int]:
        """
        Fix reframing contrast patterns by being more authentic.
        """
        changes = 0
        pattern = re.compile(r"(?:It's not just|It's not merely|It's not only)\s+(?:a cost|an expense|a problem|an issue)\s+(.+?)\s*[,;]\s*(?:it's|it is|but)\s+(.+?)\.", re.IGNORECASE)
        
        def replacement_func(match):
            nonlocal changes
            changes += 1
            first_part = match.group(1)
            second_part = match.group(2)
            
            # Be more authentic
            return f"While this involves {first_part}, it's primarily about {second_part.lower()}."
        
        text = pattern.sub(replacement_func, text)
        return text, changes
    
    def _fix_chiasmus(self, text: str, violations: Dict, brand_voice: Dict = None) -> Tuple[str, int]:
        """
        Fix chiasmus patterns by making them more direct.
        """
        changes = 0
        pattern = re.compile(r"(?:It's not what)\s+(.+?)\s+(?:does to you|makes you|gives you)\s*[,;]\s*(?:it's|it is|but)\s+(.+?)\s+(?:you do with|make of|get from)\s+(.+?)\.", re.IGNORECASE)
        
        def replacement_func(match):
            nonlocal changes
            changes += 1
            first_action = match.group(1)
            second_action = match.group(2)
            object_ref = match.group(3)
            
            # Make it more direct
            return f"The key isn't what {first_action} does to you, but what {second_action} you {object_ref}."
        
        text = pattern.sub(replacement_func, text)
        return text, changes
    
    def _fix_tagline_frame(self, text: str, violations: Dict, brand_voice: Dict = None) -> Tuple[str, int]:
        """
        Fix tagline frame patterns by being more specific.
        """
        changes = 0
        pattern = re.compile(r"(?:It's not just|It's not merely|It's not only)\s+(?:a car|a product|a service|an app|a tool)\s+(.+?)\s*[,;]\s*(?:it's|it is|but)\s+(.+?)\.", re.IGNORECASE)
        
        def replacement_func(match):
            nonlocal changes
            changes += 1
            first_part = match.group(1)
            second_part = match.group(2)
            
            # Be more specific and authentic
            return f"This {first_part} goes beyond just being a product—it's about {second_part.lower()}."
        
        text = pattern.sub(replacement_func, text)
        return text, changes

def sanitize_content(text: str, violations: Dict, brand_voice: Dict = None) -> Tuple[str, Dict]:
    """
    Convenience function to sanitize content.
    
    Args:
        text (str): Text to sanitize
        violations (Dict): Violations report
        brand_voice (Dict): Optional brand voice context
        
    Returns:
        Tuple[str, Dict]: (sanitized_text, transformation_log)
    """
    sanitizer = ContentSanitizer()
    return sanitizer.sanitize_content(text, violations, brand_voice)

if __name__ == "__main__":
    # Test the sanitizer
    test_text = "It's not just a product; it's a revolution. The AI—our most powerful tool—will transform everything. It's not laziness; it's strategic delegation."
    
    from utils.deadly_sins_detector import detect_deadly_sins
    violations = detect_deadly_sins(test_text)
    
    print("Original text:", test_text)
    print("\nViolations found:", violations["total_violations"])
    
    sanitizer = ContentSanitizer()
    sanitized_text, log = sanitizer.sanitize_content(test_text, violations)
    
    print("\nSanitized text:", sanitized_text)
    print("\nTransformation log:", log)
    
    # Verify no new violations
    final_violations = detect_deadly_sins(sanitized_text)
    print(f"\nFinal violations: {final_violations['total_violations']}")
