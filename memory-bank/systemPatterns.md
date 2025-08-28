# System Patterns: PR Firm Content Generation System

## Core Architecture

### PocketFlow Framework
- Node-based architecture with 17 specialized nodes
- Shared store for state management
- Batch processing for parallel platform generation
- Fault-tolerant retry mechanisms
- Pattern learning feedback loops

### Technical Components

#### Content Generation Pipeline
1. **Engagement Manager**: Handles user inputs and preset management
2. **Brand Bible Processor**: Converts descriptive brand text into structured parameters
3. **Format Guidelines Batch**: Generates platform-specific formatting rules
4. **Creative Inspiration Node**: Uses LLM prompts to generate high-engagement examples
5. **Pattern-Aware Prompt Engineer**: Enhances prompts with positive writing alternatives
6. **Content Generator**: Creates initial platform-optimized drafts
7. **Style Optimizer**: Refines content while maintaining brand voice
8. **Deadly Sins Scanner**: Detects specific AI patterns that must be eliminated
9. **Style Compliance Check**: Validates final content (max 5 revision cycles)
10. **Authenticity Scorer**: Evaluates human-like qualities beyond pattern avoidance
11. **Feedback Router**: Handles user feedback for iterative refinement
12. **Content Refinement**: Applies user-requested changes
13. **Pattern Learner**: Improves future prompt engineering
14. **Version Manager**: Tracks content versions
15. **Final Formatter**: Outputs clean markdown with copy functionality
16. **Preset Optimizer**: Learns from user preferences
17. **Version Analytics**: Provides performance insights

#### Shared Store Structure
```python
shared = {
    "user_config": {...},
    "task_requirements": {...},
    "brand_voice": {...},
    "platform_guidelines": {...},
    "creative_inspiration": {...},
    "content_pieces": {...},
    "quality_control": {...},
    "version_history": [...],
    "feedback_state": {...},
    "workflow_state": {...},
    "progress_metrics": {...},  # Tracks workflow progress and performance metrics
    "pattern_learning": {...},
    "authenticity_results": {...},
    "roi_analysis": {...},
    "final_output": {...},
    "analytics_report": {...},
    "optimized_preset": {...}
}
```

## Key Technical Patterns

### Deadly Sins Detection System
- **Context-Aware Detection**: Brand-voice-specific pattern libraries with adaptive recognition
- **Multi-Order Validation**: Three-stage scanning (structural → semantic → stylistic)
- **Real-Time Pattern Learning**: In-process detection provides immediate feedback
- **Enhanced Pattern Libraries**: All 7 deadly sins with adaptive recognition
- **Comprehensive Test Coverage**: Enhanced test suite with 80% pass rate achievement
- **Pattern Counting**: Accurate counting of multiple pattern occurrences in single text
- **Expanded Phrase Matching**: Enhanced antithesis detection with broader phrase recognition
- **Six Thinking Hats Methodology**: Applied for autonomous development and debugging

#### Core Pattern Detection Components
1. **Em Dash Detection**: 
   - Implemented counting functionality for multiple occurrences
   - Differentiates em dashes (—) from en dashes (–)
   - Accuracy: 100% (all test cases passing)

2. **Antithesis Detection**:
   - Enhanced pattern matching with expanded phrase recognition
   - Supports multiple contraction forms and pronouns
   - Accuracy: 100% (all test cases passing)

3. **Rhetorical Contrast Detection**:
   - Currently undergoing refinement using systematic debugging approach
   - Issue: Phrase matching for "not just"/"not only" with "it's"/"it is"
   - Next Step: Apply lambda function debugging and pattern optimization
   - Accuracy: In progress (target: 100%)

4. **Multi-Pattern Detection**:
   - Successfully identifies combined patterns in single text
   - Comprehensive violation counting across all pattern types
   - Accuracy: 100% (all test cases passing)

### Content Sanitization
- **Deterministic Pattern Elimination**: Rule-based transformation engine
- **Cross-Platform Consistency**: Unified transformation rules
- **Brand-Voice Preservation**: Advanced context-awareness
- **Transformation Tracking**: Detailed logging of changes

### Authenticity Evaluation
- **Enhanced Authenticity Metrics**: Comprehensive scoring beyond pattern avoidance
- **Quantifiable Pattern Elimination**: Measures reduction rates and effectiveness
- **ROI Justification**: Provides business-case metrics
- **Multi-Dimensional Analysis**: Evaluates content across 7+ dimensions
- **Performance Benchmarking**: Tracks improvement over time

## Implementation Patterns

### Batch Processing
- Parallel content generation for multiple platforms
- Optimized for performance with progress indicators
- Asynchronous processing with batch optimization

### Version Control
- Comprehensive version tracking with metadata
- Rollback capability for content versions
- Detailed change history and audit trails

### Preset Management
- Saves and loads brand configurations
- Learns from user preferences
- Optimizes preset templates for future use

## Technical Constraints

1. No external service integrations
2. Only connects to LLMs through OpenRouter utility functions
3. Must detect and remove all "7 Deadly Sins" patterns with zero tolerance
4. Maximum 5 revision cycles for style compliance before manual review required
5. Output must be formatted markdown with copy-to-clipboard functionality

## Performance Considerations

- Optimized batch processing for faster iteration cycles
- Asynchronous pattern detection to prevent performance bottlenecks
- Real-time pattern learning to prevent pattern generation at source
- Deterministic pattern elimination to ensure consistent results

This system architecture provides a robust foundation for creating authentic, platform-optimized content while systematically eliminating AI fingerprints that reduce engagement and authenticity.
