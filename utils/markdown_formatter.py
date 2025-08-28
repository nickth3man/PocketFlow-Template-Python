from typing import Dict, List

def format_content_as_markdown(content_pieces: Dict, platforms: List[str] = None) -> str:
    """
    Format content pieces as markdown with platform sections and copy buttons.
    
    Args:
        content_pieces (Dict): Content pieces by platform
        platforms (List[str]): Optional list of platforms to include
        
    Returns:
        str: Formatted markdown content
    """
    if platforms is None:
        platforms = list(content_pieces.keys())
    
    markdown_content = "# Generated Content\n\n"
    
    platform_titles = {
        "email": "📧 Email",
        "linkedin": "💼 LinkedIn",
        "instagram": "📸 Instagram",
        "twitter": "🐦 Twitter",
        "reddit": "🤖 Reddit",
        "blog": "📝 Blog"
    }
    
    for platform in platforms:
        if platform not in content_pieces:
            continue
            
        title = platform_titles.get(platform, f"📱 {platform.title()}")
        markdown_content += f"## {title}\n\n"
        
        content = content_pieces[platform]
        
        # Format based on platform type
        if platform == "email":
            markdown_content += format_email_content(content)
        elif platform == "linkedin":
            markdown_content += format_linkedin_content(content)
        elif platform == "instagram":
            markdown_content += format_instagram_content(content)
        elif platform == "twitter":
            markdown_content += format_twitter_content(content)
        elif platform == "reddit":
            markdown_content += format_reddit_content(content)
        elif platform == "blog":
            markdown_content += format_blog_content(content)
        else:
            markdown_content += format_generic_content(content)
        
        # Add copy button placeholder (would be implemented in frontend)
        markdown_content += "\n<details>\n<summary>📋 Copy Content</summary>\n\n"
        markdown_content += "```\n"
        markdown_content += get_raw_content(content, platform)
        markdown_content += "\n```\n</details>\n\n"
    
    return markdown_content

def format_email_content(content: Dict) -> str:
    """Format email content."""
    result = ""
    
    if "subject" in content:
        result += f"**Subject:** {content['subject']}\n\n"
    
    if "body" in content:
        result += f"{content['body']}\n\n"
    
    if "cta" in content:
        result += f"**Call to Action:** {content['cta']}\n\n"
    
    return result

def format_linkedin_content(content: Dict) -> str:
    """Format LinkedIn content."""
    result = ""
    
    if "text" in content:
        result += f"{content['text']}\n\n"
    
    if "hashtags" in content and content["hashtags"]:
        hashtags = " ".join([f"#{tag}" for tag in content["hashtags"]])
        result += f"**Hashtags:** {hashtags}\n\n"
    
    return result

def format_instagram_content(content: Dict) -> str:
    """Format Instagram content."""
    result = ""
    
    if "caption" in content:
        result += f"{content['caption']}\n\n"
    
    if "hashtags" in content and content["hashtags"]:
        hashtags = " ".join([f"#{tag}" for tag in content["hashtags"]])
        result += f"**Hashtags:** {hashtags}\n\n"
    
    return result

def format_twitter_content(content: Dict) -> str:
    """Format Twitter content."""
    result = ""
    
    if "thread" in content:
        for i, tweet in enumerate(content["thread"], 1):
            result += f"**Tweet {i}:** {tweet}\n\n"
    elif "tweet" in content:
        result += f"{content['tweet']}\n\n"
    
    return result

def format_reddit_content(content: Dict) -> str:
    """Format Reddit content."""
    result = ""
    
    if "title" in content:
        result += f"**Title:** {content['title']}\n\n"
    
    if "body" in content:
        result += f"{content['body']}\n\n"
    
    return result

def format_blog_content(content: Dict) -> str:
    """Format blog content."""
    result = ""
    
    if "title" in content:
        result += f"# {content['title']}\n\n"
    
    if "body" in content:
        result += f"{content['body']}\n\n"
    
    return result

