# Agents_KM Accessibility Framework

A comprehensive accessibility-focused AI Agent Development Kit built on Google's ADK and Agent2Agent (A2A) frameworks, providing WCAG 2.1 Level AA compliance for AI agent development.

## 🎯 Project Overview

This framework implements accessibility features for Google's Agent Development Kit (ADK) and Agent2Agent (A2A) Python frameworks, making AI agent development more inclusive and accessible to developers with disabilities.

### Key Features

- **WCAG 2.1 Level AA Compliance**: Full implementation of WCAG Principles 2 (Operable) and 3 (Understandable)
- **Multi-Agent Architecture**: Coordinated system with main agents and specialized sub-agents
- **Priority-Based Coordination**: Safety-critical accessibility features get highest priority
- **Real-time Monitoring**: Performance metrics and compliance validation
- **Gemini 2.0 Flash Integration**: Powered by Google's latest AI model

## 🏗️ Architecture

### Main Agents
- **OperableMainAgent**: Coordinates WCAG Principle 2 (Operable) compliance
- **UnderstandableMainAgent**: Coordinates WCAG Principle 3 (Understandable) compliance
- **AccessibilityMainCoordinator**: Cross-principle integration and coordination

### Sub-Agents (Operable)
1. **KeyboardAccessibleAgent** (Priority 1): WCAG 2.1.x - Keyboard functionality
2. **SeizuresPhysicalAgent** (Priority 2): WCAG 2.3.x - Safety critical seizure prevention
3. **NavigableAgent** (Priority 3): WCAG 2.4.x - Navigation and wayfinding
4. **EnoughTimeAgent** (Priority 4): WCAG 2.2.x - Timing controls
5. **InputModalitiesAgent** (Priority 5): WCAG 2.5.x - Multi-modal input support

### Sub-Agents (Understandable)
1. **ReadableAgent** (Priority 1): WCAG 3.1.x - Content readability
2. **PredictableAgent** (Priority 2): WCAG 3.2.x - Interface consistency
3. **InputAssistanceAgent** (Priority 3): WCAG 3.3.x - Error prevention and help

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/agents-km/accessibility-adk.git
cd accessibility-adk

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Basic Usage

```python
from accessibility import (
    OperableMainAgent,
    UnderstandableMainAgent,
    AccessibilityMainCoordinator
)

# Initialize the accessibility system
coordinator = AccessibilityMainCoordinator()

# Start accessibility monitoring
await coordinator.start()

# Your agent code here...
```

## 📁 Project Structure

```
src/accessibility/
├── agents/                    # Agent implementations
│   ├── main/                 # Main coordinator agents
│   ├── operable/             # WCAG Principle 2 sub-agents
│   ├── understandable/       # WCAG Principle 3 sub-agents
│   ├── base/                 # Base agent classes
│   └── legacy/               # Backward compatibility
├── wcag/                     # WCAG implementation modules
│   ├── principle_2/          # Operable criteria (2.1-2.5)
│   ├── principle_3/          # Understandable criteria (3.1-3.3)
│   └── testing/              # Compliance testing
├── ui/                       # Accessible UI components
├── a2a/                      # A2A protocol extensions
├── testing/                  # Testing framework
└── utils/                    # Utilities and helpers
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run accessibility compliance tests
pytest src/accessibility/testing/

# Run specific WCAG principle tests
pytest src/accessibility/testing/operable_tests.py
pytest src/accessibility/testing/understandable_tests.py
```

## 📊 WCAG Coverage

### Principle 2: Operable (26 criteria)
- ✅ 2.1.1-2.1.4: Keyboard Accessible
- ✅ 2.2.1-2.2.6: Enough Time
- ✅ 2.3.1-2.3.2: Seizures and Physical Reactions
- ✅ 2.4.1-2.4.10: Navigable
- ✅ 2.5.1-2.5.6: Input Modalities

### Principle 3: Understandable (17 criteria)
- ✅ 3.1.1-3.1.6: Readable
- ✅ 3.2.1-3.2.5: Predictable
- ✅ 3.3.1-3.3.6: Input Assistance

## 🔧 Configuration

Create a `.env` file or set environment variables:

```bash
# WCAG Configuration
WCAG_LEVEL=AA
WCAG_AUTO_FIX=true
WCAG_STRICT_MODE=false

# Agent Configuration
AGENT_MODEL=gemini-2.0-flash
AGENT_MAX_RETRIES=3
AGENT_TIMEOUT=30

# General Settings
DEBUG=false
LOG_LEVEL=INFO
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google ADK and A2A teams for the foundational frameworks
- W3C for WCAG 2.1 guidelines
- The accessibility community for guidance and feedback

## 📞 Support

- 📧 Email: team@agents-km.dev
- 🐛 Issues: [GitHub Issues](https://github.com/agents-km/accessibility-adk/issues)
- 📖 Documentation: [agents-km.github.io/accessibility-adk](https://agents-km.github.io/accessibility-adk/)

---

**Making AI agent development accessible to everyone** 🌟 