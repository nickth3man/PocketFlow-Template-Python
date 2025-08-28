from typing import Dict, List, Any
from collections import defaultdict
import json

class PatternLearner:
    """
    Analyzes persistent patterns to improve future prompt engineering.
    """
    
    def __init__(self):
        self.pattern_history = defaultdict(list)
        self.prompt_improvements = {}
    
    def analyze_version_history(self, version_history: List[Dict]) -> Dict:
        """
        Analyze version history to identify persistent patterns.
        
        Args:
            version_history (List[Dict]): List of version data
            
        Returns:
            Dict: Analysis results with learned patterns
        """
        if not version_history:
            return {"learned_patterns": {}, "prompt_improvements": {}}
        
        # Track violations across versions
        violation_patterns = defaultdict(int)
        violation_correlations = defaultdict(lambda: defaultdict(int))
        
        # Track changes and feedback
        change_patterns = defaultdict(int)
        feedback_patterns = defaultdict(int)
        
        # Analyze each version
        for version in version_history:
            # Analyze violations fixed
            violations_fixed = version.get("violations_fixed", [])
            for violation in violations_fixed:
                violation_patterns[violation] += 1
            
            # Analyze changes made
            changes = version.get("changes_made", [])
            for change in changes:
                change_patterns[change] += 1
            
            # Analyze user feedback
            feedback = version.get("user_feedback", "")
            if feedback:
                feedback_patterns[feedback.lower()] += 1
        
        # Identify persistent violations (appearing in multiple versions)
        persistent_violations = {
            violation: count 
            for violation, count in violation_patterns.items() 
            if count > 1
        }
        
        # Identify common change patterns
        common_changes = {
            change: count 
            for change, count in change_patterns.items() 
            if count > 1
        }
        
        # Generate learned patterns
        learned_patterns = {
            "persistent_violations": persistent_violations,
            "common_changes": common_changes,
            "feedback_trends": dict(feedback_patterns),
            "total_versions_analyzed": len(version_history)
        }
        
        # Generate prompt improvements based on patterns
        prompt_improvements = self._generate_prompt_improvements(learned_patterns)
        
        return {
            "learned_patterns": learned_patterns,
            "prompt_improvements": prompt_improvements,
            "analysis_summary": {
                "persistent_issues": len(persistent_violations),
                "common_changes": len(common_changes),
                "feedback_trends": len(feedback_patterns)
            }
        }
    
    def _generate_prompt_improvements(self, learned_patterns: Dict) -> Dict:
        """
        Generate prompt engineering improvements based on learned patterns.
        
        Args:
            learned_patterns (Dict): Patterns learned from history
            
        Returns:
            Dict: Prompt improvements
        """
        improvements = {}
        
        persistent_violations = learned_patterns.get("persistent_violations", {})
        common_changes = learned_patterns.get("common_changes", {})
        
        # Generate violation-specific improvements
        for violation, count in persistent_violations.items():
            improvement_key = f"avoid_{violation}"
            improvements[improvement_key] = {
                "frequency": count,
                "suggestion": self._get_violation_suggestion(violation),
                "prompt_addition": self._get_violation_prompt_addition(violation)
            }
        
        # Generate change-based improvements
        for change, count in common_changes.items():
            if "shorter" in change.lower():
                improvements["conciseness"] = {
                    "frequency": count,
                    "suggestion": "Emphasize concise communication in prompts",
                    "prompt_addition": "Keep the response concise and to the point. Avoid unnecessary elaboration."
                }
            elif "tone" in change.lower():
                improvements["tone_consistency"] = {
                    "frequency": count,
                    "suggestion": "Reinforce tone consistency in prompts",
                    "prompt_addition": "Maintain a consistent, brand-appropriate tone throughout the response."
                }
        
        return improvements
    
    def _get_violation_suggestion(self, violation: str) -> str:
        """Get suggestion for avoiding a specific violation."""
        suggestions = {
            "em_dash": "Avoid using em dashes; use commas or periods instead",
            "rhetorical_contrast": "Avoid 'It's not just X; it's Y' patterns; use more natural phrasing",
            "antithesis": "Avoid contrasting opposing ideas in balanced structures",
            "paradiastole": "Avoid reclassifying negative concepts positively",
            "reframing_contrast": "Avoid shifting meaning by putting things in different light",
            "chiasmus": "Avoid mirrored or inverted idea structures for emphasis",
            "tagline_frame": "Avoid elevating products by contrasting with mundane labels"
        }
        return suggestions.get(violation, f"Reduce occurrence of {violation} patterns")
    
    def _get_violation_prompt_addition(self, violation: str) -> str:
        """Get prompt addition for avoiding a specific violation."""
        additions = {
            "em_dash": "Do not use em dashes (—) or en dashes (–) in any context.",
            "rhetorical_contrast": "Do not use 'It's not just X; it's Y' formulations where Y reframes or repositions X.",
            "antithesis": "Do not use contrasting two opposing ideas in a balanced structure.",
            "paradiastole": "Do not use rhetorical reclassification that softens or elevates concepts.",
            "reframing_contrast": "Do not shift the meaning or perception of something by putting it in a different light.",
            "chiasmus": "Do not use mirrored or inverted idea structures for emphasis.",
            "tagline_frame": "Do not elevate a product or idea by contrasting it with a more mundane label."
        }
        return additions.get(violation, f"Avoid {violation} patterns that make content sound AI-generated.")
    
    def update_pattern_history(self, violations_data: Dict):
        """
        Update pattern history with new violation data.
        
        Args:
            violations_data (Dict): New violations data
        """
        for pattern_name, pattern_data in violations_data.items():
            if pattern_data.get("count", 0) > 0:
                self.pattern_history[pattern_name].append({
                    "timestamp": __import__('datetime').datetime.now().isoformat(),
                    "count": pattern_data["count"],
                    "positions": pattern_data.get("positions", [])
                })
    
    def get_pattern_trends(self) -> Dict:
        """
        Get trends in pattern occurrences over time.
        
        Returns:
            Dict: Pattern trends
        """
        trends = {}
        for pattern_name, occurrences in self.pattern_history.items():
            if len(occurrences) > 1:
                # Calculate trend (increasing, decreasing, stable)
                first_count = occurrences[0]["count"]
                last_count = occurrences[-1]["count"]
                
                if last_count < first_count:
                    trend = "decreasing"
                elif last_count > first_count:
                    trend = "increasing"
                else:
                    trend = "stable"
                
                trends[pattern_name] = {
                    "trend": trend,
                    "first_count": first_count,
                    "last_count": last_count,
                    "total_occurrences": len(occurrences)
                }
        
        return trends

