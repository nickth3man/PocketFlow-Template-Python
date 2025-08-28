"""
Utility functions package for the PR Firm Content Generation System.
"""

# Core LLM utility
from .call_llm import call_llm

# Brand and voice utilities
from .brand_bible_parser import parse_brand_bible

# AI fingerprint detection and elimination
from .deadly_sins_detector import detect_deadly_sins, DeadlySinsDetector
from .content_sanitizer import sanitize_content, ContentSanitizer

# Content formatting and platform utilities
from .platform_formatter import get_platform_guidelines, get_multiple_platform_guidelines
from .creative_inspiration import generate_creative_inspiration, get_platform_style_hints

# Content management utilities
from .version_manager import create_version, get_version_history, VersionManager
from .presets_manager import save_preset, load_preset, list_presets, PresetsManager
from .feedback_parser import parse_user_feedback, categorize_feedback
from .markdown_formatter import format_content_as_markdown, generate_copy_buttons_html

# Quality and learning utilities
from .authenticity_scorer import score_authenticity
from .pattern_learner import analyze_pattern_learning, get_prompt_improvements, PatternLearner

__all__ = [
    # Core LLM utility
    'call_llm',
    
    # Brand and voice utilities
    'parse_brand_bible',
    
    # AI fingerprint detection and elimination
    'detect_deadly_sins',
    'DeadlySinsDetector',
    'sanitize_content',
    'ContentSanitizer',
    
    # Content formatting and platform utilities
    'get_platform_guidelines',
    'get_multiple_platform_guidelines',
    'generate_creative_inspiration',
    'get_platform_style_hints',
    
    # Content management utilities
    'create_version',
    'get_version_history',
    'VersionManager',
    'save_preset',
    'load_preset',
    'list_presets',
    'PresetsManager',
    'parse_user_feedback',
    'categorize_feedback',
    'format_content_as_markdown',
    'generate_copy_buttons_html',
    
    # Quality and learning utilities
    'score_authenticity',
    'analyze_pattern_learning',
    'get_prompt_improvements',
    'PatternLearner',
]
