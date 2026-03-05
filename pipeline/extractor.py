import re


def extract_account_data(text):

    text_lower = text.lower()

    data = {
        "account_id": None,
        "company_name": None,
        "business_hours": None,
        "office_address": None,
        "services_supported": [],
        "emergency_definition": [],
        "emergency_routing_rules": None,
        "non_emergency_routing_rules": None,
        "call_transfer_rules": None,
        "integration_constraints": [],
        "after_hours_flow_summary": None,
        "office_hours_flow_summary": None,
        "questions_or_unknowns": [],
        "notes": []
    }

    # ----------------------------
    # COMPANY NAME DETECTION
    # ----------------------------

    company_patterns = [
        r"from\s+([a-zA-Z0-9\s]+)\s+company",
        r"this is .* from\s+([a-zA-Z0-9\s]+)",
        r"company\s+name\s+is\s+([a-zA-Z0-9\s]+)"
    ]

    for pattern in company_patterns:
        match = re.search(pattern, text_lower)
        if match:
            data["company_name"] = match.group(1).strip().title()
            break

    # ----------------------------
    # SERVICES DETECTION
    # ----------------------------

    if "sprinkler" in text_lower:
        data["services_supported"].append("sprinkler systems")

    if "fire alarm" in text_lower or "alarm" in text_lower:
        data["services_supported"].append("fire alarm systems")

    if "hvac" in text_lower:
        data["services_supported"].append("hvac")

    if "electrical" in text_lower:
        data["services_supported"].append("electrical services")

    # ----------------------------
    # EMERGENCY DEFINITIONS
    # ----------------------------

    if "sprinkler leak" in text_lower:
        data["emergency_definition"].append("sprinkler leak")

    if "fire alarm triggered" in text_lower or "alarm triggered" in text_lower:
        data["emergency_definition"].append("fire alarm triggered")

    if "emergency" in text_lower and len(data["emergency_definition"]) == 0:
        data["notes"].append("Emergency mentioned but not clearly defined")

    # ----------------------------
    # BUSINESS HOURS DETECTION
    # ----------------------------

    hours_match = re.search(
        r"(\d{1,2})\s?(am|pm)\s?to\s?(\d{1,2})\s?(am|pm)", text_lower
    )

    if hours_match:
        start_hour = hours_match.group(1)
        start_period = hours_match.group(2)

        end_hour = hours_match.group(3)
        end_period = hours_match.group(4)

        data["business_hours"] = {
            "days": "unknown",
            "start": f"{start_hour} {start_period}",
            "end": f"{end_hour} {end_period}",
            "timezone": None
        }

    # detect days if mentioned
    if "monday to friday" in text_lower or "mon to fri" in text_lower:
        if data["business_hours"]:
            data["business_hours"]["days"] = "Mon-Fri"

    # ----------------------------
    # EMERGENCY ROUTING RULES
    # ----------------------------

    if "dispatch phone tree" in text_lower:
        data["emergency_routing_rules"] = "transfer to dispatch phone tree"

    elif "dispatch" in text_lower:
        data["emergency_routing_rules"] = "transfer to dispatch"

    # ----------------------------
    # INTEGRATION CONSTRAINTS
    # ----------------------------

    if "never create sprinkler jobs" in text_lower:
        data["integration_constraints"].append(
            "never create sprinkler jobs in ServiceTrade"
        )

    if "servicetrade" in text_lower:
        if "never create sprinkler jobs in ServiceTrade" not in data["integration_constraints"]:
            data["notes"].append("ServiceTrade integration mentioned")

    # ----------------------------
    # CALL TRANSFER RULES
    # ----------------------------

    if "transfer" in text_lower:
        data["call_transfer_rules"] = "transfer emergency calls to dispatch"

    # ----------------------------
    # UNKNOWN FIELD HANDLING
    # ----------------------------

    if not data["company_name"]:
        data["questions_or_unknowns"].append("Company name not mentioned")

    if not data["business_hours"]:
        data["questions_or_unknowns"].append("Business hours not mentioned")

    if len(data["services_supported"]) == 0:
        data["questions_or_unknowns"].append("Services not clearly specified")

    if len(data["emergency_definition"]) == 0:
        data["questions_or_unknowns"].append("Emergency definition missing")

    return data