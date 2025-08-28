import json
import os
from typing import Dict, Any

class PresetsManager:
    """
    Manages brand configuration presets for reuse.
    """
    
    def __init__(self, presets_file: str = "brand_presets.json"):
        self.presets_file = presets_file
        self.presets = self._load_presets()
    
    def _load_presets(self) -> Dict:
        """
        Load presets from file.
        
        Returns:
            Dict: Loaded presets or empty dict
        """
        if os.path.exists(self.presets_file):
            try:
                with open(self.presets_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading presets: {e}")
                return {}
        return {}
    
    def _save_presets(self):
        """
        Save presets to file.
        """
        try:
            with open(self.presets_file, 'w') as f:
                json.dump(self.presets, f, indent=2)
        except Exception as e:
            print(f"Error saving presets: {e}")
    
    def save_preset(self, preset_name: str, preset_data: Dict) -> str:
        """
        Save a new preset or update existing one.
        
        Args:
            preset_name (str): Name for the preset
            preset_data (Dict): Preset data to save
            
        Returns:
            str: Preset ID
        """
        preset_id = preset_name.lower().replace(" ", "_")
        
        self.presets[preset_id] = {
            "name": preset_name,
            "data": preset_data,
            "created_at": self.presets.get(preset_id, {}).get("created_at", None),
            "updated_at": __import__('datetime').datetime.now().isoformat()
        }
        
        if "created_at" not in self.presets[preset_id]:
            self.presets[preset_id]["created_at"] = self.presets[preset_id]["updated_at"]
        
        self._save_presets()
        return preset_id
    
    def load_preset(self, preset_name: str) -> Dict:
        """
        Load a preset by name.
        
        Args:
            preset_name (str): Name of preset to load
            
        Returns:
            Dict: Preset data or empty dict if not found
        """
        preset_id = preset_name.lower().replace(" ", "_")
        return self.presets.get(preset_id, {}).get("data", {})
    
    def delete_preset(self, preset_name: str) -> bool:
        """
        Delete a preset.
        
        Args:
            preset_name (str): Name of preset to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        preset_id = preset_name.lower().replace(" ", "_")
        if preset_id in self.presets:
            del self.presets[preset_id]
            self._save_presets()
            return True
        return False
    
    def list_presets(self) -> Dict:
        """
        List all available presets.
        
        Returns:
            Dict: Dictionary of preset names and their basic info
        """
        return {
            preset_id: {
                "name": preset_data["name"],
                "created_at": preset_data["created_at"],
                "updated_at": preset_data["updated_at"]
            }
            for preset_id, preset_data in self.presets.items()
        }
    
    def preset_exists(self, preset_name: str) -> bool:
        """
        Check if a preset exists.
        
        Args:
            preset_name (str): Name of preset to check
            
        Returns:
            bool: True if preset exists
        """
        preset_id = preset_name.lower().replace(" ", "_")
        return preset_id in self.presets

def save_preset(preset_name: str, preset_data: Dict) -> str:
    """
    Convenience function to save a preset.
    
    Args:
        preset_name (str): Name for the preset
        preset_data (Dict): Preset data to save
        
    Returns:
        str: Preset ID
    """
    manager = PresetsManager()
    return manager.save_preset(preset_name, preset_data)

def load_preset(preset_name: str) -> Dict:
    """
    Convenience function to load a preset.
    
    Args:
        preset_name (str): Name of preset to load
        
    Returns:
        Dict: Preset data or empty dict if not found
    """
    manager = PresetsManager()
    return manager.load_preset(preset_name)

def list_presets() -> Dict:
    """
    Convenience function to list all presets.
    
    Returns:
        Dict: Available presets
    """
    manager = PresetsManager()
    return manager.list_presets()

if __name__ == "__main__":
    # Test the presets manager
    manager = PresetsManager()
    
    # Test preset data
    test_preset = {
        "user_config": {
            "individual_or_brand": "brand",
            "name": "TechCorp Marketing",
            "brand_name": "TechCorp",
            "model": "openrouter/anthropic/claude-3.5-sonnet",
            "temperature": 0.7
        },
        "task_requirements": {
            "topic": "",
            "platforms": ["email", "linkedin", "twitter"],
            "brand_bible_text": "We are a innovative tech company focused on AI solutions..."
        },
        "brand_voice": {
            "personality_traits": ["innovative", "professional", "thoughtful"],
            "tone": "thought_leadership",
            "voice": "confident",
            "values": ["innovation", "excellence"],
            "themes": ["AI", "technology", "business transformation"]
        }
    }
    
    # Save a preset
    preset_id = manager.save_preset("TechCorp Default", test_preset)
    print(f"Saved preset: {preset_id}")
    
    # List presets
    presets = manager.list_presets()
    print(f"\nAvailable presets: {list(presets.keys())}")
    
    # Load the preset
    loaded_preset = manager.load_preset("TechCorp Default")
    print(f"\nLoaded preset keys: {list(loaded_preset.keys())}")
    
    # Check if preset exists
    exists = manager.preset_exists("TechCorp Default")
    print(f"\nPreset exists: {exists}")
