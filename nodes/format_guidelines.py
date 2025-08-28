from pocketflow import BatchNode
from utils.platform_formatter import get_platform_guidelines

class FormatGuidelinesBatch(BatchNode):
    """
    Generate platform-specific formatting rules.
    BatchNode that processes multiple platforms in parallel.
    """
    
    def prep(self, shared):
        """
        Return list of selected platforms to process.
        """
        return shared["task_requirements"]["platforms"]
    
    def exec(self, platform):
        """
        For each platform, generate character limits, structure requirements, tone adjustments.
        """
        # Get brand voice from shared store
        brand_voice = shared.get("brand_voice", {}).get("parsed_attributes", {})
        topic = shared.get("task_requirements", {}).get("topic", "General topic")
        
        # Generate platform-specific guidelines
        guidelines = get_platform_guidelines(platform, brand_voice, topic)
        
        return {
            "platform": platform,
            "guidelines": guidelines
        }
    
    def post(self, shared, prep_res, exec_res_list):
        """
        Write platform_guidelines to shared store.
        """
        # Process results from all platforms
        platform_guidelines = {}
        for result in exec_res_list:
            if isinstance(result, dict) and "platform" in result:
                platform = result["platform"]
                guidelines = result["guidelines"]
                platform_guidelines[platform] = guidelines
        
        # Update shared store
        shared["platform_guidelines"] = platform_guidelines
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("format_guidelines")
        shared["workflow_state"]["current_stage"] = "creative_inspiration"
        
        print(f"\nPlatform guidelines generated for: {', '.join(platform_guidelines.keys())}")
        
        # Print summary of guidelines
        for platform, guidelines in platform_guidelines.items():
            print(f"  {platform.title()}: {guidelines.get('char_limit', 'N/A')} chars, {guidelines.get('tone_adjustment', 'N/A')} tone")
        
        return "default"  # Go to next node

if __name__ == "__main__":
    # Test the batch node
    node = FormatGuidelinesBatch()
    
    # Create test shared store
    shared = {
        "task_requirements": {
            "brand_bible_text": "Innovative marketing agency focused on education and transparency.",
            "topic": "The future of AI in marketing",
            "platforms": ["linkedin", "twitter", "email"]
        },
        "user_config": {
            "individual_or_brand": "brand",
            "name": "Test User",
            "brand_name": "TestBrand"
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
        "workflow_state": {
            "current_stage": "format_guidelines",
            "completed_stages": ["engagement", "brand_bible_processing"],
            "error_state": None
        }
    }
    
    print("Testing FormatGuidelinesBatch...")
    action = node.run(shared)
    print(f"Action: {action}")
    print(f"Platform guidelines keys: {list(shared['platform_guidelines'].keys())}")
    
    # Show detailed guidelines for one platform
    if shared['platform_guidelines']:
        first_platform = list(shared['platform_guidelines'].keys())[0]
        print(f"Sample guidelines for {first_platform}:")
        sample_guidelines = shared['platform_guidelines'][first_platform]
        print(f"  Character limit: {sample_guidelines.get('char_limit', 'N/A')}")
        print(f"  Tone adjustment: {sample_guidelines.get('tone_adjustment', 'N/A')}")
