from pocketflow import Node
from utils.call_llm import call_llm

class ContentGeneratorNode(Node):
    """
    Generate initial content drafts for each platform.
    Fifth node that creates the actual content using enhanced prompts.
    """
    
    def __init__(self, max_retries=2, wait=5):
        """
        Initialize with retry parameters for robust content generation.
        """
        super().__init__(max_retries=max_retries, wait=wait)
    
    def prep(self, shared):
        """
        Read topic, brand_voice, platform_guidelines, and enhanced prompts from shared store.
        """
        return {
            "topic": shared["task_requirements"]["topic"],
            "brand_voice": shared["brand_voice"]["parsed_attributes"],
            "platform_guidelines": shared["platform_guidelines"],
            "enhanced_prompts": shared["enhanced_prompts"],
            "platforms": shared["task_requirements"]["platforms"],
            "model": shared["user_config"]["model"],
            "temperature": shared["user_config"]["temperature"]
        }
    
    def exec(self, prep_res):
        """
        Generate platform-optimized content using LLM with explicit instructions to avoid all 7 deadly sins.
        """
        platforms = prep_res["platforms"]
        model = prep_res["model"]
        temperature = prep_res["temperature"]
        
        content_pieces = {}
        
        for platform in platforms:
            if platform not in prep_res["enhanced_prompts"]:
                print(f"Warning: No enhanced prompt found for {platform}")
                continue
            
            prompt = prep_res["enhanced_prompts"][platform]["prompt"]
            
            try:
                # Generate content using LLM
                response = call_llm(
                    prompt=prompt,
                    model=model,
                    temperature=temperature,
                    use_cache=False  # Don't cache content generation
                )
                
                # Format content based on platform type
                formatted_content = self._format_content_for_platform(response, platform, prep_res)
                content_pieces[platform] = formatted_content
                
                print(f"Generated content for {platform} ({len(response)} chars)")
                
            except Exception as e:
                print(f"Error generating content for {platform}: {e}")
                # Create fallback content
                content_pieces[platform] = self._create_fallback_content(platform, prep_res)
        
        return content_pieces
    
    def _format_content_for_platform(self, content_text, platform, prep_res):
        """
        Format the generated content appropriately for each platform.
        """
        guidelines = prep_res["platform_guidelines"].get(platform, {})
        char_limit = guidelines.get("char_limit", 1000)
        
        # Truncate if necessary
        if len(content_text) > char_limit:
            content_text = content_text[:char_limit].rsplit(' ', 1)[0] + '...'
        
        # Platform-specific formatting
        if platform == "email":
            # Split into subject and body
            lines = content_text.split('\n')
            subject = lines[0].strip() if lines else "Subject Line"
            body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else content_text
            return {
                "subject": subject,
                "body": body
            }
        
        elif platform == "linkedin":
            # Extract potential hashtags and format
            hashtags = self._extract_hashtags(content_text)
            text = self._remove_hashtags(content_text)
            return {
                "text": text.strip(),
                "hashtags": hashtags
            }
        
        elif platform == "instagram":
            # Similar to LinkedIn
            hashtags = self._extract_hashtags(content_text)
            caption = self._remove_hashtags(content_text)
            return {
                "caption": caption.strip(),
                "hashtags": hashtags
            }
        
        elif platform == "twitter":
            # Check if it should be a thread
            if len(content_text) > 240 or content_text.count('\n') > 2:
                tweets = self._split_into_tweets(content_text)
                return {"thread": tweets}
            else:
                return {"tweet": content_text.strip()}
        
        elif platform == "reddit":
            # Split into title and body
            lines = content_text.split('\n')
            title = lines[0].strip() if lines else "Discussion Title"
            body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else content_text
            return {
                "title": title,
                "body": body
            }
        
        elif platform == "blog":
            # Split into title and body
            lines = content_text.split('\n')
            title = lines[0].strip() if lines else "Blog Post Title"
            body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else content_text
            return {
                "title": title,
                "body": body
            }
        
        else:
            # Generic format
            return {"content": content_text.strip()}
    
    def _extract_hashtags(self, text):
        """
        Extract hashtags from text.
        """
        import re
        hashtags = re.findall(r'#\w+', text)
        return hashtags[:10]  # Limit to 10 hashtags
    
    def _remove_hashtags(self, text):
        """
        Remove hashtags from text.
        """
        import re
        return re.sub(r'#\w+', '', text).strip()
    
    def _split_into_tweets(self, text):
        """
        Split long text into tweet thread.
        """
        # Simple splitting - in reality, this would be more sophisticated
        sentences = text.split('. ')
        tweets = []
        current_tweet = ""
        
        for sentence in sentences:
            if len(current_tweet + sentence) < 240:
                current_tweet += sentence + ". "
            else:
                if current_tweet:
                    tweets.append(current_tweet.strip())
                current_tweet = sentence + ". "
                
                # Limit to 5 tweets
                if len(tweets) >= 4:
                    break
        
        if current_tweet and len(tweets) < 5:
            tweets.append(current_tweet.strip())
        
        return tweets[:5]  # Max 5 tweets
    
    def _create_fallback_content(self, platform, prep_res):
        """
        Create fallback content when LLM generation fails.
        """
        topic = prep_res["topic"]
        brand_voice = prep_res["brand_voice"]
        
        brand_name = brand_voice.get("brand_name", "We")
        tone = brand_voice.get("tone", "professional")
        
        fallbacks = {
            "email": {
                "subject": f"Thoughts on {topic}",
                "body": f"Hi there,\n\n{brand_name} wanted to share some thoughts on {topic}. We believe this is an important topic that deserves attention.\n\nBest regards,\n{brand_name}"
            },
            "linkedin": {
                "text": f"Excited to share some thoughts on {topic}. This is a topic that {brand_name.lower()} believes is crucial for our industry's future.",
                "hashtags": ["#IndustryInsights", "#ThoughtLeadership"]
            },
            "twitter": {
                "tweet": f"Thinking about {topic}? It's a crucial topic for our industry. What are your thoughts? #{'ThoughtLeadership' if 'thought' in tone else 'Industry'}"
            },
            "instagram": {
                "caption": f"Behind the scenes thinking about {topic}. What do you think about this important issue?",
                "hashtags": ["#IndustryInsights", "#BehindTheScenes"]
            },
            "reddit": {
                "title": f"What are your thoughts on {topic}?",
                "body": f"{brand_name} has been thinking about {topic} lately. We'd love to hear the community's perspective on this important issue."
            },
            "blog": {
                "title": f"Exploring {topic}: Key Insights and Perspectives",
                "body": f"## Introduction\n\n{topic} is an increasingly important subject in our industry. In this post, we'll explore key insights and perspectives.\n\n## Main Content\n\n[Detailed content would go here]\n\n## Conclusion\n\n{topic} continues to evolve, and we're excited to be part of the conversation."
            }
        }
        
        return fallbacks.get(platform, {"content": f"Content about {topic}"})
    
    def post(self, shared, prep_res, exec_res):
        """
        Write content_pieces to shared store.
        """
        # Update shared store with generated content
        shared["content_pieces"] = exec_res
        
        # Initialize quality control structure for each platform
        shared["quality_control"]["deadly_sins_violations"] = {
            platform: {
                "em_dash": {"count": 0, "positions": []},
                "rhetorical_contrast": {"count": 0, "positions": []},
                "antithesis": {"count": 0, "positions": []},
                "paradiastole": {"count": 0, "positions": []},
                "reframing_contrast": {"count": 0, "positions": []},
                "chiasmus": {"count": 0, "positions": []},
                "tagline_frame": {"count": 0, "positions": []}
            }
            for platform in exec_res.keys()
        }
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("content_generation")
        shared["workflow_state"]["current_stage"] = "style_optimization"
        
        print(f"\nContent generated for platforms: {', '.join(exec_res.keys())}")
        
        # Show content summary
        for platform, content in exec_res.items():
            if isinstance(content, dict):
                print(f"  {platform.title()}: {len(str(content))} chars")
            else:
                print(f"  {platform.title()}: {len(str(content))} chars")
        
        return "default"  # Go to next node

