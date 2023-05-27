console.log("js for get pipeline detail loaded");

function create_table_ui(srcObjects, div_path, table_name) {
  // Create the table with checkboxes for src_objects
  var tableContainer = $("<div class='col-12'></div>").addClass(
    "table table-bordered-custom"
  );
  var tableResponsive = $("<div class='table-responsive'></div>").css({
    "max-height": "200px",
    "overflow-y": "auto",
  });
  var table = $(
    "<table class='table table-striped table-hover table-sm'></table>"
  ).css("width", "300px"); // Set the desired width

  var thead = $("<thead></thead>").append(
    $("<tr></tr>").append($("<th></th>"), $("<th></th>").text(table_name))
  );

  var tbody = $("<tbody></tbody>");

  for (var i = 0; i < srcObjects.length; i++) {
    var object = srcObjects[i];
    var checkbox = $("<input type='checkbox'>")
      .attr("name", "selected_objects")
      .val(object);
    var row = $("<tr></tr>");
    var selectCell = $("<td></td>").append(checkbox);
    var nameCell = $("<td></td>").text(object);

    row.append(selectCell);
    row.append(nameCell);
    tbody.append(row);
  }

  table.append(thead);
  table.append(tbody);
  tableResponsive.append(table);
  tableContainer.append(tableResponsive);

  // Update the result container with the generated HTML
  console.log(tableContainer);
  $(div_path).empty();
  $(div_path).append(tableContainer);
}

$(document).ready(function () {
  $("#dashboard-form").on("submit", function (event) {
    console.log("calling pipeline button");
    event.preventDefault(); // Prevent form submission

    // Retrieve CSRF token from the form
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Retrieve form data
    var formData = $(this).serialize() + "&action=get_tables";

    // console.log(formData);

    // Send AJAX request to your Django view
    $.ajax({
      url: pipelineDetailUrl, // Use the variable here
      type: "POST",
      data: formData,
      headers: {
        "X-CSRFToken": csrfToken,
      },
      // var srcObjects = response.src_objects;
      // var destObjects = response.dest_objects;
      success: function (response) {
        var srcObjects = [
          "dept_emp",
          "dept_manager",
          "departments",
          "shivanshu_fruit",
          "test_data_nifi",
          "man_snap_metros",
          "check_snap_schema_regions",
          "regions",
        ];
        var destObjects = [
          "hack_employees",
          "hack_dept_emp",
          "hack_titles",
          "hack_departments",
          "hack_shivanshu_fruit",
        ];
        $(document).ready(function () {
          create_table_ui(srcObjects, "#result-container-1", "Source Tables");
          create_table_ui(
            destObjects,
            "#result-container-2",
            "Destination Tables"
          );
          document.getElementById("submit-tables").style.display = "block";
        });
      },
      error: function (xhr, status, error) {
        console.log(error);
      },
    });
  });
});

$(document).ready(function () {
  // Button click event
  $("#submit-tables").click(function () {
    console.log("calling table button");
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    // Get the selected checked tables
    // var selectedTables = $("input[name='selected_objects']:checked")
    //   .map(function () {
    //     return $(this).val();
    //   })
    //   .get();

    var selected_sources = $("#" + "result-container-1")
      .find("input[name='selected_objects']:checked")
      .map(function () {
        return $(this).val();
      })
      .get();

    var selected_destinations = $("#" + "result-container-2")
      .find("input[name='selected_objects']:checked")
      .map(function () {
        return $(this).val();
      })
      .get();

    console.log(selected_sources);
    console.log(selected_destinations);

    // AJAX request
    $.ajax({
      url: pipelineDetailUrl, // Replace with your server-side view URL
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      data: {
        selected_sources: selected_sources,
        selected_destinations: selected_destinations,
        action: "get_internal_data",
      },
      success: function (response) {
        // Handle the success response
        console.log(response);
      },
      error: function (xhr, status, error) {
        // Handle the error
        console.log(error);
      },
    });
  });
});
