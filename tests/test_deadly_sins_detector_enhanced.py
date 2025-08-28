import pytest
import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.deadly_sins_detector import DeadlySinsDetector

@pytest.fixture
def detector():
    return DeadlySinsDetector()

def test_em_dash_detection(detector):
    """Test em dash pattern detection"""
    tests = [
        ("Text with an — em dash", 1),
        ("Text with – an en dash (shouldn't count)", 0),
        ("Text without any dashes", 0),
        ("Email signature: John Smith—CEO—Acme Corp", 2),  # Two em dashes
        ("Multiple — em — dashes — present", 3)
    ]
    for text, expected in tests:
        results = detector.detect_patterns(text)
        assert results['violations']['em_dash']['count'] == expected

def test_rhetorical_contrast_detection(detector):
    """Test rhetorical contrast pattern detection"""
    tests = [
        ("It's not just a tool; it's a revolution", 1),
        ("It is not only efficient; it is remarkably effective", 1),
        ("This isn't merely good; it is excellent", 1),
        ("Simple statement with no contrast", 0),
        ("Our slogan: It's not just software; it is your advantage", 1),
        ("This doesn't use not just but still has contrast", 0)
    ]
    for text, expected in tests:
        results = detector.detect_patterns(text)
        assert results['violations']['rhetorical_contrast']['count'] == expected

def test_antithesis_detection(detector):
    """Test antithesis pattern detection"""
    tests = [
        ("It's not a bug; it's a feature", 1),
        ("He isn't wrong; he is just misinformed", 1),
        ("This is not failure; it is delayed success", 1),
        ("Regular sentence with no contrasts", 0),
        ("Our philosophy: It is not busy work; it is strategic", 1),
        ("This doesn't have the required phrase", 0)
    ]
    for text, expected in tests:
        results = detector.detect_patterns(text)
        assert results['violations']['antithesis']['count'] == expected

def test_multi_pattern_detection(detector):
    """Test detection of multiple patterns in one sentence"""
    text = "It's not just a product—it's a revolution! And it's not a bug; it's a feature."
    results = detector.detect_patterns(text)
    
    assert results['violations']['em_dash']['count'] == 1
    assert results['violations']['rhetorical_contrast']['count'] == 1
    assert results['violations']['antithesis']['count'] == 1
    assert results['total_violations'] == 3

def test_no_patterns_detected(detector):
    """Test that no patterns are detected in clean text"""
    text = "This is a simple sentence with no AI fingerprint patterns. It follows natural language patterns."
    results = detector.detect_patterns(text)
    assert results['total_violations'] == 0
