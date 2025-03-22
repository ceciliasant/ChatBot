# ChatBot - Conversational Agent
## Project: SI-II (Sistemas Inteligentes) - 2024/2025

## Description 
A simple conversational agent (chatbot) capable of:
- Learning facts from user input
- Recalling facts when asked
- Handling grammar corrections
- Responding intelligently to unknown or incorrect inputs

## Installation
1. Create a virtual environment (optional but recommended):
    ```sh
    python -m venv venv 
    source venv/bin/activate
    ``` 
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    python -m spacy download en
    ``` 

## Usage
Run the project using: 
```sh
python main.py
```
## Example Execution
```sh
$ python MP1.py 
Output: Hello, World!
```
