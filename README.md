# 🛡️ Ecovilance: Environmental Data Integrity Watchdog

Ecovilance is a Python-based Proof-of-Concept (PoC) designed to secure real-time environmental data streams against corporate tampering and insider threats. 

## The Problem
When factories or municipalities report real-time air pollution data, malicious actors may attempt to alter the data stream to hide violations and avoid fines. 

## The Ecovilance Solution
Ecovilance acts as a secure middleman. It fetches live environmental data, applies SHA-256 cryptographic hashing, and writes it to an immutable, chained CSV ledger. If even a single decimal point of the data is altered after logging, the cryptographic chain breaks, instantly exposing the tampering.

## Features
- Real-time API Integration: Fetches live PM2.5, PM10, and NO2 data via Open-Meteo.
- Cryptographic Hash Chaining: Implements blockchain-style hash chaining to ensure data immutability.
- Automated Auditing: Includes a secondary script to recalculate hashes and verify ledger integrity.
- Intrusion Simulation: Built-in simulation demonstrating how the system catches falsified data.

## How to Run
1. Clone the repository.
2. Install dependencies: pip install -r requirements.txt
3. Run the application: python main.py
