# Clara AI – AgentSpec Pipeline

**An automated pipeline that converts customer call transcripts into structured AI Agent Specifications, versions them over time, and visualizes the differences through a simple dashboard.**

This project simulates how companies configure **AI voice agents** using knowledge extracted from **sales and onboarding calls**.

---

# Live Demo

### Agent Dashboard

```
https://yourusername.github.io/clara-ai-agent/
```

*(Replace with your GitHub Pages link after deployment.)*

---

# Problem

When companies deploy **AI voice agents**, important operational information is usually captured through:

* Sales calls
* Onboarding conversations
* Internal documentation

However this information is typically:

* Unstructured
* Hidden inside transcripts
* Updated over time
* Difficult to maintain

AI agents require **structured specifications** to function correctly.

---

# Solution

This project builds an **AgentSpec generation pipeline** that:

1. Extracts structured data from transcripts
2. Generates an AI Agent Specification
3. Versions the specification over time
4. Detects configuration changes
5. Visualizes updates using a dashboard

---

# Architecture

```
Transcript
    │
    ▼
Extractor
    │
    ▼
Structured Account Data
    │
    ▼
AgentSpec Generator
    │
    ▼
Version Manager
    │
    ▼
Diff Engine
    │
    ▼
Dashboard UI
```

---

# Project Structure

```
clara-ai-agent
│
├── dataset
│   ├── demo_calls
│   │   └── demo1.txt
│   │
│   └── onboarding_calls
│       └── demo1.txt
│
├── pipeline
│   ├── extractor.py
│   ├── prompt_generator.py
│   ├── version_manager.py
│   └── diff_engine.py
│
├── outputs
│   └── accounts
│       └── demo1
│           ├── v1
│           │   └── memo.json
│           ├── v2
│           │   └── memo.json
│           └── changes.json
│
├── index.html
├── run_pipeline.py
└── README.md
```

---

# Core Components

## Extractor

Parses transcripts to detect structured information such as:

* Company name
* Services supported
* Emergency definitions
* Business hours

Example extraction:

```
"9 am to 5 pm"
```

becomes

```
{
  "start": "9 am",
  "end": "5 pm"
}
```

---

## Prompt Generator

Transforms structured account data into an **AI agent system prompt**.

Example:

```
You are a voice agent for Safesprinkler.

Business hours:
Mon–Fri 9am–5pm

Supported services:
• sprinkler systems
• fire alarm systems

Emergency cases:
• sprinkler leaks
```

---

## Version Manager

Each generated agent configuration is stored as a **version**.

* **v1 → initial demo call configuration**
* **v2 → onboarding updated configuration**

Files are stored in:

```
outputs/accounts/{account_id}/
```

---

## Diff Engine

Detects differences between versions.

Example output:

```
{
  "business_hours": {
    "old": "9am–5pm",
    "new": "8am–6pm"
  }
}
```

This creates a **clear audit trail of agent configuration updates.**

---

# Dashboard

The project includes a simple dashboard built using:

* HTML
* CSS
* JavaScript

The dashboard displays:

* Account information
* Services supported
* Emergency definitions
* Business hours
* Version differences

---

# Running the Project

## 1️⃣ Add Transcripts

Place transcript files inside:

```
dataset/demo_calls/
dataset/onboarding_calls/
```

---

## 2️⃣ Run the Pipeline

```
python run_pipeline.py
```

---

## 3️⃣ Generated Outputs

The system will create:

```
outputs/accounts/demo1/v1/memo.json
outputs/accounts/demo1/v2/memo.json
outputs/accounts/demo1/changes.json
```

---

# Example Change Detection

### Business Hours

**Old**

```
9am – 5pm
```

**New**

```
8am – 6pm
```

Additional detected changes:

* Emergency routing rule added
* Call transfer rule added
* Integration constraint added

---

# Technologies Used

## Backend

* Python
* Regular Expressions
* JSON Processing

## Frontend

* HTML
* CSS
* JavaScript

---

# Future Improvements

* LLM-based transcript extraction
* Automated transcript ingestion
* Multi-account support
* Real-time dashboard updates
* CRM integrations

---

# Author

Created for the **Clara AI AgentSpec Assignment** to demonstrate how **conversational data can be transformed into structured AI agent configurations.**

---

# License

Educational / demonstration project.
