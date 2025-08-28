<h1 align="center">PR Firm Content Generation System</h1>

<p align="center">
  <img src="./assets/banner.png" width="800" alt="PR Firm Content Generation System"/>
</p>

# PR Firm Content Generation System

A sophisticated content generation system built with [PocketFlow](https://github.com/The-Pocket/PocketFlow) that creates platform-optimized, brand-consistent content while eliminating AI fingerprints. This system implements a complete workflow for generating authentic marketing content across multiple platforms.

## Features

- **Multi-Platform Content Generation**: Creates optimized content for email, LinkedIn, Instagram, Twitter, Reddit, and blog posts
- **AI Fingerprint Elimination**: Detects and removes all 7 "Deadly Sins" of AI-generated content
- **Brand Voice Consistency**: Maintains consistent brand personality across all platforms
- **Authenticity Scoring**: Measures content authenticity with comprehensive metrics
- **Iterative Refinement**: Interactive feedback loop for content improvement
- **Version Control**: Tracks content versions with rollback capability
- **Performance Analytics**: Provides insights into pattern reduction and efficiency gains
- **Preset Learning**: Automatically optimizes configurations based on usage patterns

## System Architecture

The system implements a sophisticated workflow with 17 specialized nodes:

1. **Engagement Manager** - Handles user inputs and preset management
2. **Brand Bible Processor** - Converts descriptive brand text into structured parameters
3. **Format Guidelines** - Generates platform-specific formatting rules
4. **Creative Inspiration** - Creates high-engagement content examples
5. **Pattern-Aware Prompt Engineering** - Enhances prompts to prevent AI patterns
6. **Content Generator** - Creates initial platform-optimized drafts
7. **Style Optimizer** - Refines content while maintaining brand voice
8. **Deadly Sins Scanner** - Detects AI fingerprint patterns
9. **Style Compliance** - Validates content authenticity
10. **Authenticity Scorer** - Evaluates human-like qualities
11. **Feedback Router** - Manages user feedback and version control
12. **Content Refinement** - Applies user-requested changes
13. **Pattern Learner** - Improves future prompt engineering
14. **Version Manager** - Tracks content versions
15. **Final Formatter** - Outputs clean markdown with copy functionality
16. **Preset Optimizer** - Learns from user preferences
17. **Version Analytics** - Provides performance insights

## Getting Started

### Prerequisites
- Python 3.8+
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

## Project Structure
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

## Key Components

### Deadly Sins Detection
The system identifies and eliminates 7 specific AI fingerprint patterns:
1. Em Dash Usage (—)
2. Rhetorical Contrasts ("It's not just X; it's Y")
3. Antithesis (contrasting opposing ideas)
4. Paradiastole (rhetorical reclassification)
5. Reframing Contrasts (shifting meaning)
6. Chiasmus-like Contrast (mirrored structures)
7. Tagline Framing (elevating products)

### Authenticity Scoring
Advanced metrics evaluate content across multiple dimensions:
- Pattern elimination effectiveness
- Natural flow and readability
- Engagement quality
- Brand alignment
- Human-like qualities

### Version Control & Analytics
- Track content versions with change history
- Analyze pattern reduction rates
- Measure time savings and ROI
- Optimize presets based on performance

## Built with PocketFlow

This project demonstrates the power of [PocketFlow](https://github.com/The-Pocket/PocketFlow), a lightweight LLM framework that enables complex agentic workflows through simple Node and Flow abstractions.
