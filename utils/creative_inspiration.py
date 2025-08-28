from typing import Dict, List
from utils.call_llm import call_llm

def generate_creative_inspiration(topic: str, platform: str, brand_voice: Dict) -> List[str]:
    """
    Generate high-engagement content examples without external web searches.
    
    Args:
        topic (str): Content topic
        platform (str): Target platform
        brand_voice (Dict): Brand voice parameters
        
    Returns:
        List[str]: List of creative inspiration examples
    """
    # Create a prompt that generates platform-specific, brand-aligned examples
    brand_traits = ", ".join(brand_voice.get("personality_traits", ["professional"]))
    brand_tone = brand_voice.get("tone", "professional")
    brand_values = ", ".join(brand_voice.get("values", ["quality"]))
    
    prompt = f"""Generate 3 high-engagement content examples for {platform} about "{topic}".
    
Brand Voice: {brand_traits} with {brand_tone} tone, valuing {brand_values}.

For each example, provide:
1. A compelling hook or opening line
2. The main content approach
3. An engaging closing or call-to-action

Make the examples authentic and platform-appropriate. Focus on what resonates with {platform} audiences.

Format each example as a single paragraph."""

    try:
        response = call_llm(prompt)
        # Split the response into examples
        examples = [example.strip() for example in response.split("\n\n") if example.strip()]
        return examples[:3]  # Return up to 3 examples
    except Exception as e:
        print(f"Error generating creative inspiration: {e}")
        # Return fallback examples
        return [
            f"Explore {topic} in a way that resonates with your audience.",
            f"Share your unique perspective on {topic} with engaging storytelling.",
            f"Spark conversation about {topic} by asking thought-provoking questions."
        ]

def get_platform_style_hints(platform: str, brand_voice: Dict) -> Dict:
    """
    Get platform-specific style hints for content creation.
    
    Args:
        platform (str): Target platform
        brand_voice (Dict): Brand voice parameters
        
    Returns:
        Dict: Style hints for the platform
    """
    platform_hints = {
        "email": {
            "structure": "Subject → Greeting → Main Content → CTA → Signature",
            "tone": "Direct and professional",
            "length": "Keep under 200 words for main content",
            "engagement": "Clear single call-to-action"
        },
        "linkedin": {
            "structure": "Hook → Insight → Value → Engagement Question",
            "tone": "Thought leadership with accessibility",
            "length": "200-1000 words for optimal engagement",
            "engagement": "End with question to encourage comments"
        },
        "instagram": {
            "structure": "Visual hook → Story → Value → Call-to-action",
            "tone": "Conversational and visually-driven",
            "length": "100-300 words with strong visual component",
            "engagement": "Use emojis and hashtags strategically"
        },
        "twitter": {
            "structure": "Strong opening → Key insight → Engagement hook",
            "tone": "Concise and conversational",
            "length": "Single tweet or thread of 3-5 tweets",
            "engagement": "Include question, poll, or trending hashtag"
        },
        "reddit": {
            "structure": "Genuine introduction → Detailed insight → Community value",
            "tone": "Authentic and community-focused",
            "length": "As detailed as needed for the community",
            "engagement": "Encourage discussion and provide real value"
        },
        "blog": {
            "structure": "Compelling title → Introduction → Headings → Conclusion",
            "tone": "Authoritative yet approachable",
            "length": "1000+ words with proper structure",
            "engagement": "Include actionable insights and examples"
        }
    }
    
    hints = platform_hints.get(platform, {
        "structure": "Clear and engaging",
        "tone": brand_voice.get("tone", "professional"),
        "length": "Appropriate for audience",
        "engagement": "Encourage interaction"
    })
    
    # Customize hints based on brand voice
    if brand_voice:
        hints["tone"] = f"{hints['tone']} with {brand_voice.get('tone', 'professional')} brand voice"
        
    return hints

if __name__ == "__main__":
    # Test the creative inspiration generator
    test_brand_voice = {
        "personality_traits": ["innovative", "educational"],
        "tone": "thought_leadership",
        "voice": "confident",
        "values": ["innovation", "education"],
        "themes": ["AI empowerment", "skill development"]
    }
    
    topic = "The future of AI in marketing"
    platform = "linkedin"
    
    print(f"Generating creative inspiration for {platform} about '{topic}'...")
    
    examples = generate_creative_inspiration(topic, platform, test_brand_voice)
    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}:")
        print(example)
    
    print(f"\n\nPlatform Style Hints for {platform}:")
    hints = get_platform_style_hints(platform, test_brand_voice)
    for key, value in hints.items():
        print(f"  {key}: {value}")
