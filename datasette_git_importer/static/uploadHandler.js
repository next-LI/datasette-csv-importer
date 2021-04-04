var fileInput = document.getElementsByName("csv")[0];
var dropArea = document.getElementById("file-drop");
var progress = document.getElementsByTagName("progress")[0];
var progressLabel = document.getElementById("progress-label");
var label = dropArea.getElementsByTagName("label")[0];

//progress.style.display = "none";
fileInput.addEventListener("change", () => {
  uploadFile(fileInput.files[0]);
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
    uploadFile(e.dataTransfer.files[0]);
  },
  false
);

function uploadFile(file) {
  label.innerText = file.name;
  var xhr = new XMLHttpRequest();
  var formData = new FormData();
  dropArea.style.display = "none";
  progressLabel.style.display = "block";
  xhr.open("POST", fileInput.form.action, true);

  // Add following event listener
  xhr.upload.addEventListener("progress", function(e) {
    console.log("progress", e);
    progress.value = ((e.loaded * 100.0) / e.total || 100) * 0.2;
  });
  progress.style.display = "block";

  setTimeout(() => {
    progress.value = Number.parseInt(progress.value) + 20;
  }, 20000);


  xhr.addEventListener("readystatechange", function(e) {
    console.log("readystatechange", xhr.status);
    if (xhr.readyState == 4 && xhr.status == 200) {
      // get the task_id so we can fetch progress
      var data = JSON.parse(xhr.responseText);
      var task_id = data.task_id;
      console.log("data", data);
      // Show server-side processing progress bar
      progressLabel.innerHTML = "Uploading...";
      var params = `id=${task_id}&_shape=array`;
      var url = `/-/git-importer/${task_id}`;
      var status;
      function pollForProgress() {
        console.log(`Fetching ${url}`);
        fetch(url).then(d => d.json()).then((run) => {
          console.log("run", run);
          if (!run || !run.status) {
            console.log("Bad run response, waiting then trying again")
            return setTimeout(pollForProgress, 1000);
          }
          progressLabel.innerHtml = run.status;
          console.log("xhr.responseText", xhr.responseText);
          if (status !== run.status) {
            if (status !== null) {
              progress.value = Number.parseInt(progress.value) + 20;
            }
            status = run.status;
          }
          if (run.status == "completed") {
            progressLabel.innerHTML = `Complete! ${run.status} ${run.conclusion}`;
            // document.location = JSON.parse(xhr.responseText).url;
            progress.value = 100;
          } else {
            setTimeout(pollForProgress, 1000);
          }
        }).catch((e) => {
          console.log("Error polling", e);
          /*setTimeout(pollForProgress, 1000);*/
          if (e.message.startsWith("JSON.parse")) {
            document.location = data.url;
          }
        });
        /* TODO: catch error above */
      }
      pollForProgress();
    } else if (xhr.readyState == 4 && xhr.status != 200) {
      console.error("Error!", xhr.status, xhr.responseText);
    }
  });

  formData.append("xhr", "1");
  formData.append("csrftoken", "{{ csrftoken() }}");
  formData.append("csv", file);
  xhr.send(formData);
}

