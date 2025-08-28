from pocketflow import Node
from utils.deadly_sins_detector import DeadlySinsDetector

class DeadlySinsScannerNode(Node):
    """
    Detect all 7 specific AI fingerprint patterns with precise location tracking.
    Seventh node that performs detailed pattern scanning.
    """
    
    def prep(self, shared):
        """
        Read content_pieces from shared store.
        """
        return shared["content_pieces"]
    
    def exec(self, prep_res):
        """
        Scan all content for each of the 7 deadly sins patterns.
        """
        content_pieces = prep_res
        detector = DeadlySinsDetector()
        
        # Scan each platform's content
        deadly_sins_violations = {}
        
        for platform, content in content_pieces.items():
            print(f"Scanning {platform} for deadly sins...")
            
            # Extract text content from platform-specific structure
            content_text = self._get_content_text(content, platform)
            
            # Detect patterns using the enhanced detector
            violations = detector.detect_patterns(content_text)
            
            # Store violations with detailed information
            deadly_sins_violations[platform] = violations
            
            print(f"  - Found {violations['total_violations']} violations")
            if violations['total_violations'] > 0:
                for pattern_name, pattern_data in violations['patterns'].items():
                    if pattern_data['count'] > 0:
                        print(f"    * {pattern_name}: {pattern_data['count']} occurrences")
        
        return deadly_sins_violations
    
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
    
    def post(self, shared, prep_res, exec_res):
        """
        Write detailed deadly_sins_violations with counts and positions to shared store.
        """
        # Update shared store with detailed violations
        shared["quality_control"]["deadly_sins_violations"] = exec_res
        
        # Calculate severity score
        total_violations = 0
        severity_score = 0
        
        for platform, violations in exec_res.items():
            total_violations += violations["total_violations"]
            severity_score += violations["severity_score"]
        
        # Update quality control metrics
        shared["quality_control"]["total_violations"] = total_violations
        shared["quality_control"]["severity_score"] = severity_score
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("deadly_sins_scanning")
        shared["workflow_state"]["current_stage"] = "style_compliance"
        
        print(f"\nDeadly sins scanning completed!")
        print(f"Total violations found: {total_violations}")
        print(f"Overall severity score: {severity_score:.2f}")
        
        # Show detailed results
        for platform, violations in exec_res.items():
            if violations["total_violations"] > 0:
                print(f"\n{platform.title()} violations:")
                for pattern_name, pattern_data in violations["patterns"].items():
                    if pattern_data["count"] > 0:
                        print(f"  - {pattern_name}: {pattern_data['count']} ({pattern_data['severity']})")
        
        return "default"  # Go to next node

if __name__ == "__main__":
    # Test the node
    node = DeadlySinsScannerNode()
    
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
        "workflow_state": {
            "current_stage": "deadly_sins_scanning",
            "completed_stages": ["engagement", "brand_bible_processing", "format_guidelines", "creative_inspiration", "pattern_aware_prompt_engineering", "content_generation", "style_optimization"],
            "error_state": None
        },
        "quality_control": {
            "deadly_sins_violations": {},
            "revision_count": 0,
            "max_revisions_reached": False,
            "compliance_status": "pending"
        }
    }
    
    print("Testing DeadlySinsScannerNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    print(f"Violations found: {shared['quality_control']['deadly_sins_violations'].keys()}")
    
    # Show violation details
    for platform, violations in shared['quality_control']['deadly_sins_violations'].items():
        print(f"\n{platform.title()} violations:")
        print(f"  Total: {violations['total_violations']}")
        for pattern_name, pattern_data in violations['patterns'].items():
            if pattern_data['count'] > 0:
                print(f"  - {pattern_name}: {pattern_data['count']}")
