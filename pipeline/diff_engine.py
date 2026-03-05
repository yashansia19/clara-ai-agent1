def generate_diff(old_data, new_data):

    changes = {}

    for key in new_data:

        # account_id should never change
        if key == "account_id":
            continue

        if key not in old_data:
            changes[key] = {
                "old": None,
                "new": new_data[key]
            }

        elif old_data[key] != new_data[key]:

            changes[key] = {
                "old": old_data[key],
                "new": new_data[key]
            }

    return changes