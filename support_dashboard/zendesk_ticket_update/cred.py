headers = {
    "Content-Type": "application/json",
}

all_custom_fields = [
    "new_issue",
    "follow_up_issue",
    "not_an_issue",
    "reopen_after_autoclose",
    "not_a_reopen",
    "reopen_issue_resolved_additonal_info",
    "no update needed",
]

load = {"ticket": {}}

base_url = "https://hevodata.zendesk.com/api/v2/tickets/{}.json"

additional_tag = "reopen_validated"
# Reason for First reopen - 10343390026649
custom_fields = [{"id": 10343390026649}]

payload = ""

# ticket_id = 38961
# custom_field = "new_issue"
