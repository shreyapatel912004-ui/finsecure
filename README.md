# \# FinSecure: Fintech API Key Exposure Detection \& Auto-Remediation

# 

# A Python tool to detect exposed Stripe and fintech API keys on GitHub, analyze the damage, and automate remediation.

# 

# \## Overview

# 

# When developers accidentally commit API keys to GitHub, they have minutes before attackers drain their accounts. FinSecure finds these exposures automatically and can remediate them.

# 

# \## Current Status: Phase 3 COMPLETE

# 

# \### What Phase 3 Does (PRODUCTION-READY)

# \- Automatically rotates exposed API keys

# \- Verifies webhook configurations haven't been hijacked

# \- Audits charges and refunds for fraud

# \- Sends automated alerts to merchants

# \- Creates immutable audit logs

# \- Complete incident response automation

# \### What Phase 2 Does (NEW)

# \- Connects to Stripe API using exposed keys

# \- Analyzes transaction history during exposure window

# \- Detects fraud patterns (refunds, charge spikes, geographic anomalies)

# \- Calculates total fraud damage

# \- Generates forensic analysis reports

# 

# \### What Phase 1 Does

# \- Scans GitHub for exposed Stripe keys (sk\_live\_, sk\_test\_)

# \- Stores findings in SQLite database

# \- Displays key details and exposure locations

# \- Command-line interface for quick scanning

# 

# \### Key Features

# \- GitHub API integration for real-time searching

# \- Risk level classification (CRITICAL)

# \- Exposure source tracking

# \- Simple CLI menu

# 

# \## How to Use

# 

# ```bash

# \# 1. Activate virtual environment

# .\\venv\\Scripts\\Activate.ps1

# 

# \# 2. Set up .env with GitHub token

# notepad .env

# 

# \# 3. Run the tool

# python main.py

# 

# \# 4. Choose option 1 to scan

# ```

# 

# \## Project Structure

