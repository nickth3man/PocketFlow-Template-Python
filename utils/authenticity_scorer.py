from typing import Dict, List
import re

def score_authenticity(text: str, brand_voice: Dict = None, pattern_history: Dict = None) -> Dict:
    """
    Advanced authenticity evaluation with quantifiable metrics and ROI analysis.
    
    Args:
        text (str): Text to evaluate
        brand_voice (Dict): Brand voice parameters
        pattern_history (Dict): Historical pattern data
        
    Returns:
        Dict: Authenticity score and detailed feedback
    """
    metrics = {}
    
    # 1. Pattern Elimination Score (0-100)
    from utils.deadly_sins_detector import DeadlySinsDetector
    detector = DeadlySinsDetector()
    violations = detector.detect_patterns(text)
    
    pattern_elimination_score = max(0, 100 - (violations["total_violations"] * 10))
    metrics["pattern_elimination"] = {
        "score": pattern_elimination_score,
        "violations_found": violations["total_violations"],
        "severity_score": violations["severity_score"]
    }
    
    # 2. Natural Flow Score (0-100)
    flow_score = _calculate_flow_score(text)
    metrics["natural_flow"] = {
        "score": flow_score,
        "sentence_variety": _analyze_sentence_variety(text),
        "transition_quality": _analyze_transitions(text)
    }
    
    # 3. Engagement Quality Score (0-100)
    engagement_score = _calculate_engagement_score(text, brand_voice)
    metrics["engagement_quality"] = {
        "score": engagement_score,
        "questions_asked": len(re.findall(r'[?]', text)),
        "calls_to_action": _count_ctas(text),
        "personal_pronouns": len(re.findall(r'\b(I|we|us|our)\b', text, re.IGNORECASE))
    }
    
    # 4. Brand Alignment Score (0-100)
    brand_score = _calculate_brand_alignment(text, brand_voice) if brand_voice else 75
    metrics["brand_alignment"] = {
        "score": brand_score,
        "voice_consistency": _check_voice_consistency(text, brand_voice) if brand_voice else 0.75
    }
    
    # 5. Human-like Quality Score (0-100)
    human_score = _calculate_human_quality(text)
    metrics["human_quality"] = {
        "score": human_score,
        "contractions_used": len(re.findall(r"\b\w+'\w+\b", text)),
        "conversational_tone": _check_conversational_tone(text)
    }
    
    # Weighted overall score
    weights = {
        "pattern_elimination": 0.3,
        "natural_flow": 0.2,
        "engagement_quality": 0.2,
        "brand_alignment": 0.15,
        "human_quality": 0.15
    }
    
    overall_score = (
        pattern_elimination_score * weights["pattern_elimination"] +
        flow_score * weights["natural_flow"] +
        engagement_score * weights["engagement_quality"] +
        brand_score * weights["brand_alignment"] +
        human_score * weights["human_quality"]
    )
    
    # ROI Analysis
    roi_analysis = _calculate_roi_benefits(overall_score, pattern_history)
    
    return {
        "authenticity_score": round(overall_score, 2),
        "metrics": metrics,
        "weights": weights,
        "feedback": _generate_feedback(metrics),
        "roi_analysis": roi_analysis,
        "recommendations": _generate_recommendations(metrics)
    }

def _calculate_flow_score(text: str) -> float:
    """Calculate natural flow score."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return 50.0
    
    # Check sentence length variety
    lengths = [len(s.split()) for s in sentences]
    avg_length = sum(lengths) / len(lengths)
    length_variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
    
    # Score based on variety (not too uniform)
    variety_score = min(100, length_variance * 2)
    
    # Check for natural transitions
    transition_words = ["however", "therefore", "meanwhile", "furthermore", "indeed", "nevertheless"]
    transition_count = sum(1 for word in transition_words if word in text.lower())
    transition_score = min(100, transition_count * 10)
    
    return (variety_score + transition_score) / 2

def _analyze_sentence_variety(text: str) -> float:
    """Analyze sentence structure variety."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return 0.5
    
    lengths = [len(s.split()) for s in sentences]
    if len(lengths) < 2:
        return 0.5
    
    # Calculate coefficient of variation
    mean = sum(lengths) / len(lengths)
    variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
    std_dev = variance ** 0.5
    
    # Normalize to 0-1 scale
    return min(1.0, std_dev / mean if mean > 0 else 0)

