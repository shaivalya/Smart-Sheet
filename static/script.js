document.getElementById("upload-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "";

    if (data.status === "success") {
        resultDiv.innerHTML = `
            <h3 style='color:green'>✅ All Good! No Errors Found.</h3>
            <a href="/edit"><button>🔧 Edit Anyway</button></a>
        `;
    } else {
        resultDiv.innerHTML = `
            <h3 style='color:red'>❌ Validation Errors Found:</h3>
            <ul>${data.errors.map(e => `<li>${e}</li>`).join("")}</ul>
            <a href="/edit"><button>✏️ Fix Errors Now</button></a>
        `;
    }
});
