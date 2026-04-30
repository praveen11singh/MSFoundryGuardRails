import json
import requests
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
import os

load_dotenv()

# --- config ---
SUBSCRIPTION_ID = os.environ["SUBSCRIPTION_ID"]
RESOURCE_GROUP  = os.environ["RESOURCE_GROUP"]
ACCOUNT_NAME    = os.environ["ACCOUNT_NAME"]          
POLICY_NAME     = os.environ["POLICY_NAME"]
API_VERSION     = os.environ["API_VERSION"]
BLOCKLIST_NAME  = os.environ["BLOCKLIST_NAME"]

BASE_URL = (
    f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}"
    f"/resourceGroups/{RESOURCE_GROUP}"
    f"/providers/Microsoft.CognitiveServices/accounts/{ACCOUNT_NAME}"
)

# --- auth ---
token = AzureCliCredential().get_token("https://management.azure.com/.default").token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

# ---------------------------------------------------------------
# STEP 1: Create the blocklist
# ---------------------------------------------------------------
print("Step 1: Creating blocklist...")
resp = requests.put(
    f"{BASE_URL}/raiBlocklists/{BLOCKLIST_NAME}?api-version={API_VERSION}",
    headers=headers,
    json={"properties": {"description": "Custom prompt/completion blocklist"}},
)
print(resp.status_code, resp.text)
resp.raise_for_status()

# ---------------------------------------------------------------
# STEP 2: Add terms to the blocklist
# ---------------------------------------------------------------
terms = [
    {"name": "pk-block-item-1", "pattern": "Delhi",   "isRegex": False},
    {"name": "pk-block-item-2", "pattern": "Pune",  "isRegex": False},
    {"name": "pk-block-item-3", "pattern": r"hack\w+",  "isRegex": True},  # regex example
]

print("\nStep 2: Adding blocklist items...")
for item in terms:
    resp = requests.put(
        f"{BASE_URL}/raiBlocklists/{BLOCKLIST_NAME}/raiBlocklistItems/{item['name']}?api-version={API_VERSION}",
        headers=headers,
        json={"properties": {"pattern": item["pattern"], "isRegex": item["isRegex"]}},
    )
    print(f"  {item['name']}: {resp.status_code}")
    resp.raise_for_status()

# ---------------------------------------------------------------
# STEP 3: Attach blocklist to your guardrail (update the policy)
# ---------------------------------------------------------------
print("\nStep 3: Attaching blocklist to guardrail...")
resp = requests.put(
    f"{BASE_URL}/raiPolicies/{POLICY_NAME}?api-version={API_VERSION}",
    headers=headers,
    json={
        "name": POLICY_NAME,
        "properties": {
            "basePolicyName": "Microsoft.DefaultV2",
            "mode": "Blocking",
            # Attach blocklist to BOTH prompt and completion
            "promptBlocklists":     [{"blocklistName": BLOCKLIST_NAME, "blocking": True}],
            "completionBlocklists": [{"blocklistName": BLOCKLIST_NAME, "blocking": True}],
            "contentFilters": [
                {"name": "hate",      "blocking": True, "enabled": True, "allowedContentLevel": "Medium", "source": "Prompt"},
                {"name": "hate",      "blocking": True, "enabled": True, "allowedContentLevel": "Medium", "source": "Completion"},
                {"name": "violence",  "blocking": True, "enabled": True, "allowedContentLevel": "Medium", "source": "Prompt"},
                {"name": "violence",  "blocking": True, "enabled": True, "allowedContentLevel": "Medium", "source": "Completion"},
                {"name": "jailbreak", "blocking": True, "enabled": True, "source": "Prompt"},
            ],
        },
    },
)
print(resp.status_code)
print(json.dumps(resp.json(), indent=2))
resp.raise_for_status()
print("\nDone! Blocklist attached to guardrail.")