function updateSelectedRecipients() {
  var selectedRecipientsCount = document.querySelectorAll(
    'input[name="selected_people"]:checked'
  ).length;
  var selectedRecipientsCountText =
    "Selected recipients: " + selectedRecipientsCount;
  document.getElementById("selected_recipients_count").textContent =
    selectedRecipientsCountText;
}
