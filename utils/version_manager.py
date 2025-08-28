import json
import uuid
from datetime import datetime
from typing import Dict, List, Any

class VersionManager:
    """
    Manages content versions for rollback capability and comparison.
    """
    
    def __init__(self):
        self.versions = []
    
    def create_version(self, content: Dict, action: str = "create", user_feedback: str = None) -> Dict:
        """
        Create a new version snapshot with metadata.
        
        Args:
            content (Dict): Content pieces to version
            action (str): Action that triggered version creation
            user_feedback (str): Optional user feedback
            
        Returns:
            Dict: Version metadata
        """
        version_id = str(uuid.uuid4())[:8]  # Short ID for readability
        timestamp = datetime.now().isoformat()
        
        version_metadata = {
            "version_id": version_id,
            "timestamp": timestamp,
            "action": action,
            "content_pieces": content.copy() if content else {},
            "user_feedback": user_feedback,
            "changes_made": [],
            "violations_fixed": []
        }
        
        self.versions.append(version_metadata)
        return version_metadata
    
    def get_version(self, version_id: str) -> Dict:
        """
        Retrieve a specific version by ID.
        
        Args:
            version_id (str): Version ID to retrieve
            
        Returns:
            Dict: Version data or empty dict if not found
        """
        for version in self.versions:
            if version["version_id"] == version_id:
                return version
        return {}
    
    def get_version_history(self) -> List[Dict]:
        """
        Get complete version history.
        
        Returns:
            List[Dict]: List of all versions
        """
        return self.versions.copy()
    
    def get_recent_versions(self, count: int = 5) -> List[Dict]:
        """
        Get most recent versions.
        
        Args:
            count (int): Number of recent versions to return
            
        Returns:
            List[Dict]: Recent versions
        """
        return self.versions[-count:] if self.versions else []
    
    def add_change_tracking(self, version_id: str, changes: List[str], violations_fixed: List[str] = None):
        """
        Add change tracking information to a version.
        
        Args:
            version_id (str): Version ID to update
            changes (List[str]): List of changes made
            violations_fixed (List[str]): List of violations fixed
        """
        for version in self.versions:
            if version["version_id"] == version_id:
                version["changes_made"].extend(changes)
                if violations_fixed:
                    version["violations_fixed"].extend(violations_fixed)
                break
    
    def compare_versions(self, version_id_1: str, version_id_2: str) -> Dict:
        """
        Compare two versions and highlight differences.
        
        Args:
            version_id_1 (str): First version ID
            version_id_2 (str): Second version ID
            
        Returns:
            Dict: Comparison results
        """
        version_1 = self.get_version(version_id_1)
        version_2 = self.get_version(version_id_2)
        
        if not version_1 or not version_2:
            return {"error": "One or both versions not found"}
        
        differences = {}
        content_1 = version_1.get("content_pieces", {})
        content_2 = version_2.get("content_pieces", {})
        
        # Compare content pieces
        all_platforms = set(content_1.keys()) | set(content_2.keys())
        for platform in all_platforms:
            content_1_platform = content_1.get(platform, {})
            content_2_platform = content_2.get(platform, {})
            
            if content_1_platform != content_2_platform:
                differences[platform] = {
                    "version_1": content_1_platform,
                    "version_2": content_2_platform
                }
        
        return {
            "differences": differences,
            "version_1_metadata": {
                "id": version_1["version_id"],
                "timestamp": version_1["timestamp"],
                "action": version_1["action"]
            },
            "version_2_metadata": {
                "id": version_2["version_id"],
                "timestamp": version_2["timestamp"],
                "action": version_2["action"]
            }
        }

def create_version(content: Dict, action: str = "create", user_feedback: str = None) -> Dict:
    """
    Convenience function to create a version.
    
    Args:
        content (Dict): Content to version
        action (str): Action that triggered versioning
        user_feedback (str): Optional user feedback
        
    Returns:
        Dict: Version metadata
    """
    manager = VersionManager()
    return manager.create_version(content, action, user_feedback)

def get_version_history() -> List[Dict]:
    """
    Convenience function to get version history.
    
    Returns:
        List[Dict]: Version history
    """
    manager = VersionManager()
    return manager.get_version_history()

def add_change_tracking(version_id: str, changes: List[str], violations_fixed: List[str] = None):
    """
    Convenience function to add change tracking to a version.
    
    Args:
        version_id (str): Version ID to update
        changes (List[str]): List of changes made
        violations_fixed (List[str]): List of violations fixed
    """
    manager = VersionManager()
    manager.add_change_tracking(version_id, changes, violations_fixed)

if __name__ == "__main__":
    # Test the version manager
    test_content = {
        "linkedin": {
            "text": "Check out this amazing AI content!",
            "hashtags": ["#AI", "#Marketing", "#Innovation"]
        },
        "twitter": {
            "tweet": "AI is transforming marketing! #AI #Marketing"
        }
    }
    
    manager = VersionManager()
    
    # Create initial version
    version1 = manager.create_version(
        test_content, 
        "initial_creation", 
        "First draft of content"
    )
    print("Version 1 created:", version1["version_id"])
    
    # Simulate changes
    modified_content = test_content.copy()
    modified_content["linkedin"]["text"] = "Discover how AI is revolutionizing marketing strategies!"
    
    # Create second version
    version2 = manager.create_version(
        modified_content,
        "content_refinement",
        "Made it more professional"
    )
    manager.add_change_tracking(
        version2["version_id"],
        ["Updated LinkedIn text for better clarity"],
        ["em_dash", "rhetorical_contrast"]
    )
    
    print("Version 2 created:", version2["version_id"])
    
    # Compare versions
    comparison = manager.compare_versions(version1["version_id"], version2["version_id"])
    print("\nVersion comparison:")
    print(json.dumps(comparison, indent=2))
    
    # Show version history
    print("\nVersion history:")
    for version in manager.get_version_history():
        print(f"  {version['version_id']} - {version['action']} ({version['timestamp']})")
