Sure! Here’s a clean, professional README.md tailored for your **Daya** agent, ready for GitHub upload:

````markdown
# Daya — AI Assistant for Women's Safety and Support

**Daya** is an intelligent AI agent designed to assist women with safety, legal awareness, emotional support, and daily wellbeing.  
Built on [Fetch.ai's uAgents](https://fetch.ai) framework and powered by the [ASI:One LLM](https://asi.network), Daya provides timely help with trusted helplines, empathetic guidance, and legal information — all through natural conversations.

---

## Features

- 🛡️ **Emergency Helpline Finder**  
  Detects user location from conversation and provides relevant state-wise helpline numbers for immediate assistance.

- 💬 **Conversational AI Support**  
  Friendly, empathetic responses for safety, legal questions, motivation, and emotional needs.

- 🔄 **Contextual Memory**  
  Remembers recent chat history for personalized and coherent interactions.

- 🌐 **Multi-domain Knowledge**  
  Covers health, safety, legal aid, and emotional wellbeing topics tailored for women.

---

## Technology Stack

| Component        | Description                                      |
| ---------------- | ------------------------------------------------ |
| Framework        | [uAgents](https://fetch.ai) by Fetch.ai          |
| Language Model   | [ASI:One](https://asi.network) (`asi1-mini`)     |
| Deployment       | [Agentverse](https://agentverse.ai)              |
| Memory           | Session-based short-term conversation memory     |
| Communication    | Decentralized agent communication infrastructure |

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- [`uAgents`](https://github.com/fetchai/uAgents) library
- ASI API Key (set as environment variable `ASI_API_KEY`)

### Installation

```bash
git clone https://github.com/riyaarah/Daya.git
cd daya-agent
pip install -r requirements.txt
````

### Running the Agent

```bash
python agent.py
```

The agent will start locally and listen for messages on port `8001`.

---

## Usage Example

Try sending messages like:

* "I feel unsafe in Bangalore, what should I do?"
* "Can you give me the women’s helpline in Tamil Nadu?"
* "I need legal help regarding harassment."
* "I’m feeling stressed, can you motivate me?"

Daya will respond with relevant helpline numbers, advice, or emotional support.

---

## Folder Structure

```
/
├── agent.py           # Main agent script
├── requirements.txt   # Python dependencies
├── README.md          # This file
└── LICENSE            # MIT License file
```

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to improve Daya.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Contact

Created by Riya Rahim
Email: [riyaarah@gmail.com](mailto:riyaarah@gmail.com)

---

> “Empowering women through knowledge, support, and AI.”
> — Daya, your AI companion for safety and wellbeing

```
