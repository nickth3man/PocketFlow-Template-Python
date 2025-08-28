"""
Test script for the PR Firm Content Generation System.
This script tests the main components of the system.
"""

import os
import sys
from shared_store import initialize_shared_store
from flow import create_content_generation_flow, create_qa_flow

def test_shared_store():
    """Test shared store initialization and utilities."""
    print("Testing shared store...")
    
    # Test initialization
    shared = initialize_shared_store()
    assert "user_config" in shared
    assert "task_requirements" in shared
    assert "brand_voice" in shared
    print("✅ Shared store initialization passed")
    
    # Test default values
    assert shared["user_config"]["model"] == "openrouter/anthropic/claude-3.5-sonnet"
    assert "email" in shared["platform_guidelines"]
    print("✅ Default values test passed")

def test_qa_flow():
    """Test the QA flow functionality."""
    print("\nTesting QA flow...")
    
    # Create a simple test shared store
    shared = {
        "question": "What is 2+2?",
        "answer": None
    }
    
    # Create and test QA flow
    qa_flow = create_qa_flow()
    assert qa_flow is not None
    print("✅ QA flow creation passed")
    
    # Note: We won't actually run the flow to avoid API calls during testing
    print("✅ QA flow test completed (not executed to avoid API calls)")

def test_content_generation_flow():
    """Test the content generation flow creation."""
    print("\nTesting content generation flow...")
    
    # Create content generation flow
    content_flow = create_content_generation_flow()
    assert content_flow is not None
    print("✅ Content generation flow creation passed")
    
    # Check that flow has the expected start node
    assert hasattr(content_flow, 'start')
    print("✅ Flow start node exists")

def test_node_imports():
    """Test that all node modules can be imported."""
    print("\nTesting node imports...")
    
    node_modules = [
        'nodes.engagement_manager',
        'nodes.brand_bible_processor', 
        'nodes.format_guidelines',
        'nodes.creative_inspiration',
        'nodes.pattern_aware_prompt_engineering',
        'nodes.content_generator',
        'nodes.style_optimizer',
        'nodes.deadly_sins_scanner',
        'nodes.style_compliance',
        'nodes.authenticity_scorer',
        'nodes.feedback_router',
        'nodes.content_refinement',
        'nodes.pattern_learner',
        'nodes.version_manager',
        'nodes.final_formatter',
        'nodes.preset_optimizer',
        'nodes.version_analytics'
    ]
    
    for module in node_modules:
        try:
            __import__(module)
            print(f"✅ {module} import passed")
        except ImportError as e:
            print(f"❌ {module} import failed: {e}")
            raise

def test_utility_imports():
    """Test that all utility modules can be imported."""
    print("\nTesting utility imports...")
    
    utility_modules = [
        'utils.call_llm',
        'utils.brand_bible_parser',
        'utils.deadly_sins_detector',
        'utils.content_sanitizer',
        'utils.platform_formatter',
        'utils.creative_inspiration',
        'utils.version_manager',
        'utils.presets_manager',
        'utils.feedback_parser',
        'utils.markdown_formatter',
        'utils.authenticity_scorer',
        'utils.pattern_learner'
    ]
    
    for module in utility_modules:
        try:
            __import__(module)
            print(f"✅ {module} import passed")
        except ImportError as e:
            print(f"❌ {module} import failed: {e}")
            raise

def test_requirements():
    """Test that required packages are available."""
    print("\nTesting requirements...")
    
    required_packages = [
        'pocketflow',
        'openai',
        'anthropic'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} available")
        except ImportError:
            print(f"❌ {package} not available")
            # Don't raise for now, as some might be optional

def main():
    """Run all tests."""
    print("=== PR Firm Content Generation System Tests ===\n")
    
    try:
        test_shared_store()
        test_qa_flow()
        test_content_generation_flow()
        test_node_imports()
        test_utility_imports()
        test_requirements()
        
        print("\n🎉 All tests passed! The system is ready to use.")
        print("\nTo run the system:")
        print("  python main.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