if __name__ == "__main__":
    # Test the node
    node = ContentGeneratorNode()
    
    # Create test shared store
    shared = {
        "task_requirements": {
            "topic": "The future of AI in marketing",
            "platforms": ["linkedin", "twitter"]
        },
        "user_config": {
            "model": "openrouter/anthropic/claude-3.5-sonnet",
            "temperature": 0.7
        },
        "brand_voice": {
            "parsed_attributes": {
                "personality_traits": ["innovative", "educational"],
                "tone": "thought_leadership",
                "voice": "confident",
                "values": ["innovation", "education"],
                "themes": ["AI empowerment", "skill development"]
            }
        },
        "platform_guidelines": {
            "linkedin": {
                "char_limit": 3000,
                "tone_adjustment": "thought_leadership"
            },
            "twitter": {
                "char_limit": 280,
                "tone_adjustment": "conversational"
            }
        },
        "enhanced_prompts": {
            "linkedin": {
                "prompt": "Create LinkedIn content about AI in marketing...",
                "char_limit": 3000
            },
            "twitter": {
                "prompt": "Create Twitter content about AI in marketing...",
                "char_limit": 280
            }
        },
        "workflow_state": {
            "current_stage": "content_generation",
            "completed_stages": ["engagement", "brand_bible_processing", "format_guidelines", "creative_inspiration", "pattern_aware_prompt_engineering"],
            "error_state": None
        }
    }
    
    print("Testing ContentGeneratorNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    print(f"Content pieces keys: {list(shared['content_pieces'].keys())}")
    
    if shared['content_pieces']:
        first_platform = list(shared['content_pieces'].keys())[0]
        print(f"Sample content for {first_platform}: {shared['content_pieces'][first_platform]}")
