function send_selected_members() {
  document.addEventListener("DOMContentLoaded", function () {
    const createGroupBtn = document.querySelector("#create-group-btn");
    const selectedMembers = [];
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;

    const groupNameInput = document.querySelector("#group_name");

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
      console.log(groupNameInput.value);

      if (selectedMembers.length === 0) {
        window.alert("You have not selected any members.");
        return;
      }

      const xhr = new XMLHttpRequest();
      const formData = new FormData();
      for (let i = 0; i < selectedMembers.length; i++) {
        formData.append("selected_members", selectedMembers[i]);
      }
      formData.append("group_name", groupNameInput.value);
      formData.append("action", "create_group");

      xhr.open("POST", "settings_fun_calls", true);
      xhr.setRequestHeader("X-CSRFToken", csrfToken);
      xhr.send(formData);

      // Refresh the page
      window.alert("New Group created");
      cancel_selected_members();
      // Refresh the page by replacing the URL with itself
      window.location.replace(window.location.href);
    });
  });
}

function cancel_selected_members() {
  // find all the checkboxes inside the table
  console.log("on click");
  const checkboxes = document.querySelectorAll(
    '#member-table tbody input[type="checkbox"]'
  );

  // uncheck all the checkboxes that were previously checked
  checkboxes.forEach((checkbox) => {
    checkbox.checked = false;
  });

  document.querySelector("#group_name").value = "";
}

function enable_group_button() {
  const groupNameInput = document.querySelector("#group_name");
  const createGroupBtn = document.querySelector("#create-group-btn");

  groupNameInput.addEventListener("input", () => {
    if (groupNameInput.value !== "") {
      createGroupBtn.disabled = false;
    } else {
      createGroupBtn.disabled = true;
    }
  });
}
