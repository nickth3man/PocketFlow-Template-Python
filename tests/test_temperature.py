import pytest
from unittest.mock import patch
from nodes.engagement_manager import EngagementManagerNode

@pytest.mark.parametrize("temp_input, expected_temp", [
    ("0.8", 0.8),
    ("1.2", 1.0),
    ("-0.5", 0.0),
    ("abc", 0.7),
    ("", 0.7),
])
def test_temperature_logic(temp_input, expected_temp):
    """Test the temperature logic in isolation."""
    node = EngagementManagerNode()
    shared = {}

    inputs = [
        "brand",
        "Test User",
        "Test Brand",
        "1",
        temp_input,
        "1",
        "Innovative and user-friendly brand.",
        "1,2,3",
        "New features in our product"
    ]

    with patch('nodes.engagement_manager.list_presets', return_value={}), \
         patch('nodes.engagement_manager.load_preset', return_value={}), \
         patch('nodes.engagement_manager.parse_brand_bible', return_value=({}, {})), \
         patch('builtins.input', lambda _: next(iter(inputs)))]:
        action = node.run(shared)

    assert shared["user_config"]["temperature"] == expected_temp
