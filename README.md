# ChatBot - Conversational Agent
## Project: SI-II (Sistemas Inteligentes) - 2024/2025

A simple conversational agent (chatbot) capable of:
- Learning facts from user input
- Recalling facts when asked
- Handling grammar corrections
- Responding intelligently to unknown or incorrect inputs

## Features 

    - Fact Management: Store/retrieve facts (e.g., "Alice is a professor.").

    - Weather Lookup: Real-time weather using wttr.in.

    - Grammar Correction: Auto-suggest input corrections.

    - Conversational Fallback: DialoGPT-medium for open-ended dialogue.

    - SQLite Database: Stores user-specific knowledge.

## Installation

1. Clone the repo:
    ```sh
    git clone "https://github.com/ceciliasant/ChatBot"
    cd ChatBot/src
    ```
2. Create a virtual environment (optional but recommended):
    ```sh
    python -m venv venv 
    source venv/bin/activate
    ``` 
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    python -m spacy download en_core_web_sm
    ``` 

## Usage
Run the project using: 
```sh
python MP1.py
```

| Intent              | User Input                     | Bot Response                                        |
|---------------------|--------------------------------|-----------------------------------------------------|
| **Store Fact**      | "Alice works at Google."      | "Noted! Alice works at Google."                    |
| **Retrieve Fact**   | "Where does Alice work?"      | "Alice works at Google."                           |
| **Weather Query**   | "Weather in Porto?"          | "Currently, it's clear with 14°C in Porto."        |
| **Open-Ended Query**| "Tell me about sheep." | "Could you clarify what aspect interests you?" |

## Database 

Facts are stored in user_facts table:

| Column    | Description                                |
|-----------|--------------------------------------------|
| **user_id**  | Unique user identifier.                 |
| **key**      | Entity (e.g., "Alice").                 |
| **value**    | Fact (e.g., "Google").                  |
| **fact_type**| Relation (e.g., "works at").            |

## Intent Recognition

The bot uses regex patterns to detect intents.

## Contributors

Artur Almeida

Cecília Santos

Pedro Ramos

Rafael Morgado