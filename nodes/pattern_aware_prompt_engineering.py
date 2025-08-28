from pocketflow import Node
from utils.call_llm import call_llm

class PatternAwarePromptEngineerNode(Node):
    """
    Enhance generation prompts with positive writing alternatives to prevent AI patterns.
    Fourth node that creates pattern-aware prompts for content generation.
    """
    
    def prep(self, shared):
        """
        Read brand_voice, platform_guidelines, and creative inspiration from shared store.
        """
        return {
            "topic": shared["task_requirements"]["topic"],
            "brand_voice": shared["brand_voice"],
            "platform_guidelines": shared["platform_guidelines"],
            "creative_inspiration": shared["creative_inspiration"],
            "platforms": shared["task_requirements"]["platforms"]
        }
    
    def exec(self, prep_res):
        """
        Generate pattern-aware prompts with few-shot examples of approved vs rejected phrasing.
        """
        topic = prep_res["topic"]
        brand_voice = prep_res["brand_voice"]
        platform_guidelines = prep_res["platform_guidelines"]
        creative_examples = prep_res["creative_inspiration"]["examples"]
        platforms = prep_res["platforms"]
        
        # Get forbidden patterns
        forbidden_patterns = brand_voice.get("forbidden_patterns", {})
        
        # Create pattern-aware prompts for each platform
        enhanced_prompts = {}
        
        for platform in platforms:
            guidelines = platform_guidelines.get(platform, {})
            
            # Build pattern awareness instructions
            pattern_instructions = self._build_pattern_instructions(forbidden_patterns)
            
            # Get platform-specific constraints
            char_limit = guidelines.get("char_limit", 1000)
            tone_adjustment = guidelines.get("tone_adjustment", "professional")
            structure = guidelines.get("structure", [])
            best_practices = guidelines.get("best_practices", [])
            
            # Get creative examples for this platform
            platform_examples = self._get_platform_examples(creative_examples, platform)
            
            # Create enhanced prompt
            prompt = self._create_enhanced_prompt(
                topic=topic,
                platform=platform,
                brand_voice=brand_voice["parsed_attributes"],
                char_limit=char_limit,
                tone_adjustment=tone_adjustment,
                structure=structure,
                best_practices=best_practices,
                pattern_instructions=pattern_instructions,
                creative_examples=platform_examples
            )
            
            enhanced_prompts[platform] = {
                "prompt": prompt,
                "char_limit": char_limit,
                "tone_adjustment": tone_adjustment
            }
        
        return enhanced_prompts
    
    def _build_pattern_instructions(self, forbidden_patterns):
        """
        Build instructions to avoid the 7 deadly sins of AI-generated content.
        """
        instructions = [
            "CRITICAL: Avoid these AI fingerprint patterns at all costs:",
            ""
        ]
        
        for pattern_name, pattern_info in forbidden_patterns.items():
            instructions.append(f"- {pattern_name.replace('_', ' ').title()}: {pattern_info.get('description', '')}")
            if "pattern" in pattern_info:
                instructions.append(f"  Example to avoid: {pattern_info['pattern']}")
            instructions.append("")
        
        instructions.append("Instead, use natural, conversational language that sounds genuinely human.")
        instructions.append("Focus on authentic storytelling and real value for the reader.")
        
        return "\n".join(instructions)
    
    def _get_platform_examples(self, creative_examples, platform):
        """
        Get relevant creative examples for a specific platform.
        In a real implementation, this would be more sophisticated.
        """
        # For now, return a subset of examples
        return creative_examples[:3] if creative_examples else []
    
    def _create_enhanced_prompt(self, topic, platform, brand_voice, char_limit, tone_adjustment, 
                              structure, best_practices, pattern_instructions, creative_examples):
        """
        Create an enhanced prompt that incorporates all constraints and guidelines.
        """
        brand_traits = ", ".join(brand_voice.get("personality_traits", ["professional"]))
        brand_tone = brand_voice.get("tone", "professional")
        brand_values = ", ".join(brand_voice.get("values", ["quality"]))
        brand_themes = ", ".join(brand_voice.get("themes", ["innovation"]))
        
        prompt = f"""Create {platform.title()} content about "{topic}".

BRAND VOICE:
- Personality: {brand_traits}
- Tone: {brand_tone}
- Values: {brand_values}
- Themes: {brand_themes}

PLATFORM SPECIFICATIONS:
- Character limit: {char_limit}
- Tone adjustment: {tone_adjustment}
- Structure: {', '.join(structure) if structure else 'Standard'}

BEST PRACTICES:
{chr(10).join(f'- {practice}' for practice in best_practices) if best_practices else '- Follow platform conventions'}

{pattern_instructions}

CONTENT REQUIREMENTS:
1. Sound authentically human - avoid any AI-generated patterns
2. Provide genuine value to the reader
3. Maintain brand voice consistency
4. Engage the target audience appropriately
5. Include natural storytelling elements

{f'CREATIVE INSPIRATION EXAMPLES:{chr(10)}{chr(10).join(f"- {example}" for example in creative_examples)}' if creative_examples else ''}

Generate the content in a natural, engaging way that follows all guidelines above."""

        return prompt
    
    def post(self, shared, prep_res, exec_res):
        """
        Store enhanced prompts for content generation.
        """
        # Update shared store with enhanced prompts
        shared["enhanced_prompts"] = exec_res
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("pattern_aware_prompt_engineering")
        shared["workflow_state"]["current_stage"] = "content_generation"
        
        print(f"\nPattern-aware prompts generated for platforms: {', '.join(exec_res.keys())}")
        
        # Show sample prompt
        if exec_res:
            first_platform = list(exec_res.keys())[0]
            sample_prompt = exec_res[first_platform]["prompt"]
            print(f"\nSample prompt for {first_platform} ({len(sample_prompt)} chars):")
            print(f"{sample_prompt[:200]}...")
        
        return "default"  # Go to next node

