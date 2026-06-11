async function uploadFiles() {
  const input = document.getElementById("fileInput");
  const files = input.files;

  if (files.length === 0) {
    alert("Please select files first!");
    return;
  }

  const formData = new FormData();
  for (const file of files) {
    formData.append("files", file);
  }

  document.getElementById("status").innerText = "Uploading and processsing...";

  try {
    const response = await fetch("http://127.0.0.1:8000/upload-papers/", {
      method: "POST",
      body: formData,
    });

    console.log(response.status);

    const result = await response.json();
    console.log(result);
    document.getElementById("status").innerText = result.message + "Check you terminal";
  } catch (error) {
    console.error(error)
    document.getElementById("status").innerText = "Error uploading files: \n" + error.message;
  }
}
