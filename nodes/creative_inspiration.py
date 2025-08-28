from pocketflow import Node
from utils.creative_inspiration import generate_creative_inspiration, get_platform_style_hints

class CreativeInspirationNode(Node):
    """
    Use LLM prompts to generate high-engagement examples without external web searches.
    Third node in the workflow that provides creative direction.
    """
    
    def prep(self, shared):
        """
        Read topic, brand_voice, and platform_guidelines from shared store.
        """
        return {
            "topic": shared["task_requirements"]["topic"],
            "brand_voice": shared["brand_voice"]["parsed_attributes"],
            "platforms": shared["task_requirements"]["platforms"],
            "platform_guidelines": shared["platform_guidelines"]
        }
    
    def exec(self, prep_res):
        """
        Generate creative examples for each platform using LLM.
        """
        topic = prep_res["topic"]
        brand_voice = prep_res["brand_voice"]
        platforms = prep_res["platforms"]
        
        # Generate creative inspiration for each platform
        creative_examples = []
        platform_style_hints = {}
        
        for platform in platforms:
            # Generate creative examples
            examples = generate_creative_inspiration(topic, platform, brand_voice)
            creative_examples.extend(examples)
            
            # Get platform style hints
            style_hints = get_platform_style_hints(platform, brand_voice)
            platform_style_hints[platform] = style_hints
        
        return {
            "creative_examples": creative_examples,
            "platform_style_hints": platform_style_hints
        }
    
    def post(self, shared, prep_res, exec_res):
        """
        Store inspiration examples and style hints in shared store.
        """
        # Update shared store with creative inspiration
        shared["creative_inspiration"] = {
            "examples": exec_res["creative_examples"],
            "source_platforms": prep_res["platforms"]
        }
        
        # Update platform guidelines with style hints
        for platform, style_hints in exec_res["platform_style_hints"].items():
            if platform in shared["platform_guidelines"]:
                shared["platform_guidelines"][platform]["style_hints"] = style_hints
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("creative_inspiration")
        shared["workflow_state"]["current_stage"] = "pattern_aware_prompt_engineering"
        
        print(f"\nCreative inspiration generated successfully!")
        print(f"Generated {len(exec_res['creative_examples'])} examples")
        print(f"Style hints for platforms: {', '.join(exec_res['platform_style_hints'].keys())}")
        
        # Show sample examples
        if exec_res["creative_examples"]:
            print("\nSample creative examples:")
            for i, example in enumerate(exec_res["creative_examples"][:2], 1):
                print(f"  {i}. {example[:100]}...")
        
        return "default"  # Go to next node

if __name__ == "__main__":
    # Test the node
    node = CreativeInspirationNode()
    
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
            "current_stage": "creative_inspiration",
            "completed_stages": ["engagement", "brand_bible_processing", "format_guidelines"],
            "error_state": None
        }
    }
    
    print("Testing CreativeInspirationNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    print(f"Creative inspiration keys: {list(shared['creative_inspiration'].keys())}")
    
    if shared['creative_inspiration']['examples']:
        print(f"Number of examples: {len(shared['creative_inspiration']['examples'])}")
