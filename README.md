# Password-Strength-Analyzer-Wordlist-Generator
---
A comprehensive Python tool for analyzing password strength and generating custom wordlists for security testing purposes.

## 🔍 Overview
This tool combines advanced password analysis with intelligent wordlist generation, making it an essential utility for security professionals, penetration testers, and cybersecurity educators. It provides both graphical and command-line interfaces for maximum flexibility.

## ✨ Features
### Password Analysis

Entropy Calculation: Advanced mathematical analysis of password complexity
Pattern Detection: Identifies common patterns, keyboard walks, and repetitive sequences
Comprehensive Scoring: 0-100 scoring system with detailed strength ratings
Security Recommendations: Actionable suggestions for password improvement
Vulnerability Detection: Spots common substitutions and dictionary words

### Wordlist Generation

Personal Information Integration: Uses names, pets, dates, companies, and hobbies
Intelligent Transformations: Applies leetspeak, case variations, and reversals
Year & Number Combinations: Automatically appends years (1950-2030) and common numbers
Pattern Recognition: Generates variations based on common password patterns
Smart Filtering: Removes duplicates and applies minimum length requirements

### User Interface

Dual Interface: Both GUI and CLI modes available
Export Functionality: Saves wordlists in standard .txt format
Real-time Analysis: Instant feedback on password strength
Threaded Processing: Non-blocking wordlist generation

## 📖 Usage
### GUI Mode
```bash
python password_tool.py --gui
# or simply
python password_tool.py
```

### Command Line Interface
```bash
python password_tool.py --analyze "YourPasswordHere"
python password_tool.py --generate --output custom_wordlist.txt
```
