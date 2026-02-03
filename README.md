# Agentic Honey-Pot: AI-Powered Scam Detection & Intelligence Extraction

Detect, analyze, and extract actionable intelligence from scam messages—automatically.

Agentic Honey-Pot is an AI-powered system that identifies scam messages and extracts critical information such as phishing URLs, UPI IDs, and bank account numbers. It’s lightweight, easy to deploy, and comes with a secure API for seamless integration with other tools or automated systems.

## Key Features

**Smart Scam Detection: Identifies scam messages using keyword-based AI analysis.

**Actionable Intelligence: Extracts URLs, UPI IDs, and bank account numbers from messages.

**Secure API: Access the system safely using API key authentication (x-api-key).

**JSON Responses: Receive structured, clear, and machine-readable outputs.

**Lightweight & Easy: Simple setup and deployment without heavy dependencies.

##Tech Stack

**Python – Core logic and processing
**Flask – Web framework for API
**Regular Expressions (re) – Pattern extraction from messages
**REST API – For automated integration

## System Architecture

![Agentic Honey-Pot Flow]

## How to Use the API

**Endpoint: POST /analyze

Headers:

x-api-key: hello
Content-Type: application/json


## Sample Request 1:

{
  "message": "Urgent! Click https://fakebank.com to win a prize. Pay to scammer@upi"
}


## Sample Response 1:

{
  "received_message": "urgent! click https://fakebank.com to win a prize. pay to scammer@upi",
  "result": "SCAM !",
  "detected_keywords": ["urgent", "click", "win"],
  "extracted_intelligence": {
    "urls": ["https://fakebank.com"],
    "upi_ids": ["scammer@upi"],
    "bank_accounts": []
  }
}

## Run Locally
bash-
Install dependencies
pip install flask

json-
Start the application
python app.py


## Test using PowerShell

Invoke-RestMethod -Uri "http://127.0.0.1:5000/analyze" `
-Method POST `
-Headers @{ "x-api-key"="hello" } `
-ContentType "application/json" `
-Body '{"message":"Urgent! Click https://fakebank.com now"}'

## Project Structure
agentic-honeypot/
├── app.py             # Main Flask application
├── requirements.txt   # Dependencies
└── README.md          # Project documentation
└── images/
     └── flowchart.png


# Why Use Agentic Honey-Pot?

This system is ideal for developers, security analysts, or organizations wanting to automatically detect scams and extract critical intelligence from messages in real time—helping prevent fraud before it spreads.
