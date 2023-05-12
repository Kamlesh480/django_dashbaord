// get the Cancel button
console.log("in js code");
const cancelButton = document.querySelector("#cancel-btn");

// add a click event listener to the Cancel button
cancelButton.addEventListener("click", () => {
  // find all the checkboxes inside the table
  console.log("on click");
  const checkboxes = document.querySelectorAll(
    '#member-table tbody input[type="checkbox"]'
  );

  // uncheck all the checkboxes that were previously checked
  checkboxes.forEach((checkbox) => {
    checkbox.checked = false;
  });
});
