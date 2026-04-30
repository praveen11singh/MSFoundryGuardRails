import os
import requests
import subprocess
import json
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

# --- config ---
SUBSCRIPTION_ID = os.environ["SUBSCRIPTION_ID"]
RESOURCE_GROUP  = os.environ["RESOURCE_GROUP"]
ACCOUNT_NAME    = os.environ["ACCOUNT_NAME"]          
POLICY_NAME     = os.environ["POLICY_NAME"]
API_VERSION     = os.environ["API_VERSION"]

# --- get Azure AD token via Azure CLI ---
def get_bearer_token():
    credential = AzureCliCredential()
    token = credential.get_token("https://management.azure.com/.default")
    return token.token
    token = result.stdout.strip()
    if not token:
        raise RuntimeError("Could not get token. Are you logged in? Run: az login")
    return token

token = get_bearer_token()

# --- build ARM endpoint ---
url = (
    f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}"
    f"/resourceGroups/{RESOURCE_GROUP}"
    f"/providers/Microsoft.CognitiveServices/accounts/{ACCOUNT_NAME}"
    f"/raiPolicies/{POLICY_NAME}"
    f"?api-version={API_VERSION}"
)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

# --- guardrail definition ---
payload = {
    "name": POLICY_NAME,
    "properties": {
        "basePolicyName": "Microsoft.DefaultV2",
        "mode": "Blocking",
        "contentFilters": [
            # Hate
            {"name": "hate", "blocking": True, "enabled": True, "allowedContentLevel": "Medium", "source": "Prompt"},
            {"name": "hate", "blocking": True, "enabled": True, "allowedContentLevel": "Medium", "source": "Completion"},
            # Violence
            {"name": "violence", "blocking": True, "enabled": True, "allowedContentLevel": "Medium", "source": "Prompt"},
            {"name": "violence", "blocking": True, "enabled": True, "allowedContentLevel": "Medium", "source": "Completion"},
            # Jailbreak
            {"name": "jailbreak", "blocking": True, "enabled": True, "source": "Prompt"},
        ]
    }
}

print("PUT", url)
resp = requests.put(url, headers=headers, json=payload)
print(resp.status_code)
print(json.dumps(resp.json(), indent=2))
resp.raise_for_status()

guardrail = resp.json()
print("\nGuardrail created:", guardrail["name"])