def _analyze_transitions(text: str) -> float:
    """Analyze transition word usage."""
    transition_words = [
        "however", "therefore", "meanwhile", "furthermore", "indeed", "nevertheless",
        "consequently", "moreover", "otherwise", "similarly", "likewise", "instead"
    ]
    
    text_lower = text.lower()
    transition_count = sum(1 for word in transition_words if f" {word} " in f" {text_lower} ")
    
    # Normalize by text length (per 100 words)
    word_count = len(text.split())
    if word_count == 0:
        return 0.0
    
    return min(1.0, transition_count / (word_count / 100))

def _calculate_engagement_score(text: str, brand_voice: Dict = None) -> float:
    """Calculate engagement quality score."""
    score = 50.0  # Base score
    
    # Questions increase engagement
    question_count = len(re.findall(r'[?]', text))
    score += question_count * 5
    
    # Calls to action
    cta_count = _count_ctas(text)
    score += cta_count * 3
    
    # Personal pronouns (makes it more human)
    personal_pronouns = len(re.findall(r'\b(I|we|us|our|you)\b', text, re.IGNORECASE))
    score += min(personal_pronouns * 2, 20)
    
    # Brand-specific engagement words
    if brand_voice and "values" in brand_voice:
        brand_values = " ".join(brand_voice["values"]).lower()
        value_mentions = len(re.findall(rf'\b({brand_values})\b', text.lower()))
        score += value_mentions * 4
    
    return min(100.0, score)

def _count_ctas(text: str) -> int:
    """Count calls to action."""
    cta_patterns = [
        r"\b(learn more|discover|explore|try|click|visit|read more|sign up|subscribe)\b",
        r"\b(let's|we should|you can|why not)\b"
    ]
    
    count = 0
    for pattern in cta_patterns:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    
    return count

def _calculate_brand_alignment(text: str, brand_voice: Dict) -> float:
    """Calculate brand voice alignment score."""
    if not brand_voice:
        return 75.0
    
    score = 50.0  # Base score
    
    # Check for brand traits
    traits = brand_voice.get("personality_traits", [])
    trait_text = " ".join(traits).lower()
    
    for trait in traits:
        if trait.lower() in text.lower():
            score += 5
    
    # Check tone alignment
    brand_tone = brand_voice.get("tone", "professional")
    if brand_tone in text.lower():
        score += 10
    
    # Check values alignment
    values = brand_voice.get("values", [])
    for value in values:
        if value.lower() in text.lower():
            score += 3
    
    return min(100.0, score)

def _check_voice_consistency(text: str, brand_voice: Dict) -> float:
    """Check consistency with brand voice."""
    if not brand_voice:
        return 0.75
    
    # This would be more sophisticated in a full implementation
    # For now, check basic alignment
    traits = brand_voice.get("personality_traits", [])
    tone = brand_voice.get("tone", "professional")
    
    consistency_indicators = len(traits) + (1 if tone else 0)
    if consistency_indicators == 0:
        return 0.75
    
    matches = 0
    text_lower = text.lower()
    
    for trait in traits:
        if trait.lower() in text_lower:
            matches += 1
    
    if tone and tone.lower() in text_lower:
        matches += 1
    
    return matches / consistency_indicators if consistency_indicators > 0 else 0.75

def _calculate_human_quality(text: str) -> float:
    """Calculate human-like quality score."""
    score = 50.0  # Base score
    
    # Contractions make it more human
    contractions = len(re.findall(r"\b\w+'\w+\b", text))
    score += min(contractions * 3, 25)
    
    # Conversational tone
    conversational_score = _check_conversational_tone(text)
    score += conversational_score * 25
    
    # Exclamation marks (but not too many)
    exclamations = text.count('!')
    score += min(exclamations * 2, 10)
    
    return min(100.0, score)

def _check_conversational_tone(text: str) -> float:
    """Check for conversational tone indicators."""
    conversational_indicators = [
        "hey", "hi", "hello", "thanks", "thank you", "please", "sorry",
        "actually", "basically", "literally", "honestly", "frankly"
    ]
    
    text_lower = text.lower()
    indicator_count = sum(1 for indicator in conversational_indicators if indicator in text_lower)
    
    # Normalize to 0-1 scale
    return min(1.0, indicator_count / 5)

