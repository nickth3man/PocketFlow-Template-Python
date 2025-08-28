from pocketflow import Node
from utils.pattern_learner import analyze_pattern_learning, get_prompt_improvements

class PatternLearnerNode(Node):
    """
    Improves prompt engineering based on revision history.
    Node that learns from pattern improvements and optimizes future generations.
    """
    
    def prep(self, shared):
        """
        Read version history and violations data from shared store.
        """
        return {
            "version_history": shared["version_history"],
            "quality_control": shared["quality_control"],
            "brand_voice": shared["brand_voice"],
            "task_requirements": shared["task_requirements"]
        }
    
    def exec(self, prep_res):
        """
        Analyze persistent patterns to improve future prompt engineering.
        """
        version_history = prep_res["version_history"]
        quality_control = prep_res["quality_control"]
        brand_voice = prep_res["brand_voice"]
        task_requirements = prep_res["task_requirements"]
        
        print(f"\n=== Pattern Learning Analysis ===")
        print(f"Analyzing {len(version_history)} versions for pattern improvements...")
        
        if len(version_history) < 2:
            print("Not enough version history for meaningful analysis.")
            return {
                "learned_patterns": {},
                "prompt_improvements": {},
                "analysis_summary": "Insufficient version history"
            }
        
        # Analyze pattern improvements across versions
        pattern_analysis = analyze_pattern_learning(version_history)
        
        # Get prompt improvements based on analysis
        prompt_improvements = get_prompt_improvements(version_history)
        
        return {
            "learned_patterns": pattern_analysis,
            "prompt_improvements": prompt_improvements,
            "analysis_summary": self._generate_analysis_summary(pattern_analysis)
        }
    
    def _generate_analysis_summary(self, pattern_analysis):
        """
        Generate a human-readable summary of pattern analysis.
        """
        if not pattern_analysis:
            return "No pattern improvements detected"
        
        summary_parts = []
        
        # Pattern reduction analysis
        if "pattern_reduction" in pattern_analysis:
            reduction = pattern_analysis["pattern_reduction"]
            summary_parts.append(f"Pattern reduction: {reduction['rate']:.1f}%")
        
        # Common violation analysis
        if "common_violations" in pattern_analysis:
            common = pattern_analysis["common_violations"]
            if common:
                top_patterns = list(common.keys())[:3]
                summary_parts.append(f"Top recurring patterns: {', '.join(top_patterns)}")
        
        # Improvement trends
        if "improvement_trends" in pattern_analysis:
            trends = pattern_analysis["improvement_trends"]
            if trends["consistent_improvement"]:
                summary_parts.append("Consistent improvement detected")
            else:
                summary_parts.append("Mixed improvement patterns")
        
        return "; ".join(summary_parts) if summary_parts else "Analysis complete"
    
    def post(self, shared, prep_res, exec_res):
        """
        Store learned patterns and prompt improvements for future use.
        """
        # Update shared store with learning results
        shared["pattern_learning"] = {
            "learned_patterns": exec_res["learned_patterns"],
            "prompt_improvements": exec_res["prompt_improvements"],
            "last_analysis": exec_res["analysis_summary"]
        }
        
        # Update brand voice with learned preferences
        if "prompt_improvements" in exec_res["prompt_improvements"]:
            # Apply learned style preferences
            learned_preferences = exec_res["prompt_improvements"].get("style_preferences", {})
            if learned_preferences:
                shared["brand_voice"]["style_preferences"].update(learned_preferences)
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("pattern_learning")
        shared["workflow_state"]["current_stage"] = "final_formatting"
        
        print(f"\nPattern learning completed!")
        print(f"Analysis summary: {exec_res['analysis_summary']}")
        
        # Show key learnings
        if exec_res["learned_patterns"]:
            print(f"\nKey Learnings:")
            if "pattern_reduction" in exec_res["learned_patterns"]:
                reduction = exec_res["learned_patterns"]["pattern_reduction"]
                print(f"  - Pattern reduction rate: {reduction['rate']:.1f}%")
            
            if "common_violations" in exec_res["learned_patterns"]:
                common = list(exec_res["learned_patterns"]["common_violations"].keys())[:3]
                if common:
                    print(f"  - Common violations: {', '.join(common)}")
        
        # Show prompt improvements
        if exec_res["prompt_improvements"]:
            print(f"\nPrompt Improvements:")
            improvements = exec_res["prompt_improvements"]
            if "avoid_patterns" in improvements:
                print(f"  - Avoid patterns: {len(improvements['avoid_patterns'])} items")
            if "positive_examples" in improvements:
                print(f"  - Positive examples: {len(improvements['positive_examples'])} items")
            if "style_guidance" in improvements:
                print(f"  - Style guidance: {improvements['style_guidance']}")
        
        # Save learning to presets for future use
        from utils.presets_manager import save_preset
        try:
            learning_preset = {
                "user_config": shared["user_config"],
                "task_requirements": shared["task_requirements"],
                "brand_voice": shared["brand_voice"],
                "pattern_learning": shared["pattern_learning"]
            }
            
            preset_id = save_preset(
                name=f"Learned_Preferences_{len(shared['version_history'])}_versions",
                preset_data=learning_preset,
                description="Auto-learned preferences from content generation"
            )
            print(f"  - Learning saved as preset: {preset_id}")
        except Exception as e:
            print(f"  - Note: Could not save learning as preset: {e}")
        
        return "continue"  # Go to final formatting

