from pocketflow import Node
from utils.markdown_formatter import format_content_as_markdown

class FinalFormatterNode(Node):
    """
    Outputs clean markdown with copy buttons.
    Final node that formats content for presentation and export.
    """
    
    def prep(self, shared):
        """
        Read final content and formatting requirements from shared store.
        """
        return {
            "content_pieces": shared["content_pieces"],
            "task_requirements": shared["task_requirements"],
            "brand_voice": shared["brand_voice"],
            "platform_guidelines": shared["platform_guidelines"],
            "authenticity_results": shared.get("authenticity_results", {}),
            "roi_analysis": shared.get("roi_analysis", {}),
            "version_history": shared["version_history"]
        }
    
    def exec(self, prep_res):
        """
        Format final output with platform sections and copy functionality.
        """
        content_pieces = prep_res["content_pieces"]
        task_requirements = prep_res["task_requirements"]
        brand_voice = prep_res["brand_voice"]
        platform_guidelines = prep_res["platform_guidelines"]
        authenticity_results = prep_res["authenticity_results"]
        roi_analysis = prep_res["roi_analysis"]
        
        print(f"\n=== Final Formatting ===")
        print(f"Formatting content for {len(content_pieces)} platforms...")
        
        # Format content as markdown
        markdown_output = format_content_as_markdown(
            content_pieces=content_pieces,
            task_requirements=task_requirements,
            brand_voice=brand_voice,
            platform_guidelines=platform_guidelines,
            authenticity_results=authenticity_results,
            roi_analysis=roi_analysis
        )
        
        # Generate filename based on topic and timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        topic_slug = "".join(c for c in task_requirements["topic"] if c.isalnum() or c in " _-").rstrip()
        topic_slug = topic_slug.replace(" ", "_")[:50]  # Limit length
        filename = f"content_{topic_slug}_{timestamp}.md"
        
        return {
            "formatted_content": markdown_output,
            "filename": filename,
            "platforms_formatted": list(content_pieces.keys()),
            "content_stats": self._get_content_stats(content_pieces)
        }
    
    def _get_content_stats(self, content_pieces):
        """
        Get statistics about the formatted content.
        """
        stats = {}
        total_chars = 0
        total_words = 0
        
        for platform, content in content_pieces.items():
            content_text = self._get_content_text(content, platform)
            char_count = len(content_text)
            word_count = len(content_text.split())
            
            stats[platform] = {
                "characters": char_count,
                "words": word_count
            }
            
            total_chars += char_count
            total_words += word_count
        
        stats["total"] = {
            "characters": total_chars,
            "words": total_words,
            "platforms": len(content_pieces)
        }
        
        return stats
    
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
        Save formatted content and prepare for output.
        """
        # Save formatted content to file
        filename = exec_res["filename"]
        formatted_content = exec_res["formatted_content"]
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            print(f"\n✅ Formatted content saved to: {filename}")
        except Exception as e:
            print(f"\n⚠️  Error saving file: {e}")
            filename = None
        
        # Update shared store with final output info
        shared["final_output"] = {
            "filename": filename,
            "content": formatted_content,
            "platforms": exec_res["platforms_formatted"],
            "stats": exec_res["content_stats"]
        }
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("final_formatting")
        shared["workflow_state"]["current_stage"] = "final_output"
        
        print(f"\nFinal formatting completed!")
        print(f"Platforms formatted: {', '.join(exec_res['platforms_formatted'])}")
        
        # Show content statistics
        stats = exec_res["content_stats"]
        print(f"\nContent Statistics:")
        print(f"  Total characters: {stats['total']['characters']:,}")
        print(f"  Total words: {stats['total']['words']:,}")
        print(f"  Platforms: {stats['total']['platforms']}")
        
        for platform in exec_res["platforms_formatted"]:
            if platform in stats:
                print(f"  {platform.title()}: {stats[platform]['characters']} chars, {stats[platform]['words']} words")
        
        # Show authenticity scores if available
        if prep_res["authenticity_results"]:
            print(f"\nAuthenticity Scores:")
            for platform, score_data in prep_res["authenticity_results"].items():
                print(f"  {platform.title()}: {score_data['authenticity_score']}/100")
        
        # Show ROI analysis if available
        if prep_res["roi_analysis"]:
            roi = prep_res["roi_analysis"]
            print(f"\nROI Analysis:")
            print(f"  Time saved: {roi.get('total_time_saved', 0)} minutes")
            print(f"  Pattern reduction: {roi.get('pattern_reduction_rate', 0)}%")
            print(f"  Estimated ROI: {roi.get('estimated_roi', 'N/A')}")
        
        return "completed"  # Final node complete

if __name__ == "__main__":
    # Test the node
    node = FinalFormatterNode()
    
    # Create test shared store
    shared = {
        "content_pieces": {
            "linkedin": {
                "text": "AI is transforming marketing in exciting ways. The future holds incredible possibilities for brands that embrace innovation. #AI #Marketing #DigitalTransformation",
                "hashtags": ["#AI", "#Marketing", "#DigitalTransformation"]
            },
            "twitter": {
                "tweet": "Exciting developments in AI marketing! The future is bright. #AI #Marketing"
            }
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
            }
        },
        "platform_guidelines": {
            "linkedin": {
                "char_limit": 3000,
                "tone_adjustment": "thought_leadership",
                "hashtag_count": 3
            },
            "twitter": {
                "char_limit": 280,
                "tone_adjustment": "conversational"
            }
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
        "version_history": [
            {"version_id": "v1", "action": "initial_generation"},
            {"version_id": "v2", "action": "content_refinement"}
        ],
        "workflow_state": {
            "current_stage": "final_formatting",
            "completed_stages": ["engagement", "brand_bible_processing", "format_guidelines", "creative_inspiration", "pattern_aware_prompt_engineering", "content_generation", "style_optimization", "deadly_sins_scanning", "style_compliance", "authenticity_scoring", "feedback_routing", "content_refinement", "pattern_learning", "version_management"],
            "error_state": None
        }
    }
    
    print("Testing FinalFormatterNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    
    if "final_output" in shared:
        print(f"Final output filename: {shared['final_output']['filename']}")
        print(f"Platforms formatted: {shared['final_output']['platforms']}")
        print(f"Total characters: {shared['final_output']['stats']['total']['characters']:,}")
        
        # Show first 200 characters of formatted content
        if shared['final_output']['content']:
            print(f"Formatted content preview:\n{shared['final_output']['content'][:200]}...")
