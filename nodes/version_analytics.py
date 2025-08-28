from pocketflow import Node
import json

class VersionAnalyticsNode(Node):
    """
    Provides insights into pattern reduction and revision efficiency.
    Final analytics node that generates comprehensive performance reports.
    """
    
    def prep(self, shared):
        """
        Read version history, quality control, and performance data.
        """
        return {
            "version_history": shared["version_history"],
            "quality_control": shared["quality_control"],
            "authenticity_results": shared.get("authenticity_results", {}),
            "roi_analysis": shared.get("roi_analysis", {}),
            "pattern_learning": shared.get("pattern_learning", {}),
            "user_config": shared["user_config"],
            "task_requirements": shared["task_requirements"]
        }
    
    def exec(self, prep_res):
        """
        Generate comprehensive analytics and insights.
        """
        version_history = prep_res["version_history"]
        quality_control = prep_res["quality_control"]
        authenticity_results = prep_res["authenticity_results"]
        roi_analysis = prep_res["roi_analysis"]
        pattern_learning = prep_res["pattern_learning"]
        
        print(f"\n=== Version Analytics ===")
        print(f"Analyzing {len(version_history)} versions for comprehensive insights...")
        
        # Generate detailed analytics
        analytics_report = self._generate_analytics_report(
            version_history, quality_control, authenticity_results, 
            roi_analysis, pattern_learning, prep_res["user_config"]
        )
        
        # Generate insights and recommendations
        insights = self._generate_insights(analytics_report)
        
        # Create summary statistics
        summary_stats = self._create_summary_statistics(analytics_report)
        
        return {
            "analytics_report": analytics_report,
            "insights": insights,
            "summary_stats": summary_stats,
            "report_generated": True
        }
    
    def _generate_analytics_report(self, version_history, quality_control, authenticity_results, 
                                 roi_analysis, pattern_learning, user_config):
        """
        Generate detailed analytics report.
        """
        report = {
            "version_analysis": self._analyze_versions(version_history),
            "quality_metrics": self._analyze_quality(quality_control, authenticity_results),
            "efficiency_metrics": self._analyze_efficiency(version_history, roi_analysis),
            "pattern_analysis": self._analyze_patterns(pattern_learning),
            "user_preferences": self._analyze_user_preferences(user_config)
        }
        
        return report
    
    def _analyze_versions(self, version_history):
        """
        Analyze version history and actions.
        """
        if not version_history:
            return {"total_versions": 0, "actions": {}, "timeline": []}
        
        actions = {}
        timeline = []
        
        for version in version_history:
            action = version.get("action", "unknown")
            actions[action] = actions.get(action, 0) + 1
            timeline.append({
                "version_id": version["version_id"],
                "timestamp": version["timestamp"],
                "action": action
            })
        
        return {
            "total_versions": len(version_history),
            "actions": actions,
            "timeline": timeline,
            "first_version": timeline[0]["timestamp"] if timeline else None,
            "last_version": timeline[-1]["timestamp"] if timeline else None
        }
    
    def _analyze_quality(self, quality_control, authenticity_results):
        """
        Analyze quality metrics and authenticity scores.
        """
        metrics = {
            "authenticity_scores": {},
            "pattern_violations": {},
            "revision_count": quality_control.get("revision_count", 0),
            "max_revisions_reached": quality_control.get("max_revisions_reached", False)
        }
        
        # Add authenticity scores
        if authenticity_results:
            metrics["authenticity_scores"] = {
                platform: result["authenticity_score"] 
                for platform, result in authenticity_results.items()
            }
        
        # Add pattern violations
        violations = quality_control.get("deadly_sins_violations", {})
        if violations:
            metrics["pattern_violations"] = {
                platform: data.get("total_violations", 0)
                for platform, data in violations.items()
            }
        
        return metrics
    
    def _analyze_efficiency(self, version_history, roi_analysis):
        """
        Analyze efficiency metrics and ROI.
        """
        efficiency = {
            "time_saved": roi_analysis.get("total_time_saved", 0),
            "pattern_reduction_rate": roi_analysis.get("pattern_reduction_rate", 0),
            "estimated_roi": roi_analysis.get("estimated_roi", "0%"),
            "revision_cycles_avoided": roi_analysis.get("revision_cycles_avoided", 0)
        }
        
        # Calculate version processing time (if timestamps available)
        if version_history and len(version_history) > 1:
            try:
                from datetime import datetime
                first_time = datetime.fromisoformat(version_history[0]["timestamp"].replace('Z', '+00:00'))
                last_time = datetime.fromisoformat(version_history[-1]["timestamp"].replace('Z', '+00:00'))
                processing_duration = (last_time - first_time).total_seconds() / 60  # minutes
                efficiency["processing_duration_minutes"] = round(processing_duration, 1)
            except Exception:
                efficiency["processing_duration_minutes"] = 0
        
        return efficiency
    
    def _analyze_patterns(self, pattern_learning):
        """
        Analyze pattern learning and improvements.
        """
        if not pattern_learning:
            return {"learned_patterns": 0, "improvement_rate": 0, "key_insights": []}
        
        learned_patterns = len(pattern_learning.get("learned_patterns", {}))
        prompt_improvements = len(pattern_learning.get("prompt_improvements", {}))
        
        insights = []
        if "pattern_reduction" in pattern_learning.get("learned_patterns", {}):
            reduction_rate = pattern_learning["learned_patterns"]["pattern_reduction"]["rate"]
            insights.append(f"Pattern reduction rate: {reduction_rate:.1f}%")
        
        return {
            "learned_patterns": learned_patterns,
            "prompt_improvements": prompt_improvements,
            "improvement_rate": pattern_learning.get("learned_patterns", {}).get("pattern_reduction", {}).get("rate", 0),
            "key_insights": insights
        }
    
    def _analyze_user_preferences(self, user_config):
        """
        Analyze user configuration preferences.
        """
        return {
            "model": user_config.get("model", "unknown"),
            "temperature": user_config.get("temperature", 0.7),
            "user_type": user_config.get("individual_or_brand", "unknown"),
            "platforms_used": len(user_config.get("platforms", []))
        }
    
    def _generate_insights(self, analytics_report):
        """
        Generate actionable insights from analytics.
        """
        insights = []
        version_analysis = analytics_report["version_analysis"]
        quality_metrics = analytics_report["quality_metrics"]
        efficiency_metrics = analytics_report["efficiency_metrics"]
        
        # Version insights
        if version_analysis["total_versions"] > 5:
            insights.append("✅ High version iteration suggests thorough refinement process")
        elif version_analysis["total_versions"] == 1:
            insights.append("⚠️ Single version generated - consider refinement for better quality")
        
        # Quality insights
        avg_authenticity = sum(quality_metrics["authenticity_scores"].values()) / len(quality_metrics["authenticity_scores"]) if quality_metrics["authenticity_scores"] else 0
        if avg_authenticity > 85:
            insights.append("✅ High authenticity scores indicate natural, human-like content")
        elif avg_authenticity < 70:
            insights.append("⚠️ Low authenticity scores - content may sound too AI-generated")
        
        # Efficiency insights
        time_saved = efficiency_metrics["time_saved"]
        if time_saved > 30:
            insights.append("✅ Significant time savings achieved through automation")
        elif time_saved > 10:
            insights.append("✅ Moderate time savings from automated content generation")
        
        pattern_reduction = efficiency_metrics["pattern_reduction_rate"]
        if pattern_reduction > 80:
            insights.append("✅ Excellent pattern reduction - content appears authentic")
        elif pattern_reduction < 50:
            insights.append("⚠️ Low pattern reduction - content may contain AI fingerprints")
        
        return insights
    
    def _create_summary_statistics(self, analytics_report):
        """
        Create summary statistics for quick overview.
        """
        version_analysis = analytics_report["version_analysis"]
        quality_metrics = analytics_report["quality_metrics"]
        efficiency_metrics = analytics_report["efficiency_metrics"]
        pattern_analysis = analytics_report["pattern_analysis"]
        
        avg_authenticity = sum(quality_metrics["authenticity_scores"].values()) / len(quality_metrics["authenticity_scores"]) if quality_metrics["authenticity_scores"] else 0
        
        return {
            "total_versions": version_analysis["total_versions"],
            "avg_authenticity": round(avg_authenticity, 1),
            "total_violations": sum(quality_metrics["pattern_violations"].values()),
            "time_saved_minutes": efficiency_metrics["time_saved"],
            "pattern_reduction_rate": efficiency_metrics["pattern_reduction_rate"],
            "roi_percentage": efficiency_metrics["estimated_roi"],
            "learned_patterns": pattern_analysis["learned_patterns"],
            "revision_count": quality_metrics["revision_count"]
        }
    
    def post(self, shared, prep_res, exec_res):
        """
        Save analytics report and update shared store.
        """
        # Save analytics report to file
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"analytics_report_{timestamp}.json"
        
        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                json.dump(exec_res["analytics_report"], f, indent=2, default=str)
            print(f"\n✅ Analytics report saved to: {report_filename}")
        except Exception as e:
            print(f"\n⚠️  Error saving analytics report: {e}")
            report_filename = None
        
        # Update shared store
        shared["analytics_report"] = {
            "report_data": exec_res["analytics_report"],
            "insights": exec_res["insights"],
            "summary_stats": exec_res["summary_stats"],
            "report_filename": report_filename
        }
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("version_analytics")
        shared["workflow_state"]["current_stage"] = "final_output"
        
        print(f"\nVersion analytics completed!")
        print(f"Report generated: {exec_res['report_generated']}")
        
        # Show summary statistics
        stats = exec_res["summary_stats"]
        print(f"\nPerformance Summary:")
        print(f"  - Versions generated: {stats['total_versions']}")
        print(f"  - Average authenticity: {stats['avg_authenticity']}")
        print(f"  - Pattern violations: {stats['total_violations']}")
        print(f"  - Time saved: {stats['time_saved_minutes']} minutes")
        print(f"  - Pattern reduction: {stats['pattern_reduction_rate']}%")
        print(f"  - Estimated ROI: {stats['roi_percentage']}")
        print(f"  - Learned patterns: {stats['learned_patterns']}")
        print(f"  - Revisions: {stats['revision_count']}")
        
        # Show key insights
        if exec_res["insights"]:
            print(f"\nKey Insights:")
            for insight in exec_res["insights"][:5]:  # Show top 5
                print(f"  {insight}")
        
        # Generate final completion message
        avg_authenticity = stats['avg_authenticity']
        if avg_authenticity >= 90:
            quality_msg = "Excellent quality content generated! 🎉"
        elif avg_authenticity >= 80:
            quality_msg = "High quality content generated! ✅"
        elif avg_authenticity >= 70:
            quality_msg = "Good quality content generated. 👍"
        else:
            quality_msg = "Content generated - consider refinement for better quality. 🔄"
        
        time_saved = stats['time_saved_minutes']
        if time_saved > 30:
            efficiency_msg = f"Saved you {time_saved} minutes of work! ⏰"
        elif time_saved > 10:
            efficiency_msg = f"Saved you {time_saved} minutes - great efficiency! ⚡"
        else:
            efficiency_msg = f"Generated content efficiently. 🚀"
        
        print(f"\n{quality_msg}")
        print(f"{efficiency_msg}")
        
        return "completed"  # Final completion

