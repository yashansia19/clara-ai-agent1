import os
import json

from pipeline.extractor import extract_account_data
from pipeline.prompt_generator import generate_prompt
from pipeline.version_manager import save_version
from pipeline.diff_engine import generate_diff


DEMO_FOLDER = "dataset/demo_calls"
ONBOARDING_FOLDER = "dataset/onboarding_calls"


# -----------------------------
# DEMO PIPELINE (Create v1)
# -----------------------------
def process_demo(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    # Extract structured data
    account_data = extract_account_data(transcript)

    account_id = os.path.basename(file_path).replace(".txt", "")
    account_data["account_id"] = account_id

    # Generate agent prompt
    prompt = generate_prompt(account_data)

    # Extract timezone if present
    timezone = None
    if account_data.get("business_hours"):
        timezone = account_data["business_hours"].get("timezone")

    # Build agent specification
    agent_spec = {
        "agent_name": f"{account_id}_agent",
        "voice_style": "friendly professional",
        "timezone": timezone,
        "system_prompt": prompt,

        "key_variables": {
            "company_name": account_data.get("company_name"),
            "business_hours": account_data.get("business_hours"),
            "services_supported": account_data.get("services_supported"),
            "emergency_definition": account_data.get("emergency_definition")
        },

        "call_transfer_protocol": "Transfer emergency calls to dispatch if available",
        "fallback_protocol": "If transfer fails, apologize and assure the caller that dispatch will follow up",

        "version": "v1"
    }

    save_version(account_id, "v1", account_data, agent_spec)

    print(f"Generated v1 agent for {account_id}")


# -----------------------------
# DATA MERGING LOGIC
# -----------------------------
def merge_account_data(old_data, new_data):

    merged = old_data.copy()

    for key, value in new_data.items():

        # skip empty values
        if value is None:
            continue

        # skip empty lists
        if isinstance(value, list) and len(value) == 0:
            continue

        # special handling for business hours
        if key == "business_hours":

            merged_hours = old_data.get("business_hours", {}).copy()

            if isinstance(value, dict):

                for field in value:

                    if value[field] is not None and value[field] != "unknown":
                        merged_hours[field] = value[field]

            merged["business_hours"] = merged_hours
            continue

        # prevent onboarding from adding fake unknown questions
        if key == "questions_or_unknowns":
            merged[key] = old_data.get(key, [])
            continue

        # merge lists instead of replacing
        if isinstance(value, list) and isinstance(old_data.get(key), list):

            merged[key] = list(set(old_data[key] + value))

        else:
            merged[key] = value

    return merged

# -----------------------------
# ONBOARDING PIPELINE (Create v2)
# -----------------------------
def process_onboarding(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    # Extract onboarding updates
    new_data = extract_account_data(transcript)

    account_id = os.path.basename(file_path).replace(".txt", "")

    v1_path = f"outputs/accounts/{account_id}/v1/memo.json"

    if not os.path.exists(v1_path):
        print(f"No v1 found for {account_id}, skipping onboarding update.")
        return

    # Load previous data
    with open(v1_path, "r") as f:
        old_data = json.load(f)

    # Merge onboarding updates
    merged_data = merge_account_data(old_data, new_data)

    # Generate change log
    changes = generate_diff(old_data, merged_data)

    # Generate new prompt
    prompt = generate_prompt(merged_data)

    # Extract timezone
    timezone = None
    if merged_data.get("business_hours"):
        timezone = merged_data["business_hours"].get("timezone")

    # Updated agent spec (v2)
    agent_spec = {
        "agent_name": f"{account_id}_agent",
        "voice_style": "friendly professional",
        "timezone": timezone,
        "system_prompt": prompt,

        "key_variables": {
            "company_name": merged_data.get("company_name"),
            "business_hours": merged_data.get("business_hours"),
            "services_supported": merged_data.get("services_supported"),
            "emergency_definition": merged_data.get("emergency_definition")
        },

        "call_transfer_protocol": "Transfer emergency calls to dispatch phone tree",
        "fallback_protocol": "If transfer fails, apologize and assure quick follow-up from dispatch",

        "version": "v2"
    }

    # Save new version
    save_version(account_id, "v2", merged_data, agent_spec)

    # Save change log
    changelog_path = f"outputs/accounts/{account_id}/changes.json"

    with open(changelog_path, "w") as f:
        json.dump(changes, f, indent=2)

    print(f"Updated {account_id} to v2")


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def run_pipeline():

    print("\nRunning Demo Pipeline...\n")

    for file in os.listdir(DEMO_FOLDER):

        if file.endswith(".txt"):
            process_demo(os.path.join(DEMO_FOLDER, file))

    print("\nRunning Onboarding Updates...\n")

    for file in os.listdir(ONBOARDING_FOLDER):

        if file.endswith(".txt"):
            process_onboarding(os.path.join(ONBOARDING_FOLDER, file))


if __name__ == "__main__":
    run_pipeline()