console.log("js for get pipeline detail loaded");

$(document).ready(function () {
  $("#dashboard-form").on("submit", function (event) {
    event.preventDefault(); // Prevent form submission

    // Retrieve CSRF token from the form
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Retrieve form data
    var formData = $(this).serialize();
    console.log("I'm in ajax");
    console.log(formData);

    // Send AJAX request to your Django view
    $.ajax({
      url: pipelineDetailUrl, // Use the variable here
      type: "POST",
      data: formData,
      headers: {
        "X-CSRFToken": csrfToken,
      },
      success: function (response) {
        // Update the HTML content in the result container
        console.log(response);
        $("#result-container").html(response);
      },
      error: function (xhr, status, error) {
        console.log(error);
      },
    });
  });
});
