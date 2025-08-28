from pocketflow import Node
from utils.version_manager import create_version, add_change_tracking, get_version_history

class VersionManagerNode(Node):
    """
    Tracks content versions for rollback capability.
    Node that manages version control and change tracking.
    """
    
    def prep(self, shared):
        """
        Read current content and version information from shared store.
        """
        return {
            "content_pieces": shared["content_pieces"],
            "version_history": shared["version_history"],
            "feedback_state": shared["feedback_state"],
            "workflow_state": shared["workflow_state"]
        }
    
    def exec(self, prep_res):
        """
        Manage content versions and track changes.
        """
        content_pieces = prep_res["content_pieces"]
        version_history = prep_res["version_history"]
        feedback_state = prep_res["feedback_state"]
        
        print(f"\n=== Version Management ===")
        print(f"Current version history: {len(version_history)} versions")
        
        # Show version history summary
        if version_history:
            print(f"\nVersion History:")
            for i, version in enumerate(version_history[-5:], 1):  # Show last 5
                version_num = len(version_history) - 5 + i
                if version_num > 0:  # Only show if it's a valid version
                    timestamp = version.get("timestamp", "Unknown")[:19].replace("T", " ")
                    action = version.get("action", "unknown")
                    print(f"  v{version_num}: {timestamp} - {action}")
        
        # Check if we need to create a new version
        needs_version = (
            feedback_state.get("feedback_type") is not None or
            len(version_history) == 0 or
            prep_res["workflow_state"]["current_stage"] == "final_formatting"
        )
        
        if needs_version and content_pieces:
            # Create new version
            action = feedback_state.get("feedback_type", "snapshot")
            user_feedback = feedback_state.get("user_input", "")
            
            version_info = create_version(
                content_pieces,
                action=action,
                user_feedback=user_feedback
            )
            
            print(f"\nCreated new version: {version_info['version_id']}")
            print(f"Action: {version_info['action']}")
            print(f"Timestamp: {version_info['timestamp']}")
            
            return {
                "new_version": version_info,
                "version_created": True,
                "current_version_count": len(version_history) + 1
            }
        else:
            return {
                "new_version": None,
                "version_created": False,
                "current_version_count": len(version_history)
            }
    
    def post(self, shared, prep_res, exec_res):
        """
        Update version history and manage version control.
        """
        if exec_res["version_created"] and exec_res["new_version"]:
            # Add new version to history
            shared["version_history"].append(exec_res["new_version"])
            
            # Add change tracking if there were changes
            feedback_type = shared["feedback_state"].get("feedback_type", "")
            if feedback_type:
                changes = [feedback_type]
                violations_fixed = []  # This would come from quality control in real implementation
                add_change_tracking(
                    exec_res["new_version"]["version_id"],
                    changes,
                    violations_fixed
                )
        
        # Update feedback state
        shared["feedback_state"]["awaiting_feedback"] = False
        shared["feedback_state"]["feedback_type"] = None
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("version_management")
        
        print(f"\nVersion management updated!")
        print(f"Total versions: {exec_res['current_version_count']}")
        
        # Show current version info
        if shared["version_history"]:
            current_version = shared["version_history"][-1]
            print(f"Current version: {current_version['version_id']}")
            print(f"Action: {current_version['action']}")
        
        # Determine next stage
        current_stage = shared["workflow_state"]["current_stage"]
        if current_stage == "version_management":
            shared["workflow_state"]["current_stage"] = "final_formatting"
            print(f"Moving to final formatting stage.")
            return "format"
        else:
            print(f"Continuing workflow from {current_stage}.")
            return "continue"

if __name__ == "__main__":
    # Test the node
    node = VersionManagerNode()
    
    # Create test shared store
    shared = {
        "content_pieces": {
            "linkedin": {
                "text": "AI is transforming marketing in exciting ways. The future holds incredible possibilities for brands that embrace innovation. #AI #Marketing",
                "hashtags": ["#AI", "#Marketing"]
            },
            "twitter": {
                "tweet": "Exciting developments in AI marketing! The future is bright. #AI #Tech"
            }
        },
        "version_history": [
            {
                "version_id": "v1_20240101_100000",
                "timestamp": "2024-01-01T10:00:00Z",
                "content_pieces": {
                    "linkedin": {"text": "Initial version"},
                    "twitter": {"tweet": "Initial tweet"}
                },
                "action": "initial_generation",
                "user_feedback": ""
            }
        ],
        "feedback_state": {
            "awaiting_feedback": False,
            "feedback_type": "content_refinement",
            "user_input": "Made it more conversational",
            "selected_content": {}
        },
        "workflow_state": {
            "current_stage": "version_management",
            "completed_stages": ["engagement", "brand_bible_processing", "format_guidelines", "creative_inspiration", "pattern_aware_prompt_engineering", "content_generation", "style_optimization", "deadly_sins_scanning", "style_compliance", "authenticity_scoring", "feedback_routing", "content_refinement", "pattern_learning"],
            "error_state": None
        }
    }
    
    print("Testing VersionManagerNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    print(f"Version history length: {len(shared['version_history'])}")
    
    if shared['version_history']:
        latest_version = shared['version_history'][-1]
        print(f"Latest version ID: {latest_version['version_id']}")
        print(f"Latest version action: {latest_version['action']}")
