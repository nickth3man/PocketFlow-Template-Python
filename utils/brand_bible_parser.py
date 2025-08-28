import re
from typing import Dict, List, Tuple

def parse_brand_bible(brand_text: str, individual_vs_brand: str) -> Tuple[Dict, Dict]:
    """
    Parse descriptive brand text into structured voice parameters.
    
    Args:
        brand_text (str): Descriptive text about brand voice, personality, values
        individual_vs_brand (str): "individual" or "brand"
    
    Returns:
        Tuple[Dict, Dict]: (structured_voice, tone_guidelines)
    """
    # Extract personality traits using common descriptors
    personality_indicators = {
        'curious': ['curious', 'inquisitive', 'exploratory', 'questioning'],
        'teacher': ['teacher', 'educator', 'instructor', 'guide', 'mentor'],
        'purposeful': ['purposeful', 'intentional', 'meaningful', 'driven'],
        'professional': ['professional', 'formal', 'corporate', 'business'],
        'confident': ['confident', 'assured', 'bold', 'assertive'],
        'friendly': ['friendly', 'approachable', 'warm', 'welcoming'],
        'innovative': ['innovative', 'creative', 'cutting-edge', 'forward-thinking'],
        'authentic': ['authentic', 'genuine', 'real', 'honest']
    }
    
    found_traits = []
    brand_text_lower = brand_text.lower()
    
    for trait, indicators in personality_indicators.items():
        if any(indicator in brand_text_lower for indicator in indicators):
            found_traits.append(trait)
    
    # Extract tone and voice indicators
    tone_indicators = {
        'professional': ['professional', 'formal', 'corporate'],
        'casual': ['casual', 'relaxed', 'informal', 'easy-going'],
        'conversational': ['conversational', 'chat', 'talk', 'speak'],
        'thought_leadership': ['thought leader', 'expert', 'authority', 'insight'],
        'engaging': ['engaging', 'interactive', 'participatory', 'inviting'],
        'authoritative': ['authoritative', 'definitive', 'expert', 'commanding']
    }
    
    found_tone = 'professional'  # default
    for tone, indicators in tone_indicators.items():
        if any(indicator in brand_text_lower for indicator in indicators):
            found_tone = tone
            break
    
    # Extract values and themes
    value_indicators = {
        'innovation': ['innovation', 'innovate', 'creative', 'new'],
        'education': ['education', 'learn', 'teach', 'knowledge'],
        'transparency': ['transparent', 'open', 'honest', 'clear'],
        'excellence': ['excellence', 'excellent', 'quality', 'superior'],
        'community': ['community', 'together', 'collective', 'shared'],
        'growth': ['growth', 'grow', 'develop', 'improve']
    }
    
    found_values = []
    for value, indicators in value_indicators.items():
        if any(indicator in brand_text_lower for indicator in indicators):
            found_values.append(value)
    
    # Extract themes from the text
    theme_keywords = ['AI', 'technology', 'digital', 'marketing', 'brand', 'content', 'social', 'media']
    found_themes = []
    for theme in theme_keywords:
        if theme.lower() in brand_text_lower:
            found_themes.append(theme)
    
    structured_voice = {
        "personality_traits": found_traits if found_traits else ["professional", "helpful"],
        "tone": found_tone,
        "voice": "confident" if "confident" in found_traits else "professional",
        "values": found_values if found_values else ["quality", "integrity"],
        "themes": found_themes if found_themes else ["content creation", "brand strategy"]
    }
    
    # Style preferences based on personality traits
    style_preferences = {
        "sentence_variety": "high" if "creative" in found_traits else "medium",
        "transition_style": "natural",
        "ending_style": "challenging" if "thought_leadership" in found_tone else "inviting"
    }
    
    structured_voice["style_preferences"] = style_preferences
    
    # Tone guidelines for different platforms
    tone_guidelines = {
        "email": found_tone,
        "linkedin": "thought_leadership" if "thought_leadership" in found_tone else "professional",
        "instagram": "engaging" if "engaging" in found_tone else "casual",
        "twitter": "conversational" if "conversational" in found_tone else "casual",
        "reddit": "community_appropriate",
        "blog": "authoritative" if "authoritative" in found_tone else "professional"
    }
    
    return structured_voice, tone_guidelines

if __name__ == "__main__":
    # Test the function
    test_text = "We are a innovative marketing agency that values education and transparency. Our brand voice is confident and professional, focusing on AI empowerment and skill development."
    structured, guidelines = parse_brand_bible(test_text, "brand")
    print("Structured Voice:", structured)
    print("Tone Guidelines:", guidelines)
