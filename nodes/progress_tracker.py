import json
from datetime import datetime
from pocketflow import Node

class ProgressTrackerNode(Node):
    """Tracks workflow progress and updates shared store with metrics"""
    def __init__(self):
        super().__init__()
        self.node_name = "progress_tracker"
        self.successors = []  # Required by PocketFlow Node class
        
    def prep(self, shared):
        """Prepares required data from shared store"""
        return {
            'workflow_state': shared.get('workflow_state', {}),
            'task_requirements': shared.get('task_requirements', {}),
            'quality_control': shared.get('quality_control', {})
        }
        
    def exec(self, inputs):
        """Tracks progress metrics and timings"""
        return {
            'stage_start': datetime.now().isoformat(),
            'platforms_processed': len(inputs['task_requirements'].get('platforms', [])),
            'revision_count': inputs['quality_control'].get('revision_count', 0),
            'current_stage': inputs['workflow_state'].get('current_stage', '')
        }
        
    def post(self, shared, prep_res, exec_res):
        """Updates shared store with progress data"""
        if 'progress_metrics' not in shared:
            shared['progress_metrics'] = {}
            
        # Create or update progress entry
        stage = exec_res['current_stage']
        shared['progress_metrics'][stage] = {
            'start_time': exec_res['stage_start'],
            'platforms': exec_res['platforms_processed'],
            'revisions': exec_res['revision_count'],
            'completed': False
        }
        
        # Mark previous stage as completed
        if 'current_stage' in shared['workflow_state']:
            prev_stage = shared['workflow_state']['current_stage']
            if prev_stage in shared['progress_metrics']:
                shared['progress_metrics'][prev_stage]['completed'] = True
                shared['progress_metrics'][prev_stage]['end_time'] = datetime.now().isoformat()
                
        return "default"
