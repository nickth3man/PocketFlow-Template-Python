import json
from datetime import datetime
from nodes.progress_tracker import ProgressTrackerNode

def test_progress_tracker():
    print("Testing ProgressTrackerNode...")
    
    # Initialize shared store with sample data
    shared = {
        'workflow_state': {'current_stage': 'content_generation'},
        'task_requirements': {'platforms': ['email', 'linkedin', 'twitter']},
        'quality_control': {'revision_count': 2}
    }
    
    # Create and run the node
    tracker = ProgressTrackerNode()
    result = tracker.run(shared)
    
    # Print results
    print("\nShared Store After ProgressTrackerNode:")
    print(json.dumps(shared, indent=2))
    
    # Simulate stage transition
    print("\nSimulating stage transition...")
    shared['workflow_state']['current_stage'] = 'deadly_sins_scanner'
    tracker.run(shared)
    
    print("\nShared Store After Stage Transition:")
    print(json.dumps(shared, indent=2))
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_progress_tracker()
