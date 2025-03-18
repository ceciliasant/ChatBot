# ChatBot - Conversational Agent

## Project: SI-II (Sistemas Inteligentes) - 2024/2025

A simple conversational agent (chatbot) capable of:
- Learning facts from user input
- Recalling facts when asked
- Handling grammar corrections
- Responding intelligently to unknown or incorrect inputs

## Features
- Natural language processing (English)
- Persistent knowledge (JSON storage)
- Grammar correction using TextBlob
- Random fallback responses

## Dependencies
- TextBlob

## Example Conversation
  
  ```
  You: Hi
  Bot: Hello! How can I help you?
  
  You: My name is Damon
  Bot: Got it! I'll remember that my name is Damon.
  
  You: What is my name?
  Bot: You told me that my name is Damon.
  
  You: What is Portugal?
  Bot: Hmm, that's interesting! Can you tell me more?
  
  You: Portugal is a country
  Bot: Got it! I'll remember that portugal is a country.
  
  You: exit
  Bot: Goodbye!
  ```
