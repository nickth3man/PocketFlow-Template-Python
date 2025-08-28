from pocketflow import Node
from utils.presets_manager import save_preset, load_preset, list_presets

class PresetOptimizerNode(Node):
    """
    Learns from user preferences to improve preset configurations.
    Node that optimizes presets based on user interactions and outcomes.
    """
    
    def prep(self, shared):
        """
        Read user configuration, version history, and performance data.
        """
        return {
            "user_config": shared["user_config"],
            "task_requirements": shared["task_requirements"],
            "brand_voice": shared["brand_voice"],
            "version_history": shared["version_history"],
            "quality_control": shared["quality_control"],
            "authenticity_results": shared.get("authenticity_results", {}),
            "roi_analysis": shared.get("roi_analysis", {}),
            "pattern_learning": shared.get("pattern_learning", {})
        }
    
    def exec(self, prep_res):
        """
        Analyze user preferences and optimize preset configurations.
        """
        user_config = prep_res["user_config"]
        task_requirements = prep_res["task_requirements"]
        brand_voice = prep_res["brand_voice"]
        version_history = prep_res["version_history"]
        quality_control = prep_res["quality_control"]
        authenticity_results = prep_res["authenticity_results"]
        roi_analysis = prep_res["roi_analysis"]
        pattern_learning = prep_res["pattern_learning"]
        
        print(f"\n=== Preset Optimization ===")
        print(f"Analyzing {len(version_history)} versions for preset optimization...")
        
        # Analyze performance metrics
        performance_metrics = self._analyze_performance(
            version_history, quality_control, authenticity_results, roi_analysis
        )
        
        # Identify optimization opportunities
        optimizations = self._identify_optimizations(
            user_config, brand_voice, performance_metrics, pattern_learning
        )
        
        # Generate optimized preset
        optimized_preset = self._generate_optimized_preset(
            user_config, task_requirements, brand_voice, 
            performance_metrics, optimizations, pattern_learning
        )
        
        return {
            "optimized_preset": optimized_preset,
            "performance_metrics": performance_metrics,
            "optimizations": optimizations,
            "preset_name": f"Optimized_{user_config.get('name', 'User')}_{len(version_history)}_versions"
        }
    
    def _analyze_performance(self, version_history, quality_control, authenticity_results, roi_analysis):
        """
        Analyze performance metrics from version history and quality data.
        """
        metrics = {
            "version_count": len(version_history),
            "avg_authenticity": 0,
            "pattern_reduction_rate": 0,
            "revision_efficiency": 0,
            "time_saved": roi_analysis.get("total_time_saved", 0),
            "roi_percentage": roi_analysis.get("estimated_roi", "0%").rstrip('%')
        }
        
        # Calculate average authenticity
        if authenticity_results:
            scores = [result["authenticity_score"] for result in authenticity_results.values()]
            if scores:
                metrics["avg_authenticity"] = sum(scores) / len(scores)
        
        # Calculate pattern reduction rate
        if "pattern_reduction_rate" in roi_analysis:
            metrics["pattern_reduction_rate"] = roi_analysis["pattern_reduction_rate"]
        
        # Calculate revision efficiency
        if version_history:
            revisions = sum(1 for v in version_history if v.get("action") == "content_refinement")
            metrics["revision_efficiency"] = (len(version_history) - revisions) / len(version_history) if version_history else 0
        
        return metrics
    
    def _identify_optimizations(self, user_config, brand_voice, performance_metrics, pattern_learning):
        """
        Identify optimization opportunities based on performance and learning data.
        """
        optimizations = []
        
        # Model performance optimization
        current_model = user_config.get("model", "")
        if performance_metrics["avg_authenticity"] < 85 and "gpt" in current_model.lower():
            optimizations.append({
                "type": "model_upgrade",
                "suggestion": "Consider upgrading to a more capable model",
                "priority": "medium"
            })
        
        # Temperature optimization
        current_temp = user_config.get("temperature", 0.7)
        if performance_metrics["avg_authenticity"] < 80:
            if current_temp > 0.5:
                optimizations.append({
                    "type": "temperature_adjustment",
                    "suggestion": "Lower temperature for more consistent output",
                    "priority": "high"
                })
            else:
                optimizations.append({
                    "type": "temperature_adjustment",
                    "suggestion": "Increase temperature for more creative output",
                    "priority": "medium"
                })
        
        # Brand voice consistency
        if performance_metrics["avg_authenticity"] < 85:
            optimizations.append({
                "type": "brand_voice_enhancement",
                "suggestion": "Strengthen brand voice definition",
                "priority": "high"
            })
        
        # Pattern learning integration
        if pattern_learning and "prompt_improvements" in pattern_learning:
            optimizations.append({
                "type": "pattern_awareness",
                "suggestion": "Integrate learned pattern avoidance",
                "priority": "high"
            })
        
        return optimizations
    
    def _generate_optimized_preset(self, user_config, task_requirements, brand_voice, 
                                 performance_metrics, optimizations, pattern_learning):
        """
        Generate an optimized preset configuration.
        """
        # Start with current configuration
        optimized_config = {
            "user_config": user_config.copy(),
            "task_requirements": task_requirements.copy(),
            "brand_voice": brand_voice.copy()
        }
        
        # Apply optimizations
        for optimization in optimizations:
            opt_type = optimization["type"]
            
            if opt_type == "temperature_adjustment":
                current_temp = optimized_config["user_config"].get("temperature", 0.7)
                if "lower" in optimization["suggestion"].lower():
                    optimized_config["user_config"]["temperature"] = max(0.1, current_temp - 0.1)
                else:
                    optimized_config["user_config"]["temperature"] = min(1.0, current_temp + 0.1)
            
            elif opt_type == "pattern_awareness" and pattern_learning:
                # Integrate learned pattern improvements
                prompt_improvements = pattern_learning.get("prompt_improvements", {})
                if prompt_improvements:
                    # Add learned avoid patterns to brand voice
                    if "avoid_patterns" in prompt_improvements:
                        if "forbidden_patterns" not in optimized_config["brand_voice"]:
                            optimized_config["brand_voice"]["forbidden_patterns"] = {}
                        
                        # Add learned patterns to forbidden list
                        for pattern in prompt_improvements["avoid_patterns"][:3]:  # Top 3
                            pattern_key = f"learned_pattern_{len(optimized_config['brand_voice']['forbidden_patterns']) + 1}"
                            optimized_config["brand_voice"]["forbidden_patterns"][pattern_key] = {
                                "pattern": pattern,
                                "severity": "high",
                                "source": "learned"
                            }
        
        # Add performance metadata
        optimized_config["performance_metadata"] = {
            "optimization_date": self._get_current_timestamp(),
            "performance_metrics": performance_metrics,
            "applied_optimizations": [opt["type"] for opt in optimizations],
            "version_count": performance_metrics["version_count"]
        }
        
        return optimized_config
    
    def _get_current_timestamp(self):
        """
        Get current timestamp in ISO format.
        """
        import datetime
        return datetime.datetime.now().isoformat()
    
    def post(self, shared, prep_res, exec_res):
        """
        Save optimized preset and update shared store.
        """
        optimized_preset = exec_res["optimized_preset"]
        preset_name = exec_res["preset_name"]
        
        # Save optimized preset
        try:
            preset_id = save_preset(
                name=preset_name,
                preset_data=optimized_preset,
                description=f"Auto-optimized preset based on {exec_res['performance_metrics']['version_count']} versions"
            )
            print(f"\n✅ Optimized preset saved: {preset_id}")
        except Exception as e:
            print(f"\n⚠️  Error saving optimized preset: {e}")
            preset_id = None
        
        # Update shared store
        shared["optimized_preset"] = {
            "preset_id": preset_id,
            "preset_data": optimized_preset,
            "optimizations_applied": exec_res["optimizations"],
            "performance_metrics": exec_res["performance_metrics"]
        }
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("preset_optimization")
        shared["workflow_state"]["current_stage"] = "version_analytics"
        
        print(f"\nPreset optimization completed!")
        print(f"Preset name: {preset_name}")
        print(f"Performance metrics:")
        metrics = exec_res["performance_metrics"]
        print(f"  - Average authenticity: {metrics['avg_authenticity']:.1f}")
        print(f"  - Pattern reduction: {metrics['pattern_reduction_rate']:.1f}%")
        print(f"  - Time saved: {metrics['time_saved']} minutes")
        print(f"  - ROI: {metrics['roi_percentage']}%")
        
        # Show applied optimizations
        if exec_res["optimizations"]:
            print(f"\nApplied optimizations:")
            for opt in exec_res["optimizations"]:
                print(f"  - {opt['type']}: {opt['suggestion']} ({opt['priority']})")
        
        return "continue"  # Continue to next node

