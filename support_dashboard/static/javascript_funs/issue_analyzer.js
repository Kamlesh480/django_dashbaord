console.log("js for get pipeline detail loaded");

function create_table_ui(srcObjects, div_path, table_name) {
  // Create the table with checkboxes for src_objects
  var tableContainer = $("<div class='col-12'></div>").addClass(
    "table table-bordered-custom"
  );
  var tableResponsive = $("<div class='table-responsive'></div>").css({
    "max-height": "180px",
    "overflow-y": "auto",
  });
  var table = $(
    "<table class='table table-striped table-hover table-sm'></table>"
  ).css("width", "220px"); // Set the desired width

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

function create_table_ui_json(data, div_path, table_name) {
  // Create the table for data objects
  var tableContainer = $("<div></div>").addClass("table-responsive").css({
    "max-height": "180px",
    "overflow-y": "auto",
  });
  var table = $("<table></table>")
    .addClass("table table-striped table-hover table-sm")
    .css("width", "200px");

  var thead = $("<thead></thead>").append(
    $("<tr></tr>").append($("<th></th>").text(table_name))
  );

  var tbody = $("<tbody></tbody>");

  // Extract column names from the first object
  var columnNames = [];
  var firstObject = data[0];
  for (var key in firstObject) {
    if (firstObject.hasOwnProperty(key)) {
      columnNames.push(key);
    }
  }

  // Create column headers
  var headerRow = $("<tr></tr>");
  for (var i = 0; i < columnNames.length; i++) {
    var columnName = columnNames[i];
    headerRow.append($("<th></th>").text(columnName));
  }
  thead.append(headerRow);

  // Create rows and populate data
  for (var j = 0; j < data.length; j++) {
    var object = data[j];
    var row = $("<tr></tr>");

    for (var k = 0; k < columnNames.length; k++) {
      var columnName = columnNames[k];
      var columnValue = object[columnName];

      if (columnValue === null) {
        columnValue = "NULL";
      }

      var cell = $("<td></td>").text(columnValue);
      row.append(cell);
    }

    tbody.append(row);
  }

  table.append(thead);
  table.append(tbody);
  tableContainer.append(table);

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
      //   var srcObjects = response.src_objects;
      //   var destObjects = response.dest_objects;
      success: function (response) {
        var srcObjects = response.src_objects;
        var destObjects = response.dest_objects;
        console.log(srcObjects);
        console.log(destObjects);
        // var srcObjects = [
        //   "dept_emp",
        //   "dept_manager",
        //   "departments",
        //   "shivanshu_fruit",
        //   "test_data_nifi",
        //   "man_snap_metros",
        //   "check_snap_schema_regions",
        //   "regions",
        // ];
        // var destObjects = [
        //   "hack_employees",
        //   "hack_dept_emp",
        //   "hack_titles",
        //   "hack_departments",
        //   "hack_shivanshu_fruit",
        // ];
        $(document).ready(function () {
          create_table_ui(srcObjects, "#result-container-1", "Source Tables");
          create_table_ui(
            destObjects,
            "#result-container-2",
            "Destination Tables"
          );
          document.getElementById("submit-tables").style.display = "block";
          document.getElementById("result-container-3").style.display = "block";
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

    var pipelineNumber = $('input[name="pipelineNumber"]').val();
    var cluster = $('select[name="cluster"]').val();
    var accountName = $('input[name="accountName"]').val();
    // console.log(pipelineNumber);
    // console.log(cluster);
    // console.log(accountName);

    var checkboxes = $('input[type="checkbox"]');
    var data = {};

    checkboxes.each(function () {
      var name = $(this).attr("name");
      var value = $(this).is(":checked");
      data[name] = value;
    });

    console.log(data);

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
        pipelineNumber: pipelineNumber,
        cluster: cluster,
        accountName: accountName,
      },
      success: function (response) {
        var connector_task = response.connector_task;
        var handyman_connector_poll = response.handyman_connector_poll;
        var handyman_copy_job = response.handyman_copy_job;
        // console.log(srcObjects);
        // console.log(destObjects);
        // var sideline = [
        //   {
        //     schema_name: "dept",
        //     stage: "MAPPER",
        //     reason: null,
        //     total_records: 10,
        //     status: "UPLOADED",
        //     code: 300,
        //     params: null,
        //   },
        //   {
        //     schema_name: "ping",
        //     stage: "MAPPER",
        //     reason: null,
        //     total_records: 10,
        //     status: "UPLOADED",
        //     code: 301,
        //     params: null,
        //   },
        //   {
        //     schema_name: "ping",
        //     stage: "MAPPER",
        //     reason: null,
        //     total_records: 10,
        //     status: "UPLOADED",
        //     code: 301,
        //     params: null,
        //   },
        //   {
        //     schema_name: "ping",
        //     stage: "MAPPER",
        //     reason: null,
        //     total_records: 10,
        //     status: "UPLOADED",
        //     code: 301,
        //     params: null,
        //   },
        //   {
        //     schema_name: "ping",
        //     stage: "MAPPER",
        //     reason: null,
        //     total_records: 10,
        //     status: "UPLOADED",
        //     code: 301,
        //     params: null,
        //   },
        //   {
        //     schema_name: "ping",
        //     stage: "MAPPER",
        //     reason: null,
        //     total_records: 10,
        //     status: "UPLOADED",
        //     code: 301,
        //     params: null,
        //   },
        //   {
        //     schema_name: "ping",
        //     stage: "MAPPER",
        //     reason: null,
        //     total_records: 10,
        //     status: "UPLOADED",
        //     code: 301,
        //     params: null,
        //   },
        // ];
        create_table_ui_json(connector_task, "#place-1", "connector_task");
        create_table_ui_json(
          handyman_connector_poll,
          "#place-2",
          "handyman_connector_poll"
        );
        create_table_ui_json(
          handyman_copy_job,
          "#place-3",
          "handyman_copy_job"
        );
      },
      error: function (xhr, status, error) {
        // Handle the error
        console.log(error);
      },
    });
  });
});
