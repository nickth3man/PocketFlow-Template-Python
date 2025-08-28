
import pytest
from utils.deadly_sins_detector import DeadlySinsDetector

@pytest.fixture
def detector():
    return DeadlySinsDetector()

def test_detect_em_dash(detector):
    text = "This is a sentence—with an em dash."
    results = detector.detect_patterns(text)
    assert results['violations']['em_dash']['count'] == 1
    assert results['total_violations'] == 1

def test_detect_rhetorical_contrast(detector):
    text = "It's not just a tool; it's a new way of thinking."
    results = detector.detect_patterns(text)
    assert results['violations']['rhetorical_contrast']['count'] >= 1

def test_detect_antithesis(detector):
    text = "It's not a bug; it's a feature."
    results = detector.detect_patterns(text)
    assert results['violations']['antithesis']['count'] >= 1

def test_detect_paradiastole(detector):
    text = "He is not lazy; he is strategically conserving energy."
    results = detector.detect_patterns(text)
    # This might be caught by antithesis as well, which is acceptable for now
    assert results['total_violations'] > 0

def test_detect_reframing_contrast(detector):
    text = "This isn't a problem; it's an opportunity for growth."
    results = detector.detect_patterns(text)
    assert results['total_violations'] > 0

def test_detect_chiasmus_like_contrast(detector):
    text = "It's not what the country can do for you, but what you can do for your country."
    results = detector.detect_patterns(text)
    assert results['total_violations'] > 0

def test_detect_tagline_framing(detector):
    text = "It's not just a car; it's a lifestyle."
    results = detector.detect_patterns(text)
    assert results['violations']['tagline_frame']['count'] >= 1

def test_no_violations(detector):
    text = "This is a normal sentence. It is straightforward and clear."
    results = detector.detect_patterns(text)
    assert results['total_violations'] == 0
