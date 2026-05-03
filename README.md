# MSFoundryGuardRails

This repository contains Python scripts for managing Azure AI Foundry Guardrails, including creating RAI policies, attaching guardrails to model deployments, and managing blocklists for content filtering.

## Overview

The repository includes three main scripts:

- `custom_create_guardrails.py`: Creates a new Responsible AI (RAI) policy guardrail with content filters for hate, violence, and jailbreak attacks.
- `custom_guardrails_attachto_model.py`: Lists available RAI policies and attaches a selected guardrail to an existing model deployment.
- `custom_guardrails_create_blocklist.py`: Creates a custom blocklist, adds terms/patterns to it, and updates a guardrail policy to include the blocklist.

## Prerequisites

- Python 3.8 or higher
- Azure CLI installed and authenticated (`az login`)
- Access to an Azure subscription with Cognitive Services resources
- Required Python packages:
  - `azure-identity`
  - `azure-mgmt-cognitiveservices`
  - `python-dotenv`
  - `requests`

## Setup

1. Clone or download this repository.

2. Create a Python virtual environment (recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the required dependencies:

   ```powershell
   pip install azure-identity azure-mgmt-cognitiveservices python-dotenv requests
   ```

4. Create a `.env` file in the repository root with your Azure configuration:

   ```env
   SUBSCRIPTION_ID=your-subscription-id
   RESOURCE_GROUP=your-resource-group-name
   ACCOUNT_NAME=your-cognitive-services-account-name
   POLICY_NAME=your-desired-guardrail-policy-name
   API_VERSION=2024-07-01-preview
   BLOCKLIST_NAME=your-desired-blocklist-name
   AZURE_SUBSCRIPTION_ID=your-subscription-id
   ```

   > **Note**: `custom_guardrails_attachto_model.py` uses `AZURE_SUBSCRIPTION_ID` and has hardcoded defaults for `RESOURCE_GROUP`, `ACCOUNT_NAME`, and `DEPLOYMENT_NAME`. Update these values in the script or modify it to read from environment variables for flexibility.

## Usage

### Creating a Guardrail Policy

Run `custom_create_guardrails.py` to create a new RAI policy with default content filters:

```powershell
python custom_create_guardrails.py
```

This script creates a blocking guardrail that filters hate, violence, and jailbreak content in both prompts and completions.

### Attaching a Guardrail to a Model Deployment

Run `custom_guardrails_attachto_model.py` to attach an existing guardrail to a model deployment:

```powershell
python custom_guardrails_attachto_model.py
```

The script will:
1. List all available guardrails in your Cognitive Services account
2. Prompt you to select one
3. Attach the selected guardrail to the specified model deployment

### Creating and Managing Blocklists

Run `custom_guardrails_create_blocklist.py` to create a blocklist and attach it to a guardrail:

```powershell
python custom_guardrails_create_blocklist.py
```

This script:
1. Creates a new blocklist
2. Adds predefined terms/patterns (e.g., "Delhi", "Pune", regex patterns like "hack\w+")
3. Updates the guardrail policy to include the blocklist for both prompts and completions

## Customization

- Modify the content filters in `custom_create_guardrails.py` to adjust blocking levels or add new filters.
- Update the blocklist terms in `custom_guardrails_create_blocklist.py` to include your specific blocked content.
- Adjust hardcoded values in `custom_guardrails_attachto_model.py` for different resource groups, accounts, or deployments.

## Security Notes

- Ensure your Azure account has the necessary permissions to manage RAI policies and Cognitive Services resources.
- Store sensitive information like subscription IDs securely using environment variables.
- Review and test guardrails in a development environment before applying to production deployments.

## Contributing

Feel free to submit issues or pull requests to improve these scripts or add new functionality.

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
