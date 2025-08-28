
import pytest
from unittest.mock import patch, MagicMock
from nodes.engagement_manager import EngagementManagerNode

@pytest.fixture
def mock_input():
    """Fixture to mock user input."""
    inputs = [
        "brand",  # individual_or_brand
        "Test User",  # name
        "Test Brand",  # brand_name
        "1",  # model_choice
        "0.8",  # temperature
        "1",  # preset_choice (create new)
        "Innovative and user-friendly brand.",  # brand_bible_text
        "1,2,3",  # platform_input
        "New features in our product"  # topic
    ]
    return iter(inputs)

@patch('utils.presets_manager.list_presets', MagicMock(return_value={}))
@patch('utils.presets_manager.load_preset', MagicMock(return_value={}))
def test_engagement_manager_node(mock_input):
    """Test the EngagementManagerNode with mocked input."""
    node = EngagementManagerNode()
    shared = {}

    with patch('builtins.input', lambda _: next(mock_input)):
        action = node.run(shared)

    assert action == "default"
    assert "user_config" in shared
    assert shared["user_config"]["individual_or_brand"] == "brand"
    assert shared["user_config"]["name"] == "Test User"
    assert shared["user_config"]["brand_name"] == "Test Brand"
    assert shared["user_config"]["model"] == "openrouter/anthropic/claude-3.5-sonnet"
    assert shared["user_config"]["temperature"] == 0.8
    assert "task_requirements" in shared
    assert shared["task_requirements"]["topic"] == "New features in our product"
    assert shared["task_requirements"]["platforms"] == ["email", "linkedin", "instagram"]
    assert "brand_voice" in shared
    assert "parsed_attributes" in shared["brand_voice"]


