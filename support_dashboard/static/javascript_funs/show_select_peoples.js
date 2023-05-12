function updateSelectedRecipients() {
  var selectedRecipients = document.querySelectorAll(
    'input[name="selected_people"]:checked'
  );
  var selectedRecipientsList = document.getElementById("selected_recipients");
  selectedRecipientsList.innerHTML = "";
  selectedRecipients.forEach(function (recipient) {
    var recipientName = recipient.value;
    var listItem = document.createElement("li");
    listItem.textContent = recipientName;
    selectedRecipientsList.appendChild(listItem);
  });
}