def analyze_pattern_learning(version_history: List[Dict]) -> Dict:
    """
    Convenience function to analyze pattern learning from version history.
    
    Args:
        version_history (List[Dict]): Version history data
        
    Returns:
        Dict: Analysis results
    """
    learner = PatternLearner()
    return learner.analyze_version_history(version_history)

def get_prompt_improvements(version_history: List[Dict]) -> Dict:
    """
    Get prompt improvements based on version history analysis.
    
    Args:
        version_history (List[Dict]): Version history data
        
    Returns:
        Dict: Prompt improvements
    """
    learner = PatternLearner()
    analysis = learner.analyze_version_history(version_history)
    return analysis.get("prompt_improvements", {})

if __name__ == "__main__":
    # Test the pattern learner
    test_version_history = [
        {
            "version_id": "v1",
            "content_pieces": {
                "linkedin": {"text": "It's not just AI; it's a revolution! The future—our most powerful tool—is here."},
                "twitter": {"tweet": "AI is transforming everything! #AI #Future"}
            },
            "timestamp": "2024-01-01T10:00:00Z",
            "user_feedback": "Too corporate sounding, fix the em dash",
            "changes_made": ["removed_em_dash", "fixed_rhetorical_contrast"],
            "violations_fixed": ["em_dash", "rhetorical_contrast"]
        },
        {
            "version_id": "v2",
            "content_pieces": {
                "linkedin": {"text": "AI is transforming marketing. The future is now."},
                "twitter": {"tweet": "AI is revolutionizing marketing! #AI #Marketing"}
            },
            "timestamp": "2024-01-02T10:00:00Z",
            "user_feedback": "Good but could be more engaging",
            "changes_made": ["improved_engagement", "added_questions"],
            "violations_fixed": []
        },
        {
            "version_id": "v3",
            "content_pieces": {
                "linkedin": {"text": "It's not just technology; it's transformation! AI—our greatest asset—is reshaping marketing."},
                "twitter": {"tweet": "Technology is changing everything! #Tech #AI"}
            },
            "timestamp": "2024-01-03T10:00:00Z",
            "user_feedback": "Still has the same pattern issues",
            "changes_made": ["removed_em_dash_again"],
            "violations_fixed": ["em_dash", "rhetorical_contrast"]
        }
    ]
    
    print("Testing pattern learner...")
    
    learner = PatternLearner()
    analysis = learner.analyze_version_history(test_version_history)
    
    print(f"Analysis Summary:")
    summary = analysis["analysis_summary"]
    print(f"  Persistent issues: {summary['persistent_issues']}")
    print(f"  Common changes: {summary['common_changes']}")
    print(f"  Feedback trends: {summary['feedback_trends']}")
    
    print(f"\nLearned Patterns:")
    patterns = analysis["learned_patterns"]
    print(f"  Persistent violations: {patterns['persistent_violations']}")
    print(f"  Common changes: {patterns['common_changes']}")
    
    print(f"\nPrompt Improvements:")
    improvements = analysis["prompt_improvements"]
    for key, improvement in improvements.items():
        print(f"  {key}:")
        print(f"    Frequency: {improvement['frequency']}")
        print(f"    Suggestion: {improvement['suggestion']}")
        print(f"    Prompt addition: {improvement['prompt_addition']}")
    
    # Test pattern trends
    print(f"\nPattern Trends:")
    trends = learner.get_pattern_trends()
    for pattern, trend_data in trends.items():
        print(f"  {pattern}: {trend_data['trend']} ({trend_data['first_count']} → {trend_data['last_count']})")
