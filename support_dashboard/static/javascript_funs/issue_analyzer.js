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
    .css("width", "500px");

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

function create_table_ui_json_button(data, div_path, table_name) {
  // Create the table for data objects
  var tableContainer = $("<div></div>").addClass("table-responsive").css({
    "max-height": "180px",
    "overflow-y": "auto",
  });
  var table = $("<table></table>")
    .addClass("table table-striped table-hover table-sm")
    .css("width", "500px");

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
  headerRow.append($("<th></th>").text("Actions")); // Add Actions column header
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

    // Create button for sending row data
    var button = $("<button></button>")
      .text("Replay")
      .addClass("btn btn-primary btn-sm");
    button.on("click", createRowDataHandler(object)); // Attach click event handler

    var actionCell = $("<td></td>").append(button);
    row.append(actionCell);

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

// // Function to handle button click and send row data to Django view
// function createRowDataHandler(rowData) {
//   return function () {
//     // Send rowData to Django view using Ajax or other method
//     console.log("Sending row data:", rowData);
//     // Add your code here to send the data to the Django view
//   };
// }

// Function to handle button click and send row data to Django view
function createRowDataHandler(rowData) {
  return function () {
    // Send rowData to Django view using Ajax
    console.log("Sending row data:", rowData);
    var pipelineNumber = $('input[name="pipelineNumber"]').val();

    // Get the CSRF token value
    var csrftoken = getCookie("csrftoken");

    // Prepare the data to send
    var data = {
      rowData: rowData,
      csrfmiddlewaretoken: csrftoken,
      action: "reply_sideline_file",
      pipelineNumber: pipelineNumber,
    };
    console.log(data);

    // Send the data using Ajax
    $.ajax({
      url: pipelineDetailUrl,
      type: "POST",
      data: data,

      success: function (response) {
        // Handle the success response from the Django view
        console.log("Data sent successfully");
        console.log("Response:", response);
      },
      error: function (xhr, status, error) {
        // Handle the error response
        console.error("Error:", error);
      },
    });
  };
}

// Function to get the value of the CSRF token cookie
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function transformKey(key) {
  // Split the key by underscores
  var words = key.split("_");

  // Join the words without spaces
  var transformedKey = words.join("");

  return transformedKey;
}
// Function to capitalize a word
function capitalize(word) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}

function createButtonsFromDict(dict1, dict2) {
  var placeDiv = document.getElementById("place-1");
  var placeDivforbutton = document.getElementById("place-3-1");

  // Create buttons from dict1
  // Create buttons from dict1
  for (var key in dict1) {
    if (dict1.hasOwnProperty(key)) {
      var transformedKey = transformKey(key); // Transform the key value

      var button = document.createElement("button");
      button.textContent = transformedKey;
      button.setAttribute("onclick", "openLink('" + dict1[key] + "')");
      button.classList.add("btn", "btn-primary", "m-2");

      placeDivforbutton.appendChild(button);
    }
  }

  // Display integration data from dict2
  var integrationDiv = document.createElement("div");
  integrationDiv.classList.add("mt-3");
  integrationDiv.style.padding = "10px"; // Add padding to the div

  var integrationText = "";

  for (var key in dict2) {
    if (dict2.hasOwnProperty(key)) {
      var value = dict2[key];
      if (typeof value === "object") {
        for (var prop in value) {
          if (value.hasOwnProperty(prop)) {
            integrationText += `${prop}: ${value[prop]}\n`;
          }
        }
      } else {
        integrationText += `${key}: ${value}\n`;
      }
    }
  }

  var integrationTextElement = document.createElement("pre");
  integrationTextElement.textContent = integrationText;
  integrationTextElement.style.fontSize = "small"; // Set the font size to small
  integrationDiv.appendChild(integrationTextElement);
  placeDiv.appendChild(integrationDiv);
}

function openLink(url) {
  // Open the link in a new tab/window
  window.open(url);
}

$(document).ready(function () {
  $("#dashboard-form").on("submit", function (event) {
    console.log("calling pipeline button");
    event.preventDefault();

    // Retrieve CSRF token from the form
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    var formData = $(this).serialize() + "&action=get_tables";
    // Send AJAX request to your Django view
    $.ajax({
      url: pipelineDetailUrl, // Use the variable here
      type: "POST",
      data: formData,
      headers: {
        "X-CSRFToken": csrfToken,
      },

      success: function (response) {
        var srcObjects = response.src_objects;
        var destObjects = response.dest_objects;
        console.log(srcObjects);
        console.log(destObjects);
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
        var sideline = response.sideline;
        var sink = response.sink;
        var integration = response.integration;
        var grafana = response.grafana;

        createButtonsFromDict(grafana, integration);

        create_table_ui_json(connector_task, "#place-2", "Connector Tasks");
        create_table_ui_json(handyman_connector_poll, "#place-3", "Poll Tasks");
        create_table_ui_json(
          handyman_copy_job,
          "#place-4",
          "Handyman Copy Jobs"
        );
        create_table_ui_json_button(sideline, "#place-5", "Sideline Files");
        create_table_ui_json(sink, "#place-6", "Sink Files");
      },
      error: function (xhr, status, error) {
        // Handle the error
        console.log(error);
      },
    });
  });
});
