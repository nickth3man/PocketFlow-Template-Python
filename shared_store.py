"""
Shared store management for the content generation system.
This module provides utilities for initializing and managing the shared store.
"""

def initialize_shared_store():
    """
    Initialize the shared store with default values.
    """
    return {
        "user_config": {
            "individual_or_brand": "individual",  # or "brand"
            "name": "",
            "brand_name": None,
            "model": "openrouter/anthropic/claude-3.5-sonnet",
            "temperature": 0.7
        },
        "task_requirements": {
            "topic": "",
            "platforms": ["email", "linkedin", "instagram", "twitter", "reddit", "blog"],
            "brand_bible_text": ""
        },
        "brand_voice": {
            "parsed_attributes": {
                "personality_traits": [],
                "tone": "professional",
                "voice": "confident", 
                "values": [],
                "themes": []
            },
            "forbidden_patterns": {
                "em_dash": {"pattern": "—", "severity": "critical"},
                "rhetorical_contrast": {"pattern": r"It's not just .+; it's .+", "severity": "critical"},
                "antithesis": {"pattern": r"It's not .+; it's .+", "severity": "critical"},
                "paradiastole": {"pattern": r"It's not .+; it's .+", "severity": "critical"},
                "reframing_contrast": {"pattern": r"It's not just .+; it's .+", "severity": "critical"},
                "chiasmus": {"pattern": r"It's not what .+ to .+; it's what .+ with .+", "severity": "critical"},
                "tagline_frame": {"pattern": r"It's not just .+; it's .+", "severity": "critical"}
            },
            "style_preferences": {
                "sentence_variety": "high",
                "transition_style": "natural",
                "ending_style": "challenging"
            }
        },
        "platform_guidelines": {
            "email": {
                "char_limit": 500,
                "structure": ["subject", "greeting", "body", "cta", "signature"],
                "tone_adjustment": "professional"
            },
            "linkedin": {
                "char_limit": 3000,
                "reveal_cutoff": 210,
                "hashtag_count": 3,
                "tone_adjustment": "thought_leadership"
            },
            "instagram": {
                "char_limit": 2200,
                "reveal_cutoff": 125,
                "hashtag_count": [8, 20],
                "tone_adjustment": "engaging"
            },
            "twitter": {
                "char_limit": 280,
                "thread_threshold": 240,
                "hashtag_count": [0, 3],
                "tone_adjustment": "conversational"
            },
            "reddit": {
                "char_limit": 40000,
                "style_hints": {},
                "tone_adjustment": "community_appropriate"
            },
            "blog": {
                "target_words": 1200,
                "structure": "deep_headings",
                "tone_adjustment": "authoritative"
            }
        },
        "creative_inspiration": {
            "examples": [],
            "source_platforms": []
        },
        "content_pieces": {},
        "quality_control": {
            "deadly_sins_violations": {},
            "revision_count": 0,
            "max_revisions_reached": False,
            "compliance_status": "pending",
            "authenticity_scores": {}
        },
        "version_history": [],
        "feedback_state": {
            "awaiting_feedback": False,
            "feedback_type": None,  # "sentence_edit", "general_refinement", "done"
            "user_input": "",
            "selected_content": {}
        },
        "workflow_state": {
            "current_stage": "engagement",
            "completed_stages": [],
            "error_state": None
        },
        "pattern_learning": {
            "learned_patterns": {},
            "prompt_improvements": {},
            "last_analysis": ""
        },
        "authenticity_results": {},
        "roi_analysis": {},
        "final_output": {},
        "analytics_report": {},
        "optimized_preset": {}
    }

def update_shared_store(shared, updates):
    """
    Update the shared store with new values.
    
    Args:
        shared (dict): The shared store dictionary
        updates (dict): Dictionary of updates to apply
    
    Returns:
        dict: Updated shared store
    """
    for key, value in updates.items():
        if key in shared and isinstance(shared[key], dict) and isinstance(value, dict):
            # Merge dictionaries
            shared[key].update(value)
        else:
            # Replace value
            shared[key] = value
    return shared

def get_shared_value(shared, key_path, default=None):
    """
    Get a value from the shared store using dot notation path.
    
    Args:
        shared (dict): The shared store dictionary
        key_path (str): Dot-separated path to the value (e.g., "user_config.name")
        default: Default value if key not found
    
    Returns:
        The value at the specified path or default
    """
    keys = key_path.split('.')
    current = shared
    
    try:
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return default

def set_shared_value(shared, key_path, value):
    """
    Set a value in the shared store using dot notation path.
    
    Args:
        shared (dict): The shared store dictionary
        key_path (str): Dot-separated path to the value (e.g., "user_config.name")
        value: Value to set
    
    Returns:
        bool: True if successful, False otherwise
    """
    keys = key_path.split('.')
    current = shared
    
    try:
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set the final value
        current[keys[-1]] = value
        return True
    except (KeyError, TypeError):
        return False

if __name__ == "__main__":
    # Test the shared store functions
    print("Testing shared store utilities...")
    
    # Initialize shared store
    shared = initialize_shared_store()
    print(f"Shared store initialized with keys: {list(shared.keys())}")
    
    # Test updates
    updates = {
        "user_config": {"name": "Test User"},
        "task_requirements": {"topic": "AI Marketing"}
    }
    shared = update_shared_store(shared, updates)
    print(f"User name: {shared['user_config']['name']}")
    print(f"Task topic: {shared['task_requirements']['topic']}")
    
    # Test get/set with dot notation
    name = get_shared_value(shared, "user_config.name")
    print(f"Name via dot notation: {name}")
    
    set_shared_value(shared, "user_config.temperature", 0.8)
    temp = get_shared_value(shared, "user_config.temperature")
    print(f"Temperature via dot notation: {temp}")
