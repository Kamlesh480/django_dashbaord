all_custom_fields = [
    "new_issue",
    "follow_up_issue",
    "not_an_issue",
    "reopen_after_autoclose",
    "not_a_reopen",
    "reopen_issue_resolved_additonal_info",
]


while True:
    print(
        "Enter a number between 1 and {} to select a custom field:".format(
            len(all_custom_fields) + 1
        )
    )
    for index, field in enumerate(all_custom_fields):
        print("{}. {}".format(index + 1, field))
    print("{}. Other".format(len(all_custom_fields) + 1))

    selection = input()

    if not selection.isdigit():
        print("Oops! That was not a valid number. Please try again...")
    elif int(selection) < 1 or int(selection) > len(all_custom_fields) + 1:
        print("Oops! Number not in range. Please try again...")
    elif selection == "" or selection == str(len(all_custom_fields) + 1):
        custom_field = None
        print("You have selected: Other")
        break
    else:
        custom_field = all_custom_fields[int(selection) - 1]
        print("You have selected: {}".format(custom_field))
        break


all_custom_fields = [
    "Other",
    "new_issue",
    "follow_up_issue",
    "not_an_issue",
    "reopen_after_autoclose",
    "not_a_reopen",
    "reopen_issue_resolved_additonal_info",
]
