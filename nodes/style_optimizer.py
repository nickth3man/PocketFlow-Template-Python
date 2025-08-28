from pocketflow import Node
from utils.content_sanitizer import sanitize_content
from utils.deadly_sins_detector import detect_deadly_sins

class StyleOptimizerNode(Node):
    """
    Merged node for initial cleanup, brand voice enforcement, and AI pattern removal.
    Sixth node that optimizes content style while maintaining brand voice.
    """
    
    def prep(self, shared):
        """
        Read content_pieces and brand_voice from shared store.
        """
        return {
            "content_pieces": shared["content_pieces"],
            "brand_voice": shared["brand_voice"],
            "platform_guidelines": shared["platform_guidelines"]
        }
    
    def exec(self, prep_res):
        """
        Apply conservative edits to improve style while maintaining brand voice and avoiding deadly sins.
        """
        content_pieces = prep_res["content_pieces"]
        brand_voice = prep_res["brand_voice"]
        platform_guidelines = prep_res["platform_guidelines"]
        
        optimized_content = {}
        optimization_log = {}
        
        for platform, content in content_pieces.items():
            print(f"Optimizing content for {platform}...")
            
            try:
                # Get platform-specific guidelines
                guidelines = platform_guidelines.get(platform, {})
                
                # First, detect deadly sins in the content
                content_text = self._get_content_text(content, platform)
                violations = detect_deadly_sins(content_text)
                
                # Store violations for quality control
                optimization_log[platform] = {
                    "initial_violations": violations,
                    "violations_fixed": [],
                    "changes_made": []
                }
                
                # Sanitize content to remove deadly sins while preserving brand voice
                sanitized_result = sanitize_content(content_text, violations, brand_voice)
                optimized_text = sanitized_result["sanitized_text"]
                transformation_log = sanitized_result["transformation_log"]
                
                # Update optimization log
                optimization_log[platform]["violations_fixed"] = list(transformation_log.keys())
                optimization_log[platform]["changes_made"] = list(transformation_log.values())
                
                # Format back to platform-specific structure
                formatted_content = self._format_back_to_platform(optimized_text, content, platform, guidelines)
                optimized_content[platform] = formatted_content
                
                print(f"  - Fixed {len(violations)} violations")
                print(f"  - Applied {len(transformation_log)} transformations")
                
            except Exception as e:
                print(f"Error optimizing content for {platform}: {e}")
                # Keep original content if optimization fails
                optimized_content[platform] = content
        
        return {
            "optimized_content": optimized_content,
            "optimization_log": optimization_log
        }
    
    def _get_content_text(self, content, platform):
        """
        Extract text content from platform-specific structure.
        """
        if isinstance(content, str):
            return content
        elif isinstance(content, dict):
            if platform == "email":
                return f"{content.get('subject', '')}\n\n{content.get('body', '')}"
            elif platform in ["linkedin", "instagram"]:
                return f"{content.get('text', '')} {' '.join(content.get('hashtags', []))}"
            elif platform == "twitter":
                if "thread" in content:
                    return " ".join(content["thread"])
                else:
                    return content.get("tweet", "")
            elif platform == "reddit":
                return f"{content.get('title', '')}\n\n{content.get('body', '')}"
            elif platform == "blog":
                return f"{content.get('title', '')}\n\n{content.get('body', '')}"
            else:
                return str(content)
        else:
            return str(content)
    
    def _format_back_to_platform(self, optimized_text, original_content, platform, guidelines):
        """
        Format optimized text back to platform-specific structure.
        """
        char_limit = guidelines.get("char_limit", 1000)
        
        # Truncate if necessary
        if len(optimized_text) > char_limit:
            optimized_text = optimized_text[:char_limit].rsplit(' ', 1)[0] + '...'
        
        # Preserve original structure as much as possible
        if isinstance(original_content, dict):
            if platform == "email":
                lines = optimized_text.split('\n')
                subject = lines[0].strip() if lines else "Subject Line"
                body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else optimized_text
                return {
                    "subject": subject,
                    "body": body
                }
            
            elif platform in ["linkedin", "instagram"]:
                # Try to preserve original hashtags if they exist
                original_hashtags = original_content.get("hashtags", [])
                # Extract new hashtags from optimized text
                import re
                new_hashtags = re.findall(r'#\w+', optimized_text)
                # Combine, but limit to reasonable number
                combined_hashtags = list(set(original_hashtags + new_hashtags))[:10]
                text = re.sub(r'#\w+', '', optimized_text).strip()
                return {
                    "text": text,
                    "hashtags": combined_hashtags
                }
            
            elif platform == "twitter":
                # Check if it should be a thread
                if len(optimized_text) > 240 or optimized_text.count('\n') > 2:
                    tweets = self._split_into_tweets(optimized_text)
                    return {"thread": tweets}
                else:
                    return {"tweet": optimized_text.strip()}
            
            elif platform == "reddit":
                lines = optimized_text.split('\n')
                title = lines[0].strip() if lines else "Discussion Title"
                body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else optimized_text
                return {
                    "title": title,
                    "body": body
                }
            
            elif platform == "blog":
                lines = optimized_text.split('\n')
                title = lines[0].strip() if lines else "Blog Post Title"
                body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else optimized_text
                return {
                    "title": title,
                    "body": body
                }
            
            else:
                return {"content": optimized_text.strip()}
        else:
            return optimized_text
    
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
    
    def post(self, shared, prep_res, exec_res):
        """
        Update content_pieces with edited versions.
        """
        # Update shared store with optimized content
        shared["content_pieces"] = exec_res["optimized_content"]
        
        # Update version history
        from utils.version_manager import create_version
        version_info = create_version(
            exec_res["optimized_content"],
            action="style_optimization",
            user_feedback="Initial style optimization and pattern removal"
        )
        
        # Add change tracking
        from utils.version_manager import add_change_tracking
        for platform, log_info in exec_res["optimization_log"].items():
            changes = log_info["changes_made"]
            violations_fixed = log_info["violations_fixed"]
            add_change_tracking(version_info["version_id"], changes, violations_fixed)
        
        shared["version_history"].append(version_info)
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("style_optimization")
        shared["workflow_state"]["current_stage"] = "deadly_sins_scanning"
        
        print(f"\nStyle optimization completed!")
        print(f"Content optimized for platforms: {', '.join(exec_res['optimized_content'].keys())}")
        
        # Show optimization summary
        for platform, log_info in exec_res["optimization_log"].items():
            violations_fixed = len(log_info["violations_fixed"])
            changes_made = len(log_info["changes_made"])
            print(f"  {platform.title()}: {violations_fixed} violations fixed, {changes_made} changes made")
        
        return "default"  # Go to next node

