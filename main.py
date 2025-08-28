from flow import create_content_generation_flow, create_qa_flow
from shared_store import initialize_shared_store

def main():
    """Main function to run the content generation system."""
    print("=== PR Firm Content Generation System ===")
    print("Choose mode:")
    print("1. Content Generation (default)")
    print("2. QA Mode")
    
    choice = input("Select mode (1 or 2): ").strip()
    
    if choice == "2":
        # QA mode
        shared = {
            "question": input("Enter your question: "),
            "answer": None
        }
        qa_flow = create_qa_flow()
        qa_flow.run(shared)
        print("Question:", shared["question"])
        print("Answer:", shared["answer"])
    else:
        # Content generation mode
        shared = initialize_shared_store()
        
        # Set some default values for testing
        shared["user_config"]["individual_or_brand"] = "brand"
        shared["user_config"]["name"] = "TestBrand"
        shared["task_requirements"]["platforms"] = ["linkedin", "twitter"]
        
        content_flow = create_content_generation_flow()
        content_flow.run(shared)
        
        # Show final results
        if "final_output" in shared and shared["final_output"].get("filename"):
            print(f"\n✅ Content generation completed!")
            print(f"Output file: {shared['final_output']['filename']}")
            print(f"Platforms generated: {', '.join(shared['final_output']['platforms'])}")
        else:
            print(f"\n⚠️  Content generation completed with issues.")
        
        if "analytics_report" in shared and "summary_stats" in shared["analytics_report"]:
            stats = shared['analytics_report']['summary_stats']
            print(f"\nPerformance Summary:")
            print(f"  - Authenticity: {stats.get('avg_authenticity', 0)}/100")
            print(f"  - Time saved: {stats.get('time_saved_minutes', 0)} minutes")
            print(f"  - Pattern reduction: {stats.get('pattern_reduction_rate', 0)}%")

if __name__ == "__main__":
    main()
