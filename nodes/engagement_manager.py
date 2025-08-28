from pocketflow import Node
from utils.presets_manager import load_preset, list_presets
from utils.brand_bible_parser import parse_brand_bible

class EngagementManagerNode(Node):
    """
    Handle GUI inputs and preset management.
    First node in the workflow that initializes the shared store.
    """
    
    def exec(self, _):
        """
        Handle user inputs and preset loading.
        In a real implementation, this would interact with a GUI.
        For now, we'll simulate the process.
        """
        print("=== PR Firm Content Generation System ===")
        print("Welcome! Let's create authentic, platform-optimized content.")
        print()
        
        # Simulate user input collection
        individual_or_brand = input("Are you an individual or brand? (individual/brand): ").strip().lower()
        if individual_or_brand not in ["individual", "brand"]:
            individual_or_brand = "individual"
        
        if individual_or_brand == "individual":
            name = input("Your name: ").strip()
            brand_name = None
        else:
            name = input("Your name: ").strip()
            brand_name = input("Brand name: ").strip()
        
        # Model selection
        print("\nAvailable models:")
        print("1. Claude 3.5 Sonnet (recommended)")
        print("2. GPT-4 Turbo")
        print("3. Custom model")
        model_choice = input("Select model (1-3, default 1): ").strip()
        
        model_map = {
            "1": "openrouter/anthropic/claude-3.5-sonnet",
            "2": "openrouter/openai/gpt-4-turbo",
            "3": input("Enter custom model name: ").strip()
        }
        
        model = model_map.get(model_choice, "openrouter/anthropic/claude-3.5-sonnet")
        
        # Temperature
        temp_input = input("Temperature (0.0-1.0, default 0.7): ").strip()
        print(f"temp_input: {temp_input}")
        try:
            temperature = float(temp_input) if temp_input else 0.7
            print(f"temperature after float conversion: {temperature}")
            temperature = max(0.0, min(1.0, temperature))  # Clamp to valid range
            print(f"temperature after clamping: {temperature}")
        except ValueError:
            temperature = 0.7
        
        # Preset management
        print("\nAvailable presets:")
        presets = list_presets()
        if presets:
            for i, (preset_id, preset_info) in enumerate(presets.items(), 1):
                print(f"{i}. {preset_info['name']} (created: {preset_info['created_at'][:10]})")
            print(f"{len(presets) + 1}. Create new configuration")
            
            preset_choice = input(f"Select preset (1-{len(presets) + 1}): ").strip()
            try:
                preset_index = int(preset_choice) - 1
                if 0 <= preset_index < len(presets):
                    preset_names = list(presets.keys())
                    selected_preset = preset_names[preset_index]
                    preset_data = load_preset(selected_preset)
                    print(f"Loaded preset: {presets[selected_preset]['name']}")
                    return {
                        "user_config": preset_data.get("user_config", {}),
                        "task_requirements": preset_data.get("task_requirements", {}),
                        "brand_voice": preset_data.get("brand_voice", {}),
                        "preset_loaded": True
                    }
            except ValueError:
                pass
        
        # If no preset loaded, collect new configuration
        print("\n=== Brand Configuration ===")
        brand_bible_text = input("Describe your brand voice, personality, and values: ").strip()
        if not brand_bible_text:
            brand_bible_text = "Professional brand focused on quality and innovation."
        
        # Parse brand bible
        structured_voice, tone_guidelines = parse_brand_bible(brand_bible_text, individual_or_brand)
        
        # Platform selection
        print("\nAvailable platforms:")
        all_platforms = ["email", "linkedin", "instagram", "twitter", "reddit", "blog"]
        for i, platform in enumerate(all_platforms, 1):
            print(f"{i}. {platform.title()}")
        
        platform_input = input("Select platforms (comma-separated numbers, e.g., 1,2,3): ").strip()
        if platform_input:
            try:
                selected_indices = [int(x.strip()) - 1 for x in platform_input.split(",")]
                platforms = [all_platforms[i] for i in selected_indices if 0 <= i < len(all_platforms)]
            except ValueError:
                platforms = ["email", "linkedin", "twitter"]  # Default
        else:
            platforms = ["email", "linkedin", "twitter"]  # Default
        
        topic = input("\nMain content topic: ").strip()
        if not topic:
            topic = "Latest industry insights and trends"
        
        return {
            "user_config": {
                "individual_or_brand": individual_or_brand,
                "name": name,
                "brand_name": brand_name,
                "model": model,
                "temperature": temperature
            },
            "task_requirements": {
                "topic": topic,
                "platforms": platforms,
                "brand_bible_text": brand_bible_text
            },
            "brand_voice": {
                "parsed_attributes": structured_voice,
                "tone_guidelines": tone_guidelines
            },
            "preset_loaded": False
        }
    
    def post(self, shared, prep_res, exec_res):
        """
        Initialize shared store with user configuration.
        """
        # Initialize shared store structure
        shared.update({
            "user_config": exec_res["user_config"],
            "task_requirements": exec_res["task_requirements"],
            "brand_voice": exec_res["brand_voice"],
            "platform_guidelines": {},
            "creative_inspiration": {
                "examples": [],
                "source_platforms": []
            },
            "content_pieces": {},
            "quality_control": {
                "deadly_sins_violations": {},
                "revision_count": 0,
                "max_revisions_reached": False,
                "compliance_status": "pending"
            },
            "version_history": [],
            "feedback_state": {
                "awaiting_feedback": False,
                "feedback_type": None,
                "user_input": "",
                "selected_content": {}
            },
            "workflow_state": {
                "current_stage": "engagement",
                "completed_stages": [],
                "error_state": None
            }
        })
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("engagement")
        shared["workflow_state"]["current_stage"] = "brand_bible_processing"
        
        print(f"\nConfiguration loaded successfully!")
        print(f"User: {exec_res['user_config']['name']}")
        print(f"Model: {exec_res['user_config']['model']}")
        print(f"Platforms: {', '.join(exec_res['task_requirements']['platforms'])}")
        print(f"Topic: {exec_res['task_requirements']['topic']}")
        
        return "default"  # Go to next node

if __name__ == "__main__":
    # Test the node
    node = EngagementManagerNode()
    shared = {}
    
    print("Testing EngagementManagerNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    print(f"Shared store keys: {list(shared.keys())}")