if __name__ == "__main__":
    # Test the node
    node = PresetOptimizerNode()
    
    # Create test shared store
    shared = {
        "user_config": {
            "individual_or_brand": "brand",
            "name": "TestBrand",
            "model": "openrouter/anthropic/claude-3.5-sonnet",
            "temperature": 0.7
        },
        "task_requirements": {
            "topic": "AI in Marketing",
            "platforms": ["linkedin", "twitter"],
            "brand_bible_text": "Innovative marketing agency focused on AI and technology."
        },
        "brand_voice": {
            "parsed_attributes": {
                "personality_traits": ["innovative", "professional"],
                "tone": "thought_leadership",
                "voice": "confident",
                "values": ["innovation", "excellence"],
                "themes": ["AI", "technology"]
            },
            "forbidden_patterns": {
                "em_dash": {"pattern": "—", "severity": "critical"},
                "rhetorical_contrast": {"pattern": r"It's not just .+; it's .+", "severity": "critical"}
            }
        },
        "version_history": [
            {"version_id": "v1", "action": "initial_generation", "timestamp": "2024-01-01T10:00:00Z"},
            {"version_id": "v2", "action": "content_refinement", "timestamp": "2024-01-01T11:00:00Z"}
        ],
        "quality_control": {
            "deadly_sins_violations": {
                "v1": {"linkedin": {"total_violations": 2}},
                "v2": {"linkedin": {"total_violations": 0}}
            },
            "revision_count": 1
        },
        "authenticity_results": {
            "linkedin": {"authenticity_score": 87},
            "twitter": {"authenticity_score": 82}
        },
        "roi_analysis": {
            "total_time_saved": 15.5,
            "pattern_reduction_rate": 92.3,
            "estimated_roi": "174.0%"
        },
        "pattern_learning": {
            "prompt_improvements": {
                "avoid_patterns": ["avoid em dashes", "don't use rhetorical contrasts"],
                "style_guidance": "Use more natural sentence structures"
            }
        },
        "workflow_state": {
            "current_stage": "preset_optimization",
            "completed_stages": ["engagement", "brand_bible_processing", "format_guidelines", "creative_inspiration", "pattern_aware_prompt_engineering", "content_generation", "style_optimization", "deadly_sins_scanning", "style_compliance", "authenticity_scoring", "feedback_routing", "content_refinement", "pattern_learning", "version_management", "final_formatting"],
            "error_state": None
        }
    }
    
    print("Testing PresetOptimizerNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    
    if "optimized_preset" in shared:
        print(f"Optimized preset ID: {shared['optimized_preset']['preset_id']}")
        print(f"Optimizations applied: {len(shared['optimized_preset']['optimizations_applied'])}")
        metrics = shared['optimized_preset']['performance_metrics']
        print(f"Average authenticity: {metrics['avg_authenticity']:.1f}")
