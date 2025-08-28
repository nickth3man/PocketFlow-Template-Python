from pocketflow import Node
from utils.authenticity_scorer import score_authenticity
from utils.pattern_learner import get_prompt_improvements

class StyleComplianceNode(Node):
    """
    Final validation and revision loop management.
    Eighth node that checks compliance and manages revision cycles.
    """
    
    def prep(self, shared):
        """
        Read content_pieces and revision information from shared store.
        """
        return {
            "content_pieces": shared["content_pieces"],
            "brand_voice": shared["brand_voice"],
            "quality_control": shared["quality_control"],
            "version_history": shared["version_history"],
            "platform_guidelines": shared["platform_guidelines"]
        }
    
    def exec(self, prep_res):
        """
        Validate content and manage revision loop.
        """
        quality_control = prep_res["quality_control"]
        revision_count = quality_control.get("revision_count", 0)
        max_revisions = 5  # Maximum revision cycles
        
        # Check if maximum revisions reached
        if revision_count >= max_revisions:
            return {
                "compliance_status": "manual_review",
                "reason": f"Maximum revision count ({max_revisions}) reached",
                "authenticity_scores": {},
                "recommendations": []
            }
        
        # Score authenticity for each platform
        authenticity_scores = {}
        all_compliant = True
        recommendations = []
        
        for platform, content in prep_res["content_pieces"].items():
            # Extract content text
            content_text = self._get_content_text(content, platform)
            
            # Score authenticity
            score_result = score_authenticity(
                text=content_text,
                brand_voice=prep_res["brand_voice"]["parsed_attributes"],
                pattern_history=quality_control.get("deadly_sins_violations", {}).get(platform, {})
            )
            
            authenticity_scores[platform] = score_result
            
            # Check if compliant (authenticity score > 80 and no critical violations)
            is_compliant = (
                score_result["authenticity_score"] >= 80 and
                quality_control["deadly_sins_violations"].get(platform, {}).get("total_violations", 0) == 0
            )
            
            if not is_compliant:
                all_compliant = False
                # Add recommendations
                platform_recommendations = score_result.get("recommendations", [])
                recommendations.extend([f"{platform}: {rec}" for rec in platform_recommendations])
        
        # Determine compliance status
        if all_compliant:
            compliance_status = "pass"
            reason = "All content meets authenticity and quality standards"
        else:
            compliance_status = "revise"
            reason = "Content needs revision to meet authenticity standards"
            
            # Increment revision count
            revision_count += 1
        
        return {
            "compliance_status": compliance_status,
            "reason": reason,
            "authenticity_scores": authenticity_scores,
            "recommendations": recommendations,
            "revision_count": revision_count,
            "all_compliant": all_compliant
        }
    
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
        Update quality control and manage workflow based on compliance results.
        """
        # Update quality control
        shared["quality_control"]["revision_count"] = exec_res["revision_count"]
        shared["quality_control"]["compliance_status"] = exec_res["compliance_status"]
        shared["quality_control"]["max_revisions_reached"] = exec_res["revision_count"] >= 5
        
        # Store authenticity scores
        shared["quality_control"]["authenticity_scores"] = exec_res["authenticity_scores"]
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("style_compliance")
        
        print(f"\nStyle compliance check completed!")
        print(f"Status: {exec_res['compliance_status']}")
        print(f"Reason: {exec_res['reason']}")
        print(f"Revision count: {exec_res['revision_count']}/5")
        
        # Show authenticity scores
        if exec_res["authenticity_scores"]:
            print(f"\nAuthenticity Scores:")
            for platform, score_data in exec_res["authenticity_scores"].items():
                print(f"  {platform.title()}: {score_data['authenticity_score']}/100")
        
        # Show recommendations if any
        if exec_res["recommendations"]:
            print(f"\nRecommendations:")
            for rec in exec_res["recommendations"][:5]:  # Show top 5
                print(f"  - {rec}")
        
        # Determine next action
        if exec_res["compliance_status"] == "pass":
            shared["workflow_state"]["current_stage"] = "authenticity_scoring"
            print(f"\n✅ Content approved! Moving to final formatting.")
            return "approved"
        elif exec_res["compliance_status"] == "manual_review":
            shared["workflow_state"]["current_stage"] = "manual_review"
            print(f"\n⚠️ Maximum revisions reached. Manual review required.")
            return "manual_review"
        else:
            shared["workflow_state"]["current_stage"] = "content_refinement"
            print(f"\n🔄 Content needs revision. Moving to refinement stage.")
            return "revise"

if __name__ == "__main__":
    # Test the node
    node = StyleComplianceNode()
    
    # Create test shared store
    shared = {
        "content_pieces": {
            "linkedin": {
                "text": "AI is transforming marketing. The future is now. #AI #Marketing",
                "hashtags": ["#AI", "#Marketing"]
            },
            "twitter": {
                "tweet": "AI is revolutionizing marketing! #AI #Tech"
            }
        },
        "brand_voice": {
            "parsed_attributes": {
                "personality_traits": ["innovative", "professional"],
                "tone": "thought_leadership",
                "voice": "confident",
                "values": ["innovation", "excellence"],
                "themes": ["AI", "technology"]
            }
        },
        "platform_guidelines": {
            "linkedin": {
                "char_limit": 3000,
                "tone_adjustment": "thought_leadership"
            },
            "twitter": {
                "char_limit": 280,
                "tone_adjustment": "conversational"
            }
        },
        "quality_control": {
            "deadly_sins_violations": {
                "linkedin": {"total_violations": 0},
                "twitter": {"total_violations": 0}
            },
            "revision_count": 0,
            "max_revisions_reached": False,
            "compliance_status": "pending"
        },
        "version_history": [],
        "workflow_state": {
            "current_stage": "style_compliance",
            "completed_stages": ["engagement", "brand_bible_processing", "format_guidelines", "creative_inspiration", "pattern_aware_prompt_engineering", "content_generation", "style_optimization", "deadly_sins_scanning"],
            "error_state": None
        }
    }
    
    print("Testing StyleComplianceNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    print(f"Compliance status: {shared['quality_control']['compliance_status']}")
    print(f"Revision count: {shared['quality_control']['revision_count']}")
