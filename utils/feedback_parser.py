import re
from typing import Dict, Tuple

def parse_user_feedback(user_feedback: str, content_pieces: Dict) -> Tuple[Dict, str]:
    """
    Parse user feedback into actionable content modifications.
    
    Args:
        user_feedback (str): User feedback text
        content_pieces (Dict): Current content pieces
        
    Returns:
        Tuple[Dict, str]: (edit_instructions, edit_type)
    """
    feedback_lower = user_feedback.lower()
    
    # Determine feedback type
    if any(word in feedback_lower for word in ["done", "finish", "complete", "looks good"]):
        return {}, "done"
    elif any(word in feedback_lower for word in ["edit", "change", "modify", "fix", "shorter", "longer"]):
        edit_type = "sentence_edit"
    else:
        edit_type = "general_refinement"
    
    # Extract specific edit instructions
    edit_instructions = {}
    
    # Look for platform-specific feedback
    platforms = list(content_pieces.keys()) if content_pieces else ["general"]
    
    for platform in platforms:
        platform_feedback = _extract_platform_feedback(user_feedback, platform)
        if platform_feedback:
            edit_instructions[platform] = {
                "feedback": platform_feedback,
                "current_content": content_pieces.get(platform, {}) if content_pieces else {}
            }
    
    # If no platform-specific feedback found, apply to all
    if not edit_instructions and content_pieces:
        for platform in content_pieces.keys():
            edit_instructions[platform] = {
                "feedback": user_feedback,
                "current_content": content_pieces[platform]
            }
    elif not edit_instructions:
        # General feedback without content context
        edit_instructions["general"] = {
            "feedback": user_feedback,
            "current_content": {}
        }
    
    return edit_instructions, edit_type

def _extract_platform_feedback(feedback: str, platform: str) -> str:
    """
    Extract platform-specific feedback from general feedback.
    
    Args:
        feedback (str): General feedback text
        platform (str): Platform name
        
    Returns:
        str: Platform-specific feedback or empty string
    """
    # Look for platform mentions in feedback
    platform_patterns = {
        "linkedin": [r"linkedin", r"linked in"],
        "twitter": [r"twitter", r"tweet", r"X"],
        "email": [r"email", r"mail"],
        "instagram": [r"instagram", r"ig", r"insta"],
        "reddit": [r"reddit", r"post"],
        "blog": [r"blog", r"article", r"post"]
    }
    
    if platform in platform_patterns:
        patterns = platform_patterns[platform]
        for pattern in patterns:
            if re.search(pattern, feedback, re.IGNORECASE):
                # Extract sentence containing the platform mention
                sentences = re.split(r'[.!?]+', feedback)
                for sentence in sentences:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        return sentence.strip()
    
    return ""

def categorize_feedback(feedback: str) -> Dict:
    """
    Categorize feedback into different types for better processing.
    
    Args:
        feedback (str): User feedback
        
    Returns:
        Dict: Feedback categorization
    """
    categories = {
        "tone": ["tone", "sound", "voice", "style", "formal", "casual"],
        "length": ["long", "short", "length", "brief", "concise", "wordy"],
        "content": ["content", "message", "point", "idea", "topic"],
        "structure": ["structure", "format", "organization", "flow"],
        "grammar": ["grammar", "spelling", "typo", "error"],
        "engagement": ["engage", "hook", "interest", "click", "like"],
        "brand": ["brand", "voice", "personality", "value"],
        "platform": ["linkedin", "twitter", "email", "instagram", "reddit", "blog"]
    }
    
    feedback_lower = feedback.lower()
    identified_categories = []
    
    for category, keywords in categories.items():
        if any(keyword in feedback_lower for keyword in keywords):
            identified_categories.append(category)
    
    # Determine urgency/sentiment
    positive_indicators = ["good", "great", "excellent", "perfect", "love", "like"]
    negative_indicators = ["bad", "terrible", "awful", "hate", "dislike", "wrong", "fix"]
    
    sentiment = "neutral"
    if any(indicator in feedback_lower for indicator in positive_indicators):
        sentiment = "positive"
    elif any(indicator in feedback_lower for indicator in negative_indicators):
        sentiment = "negative"
    
    return {
        "categories": identified_categories,
        "sentiment": sentiment,
        "word_count": len(feedback.split()),
        "has_specific_requests": any(char in feedback for char in ["?", "!", "please", "could you"])
    }

if __name__ == "__main__":
    # Test the feedback parser
    test_feedback = "The LinkedIn post is too long and sounds too corporate. Can you make it more conversational? The Twitter version looks good though."
    
    test_content = {
        "linkedin": {
            "text": "Our innovative AI solution represents a paradigm shift in marketing technology...",
            "hashtags": ["#AI", "#Marketing", "#Innovation"]
        },
        "twitter": {
            "tweet": "AI is transforming marketing! #AI #Marketing"
        }
    }
    
    print("Testing feedback parser...")
    print(f"Feedback: {test_feedback}")
    
    # Parse feedback
    instructions, edit_type = parse_user_feedback(test_feedback, test_content)
    print(f"\nEdit type: {edit_type}")
    print(f"Instructions: {instructions}")
    
    # Categorize feedback
    categories = categorize_feedback(test_feedback)
    print(f"\nCategories: {categories}")
    
    # Test different feedback types
    test_cases = [
        "This is perfect, I'm done!",
        "Make the email shorter and add more emojis",
        "The tone feels off, can you make it more professional?",
        "Great job on the blog post!"
    ]
    
    print("\nTesting different feedback types:")
    for feedback in test_cases:
        instructions, edit_type = parse_user_feedback(feedback, test_content)
        categories = categorize_feedback(feedback)
        print(f"\nFeedback: '{feedback}'")
        print(f"  Type: {edit_type}")
        print(f"  Categories: {categories['categories']}")
        print(f"  Sentiment: {categories['sentiment']}")
