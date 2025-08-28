from pocketflow import Node

class FeedbackRouterNode(Node):
    """
    Handles user feedback for iterative refinement with version control.
    Node that manages feedback routing and version management.
    """
    
    def prep(self, shared):
        """
        Read current state and determine feedback routing options.
        """
        return {
            "content_pieces": shared["content_pieces"],
            "authenticity_results": shared.get("authenticity_results", {}),
            "quality_control": shared["quality_control"],
            "workflow_state": shared["workflow_state"]
        }
    
    def exec(self, prep_res):
        """
        Handle user feedback routing and version management decisions.
        """
        content_pieces = prep_res["content_pieces"]
        authenticity_results = prep_res["authenticity_results"]
        quality_control = prep_res["quality_control"]
        
        print(f"\n=== Feedback Router ===")
        print("Content generation complete! What would you like to do?")
        print()
        
        # Show content summary
        print("Generated content for platforms:")
        for platform, content in content_pieces.items():
            auth_score = authenticity_results.get(platform, {}).get("authenticity_score", 0)
            print(f"  {platform.title()}: {auth_score}/100 authenticity")
        
        print()
        print("Options:")
        print("1. Review and refine content")
        print("2. Make specific edits to individual pieces")
        print("3. Regenerate specific platforms")
        print("4. Save current version and exit")
        print("5. View detailed results")
        print("6. Exit without changes")
        
        choice = input("Select option (1-6): ").strip()
        
        if choice == "1":
            return {
                "action": "review_refine",
                "feedback_type": "general_refinement",
                "selected_content": content_pieces
            }
        elif choice == "2":
            # Let user select specific platform to edit
            platforms = list(content_pieces.keys())
            print(f"\nSelect platform to edit:")
            for i, platform in enumerate(platforms, 1):
                print(f"{i}. {platform.title()}")
            
            try:
                selection = int(input(f"Select platform (1-{len(platforms)}): ").strip()) - 1
                if 0 <= selection < len(platforms):
                    selected_platform = platforms[selection]
                    return {
                        "action": "edit_specific",
                        "feedback_type": "sentence_edit",
                        "selected_content": {selected_platform: content_pieces[selected_platform]},
                        "selected_platform": selected_platform
                    }
            except ValueError:
                pass
            
            return {
                "action": "review_refine",
                "feedback_type": "general_refinement",
                "selected_content": content_pieces
            }
        elif choice == "3":
            # Let user select platforms to regenerate
            platforms = list(content_pieces.keys())
            print(f"\nSelect platforms to regenerate (comma-separated numbers):")
            for i, platform in enumerate(platforms, 1):
                print(f"{i}. {platform.title()}")
            
            try:
                selections = input("Select platforms: ").strip()
                selected_indices = [int(x.strip()) - 1 for x in selections.split(",")]
                selected_platforms = [platforms[i] for i in selected_indices if 0 <= i < len(platforms)]
                
                if selected_platforms:
                    return {
                        "action": "regenerate",
                        "feedback_type": "regenerate_platforms",
                        "selected_platforms": selected_platforms,
                        "selected_content": {p: content_pieces[p] for p in selected_platforms}
                    }
            except ValueError:
                pass
            
            return {
                "action": "review_refine",
                "feedback_type": "general_refinement",
                "selected_content": content_pieces
            }
        elif choice == "4":
            return {
                "action": "save_exit",
                "feedback_type": "done",
                "selected_content": content_pieces
            }
        elif choice == "5":
            return {
                "action": "view_details",
                "feedback_type": "view_details",
                "selected_content": content_pieces
            }
        else:  # choice == "6" or invalid
            return {
                "action": "exit",
                "feedback_type": "done",
                "selected_content": content_pieces
            }
    
    def post(self, shared, prep_res, exec_res):
        """
        Update feedback state and route to appropriate next node.
        """
        # Update feedback state in shared store
        shared["feedback_state"] = {
            "awaiting_feedback": True,
            "feedback_type": exec_res["feedback_type"],
            "user_input": "",
            "selected_content": exec_res["selected_content"]
        }
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("feedback_routing")
        
        action = exec_res["action"]
        
        if action == "review_refine":
            shared["workflow_state"]["current_stage"] = "content_refinement"
            print(f"\n🔄 Moving to content refinement stage.")
            return "refine"
        elif action == "edit_specific":
            shared["workflow_state"]["current_stage"] = "content_refinement"
            print(f"\n✏️  Editing {exec_res['selected_platform']} content.")
            return "edit"
        elif action == "regenerate":
            shared["workflow_state"]["current_stage"] = "content_regeneration"
            print(f"\n🔄 Regenerating content for: {', '.join(exec_res['selected_platforms'])}")
            return "regenerate"
        elif action == "save_exit":
            shared["workflow_state"]["current_stage"] = "final_formatting"
            print(f"\n💾 Saving current version and preparing final output.")
            return "save"
        elif action == "view_details":
            shared["workflow_state"]["current_stage"] = "detailed_view"
            print(f"\n📊 Showing detailed results.")
            return "view"
        else:  # exit
            shared["workflow_state"]["current_stage"] = "final_output"
            print(f"\n👋 Exiting without further changes.")
            return "exit"

if __name__ == "__main__":
    # Test the node
    node = FeedbackRouterNode()
    
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
        "authenticity_results": {
            "linkedin": {"authenticity_score": 85},
            "twitter": {"authenticity_score": 78}
        },
        "quality_control": {
            "deadly_sins_violations": {
                "linkedin": {"total_violations": 0},
                "twitter": {"total_violations": 0}
            },
            "revision_count": 1,
            "max_revisions_reached": False,
            "compliance_status": "pass"
        },
        "workflow_state": {
            "current_stage": "feedback_routing",
            "completed_stages": ["engagement", "brand_bible_processing", "format_guidelines", "creative_inspiration", "pattern_aware_prompt_engineering", "content_generation", "style_optimization", "deadly_sins_scanning", "style_compliance", "authenticity_scoring"],
            "error_state": None
        }
    }
    
    print("Testing FeedbackRouterNode...")
    # For testing, we'll simulate a simple choice
    action = node.run(shared)
    print(f"Action: {action}")
    print(f"Feedback state: {shared['feedback_state']['feedback_type']}")
    print(f"Current stage: {shared['workflow_state']['current_stage']}")
