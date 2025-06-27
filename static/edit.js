document.getElementById("edit-form").addEventListener("submit", function (e) {
  e.preventDefault(); // Stop normal form submission

  const tables = {};
  const allTables = document.querySelectorAll("table");

  allTables.forEach(table => {
    const title = table.previousElementSibling.innerText.replace(" Table", "");
    const headers = Array.from(table.querySelectorAll("thead th")).map(th => th.innerText);
    const rows = table.querySelectorAll("tbody tr");

    const data = [];
    rows.forEach(row => {
      const rowData = {};
      const inputs = row.querySelectorAll("input");
      inputs.forEach((input, index) => {
        rowData[headers[index]] = input.value;
      });
      data.push(rowData);
    });

    tables[title.toLowerCase()] = data; // keys: "clients", "tasks", "workers"
  });

  fetch("/save_edits", {
    method: "POST",
    body: JSON.stringify(tables),
    headers: {
      "Content-Type": "application/json"
    }
  })
    .then(response => response.json())
    .then(result => {
      document.getElementById("result").innerText = result.message;
    })
    .catch(error => {
      document.getElementById("result").innerText = "❌ Failed to save: " + error;
    });
});