if __name__ == "__main__":
    # Test the node
    node = PatternAwarePromptEngineerNode()
    
    # Create test shared store
    shared = {
        "task_requirements": {
            "topic": "The future of AI in marketing",
            "platforms": ["linkedin", "twitter"]
        },
        "brand_voice": {
            "parsed_attributes": {
                "personality_traits": ["innovative", "educational"],
                "tone": "thought_leadership",
                "voice": "confident",
                "values": ["innovation", "education"],
                "themes": ["AI empowerment", "skill development"]
            },
            "forbidden_patterns": {
                "em_dash": {
                    "pattern": "—", 
                    "severity": "critical",
                    "description": "Em dash usage creates robotic pauses"
                },
                "rhetorical_contrast": {
                    "pattern": r"(?:It's not just|It's not merely|It's not only).+?[,;]\s*(?:it's|it is|but).+?",
                    "severity": "critical",
                    "description": "Rhetorical contrast creates artificial drama"
                }
            }
        },
        "platform_guidelines": {
            "linkedin": {
                "char_limit": 3000,
                "tone_adjustment": "thought_leadership",
                "structure": ["hook", "insight", "value", "engagement"],
                "best_practices": ["Hook in first 210 characters", "End with engaging question"]
            },
            "twitter": {
                "char_limit": 280,
                "tone_adjustment": "conversational",
                "structure": ["strong opening", "key insight", "engagement hook"],
                "best_practices": ["Clear, concise messaging", "Include relevant hashtag"]
            }
        },
        "creative_inspiration": {
            "examples": [
                "Start with a surprising statistic about AI adoption",
                "Share a personal anecdote about technology transformation",
                "Pose a thought-provoking question to engage readers"
            ],
            "source_platforms": ["linkedin", "twitter"]
        },
        "workflow_state": {
            "current_stage": "pattern_aware_prompt_engineering",
            "completed_stages": ["engagement", "brand_bible_processing", "format_guidelines", "creative_inspiration"],
            "error_state": None
        }
    }
    
    print("Testing PatternAwarePromptEngineerNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    print(f"Enhanced prompts keys: {list(shared['enhanced_prompts'].keys())}")
    
    if shared['enhanced_prompts']:
        first_platform = list(shared['enhanced_prompts'].keys())[0]
        print(f"Sample prompt length: {len(shared['enhanced_prompts'][first_platform]['prompt'])} chars")
