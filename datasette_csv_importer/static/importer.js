const fileForm = document.getElementById("file-form");
const fileInput = document.getElementsByName("csv")[0];
const dropArea = document.getElementById("file-drop");
const progress = document.getElementsByTagName("progress")[0];
const progressLabel = document.getElementById("progress-label");
const label = dropArea.getElementsByTagName("label")[0];
const configForm = document.getElementById("import-config");
const progressDiv = document.getElementById("progress");
const completedDiv = document.getElementById("completed");
const end_area = {
  short_txt: document.querySelector("#completed .result-short"),
  full_txt: document.querySelector("#completed .result-text"),
  output: document.querySelector("#completed .output"),
  db_link: document.querySelector("#to-db")
};
const POLL_SECONDS = 5000;

function get_csrftoken() {
  return document.querySelector('input[name="csrftoken"]').value;
}

function sleep(milliseconds) {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

function startOver() {
  dropArea.style.display = "none";
  configForm.style.display = "block";
  completedDiv.style.display = "none";
}

function show_end_screen(status_code, last_status) {
  console.log("End status", status_code, last_status);
  progressDiv.style.display = "none";
  completedDiv.style.display = "block";
  if (status_code !== 200) {
    end_area.short_txt.innerText = "Failure";
    if (last_status && last_status.message) {
      end_area.full_txt.innerText = `Server error: ${last_status.message}`;
    } else {
      end_area.full_txt.innerText = `Server error: ${status_code}`;
    }
  } else if (!!last_status.exitcode) {
    end_area.short_txt.innerText = "Failure";
    end_area.full_txt.innerText = last_status.message;
  } else {
    end_area.short_txt.innerText = "Success";
    end_area.full_txt.innerText = last_status.message;
    end_area.output.innerText = last_status.output;
    end_area.output.style.display = "block";
    end_area.db_link.setAttribute("href", `/${last_status.dbname}`);
    end_area.db_link.innerText = "Click here to go to imported database →";
    end_area.db_link.style.display = "block";
  }
}

function show_progress_screen() {
  progressDiv.style.display = "block";
  configForm.style.display = "none";
}

function update_progress_screen(last_status) {
  console.log("Status", last_status);
  document.querySelector("#progress .status-message").innerText = last_status.message;
}

/**
 * Gets the datasette "base_url" setting, which is actually
 * not a URL, but a path prefix, e.g., /datasette
 */
function get_base_url() {
  return window.DATASETTE_BASE_URL;
}

/* {url: "/test.csv", status_database_path: "_internal", task_id: "e6dd81b4-fe1a-4f88-8d66-f1f9239ce0f6"} */
function poll(response_data, remaining_failures=30) {
  console.log("Upload Response Data", response_data);
  const status_database_path = response_data.status_database_path;
  const status_table = response_data.status_table;
  const task_id = response_data.task_id;
  const base_url = get_base_url();
  const status_url = `${base_url}/-/csv-importer/${task_id}`;
  console.log("fetching status_url", status_url);
  fetch(status_url).then((r) => r.json()).then((status) => {
    console.log("poll status", status);
    update_progress_screen(status);
    if (status.completed) show_end_screen(200, status);
    else setTimeout(poll.bind(this, response_data), POLL_SECONDS);
  }).catch((e) => {
    if (!remaining_failures--) {
      show_end_screen(500, {
        message: e
      });
    }
    setTimeout(poll.bind(this, response_data), POLL_SECONDS);
  });
}

function uploadFile(file, options, cb) {
  update_progress_screen({
    "message": "Preparing for upload...",
  });
  show_progress_screen();

  const formData = new FormData();
  formData.append("xhr", "1");
  formData.append("csrftoken", get_csrftoken());
  formData.append("csv", file);
	Object.entries(options).forEach(([key, value], ix) => {
		/* these don't take arguments, they are flag-only cli args */
		if (value === true) {
			formData.append(key, true);
		}
		/* false means the firld was left blank, if it's not false then
			* we have an argument with a value! add both.
			*/
		else if (value !== false) {
			formData.append(key, value);
		}
	});

  const xhr = new XMLHttpRequest();

  xhr.upload.addEventListener("progress", (e) => {
    const pct_done = ((e.loaded * 100.0) / e.total || 100.0).toFixed(1);
		update_progress_screen({
			"message": `Uploading file (${pct_done}% done)`,
		});
  });

	xhr.addEventListener("readystatechange", (e) => {
    console.log("readystatechange xhr.readyState", xhr.readyState, "xhr.status", xhr.status);
    console.log("XMLHttpRequest.DONE", XMLHttpRequest.DONE);
		if (xhr.readyState !== XMLHttpRequest.DONE) return;
		if (xhr.status !== 200) {
      return show_end_screen(xhr.status);
    }
    const data = JSON.parse(xhr.responseText);
    // Show server-side processing progress bar
    update_progress_screen({
			"message": "Fetching initial CSV upload status...",
		});

    console.log("Calling cb");
    cb(data);
  });

  xhr.open("POST", fileInput.form.action, true);
  xhr.send(formData);
}

/**
 * This pulls the JSON that we're storing as schema.json
 */
function getSchema() {
  return JSON.parse(document.getElementById('schema').innerHTML);
}

/**
 * This handles a file selected/dropped. From here, we
 * render the JSON schema form builder and setup the
 * final submit button callback to `uploadFile`.
 */
async function handleFile(file) {
  console.log("Handling file", file);
  const schema = getSchema();
  console.log("schema", schema);
  $('form#import-config').jsonForm({
    "schema": schema,
    "value": {
      "--table": file.name.replace(".csv", ""),
    },
    "onSubmitValid": function (options) {
      console.log("Submitting...");
      console.log("options", options);
      uploadFile(file, options, poll);
    },
  });
  dropArea.style.display = "none";
}

function setupFileHandler() {
  console.log("Setting up file handler");
  fileInput.addEventListener("change", () => {
    handleFile(fileInput.files[0]);
  });
  ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
    dropArea.addEventListener(
      eventName,
      e => {
        e.preventDefault();
        e.stopPropagation();
      },
      false
    );
  });
  ["dragenter", "dragover"].forEach(eventName => {
    dropArea.addEventListener(
      eventName,
      () => {
        dropArea.classList.add("highlight");
      },
      false
    );
  });
  ["dragleave", "drop"].forEach(eventName => {
    dropArea.addEventListener(
      eventName,
      () => {
        dropArea.classList.remove("highlight");
      },
      false
    );
  });
  dropArea.addEventListener(
    "drop",
    e => {
      handleFile(e.dataTransfer.files[0]);
    },
    false
  );
}

setupFileHandler();
