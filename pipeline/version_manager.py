import os
import json


def save_version(account_id, version, memo, agent):

    base_path = f"outputs/accounts/{account_id}/{version}"

    # create folder if it doesn't exist
    os.makedirs(base_path, exist_ok=True)

    # save account memo
    with open(f"{base_path}/memo.json", "w") as f:
        json.dump(memo, f, indent=2)

    # save agent configuration
    with open(f"{base_path}/agent.json", "w") as f:
        json.dump(agent, f, indent=2)

    print(f"Saved {account_id} {version}")