if __name__ == "__main__":
    # Test the node
    node = PatternLearnerNode()
    
    # Create test shared store with version history
    shared = {
        "version_history": [
            {
                "version_id": "v1",
                "timestamp": "2024-01-01T10:00:00Z",
                "violations_fixed": ["em_dash", "rhetorical_contrast"],
                "changes_made": ["removed_patterns", "improved_flow"],
                "content_pieces": {
                    "linkedin": {"text": "It's not just AI—this is a revolution! #AI"},
                    "twitter": {"tweet": "AI is transforming everything! #AI"}
                }
            },
            {
                "version_id": "v2",
                "timestamp": "2024-01-01T11:00:00Z",
                "violations_fixed": ["em_dash"],
                "changes_made": ["removed_em_dash", "enhanced_authenticity"],
                "content_pieces": {
                    "linkedin": {"text": "AI is transforming marketing in exciting ways. #AI"},
                    "twitter": {"tweet": "Exciting AI developments in marketing! #AI"}
                }
            }
        ],
        "quality_control": {
            "deadly_sins_violations": {
                "v1": {
                    "linkedin": {"total_violations": 2},
                    "twitter": {"total_violations": 1}
                },
                "v2": {
                    "linkedin": {"total_violations": 0},
                    "twitter": {"total_violations": 0}
                }
            },
            "revision_count": 1,
            "max_revisions_reached": False,
            "compliance_status": "pass"
        },
        "brand_voice": {
            "parsed_attributes": {
                "personality_traits": ["innovative", "professional"],
                "tone": "thought_leadership",
                "voice": "confident",
                "values": ["innovation", "excellence"],
                "themes": ["AI", "technology"]
            },
            "style_preferences": {
                "sentence_variety": "high",
                "transition_style": "natural",
                "ending_style": "inviting"
            }
        },
        "task_requirements": {
            "topic": "AI in marketing",
            "platforms": ["linkedin", "twitter"],
            "brand_bible_text": "Innovative marketing agency focused on AI and technology."
        },
        "user_config": {
            "individual_or_brand": "brand",
            "name": "TestBrand",
            "model": "openrouter/anthropic/claude-3.5-sonnet",
            "temperature": 0.7
        },
        "workflow_state": {
            "current_stage": "pattern_learning",
            "completed_stages": ["engagement", "brand_bible_processing", "format_guidelines", "creative_inspiration", "pattern_aware_prompt_engineering", "content_generation", "style_optimization", "deadly_sins_scanning", "style_compliance", "authenticity_scoring", "feedback_routing", "content_refinement"],
            "error_state": None
        }
    }
    
    print("Testing PatternLearnerNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    
    if "pattern_learning" in shared:
        print(f"Pattern learning results stored: {list(shared['pattern_learning'].keys())}")
        print(f"Analysis summary: {shared['pattern_learning']['last_analysis']}")
