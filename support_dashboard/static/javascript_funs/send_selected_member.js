console.log("calling");

document.addEventListener("DOMContentLoaded", function () {
  const createGroupBtn = document.querySelector("#create-group-btn");
  const selectedMembers = [];
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  createGroupBtn.addEventListener("click", function () {
    const checkboxes = document.querySelectorAll(
      'input[name="selected_members"]'
    );

    for (let i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i].checked) {
        selectedMembers.push(checkboxes[i].value);
      }
    }

    console.log(selectedMembers);

    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    for (let i = 0; i < selectedMembers.length; i++) {
      formData.append("selected_members", selectedMembers[i]);
    }
    formData.append("action", "create_group");

    xhr.open("POST", "settings_fun_calls", true);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.send(formData);
  });
});
