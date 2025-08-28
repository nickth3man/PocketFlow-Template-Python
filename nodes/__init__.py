"""
nodes package initialization.
"""

# Import nodes from the parent nodes.py module first
try:
    from nodes import GetQuestionNode, AnswerNode
except ImportError:
    # If that fails, import from parent directory
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from nodes import GetQuestionNode, AnswerNode
    except ImportError:
        # Define dummy nodes if import fails
        GetQuestionNode = None
        AnswerNode = None

# Import all nodes from this package
from .engagement_manager import EngagementManagerNode
from .brand_bible_processor import BrandBibleProcessorNode
from .format_guidelines import FormatGuidelinesBatch
from .creative_inspiration import CreativeInspirationNode
from .pattern_aware_prompt_engineering import PatternAwarePromptEngineerNode
from .content_generator import ContentGeneratorNode
from .style_optimizer import StyleOptimizerNode
from .deadly_sins_scanner import DeadlySinsScannerNode
from .style_compliance import StyleComplianceNode
from .authenticity_scorer import AuthenticityScorerNode
from .feedback_router import FeedbackRouterNode
from .content_refinement import ContentRefinementNode
from .pattern_learner import PatternLearnerNode
from .version_manager import VersionManagerNode
from .final_formatter import FinalFormatterNode
from .preset_optimizer import PresetOptimizerNode
from .version_analytics import VersionAnalyticsNode

__all__ = [
    'GetQuestionNode',
    'AnswerNode',
    'EngagementManagerNode',
    'BrandBibleProcessorNode',
    'FormatGuidelinesBatch',
    'CreativeInspirationNode',
    'PatternAwarePromptEngineerNode',
    'ContentGeneratorNode',
    'StyleOptimizerNode',
    'DeadlySinsScannerNode',
    'StyleComplianceNode',
    'AuthenticityScorerNode',
    'FeedbackRouterNode',
    'ContentRefinementNode',
    'PatternLearnerNode',
    'VersionManagerNode',
    'FinalFormatterNode',
    'PresetOptimizerNode',
    'VersionAnalyticsNode'
]
