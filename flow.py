from pocketflow import Flow
from nodes.engagement_manager import EngagementManagerNode
from nodes.brand_bible_processor import BrandBibleProcessorNode
from nodes.format_guidelines import FormatGuidelinesBatch
from nodes.creative_inspiration import CreativeInspirationNode
from nodes.pattern_aware_prompt_engineering import PatternAwarePromptEngineerNode
from nodes.content_generator import ContentGeneratorNode
from nodes.style_optimizer import StyleOptimizerNode
from nodes.deadly_sins_scanner import DeadlySinsScannerNode
from nodes.style_compliance import StyleComplianceNode
from nodes.authenticity_scorer import AuthenticityScorerNode
from nodes.feedback_router import FeedbackRouterNode
from nodes.content_refinement import ContentRefinementNode
from nodes.pattern_learner import PatternLearnerNode
from nodes.version_manager import VersionManagerNode
from nodes.final_formatter import FinalFormatterNode
from nodes.preset_optimizer import PresetOptimizerNode
from nodes.version_analytics import VersionAnalyticsNode
from nodes import GetQuestionNode, AnswerNode

def create_content_generation_flow():
    """Create and return the complete content generation flow."""
    # Create all nodes
    engagement_manager = EngagementManagerNode()
    brand_bible_processor = BrandBibleProcessorNode()
    format_guidelines = FormatGuidelinesBatch()
    creative_inspiration = CreativeInspirationNode()
    pattern_aware_prompt_engineer = PatternAwarePromptEngineerNode()
    content_generator = ContentGeneratorNode()
    style_optimizer = StyleOptimizerNode()
    deadly_sins_scanner = DeadlySinsScannerNode()
    style_compliance = StyleComplianceNode()
    authenticity_scorer = AuthenticityScorerNode()
    feedback_router = FeedbackRouterNode()
    content_refinement = ContentRefinementNode()
    pattern_learner = PatternLearnerNode()
    version_manager = VersionManagerNode()
    final_formatter = FinalFormatterNode()
    preset_optimizer = PresetOptimizerNode()
    version_analytics = VersionAnalyticsNode()
    
    # Connect nodes in the main flow
    engagement_manager >> brand_bible_processor
    brand_bible_processor >> format_guidelines
    format_guidelines >> creative_inspiration
    creative_inspiration >> pattern_aware_prompt_engineer
    pattern_aware_prompt_engineer >> content_generator
    content_generator >> style_optimizer
    style_optimizer >> deadly_sins_scanner
    deadly_sins_scanner >> style_compliance
    
    # Compliance branching
    style_compliance - "approved" >> authenticity_scorer
    style_compliance - "revise" >> content_refinement
    style_compliance - "manual_review" >> final_formatter
    
    # Refinement loop
    content_refinement >> deadly_sins_scanner  # Go back to scanning
    
    # Post-approval flow
    authenticity_scorer >> feedback_router
    
    # Feedback routing
    feedback_router - "refine" >> content_refinement
    feedback_router - "edit" >> content_refinement
    feedback_router - "regenerate" >> content_generator
    feedback_router - "save" >> version_manager
    feedback_router - "view" >> authenticity_scorer
    feedback_router - "exit" >> version_manager
    
    # Version management to final stages
    version_manager >> pattern_learner
    pattern_learner >> final_formatter
    final_formatter >> preset_optimizer
    preset_optimizer >> version_analytics
    
    # Create flow starting with engagement manager
    return Flow(start=engagement_manager)

def create_qa_flow():
    """Create and return a question-answering flow."""
    # Create nodes
    get_question_node = GetQuestionNode()
    answer_node = AnswerNode()
    
    # Connect nodes in sequence
    get_question_node >> answer_node
    
    # Create flow starting with input node
    return Flow(start=get_question_node)

# Create both flows
content_generation_flow = create_content_generation_flow()
qa_flow = create_qa_flow()
