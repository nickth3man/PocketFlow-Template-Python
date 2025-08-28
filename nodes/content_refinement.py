from pocketflow import Node
from utils.feedback_parser import parse_user_feedback, categorize_feedback
from utils.call_llm import call_llm
from utils.version_manager import create_version, add_change_tracking

class ContentRefinementNode(Node):
    """
    Applies user-requested changes to content.
    Node that handles iterative content refinement based on user feedback.
    """
    
    def prep(self, shared):
        """
        Read feedback state and current content from shared store.
        """
        return {
            "feedback_state": shared["feedback_state"],
            "content_pieces": shared["content_pieces"],
            "brand_voice": shared["brand_voice"],
            "platform_guidelines": shared["platform_guidelines"],
            "user_config": shared["user_config"]
        }
    
    def exec(self, prep_res):
        """
        Interpret user feedback and apply content modifications.
        """
        feedback_state = prep_res["feedback_state"]
        content_pieces = prep_res["content_pieces"]
        brand_voice = prep_res["brand_voice"]
        platform_guidelines = prep_res["platform_guidelines"]
        user_config = prep_res["user_config"]
        
        feedback_type = feedback_state["feedback_type"]
        selected_content = feedback_state["selected_content"]
        
        print(f"\n=== Content Refinement ===")
        print(f"Feedback type: {feedback_type}")
        
        refined_content = content_pieces.copy()
        
        if feedback_type == "general_refinement":
            # Handle general refinement feedback
            print("Please provide general feedback on the content:")
            print("(e.g., 'Make it more conversational', 'Add more specific examples', 'Shorten the LinkedIn post')")
            user_feedback = input("Your feedback: ").strip()
            
            if user_feedback:
                # Apply feedback to selected content
                for platform, content in selected_content.items():
                    print(f"Refining {platform} content...")
                    
                    # Get platform guidelines
                    guidelines = platform_guidelines.get(platform, {})
                    
                    # Create refinement prompt
                    refinement_prompt = self._create_refinement_prompt(
                        content, platform, user_feedback, brand_voice, guidelines
                    )
                    
                    try:
                        # Generate refined content
                        refined_text = call_llm(
                            prompt=refinement_prompt,
                            model=user_config["model"],
                            temperature=user_config["temperature"]
                        )
                        
                        # Format back to platform structure
                        formatted_content = self._format_back_to_platform(
                            refined_text, content, platform, guidelines
                        )
                        refined_content[platform] = formatted_content
                        
                        print(f"  ✅ {platform} content refined")
                        
                    except Exception as e:
                        print(f"  ⚠️  Error refining {platform}: {e}")
                        # Keep original content
                        refined_content[platform] = content
        
        elif feedback_type == "sentence_edit":
            # Handle specific sentence-level edits
            platform = list(selected_content.keys())[0]
            content = selected_content[platform]
            
            print(f"Editing {platform} content:")
            content_text = self._get_content_text(content, platform)
            print(f"Current content:\n{content_text}\n")
            
            print("Please provide specific edit instructions:")
            print("(e.g., 'Change the first sentence to be more direct', 'Remove the hashtag #AI')")
            user_feedback = input("Your edit instructions: ").strip()
            
            if user_feedback:
                # Create targeted edit prompt
                edit_prompt = self._create_edit_prompt(
                    content_text, user_feedback, brand_voice, platform
                )
                
                try:
                    edited_text = call_llm(
                        prompt=edit_prompt,
                        model=user_config["model"],
                        temperature=user_config["temperature"]
                    )
                    
                    # Format back to platform structure
                    guidelines = platform_guidelines.get(platform, {})
                    formatted_content = self._format_back_to_platform(
                        edited_text, content, platform, guidelines
                    )
                    refined_content[platform] = formatted_content
                    
                    print(f"  ✅ {platform} content edited")
                    
                except Exception as e:
                    print(f"  ⚠️  Error editing {platform}: {e}")
                    refined_content[platform] = content
        
        elif feedback_type == "regenerate_platforms":
            # Handle platform regeneration (this would typically go to a different node)
            # For now, we'll treat it as general refinement
            platforms_to_regenerate = list(selected_content.keys())
            print(f"Preparing to regenerate: {', '.join(platforms_to_regenerate)}")
            # In a real implementation, this would route to regeneration nodes
            
        return {
            "refined_content": refined_content,
            "user_feedback": feedback_state.get("user_input", ""),
            "feedback_type": feedback_type,
            "changes_made": list(set(content_pieces.keys()) - set(refined_content.keys())) or ["content_refined"]
        }
    
    def _create_refinement_prompt(self, content, platform, user_feedback, brand_voice, guidelines):
        """
        Create a prompt for content refinement based on user feedback.
        """
        content_text = self._get_content_text(content, platform)
        char_limit = guidelines.get("char_limit", 1000)
        
        brand_traits = ", ".join(brand_voice["parsed_attributes"].get("personality_traits", []))
        brand_tone = brand_voice["parsed_attributes"].get("tone", "professional")
        
        prompt = f"""Refine the following {platform} content based on user feedback.

CURRENT CONTENT:
{content_text}

USER FEEDBACK:
{user_feedback}

BRAND VOICE:
- Traits: {brand_traits}
- Tone: {brand_tone}

PLATFORM CONSTRAINTS:
- Character limit: {char_limit}
- Tone adjustment: {guidelines.get('tone_adjustment', 'professional')}

REQUIREMENTS:
1. Address the user's feedback specifically
2. Maintain brand voice consistency
3. Keep within platform character limits
4. Preserve the core message and value
5. Ensure content sounds authentically human
6. Avoid AI fingerprint patterns

Please provide the refined content:"""
        
        return prompt
    
    def _create_edit_prompt(self, content_text, edit_instructions, brand_voice, platform):
        """
        Create a prompt for specific content edits.
        """
        brand_traits = ", ".join(brand_voice["parsed_attributes"].get("personality_traits", []))
        brand_tone = brand_voice["parsed_attributes"].get("tone", "professional")
        
        prompt = f"""Edit the following {platform} content according to specific instructions.

CONTENT TO EDIT:
{content_text}

EDIT INSTRUCTIONS:
{edit_instructions}

BRAND VOICE:
- Traits: {brand_traits}
- Tone: {brand_tone}

REQUIREMENTS:
1. Apply the edit instructions precisely
2. Maintain brand voice consistency
3. Keep the content natural and human-sounding
4. Preserve the overall message and intent
5. Avoid AI fingerprint patterns

Please provide the edited content:"""
        
        return prompt
    
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
    
    def _format_back_to_platform(self, refined_text, original_content, platform, guidelines):
        """
        Format refined text back to platform-specific structure.
        """
        char_limit = guidelines.get("char_limit", 1000)
        
        # Truncate if necessary
        if len(refined_text) > char_limit:
            refined_text = refined_text[:char_limit].rsplit(' ', 1)[0] + '...'
        
        # Preserve original structure as much as possible
        if isinstance(original_content, dict):
            if platform == "email":
                lines = refined_text.split('\n')
                subject = lines[0].strip() if lines else "Subject Line"
                body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else refined_text
                return {
                    "subject": subject,
                    "body": body
                }
            
            elif platform in ["linkedin", "instagram"]:
                # Try to preserve original hashtags if they exist
                original_hashtags = original_content.get("hashtags", [])
                # Extract new hashtags from refined text
                import re
                new_hashtags = re.findall(r'#\w+', refined_text)
                # Combine, but limit to reasonable number
                combined_hashtags = list(set(original_hashtags + new_hashtags))[:10]
                text = re.sub(r'#\w+', '', refined_text).strip()
                return {
                    "text": text,
                    "hashtags": combined_hashtags
                }
            
            elif platform == "twitter":
                # Check if it should be a thread
                if len(refined_text) > 240 or refined_text.count('\n') > 2:
                    tweets = self._split_into_tweets(refined_text)
                    return {"thread": tweets}
                else:
                    return {"tweet": refined_text.strip()}
            
            elif platform == "reddit":
                lines = refined_text.split('\n')
                title = lines[0].strip() if lines else "Discussion Title"
                body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else refined_text
                return {
                    "title": title,
                    "body": body
                }
            
            elif platform == "blog":
                lines = refined_text.split('\n')
                title = lines[0].strip() if lines else "Blog Post Title"
                body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else refined_text
                return {
                    "title": title,
                    "body": body
                }
            
            else:
                return {"content": refined_text.strip()}
        else:
            return refined_text
    
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
        Update content_pieces with refined versions and manage version history.
        """
        # Update shared store with refined content
        shared["content_pieces"] = exec_res["refined_content"]
        
        # Update version history
        version_info = create_version(
            exec_res["refined_content"],
            action="content_refinement",
            user_feedback=exec_res["user_feedback"]
        )
        
        # Add change tracking
        changes = exec_res["changes_made"]
        violations_fixed = []  # This would come from re-scanning in a real implementation
        add_change_tracking(version_info["version_id"], changes, violations_fixed)
        
        shared["version_history"].append(version_info)
        
        # Update feedback state
        shared["feedback_state"]["awaiting_feedback"] = False
        shared["feedback_state"]["feedback_type"] = None
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("content_refinement")
        shared["workflow_state"]["current_stage"] = "deadly_sins_scanning"  # Go back to scanning
        
        print(f"\nContent refinement completed!")
        print(f"Changes applied to: {', '.join(exec_res['changes_made'])}")
        
        # Show summary of refined content
        for platform in exec_res["changes_made"]:
            if platform in exec_res["refined_content"]:
                content = exec_res["refined_content"][platform]
                content_text = self._get_content_text(content, platform)
                print(f"  {platform.title()}: {len(content_text)} chars")
        
        return "refined"  # Go back to scanning for compliance

if __name__ == "__main__":
    # Test the node
    node = ContentRefinementNode()
    
    # Create test shared store
    shared = {
        "feedback_state": {
            "awaiting_feedback": True,
            "feedback_type": "general_refinement",
            "user_input": "Make it more conversational",
            "selected_content": {
                "linkedin": {
                    "text": "AI is transforming marketing in exciting ways. The future holds incredible possibilities for brands that embrace innovation. #AI #Marketing",
                    "hashtags": ["#AI", "#Marketing"]
                }
            }
        },
        "content_pieces": {
            "linkedin": {
                "text": "AI is transforming marketing in exciting ways. The future holds incredible possibilities for brands that embrace innovation. #AI #Marketing",
                "hashtags": ["#AI", "#Marketing"]
            },
            "twitter": {
                "tweet": "Exciting developments in AI marketing! The future is bright. #AI #Tech"
            }
        },
        "brand_voice": {
            "parsed_attributes": {
                "personality_traits": ["innovative", "professional"],
                "tone": "thought_leadership",
                "voice": "confident",
                "values": ["innovation", "excellence"],
                "themes": ["AI", "technology"]
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
        "user_config": {
            "model": "openrouter/anthropic/claude-3.5-sonnet",
            "temperature": 0.7
        },
        "version_history": [],
        "workflow_state": {
            "current_stage": "content_refinement",
            "completed_stages": ["engagement", "brand_bible_processing", "format_guidelines", "creative_inspiration", "pattern_aware_prompt_engineering", "content_generation", "style_optimization", "deadly_sins_scanning", "style_compliance", "authenticity_scoring", "feedback_routing"],
            "error_state": None
        }
    }
    
    print("Testing ContentRefinementNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    print(f"Content pieces updated: {list(shared['content_pieces'].keys())}")
    
    if shared['content_pieces'] and 'linkedin' in shared['content_pieces']:
        linkedin_content = shared['content_pieces']['linkedin']
        if isinstance(linkedin_content, dict):
            print(f"LinkedIn content: {linkedin_content.get('text', '')[:100]}...")