def _calculate_roi_benefits(overall_score: float, pattern_history: Dict = None) -> Dict:
    """Calculate ROI benefits of authenticity."""
    # Time savings estimation
    time_saved_per_piece = (overall_score / 100) * 15  # minutes
    
    # Quality improvement
    quality_improvement = (overall_score - 50) / 50 if overall_score > 50 else 0
    
    # Pattern reduction analysis
    pattern_reduction = 0
    if pattern_history and "total_violations" in pattern_history:
        if pattern_history["total_violations"] > 0:
            pattern_reduction = (pattern_history["total_violations"] - 
                               len(re.findall(r'[—–]|(?:It\'s not)', "sample text"))) / pattern_history["total_violations"]
    
    return {
        "time_saved_per_piece_minutes": round(time_saved_per_piece, 1),
        "quality_improvement_percent": round(quality_improvement * 100, 1),
        "pattern_reduction_rate": round(max(0, pattern_reduction) * 100, 1),
        "estimated_roi": f"{round(overall_score * 2, 1)}%"  # Simplified ROI calculation
    }

def _generate_feedback(metrics: Dict) -> List[str]:
    """Generate feedback based on metrics."""
    feedback = []
    
    if metrics["pattern_elimination"]["score"] < 70:
        feedback.append("Consider further elimination of AI fingerprint patterns for better authenticity.")
    
    if metrics["natural_flow"]["score"] < 60:
        feedback.append("Improve sentence variety and natural transitions for better flow.")
    
    if metrics["engagement_quality"]["score"] < 60:
        feedback.append("Add more questions and calls-to-action to increase engagement.")
    
    if metrics["human_quality"]["score"] < 60:
        feedback.append("Use more contractions and conversational language to sound more human.")
    
    if not feedback:
        feedback.append("Excellent authenticity score! The content sounds natural and engaging.")
    
    return feedback

def _generate_recommendations(metrics: Dict) -> List[str]:
    """Generate specific recommendations."""
    recommendations = []
    
    # Pattern elimination recommendations
    if metrics["pattern_elimination"]["violations_found"] > 0:
        recommendations.append(f"Eliminate {metrics['pattern_elimination']['violations_found']} AI fingerprint patterns")
    
    # Flow recommendations
    if metrics["natural_flow"]["sentence_variety"] < 0.5:
        recommendations.append("Vary sentence lengths for better rhythm")
    
    # Engagement recommendations
    if metrics["engagement_quality"]["questions_asked"] == 0:
        recommendations.append("Add questions to encourage reader interaction")
    
    # Human quality recommendations
    if metrics["human_quality"]["contractions_used"] < 3:
        recommendations.append("Use more contractions to sound more conversational")
    
    return recommendations

if __name__ == "__main__":
    # Test the authenticity scorer
    test_text = """The future of AI in marketing is here! We're excited to share how this technology is transforming the way we connect with customers. Our innovative approach combines cutting-edge AI with human creativity to deliver exceptional results.
    
    Why is this important? Because traditional marketing methods are no longer enough. We need smarter, more personalized approaches that speak directly to each customer's unique needs.
    
    Here are three key benefits you'll experience:
    
    1. Personalization at scale - reaching each customer with relevant messages
    2. Real-time optimization - constantly improving based on performance data  
    3. Predictive analytics - anticipating customer needs before they arise
    
    We believe the future is now, and we're here to help you embrace it. Ready to transform your marketing strategy? Let's discuss how AI can work for your business!"""
    
    test_brand_voice = {
        "personality_traits": ["innovative", "helpful", "professional"],
        "tone": "thought_leadership",
        "voice": "confident",
        "values": ["innovation", "customer_success"],
        "themes": ["AI", "marketing", "transformation"]
    }
    
    print("Testing authenticity scorer...")
    print(f"Text length: {len(test_text.split())} words")
    
    # Score the content
    score_result = score_authenticity(test_text, test_brand_voice)
    
    print(f"\nOverall Authenticity Score: {score_result['authenticity_score']}/100")
    print(f"Weighted Metrics:")
    for metric, data in score_result['metrics'].items():
        print(f"  {metric}: {data['score']:.1f}/100")
    
    print(f"\nFeedback:")
    for feedback in score_result['feedback']:
        print(f"  - {feedback}")
    
    print(f"\nRecommendations:")
    for rec in score_result['recommendations']:
        print(f"  - {rec}")
    
    print(f"\nROI Analysis:")
    roi = score_result['roi_analysis']
    print(f"  Time saved per piece: {roi['time_saved_per_piece_minutes']} minutes")
    print(f"  Quality improvement: {roi['quality_improvement_percent']}%")
    print(f"  Estimated ROI: {roi['estimated_roi']}")
