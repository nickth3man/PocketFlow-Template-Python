from typing import Dict, List

def get_platform_guidelines(platform: str, brand_voice: Dict, topic: str) -> Dict:
    """
    Generate platform-specific formatting guidelines and constraints.
    
    Args:
        platform (str): Target platform (email, linkedin, instagram, twitter, reddit, blog)
        brand_voice (Dict): Brand voice parameters
        topic (str): Content topic
        
    Returns:
        Dict: Platform-specific formatting guidelines
    """
    base_guidelines = {
        "topic": topic,
        "brand_voice": brand_voice
    }
    
    platform_configs = {
        "email": {
            "char_limit": 500,
            "structure": ["subject", "greeting", "body", "cta", "signature"],
            "tone_adjustment": "professional",
            "best_practices": [
                "Clear subject line",
                "Personal greeting when possible",
                "Concise main message",
                "Single clear call-to-action",
                "Professional signature"
            ]
        },
        "linkedin": {
            "char_limit": 3000,
            "reveal_cutoff": 210,
            "hashtag_count": 3,
            "tone_adjustment": "thought_leadership",
            "best_practices": [
                "Hook in first 210 characters",
                "Professional yet conversational",
                "Include relevant hashtags (3-5)",
                "Tag relevant people/companies when appropriate",
                "End with engaging question or CTA"
            ]
        },
        "instagram": {
            "char_limit": 2200,
            "reveal_cutoff": 125,
            "hashtag_count": [8, 20],
            "tone_adjustment": "engaging",
            "best_practices": [
                "Hook in first 125 characters",
                "Visual storytelling",
                "Use emojis appropriately",
                "Include 8-20 relevant hashtags",
                "Encourage engagement with questions"
            ]
        },
        "twitter": {
            "char_limit": 280,
            "thread_threshold": 240,
            "hashtag_count": [0, 3],
            "tone_adjustment": "conversational",
            "best_practices": [
                "Clear, concise messaging",
                "Use threads for complex topics",
                "Include 0-3 relevant hashtags",
                "Engage with trending topics when relevant",
                "Use polls or questions for engagement"
            ]
        },
        "reddit": {
            "char_limit": 40000,
            "style_hints": {
                "community_specific": True,
                "detailed_explanations": True,
                "authentic_tone": True
            },
            "tone_adjustment": "community_appropriate",
            "best_practices": [
                "Follow community rules and culture",
                "Provide detailed, valuable content",
                "Be authentic and transparent",
                "Engage in genuine discussion",
                "Avoid obvious self-promotion"
            ]
        },
        "blog": {
            "target_words": 1200,
            "structure": "deep_headings",
            "tone_adjustment": "authoritative",
            "best_practices": [
                "Clear, keyword-rich title",
                "Compelling introduction",
                "Well-structured with headings",
                "Include data/examples when possible",
                "Strong conclusion with takeaway"
            ]
        }
    }
    
    if platform in platform_configs:
        guidelines = base_guidelines.copy()
        guidelines.update(platform_configs[platform])
        
        # Adjust tone based on brand voice
        if brand_voice and "tone" in brand_voice:
            brand_tone = brand_voice["tone"]
            # Override with brand tone if it's more specific
            if brand_tone != "professional":  # professional is default
                guidelines["tone_adjustment"] = brand_tone
        
        return guidelines
    else:
        # Return default guidelines for unknown platforms
        return {
            **base_guidelines,
            "char_limit": 1000,
            "tone_adjustment": brand_voice.get("tone", "professional") if brand_voice else "professional",
            "best_practices": ["Be clear and concise", "Maintain brand voice", "Engage the audience"]
        }

def get_multiple_platform_guidelines(platforms: List[str], brand_voice: Dict, topic: str) -> Dict:
    """
    Generate formatting guidelines for multiple platforms.
    
    Args:
        platforms (List[str]): List of target platforms
        brand_voice (Dict): Brand voice parameters
        topic (str): Content topic
        
    Returns:
        Dict: Guidelines for all requested platforms
    """
    all_guidelines = {}
    for platform in platforms:
        all_guidelines[platform] = get_platform_guidelines(platform, brand_voice, topic)
    return all_guidelines

if __name__ == "__main__":
    # Test the formatter
    test_brand_voice = {
        "personality_traits": ["innovative", "educational"],
        "tone": "thought_leadership",
        "voice": "confident",
        "values": ["innovation", "education"],
        "themes": ["AI empowerment", "skill development"]
    }
    
    platforms = ["linkedin", "twitter", "email"]
    topic = "The future of AI in marketing"
    
    guidelines = get_multiple_platform_guidelines(platforms, test_brand_voice, topic)
    
    for platform, guide in guidelines.items():
        print(f"\n{platform.upper()} Guidelines:")
        print(f"  Character limit: {guide.get('char_limit', 'N/A')}")
        print(f"  Tone: {guide.get('tone_adjustment', 'N/A')}")
        if 'best_practices' in guide:
            print("  Best practices:")
            for practice in guide['best_practices']:
                print(f"    - {practice}")