if __name__ == "__main__":
    # Test the node
    node = VersionAnalyticsNode()
    
    # Create test shared store
    shared = {
        "version_history": [
            {
                "version_id": "v1_20240101_100000",
                "timestamp": "2024-01-01T10:00:00Z",
                "action": "initial_generation",
                "user_feedback": ""
            },
            {
                "version_id": "v2_20240101_110000",
                "timestamp": "2024-01-01T11:00:00Z",
                "action": "content_refinement",
                "user_feedback": "Made more conversational"
            }
        ],
        "quality_control": {
            "deadly_sins_violations": {
                "linkedin": {"total_violations": 0},
                "twitter": {"total_violations": 0}
            },
            "revision_count": 1,
            "max_revisions_reached": False,
            "authenticity_scores": {
                "linkedin": 87,
                "twitter": 82
            }
        },
        "authenticity_results": {
            "linkedin": {"authenticity_score": 87},
            "twitter": {"authenticity_score": 82}
        },
        "roi_analysis": {
            "total_time_saved": 25.5,
            "pattern_reduction_rate": 95.2,
            "estimated_roi": "185.0%",
            "revision_cycles_avoided": 2
        },
        "pattern_learning": {
            "learned_patterns": {
                "pattern_reduction": {"rate": 95.2},
                "common_violations": {"em_dash": 3, "rhetorical_contrast": 2}
            },
            "prompt_improvements": {
                "avoid_patterns": ["avoid em dashes", "natural sentence flow"],
                "style_guidance": "use conversational tone"
            }
        },
        "user_config": {
            "individual_or_brand": "brand",
            "name": "TestBrand",
            "model": "openrouter/anthropic/claude-3.5-sonnet",
            "temperature": 0.7,
            "platforms": ["linkedin", "twitter"]
        },
        "task_requirements": {
            "topic": "AI in Marketing",
            "platforms": ["linkedin", "twitter"]
        },
        "workflow_state": {
            "current_stage": "version_analytics",
            "completed_stages": ["engagement", "brand_bible_processing", "format_guidelines", "creative_inspiration", "pattern_aware_prompt_engineering", "content_generation", "style_optimization", "deadly_sins_scanning", "style_compliance", "authenticity_scoring", "feedback_routing", "content_refinement", "pattern_learning", "version_management", "final_formatting", "preset_optimization"],
            "error_state": None
        }
    }
    
    print("Testing VersionAnalyticsNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    
    if "analytics_report" in shared:
        print(f"Analytics report generated successfully!")
        stats = shared['analytics_report']['summary_stats']
        print(f"Total versions: {stats['total_versions']}")
        print(f"Average authenticity: {stats['avg_authenticity']}")
        print(f"Time saved: {stats['time_saved_minutes']} minutes")
