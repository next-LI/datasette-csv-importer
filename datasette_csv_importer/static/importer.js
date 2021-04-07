const fileForm = document.getElementById("file-form");
const fileInput = document.getElementsByName("csv")[0];
const dropArea = document.getElementById("file-drop");
const progress = document.getElementsByTagName("progress")[0];
const progressLabel = document.getElementById("progress-label");
const label = dropArea.getElementsByTagName("label")[0];
const configForm = document.getElementById("import-config");
const completedDiv = document.getElementById("completed");
const end_area = {
  short_txt: document.querySelector("#completed .result-short"),
  full_txt: document.querySelector("#completed .result-text"),
  output: document.querySelector("#completed .output"),
};

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
  console.log("last_status", last_status);
  completedDiv.style.display = "block";
  configForm.style.display = "none";
  if (status_code !== 200) {
    end_area.short_txt.innerText = "Failure";
    end_area.full_txt.innerText = `Server error: ${status_code}`;
  } else {
    end_area.short_txt.innerText = last_status.exitcode ? "Failure": "Success";
    end_area.full_txt.innerText = last_status.message;
    end_area.output.innerText = last_status.output;
    end_area.output.style.display = "block";
  }
}

/* {url: "/test.csv", status_database_path: "_internal", task_id: "e6dd81b4-fe1a-4f88-8d66-f1f9239ce0f6"} */
async function poll(response_data) {
  console.log("Upload Response Data", response_data);
  const task_id = response_data.task_id;
  const status_database_path = response_data.status_database_path;
  const status_url = `/${status_database_path}/_csv_importer_progress_.json?id=${task_id}&_shape=array`;

  show_progress_screen();

  let status_code = 200;
  let completed = false;
  let last_status = {};
  while (status_code === 200 && !completed) {
    try {
      let status_resp = await fetch(status_url);
      status_code = status_resp.status;

      let recs = await status_resp.json();
      last_status = recs[0];
      completed = last_status;
    } catch(e) {
      // failure!
      break;
    }
    update_progress_screen(last_status);
    await sleep(1000);
  }
  window.sleep = sleep;
  // last_status = [{
  //   "id": "c6c5353a-cff6-48db-a688-68e677747ac8",
  //   "filename": "test.csv",
  //   "dbname": "test",
  //   "started": "2021-04-07 04:29:41.145045",
  //   "completed": "2021-04-07 04:29:41.157599",
  //   "exitcode": 0,
  //   "status": "completed",
  //   "message": "Import successful!"}]
  show_end_screen(status_code, last_status);
}

// watches for a success or failure on our file upload
function fileUploadStateChange(xhr, res, rej, e) {
  if (xhr.readyState == 4 && xhr.status == 200) {
    const data = JSON.parse(xhr.responseText);
    return res(data);
  } else if (xhr.readyState == 4 && xhr.status != 200) {
    return rej({
      status: xhr.status,
      data: xhr.responseText,
    });
  }
}

function uploadFile(file, options) {
  console.log("uploadFile file", file, "options", options);
  return new Promise((res, rej) => {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    xhr.open("POST", fileInput.form.action, true);
    xhr.addEventListener("readystatechange", fileUploadStateChange.bind(this, xhr, res, rej));
    formData.append("xhr", "1");
    formData.append("csrftoken", get_csrftoken());
    /*
    Object.entries(options).forEach((key, value) => {
      formData.append(key, value);
    });
    */
    formData.append("csv", file);
    xhr.send(formData);
  });
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
      console.log("options", options);
      uploadFile(file, options).then(poll);
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
