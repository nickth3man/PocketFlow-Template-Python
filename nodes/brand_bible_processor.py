from pocketflow import Node
from utils.brand_bible_parser import parse_brand_bible

class BrandBibleProcessorNode(Node):
    """
    Convert descriptive brand text into structured voice parameters.
    Second node in the workflow that processes brand configuration.
    """
    
    def prep(self, shared):
        """
        Read brand bible text and individual/brand setting from shared store.
        """
        return {
            "brand_bible_text": shared["task_requirements"]["brand_bible_text"],
            "individual_or_brand": shared["user_config"]["individual_or_brand"]
        }
    
    def exec(self, prep_res):
        """
        Parse descriptive brand text into structured voice parameters.
        """
        brand_bible_text = prep_res["brand_bible_text"]
        individual_or_brand = prep_res["individual_or_brand"]
        
        # Parse the brand bible text
        structured_voice, tone_guidelines = parse_brand_bible(brand_bible_text, individual_or_brand)
        
        # Define forbidden patterns (the 7 deadly sins of AI-generated content)
        forbidden_patterns = {
            "em_dash": {
                "pattern": "—", 
                "severity": "critical",
                "description": "Em dash usage creates robotic pauses"
            },
            "rhetorical_contrast": {
                "pattern": r"(?:It's not just|It's not merely|It's not only).+?[,;]\s*(?:it's|it is|but).+?",
                "severity": "critical",
                "description": "Rhetorical contrast creates artificial drama"
            },
            "antithesis": {
                "pattern": r"(?:It's not|It is not|It isn't).+?[,;]\s*(?:it's|it is|but).+?",
                "severity": "critical",
                "description": "Antithesis creates false dichotomies"
            },
            "paradiastole": {
                "pattern": r"(?:It's not|It is not|It isn't)\s+(?:laziness|failure|mistake|problem).+?[,;]\s*(?:it's|it is|but).+?",
                "severity": "critical",
                "description": "Paradiastole reclassifies concepts disingenuously"
            },
            "reframing_contrast": {
                "pattern": r"(?:It's not just|It's not merely|It's not only)\s+(?:a cost|an expense|a problem).+?[,;]\s*(?:it's|it is|but).+?",
                "severity": "critical",
                "description": "Reframing contrast disconnects from reality"
            },
            "chiasmus": {
                "pattern": r"(?:It's not what).+?(?:does to you|makes you|gives you).+?[,;]\s*(?:it's|it is|but).+?(?:you do with|make of|get from).+?",
                "severity": "critical",
                "description": "Chiasmus creates contrived parallelism"
            },
            "tagline_frame": {
                "pattern": r"(?:It's not just|It's not merely|It's not only)\s+(?:a car|a product|a service|an app|a tool).+?[,;]\s*(?:it's|it is|but).+?",
                "severity": "critical",
                "description": "Tagline framing feels like corporate jargon"
            }
        }
        
        return {
            "parsed_attributes": structured_voice,
            "tone_guidelines": tone_guidelines,
            "forbidden_patterns": forbidden_patterns
        }
    
    def post(self, shared, prep_res, exec_res):
        """
        Write structured brand voice with all 7 deadly sins patterns to shared store.
        """
        # Update brand voice in shared store
        shared["brand_voice"] = {
            "parsed_attributes": exec_res["parsed_attributes"],
            "tone_guidelines": exec_res["tone_guidelines"],
            "forbidden_patterns": exec_res["forbidden_patterns"],
            "style_preferences": exec_res["parsed_attributes"].get("style_preferences", {
                "sentence_variety": "medium",
                "transition_style": "natural",
                "ending_style": "inviting"
            })
        }
        
        # Mark stage as completed
        shared["workflow_state"]["completed_stages"].append("brand_bible_processing")
        shared["workflow_state"]["current_stage"] = "format_guidelines"
        
        print(f"\nBrand voice processed successfully!")
        print(f"Personality traits: {', '.join(exec_res['parsed_attributes']['personality_traits'])}")
        print(f"Tone: {exec_res['parsed_attributes']['tone']}")
        print(f"Values: {', '.join(exec_res['parsed_attributes']['values'])}")
        
        return "default"  # Go to next node

if __name__ == "__main__":
    # Test the node
    node = BrandBibleProcessorNode()
    
    # Create test shared store
    shared = {
        "task_requirements": {
            "brand_bible_text": "We are an innovative marketing agency that values education and transparency. Our brand voice is confident and professional, focusing on AI empowerment and skill development.",
            "topic": "AI in marketing",
            "platforms": ["linkedin", "twitter"]
        },
        "user_config": {
            "individual_or_brand": "brand",
            "name": "Test User",
            "brand_name": "TestBrand"
        },
        "workflow_state": {
            "current_stage": "brand_bible_processing",
            "completed_stages": ["engagement"],
            "error_state": None
        }
    }
    
    print("Testing BrandBibleProcessorNode...")
    action = node.run(shared)
    print(f"Action: {action}")
    print(f"Brand voice keys: {list(shared['brand_voice'].keys())}")
    print(f"Forbidden patterns: {list(shared['brand_voice']['forbidden_patterns'].keys())}")