def format_generic_content(content: Dict) -> str:
    """Format generic content."""
    result = ""
    
    for key, value in content.items():
        if isinstance(value, list):
            result += f"**{key.title()}:** {', '.join(map(str, value))}\n\n"
        else:
            result += f"**{key.title()}:** {value}\n\n"
    
    return result

def get_raw_content(content: Dict, platform: str) -> str:
    """Get raw content for copying."""
    if platform == "email":
        parts = []
        if "subject" in content:
            parts.append(f"Subject: {content['subject']}")
        if "body" in content:
            parts.append(content["body"])
        if "cta" in content:
            parts.append(f"CTA: {content['cta']}")
        return "\n\n".join(parts)
    
    elif platform in ["linkedin", "instagram"]:
        parts = []
        if "text" in content:
            parts.append(content["text"])
        if "caption" in content:
            parts.append(content["caption"])
        if "hashtags" in content:
            parts.append(" ".join([f"#{tag}" for tag in content["hashtags"]]))
        return "\n\n".join(parts)
    
    elif platform == "twitter":
        if "thread" in content:
            return "\n\n---\n\n".join(content["thread"])
        elif "tweet" in content:
            return content["tweet"]
    
    elif platform == "reddit":
        parts = []
        if "title" in content:
            parts.append(f"Title: {content['title']}")
        if "body" in content:
            parts.append(content["body"])
        return "\n\n".join(parts)
    
    elif platform == "blog":
        parts = []
        if "title" in content:
            parts.append(f"# {content['title']}")
        if "body" in content:
            parts.append(content["body"])
        return "\n\n".join(parts)
    
    else:
        # Generic fallback
        lines = []
        for key, value in content.items():
            if isinstance(value, list):
                lines.append(f"{key}: {', '.join(map(str, value))}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)

def generate_copy_buttons_html(platforms: List[str]) -> str:
    """
    Generate HTML for copy buttons (for web interface).
    
    Args:
        platforms (List[str]): List of platforms
        
    Returns:
        str: HTML for copy buttons
    """
    html = "<div class='copy-buttons'>\n"
    
    for platform in platforms:
        html += f"  <button onclick='copyContent(\"{platform}\")' class='copy-btn'>\n"
        html += f"    Copy {platform.title()} Content\n"
        html += "  </button>\n"
    
    html += "</div>\n"
    return html

if __name__ == "__main__":
    # Test the markdown formatter
    test_content = {
        "email": {
            "subject": "Exciting AI Marketing Updates",
            "body": "Dear valued customer,\n\nWe're excited to share the latest developments in AI marketing...",
            "cta": "Learn more about our AI solutions"
        },
        "linkedin": {
            "text": "The future of marketing is here! AI is transforming how we connect with customers...",
            "hashtags": ["AI", "Marketing", "Innovation", "DigitalTransformation"]
        },
        "twitter": {
            "thread": [
                "AI is revolutionizing marketing! 🚀",
                "Here are 3 ways it's changing the game:",
                "1. Personalization at scale\n2. Real-time optimization\n3. Predictive analytics",
                "The future is now! #AI #Marketing"
            ]
        },
        "instagram": {
            "caption": "Behind the scenes of our AI marketing magic! ✨\n\n#AI #Marketing #Tech",
            "hashtags": ["AI", "Marketing", "Tech", "Innovation", "DigitalMarketing"]
        }
    }
    
    print("Testing markdown formatter...")
    
    # Format all content
    markdown = format_content_as_markdown(test_content)
    print(markdown)
    
    # Test raw content extraction
    print("\n" + "="*50)
    print("Raw content for copying:")
    print("="*50)
    
    for platform in ["email", "linkedin", "twitter"]:
        if platform in test_content:
            raw = get_raw_content(test_content[platform], platform)
            print(f"\n{platform.upper()}:")
            print(raw)
