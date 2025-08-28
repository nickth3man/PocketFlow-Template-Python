# Technical Context: PR Firm Content Generation System

## Technology Stack

### Core Framework
- **PocketFlow**: Lightweight LLM framework for agentic workflows
- **Python 3.8+**: Primary programming language
- **OpenRouter**: Multi-model LLM access utility
- **Anthropic API**: Primary LLM provider (Claude models)

### Key Dependencies
- pocketflow>=0.0.1
- openai>=1.0.0
- anthropic>=0.30.0

## Development Environment

### System Requirements
- Python 3.8+ environment
- OpenAI API key or compatible LLM service
- Anthropic API key (optional)

### Installation
```bash
pip install -r requirements.txt
```

### Usage
```bash
python main.py
```

Choose between:
1. **Content Generation Mode**: Full PR content workflow with brand voice and platform optimization
2. **QA Mode**: Simple question-answering functionality

## Technical Architecture

### Core Components
1. **Flow Management**: Defines the 17-node workflow pipeline
2. **Node Implementation**: Specialized processing nodes for each stage
3. **Shared Store**: Comprehensive state management system
4. **Utility Functions**: Modular helper functions for specific tasks
5. **Version Control**: Content version tracking system

### Key Features
- **Multi-Platform Content Generation**: Creates optimized content for email, LinkedIn, Instagram, Twitter, Reddit, and blog posts
- **AI Fingerprint Elimination**: Detects and removes all 7 "Deadly Sins" of AI-generated content
- **Brand Voice Consistency**: Maintains consistent brand personality across all platforms
- **Authenticity Scoring**: Measures content authenticity with comprehensive metrics
- **Iterative Refinement**: Interactive feedback loop for content improvement
- **Version Control**: Tracks content versions with rollback capability
- **Performance Analytics**: Provides insights into pattern reduction and efficiency gains
- **Preset Learning**: Automatically optimizes configurations based on usage patterns
- **Enhanced Testing Framework**: Comprehensive test suite with 80% pass rate achievement
- **Autonomous Development**: Six Thinking Hats methodology for systematic debugging and enhancement

### Testing Framework
- **Pattern Detection Testing**: `tests/test_deadly_sins_detector_enhanced.py`
  - 5 comprehensive test cases covering all pattern types
  - Multi-pattern detection validation
  - Negative testing to prevent false positives
  - Current achievement: 80% pass rate (4/5 tests passing)
- **Test Coverage**:
  - Em dash detection: ✅ Perfect functionality (counts multiple occurrences)
  - Antithesis detection: ✅ Enhanced pattern matching with expanded phrase recognition
  - Multi-pattern detection: ✅ Successfully identifies combined patterns
  - Rhetorical contrast: ❌ Currently being debugged and refined
  - Negative testing: ✅ Validates specificity to prevent false positives

### Debugging Methodology
- **Six Thinking Hats Framework**: Applied for autonomous development decision-making
  - Blue Hat: Process Management & Orchestration
  - White Hat: Comprehensive Data Architecture
  - Red Hat: Emotional Intelligence Architecture
  - Black Hat: Comprehensive Risk Architecture
  - Yellow Hat: Value Architecture & Opportunity Framework
  - Green Hat: Innovation & Creative Synthesis Architecture
- **Systematic Debugging**: Structured approach to pattern detection refinement
  - Data collection and analysis (White Hat)
  - Risk assessment and mitigation (Black Hat)
  - Creative solution generation (Green Hat)
  - Value optimization (Yellow Hat)
  - Emotional landscape analysis (Red Hat)
  - Process orchestration (Blue Hat)

## Development Process

### Project Structure
```
├── main.py                 # Entry point
├── flow.py                # Workflow definitions
├── nodes/                 # Individual workflow nodes
│   ├── engagement_manager.py
│   ├── brand_bible_processor.py
│   ├── format_guidelines.py
│   └── ... (14 more nodes)
├── utils/                 # Utility functions
│   ├── call_llm.py
│   ├── brand_bible_parser.py
│   ├── deadly_sins_detector.py
│   └── ... (9 more utilities)
├── shared_store.py        # Shared state management
└── requirements.txt       # Dependencies
```

### Development Workflow
1. **Design Phase**: Define system architecture and workflow
2. **Implementation Phase**: Build core components and nodes
3. **Testing Phase**: Validate pattern detection and content generation
4. **Optimization Phase**: Improve performance and accuracy
5. **Deployment Phase**: Prepare for production use

## Technical Constraints

1. **No External Service Integrations**: System must be self-contained
2. **LLM Access Only Through OpenRouter**: All LLM interactions must go through utility functions
3. **Strict Pattern Elimination**: Must detect and remove all 7 Deadly Sins with zero tolerance
4. **Revision Limit**: Maximum 5 revision cycles for style compliance before manual review required
5. **Output Format**: Final output must be formatted markdown with copy-to-clipboard functionality

## Performance Considerations

- Optimized batch processing for faster iteration cycles
- Asynchronous pattern detection to prevent performance bottlenecks
- Real-time pattern learning to prevent pattern generation at source
- Deterministic pattern elimination to ensure consistent results

This technical context provides the foundation for understanding the implementation details of the PR Firm Content Generation System, including the technology stack, development environment, architecture, and key features.
