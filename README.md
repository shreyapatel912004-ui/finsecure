# \# FinSecure: Fintech API Key Exposure Detection \& Auto-Remediation

# 

# A Python tool to detect exposed Stripe and fintech API keys on GitHub, analyze the damage, and automate remediation.

# 

# \## Overview

# 

# When developers accidentally commit API keys to GitHub, they have minutes before attackers drain their accounts. FinSecure finds these exposures automatically and can remediate them.

# 

# \## Current Status: Phase 1 ✅

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