if __name__ == "__main__":
    # Test the node
    node = StyleOptimizerNode()
    
    # Create test shared store
    shared = {
        "content_pieces": {
            "linkedin": {
                "text": "It's not just AI; it's a revolution! The future—our most powerful tool—is here. #AI #Future",
                "hashtags": ["#AI", "#Future"]
            },
            "twitter": {
                "tweet": "AI is transforming everything! It's not just technology; it's the future. #AI #Tech"
            }
        },
        "brand_voice": {
            "parsed_attributes": {
                "personality_traits": ["innovative", "professional"],
                "tone": "thought_leadership",
                "voice": "confident",
                "values": ["innovation", "excellence"],
                "themes": ["AI", "technology"]
            },
            "forbidden_patterns": {
                "em_dash": {"pattern": "—", "severity": "critical"},
                "rhetorical_contrast": {"pattern": r"It's not just .+; it's .+", "severity": "critical"}
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
        "workflow_state": {
            "current_stage": "style_optimization",
            "completed_stages": ["engagement", "brand_bible_processing", "format_guidelines", "creative_inspiration", "pattern_aware_prompt_engineering", "content_generation"],
            "error_state": None
        },
        "version_history": []
    }
    
    print("Testing StyleOptimizerNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    print(f"Optimized content keys: {list(shared['content_pieces'].keys())}")
    
    # Show before/after comparison
    print("\nContent comparison:")
    for platform in ["linkedin", "twitter"]:
        if platform in shared['content_pieces']:
            content = shared['content_pieces'][platform]
            if isinstance(content, dict) and "text" in content:
                print(f"  {platform.title()}: {content['text'][:100]}...")
            elif isinstance(content, dict) and "tweet" in content:
                print(f"  {platform.title()}: {content['tweet'][:100]}...")
