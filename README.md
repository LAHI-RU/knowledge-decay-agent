# Internal Knowledge Decay Detection Agent 🕵️‍♂️📚

An autonomous Agentic AI system that monitors internal documentation, evaluates its relevance using LLMs, and flags "stale" or outdated knowledge.

## 🚀 Overview

Engineering teams often suffer from "Knowledge Decay"—documentation that becomes misleading over time. This tool automates the maintenance process by:
1.  **Scanning** repositories (Local or GitHub) for Markdown files.
2.  **Evaluating** content using OpenAI (GPT-4) to detect signs of staleness.
3.  **Notifying** the team via console alerts (extensible to Slack/Email).

## 🏗 Architecture

The system follows a modular Agentic workflow:

* **Scanner Agent (`src/scanner.py`):** Handles file I/O and GitHub API traversal.
* **Evaluator Agent (`src/evaluator.py`):** Uses Prompt Engineering to judge document freshness.
* **Notifier Agent (`src/notifier.py`):** Aggregates results and generates alerts.
* **Orchestrator (`main.py`):** Manages the data flow between agents.

## 🛠 Tech Stack

* **Language:** Python 3.10+
* **AI:** OpenAI API (GPT-4o / GPT-3.5)
* **Integration:** PyGithub (GitHub API)
* **Environment:** `python-dotenv` for security

## ⚙️ Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/knowledge-decay-agent.git](https://github.com/YOUR_USERNAME/knowledge-decay-agent.git)
    cd knowledge-decay-agent
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Credentials**
    Create a `.env` file in the root directory:
    ```ini
    OPENAI_API_KEY=sk-...
    GITHUB_TOKEN=ghp-...
    ```

## 🏃 Usage

**Scan a Local Directory:**
```bash
python main.py --target "docs/"