# MSFoundryGuardRails

This repository contains simple Python scripts for working with Azure AI Guardrails and related RAI policy/blocklist features.

## Overview

- `custom_create_guardrails.py`: Creates a new Azure Cognitive Services RAI policy guardrail with blocking content filters for hate, violence, and jailbreak.
- `custom_guardrails_attachto_model.py`: Lists existing RAI policies and attaches a selected guardrail to an existing model deployment.
- `custom_guardrails_create_blocklist.py`: Creates a blocklist, adds terms to it, and updates a guardrail policy to attach the blocklist.

## Prerequisites

- Python 3.8+ installed
- Azure CLI installed and authenticated (`az login`)
- Access to the Azure subscription, resource group, and Cognitive Services account used for RAI policies
- The following Python packages:
  - `azure-identity`
  - `azure-mgmt-cognitiveservices`
  - `python-dotenv`
  - `requests`

## Setup

1. Create a Python virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install azure-identity azure-mgmt-cognitiveservices python-dotenv requests
```

3. Create a `.env` file in the repository root with the required variables:

```text
SUBSCRIPTION_ID=your-subscription-id
RESOURCE_GROUP=your-resource-group
ACCOUNT_NAME=your-cognitive-services-account
POLICY_NAME=your-guardrail-policy-name
API_VERSION=2024-07-01-preview
BLOCKLIST_NAME=your-blocklist-name
AZURE_SUBSCRIPTION_ID=your-subscription-id
```

> `custom_guardrails_attachto_model.py` uses `AZURE_SUBSCRIPTION_ID` and also includes hardcoded defaults for `RESOURCE_GROUP`, `ACCOUNT_NAME`, and `DEPLOYMENT_NAME`. Update these values directly in the script or modify the script to use environment variables.

## Usage

### 1. Create a guardrail policy

```powershell
python custom_create_guardrails.py
```

### 2. Create a blocklist and attach it to a guardrail

```powershell
python custom_guardrails_create_blocklist.py
```

### 3. Attach an existing guardrail to a model deployment

```powershell
python custom_guardrails_attachto_model.py
```

The attach script will prompt you to select from available guardrails in the configured Cognitive Services account.

## Notes

- The scripts use Azure authentication via Azure CLI / default credential flows.
- Confirm the `API_VERSION` value matches the Azure Cognitive Services REST API version supported by your account.
- For production use, consider improving configuration handling, validation, and error management.
