# ---------------------------------------------------------------
# Assign an existing Guardrail to a model deployment
# — Guardrail is selected dynamically (no hardcoded name)
# ---------------------------------------------------------------
# pip install azure-identity azure-mgmt-cognitiveservices

import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

# -----------------------------------------
# 1. Configuration
# -----------------------------------------
SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID", "7d1784d8-182b-451e-8150-955f496adb74")
RESOURCE_GROUP  = "PK_AIRG"
ACCOUNT_NAME    = "pkswdenfoundry"
DEPLOYMENT_NAME = "gpt-4.1"

# -----------------------------------------
# 2. Authenticate
# -----------------------------------------
credential  = DefaultAzureCredential()
mgmt_client = CognitiveServicesManagementClient(
    credential=credential,
    subscription_id=SUBSCRIPTION_ID,
)

# -----------------------------------------
# 3. List ALL existing guardrails on this account
# -----------------------------------------
print("Fetching available guardrails...\n")

policies = list(mgmt_client.rai_policies.list(
    resource_group_name=RESOURCE_GROUP,
    account_name=ACCOUNT_NAME,
))

if not policies:
    print("❌ No guardrails found on this account. Create one first in the Azure portal.")
    exit(1)

# -----------------------------------------
# 4. Display them and let the user pick one
# -----------------------------------------
print("Available Guardrails:")
for i, policy in enumerate(policies):
    print(f"  [{i}] {policy.name}")

choice = int(input("\nEnter the number of the guardrail to assign: "))
selected_policy = policies[choice]
RAI_POLICY_NAME = selected_policy.name

print(f"\n✅ Selected: '{RAI_POLICY_NAME}'")

# -----------------------------------------
# 5. Fetch current deployment to preserve
#    its model + SKU settings
# -----------------------------------------
print(f"\nFetching deployment '{DEPLOYMENT_NAME}'...")
current = mgmt_client.deployments.get(
    resource_group_name=RESOURCE_GROUP,
    account_name=ACCOUNT_NAME,
    deployment_name=DEPLOYMENT_NAME,
)
print(f"Current raiPolicyName: {current.properties.rai_policy_name or 'None'}")

# -----------------------------------------
# 6. Update deployment with selected guardrail
# -----------------------------------------
print(f"\nAttaching '{RAI_POLICY_NAME}' to deployment '{DEPLOYMENT_NAME}'...")

updated = mgmt_client.deployments.begin_create_or_update(
    resource_group_name=RESOURCE_GROUP,
    account_name=ACCOUNT_NAME,
    deployment_name=DEPLOYMENT_NAME,
    deployment={
        "sku": {
            "name":     current.sku.name,
            "capacity": current.sku.capacity,
        },
        "properties": {
            "model": {
                "format":  current.properties.model.format,
                "name":    current.properties.model.name,
                "version": current.properties.model.version,
            },
            "raiPolicyName": RAI_POLICY_NAME,  # Dynamically selected
        },
    },
).result()

print(f"\n✅ Done! Updated raiPolicyName: {updated.properties.rai_policy_name}")