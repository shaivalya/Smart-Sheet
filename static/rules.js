let rules = [];

function addRule() {
  const rule = {
    type: "slot_limit", // default
    target: "",
    limit: 1
  };
  rules.push(rule);
  renderRules();
}

function renderRules() {
  const container = document.getElementById("rules-container");
  container.innerHTML = '';
  rules.forEach((rule, index) => {
    container.innerHTML += `
      <div>
        <select onchange="updateRuleType(${index}, this.value)">
          <option value="slot_limit">slot_limit</option>
          <option value="co_run">co_run</option>
          <option value="regex_task_name">regex_task_name</option>
        </select>
        <input placeholder="target or pattern" onchange="updateRuleField(${index}, this.value)" />
      </div>
    `;
  });
}

function updateRuleType(index, value) {
  rules[index].type = value;
}

function updateRuleField(index, value) {
  if (rules[index].type === "slot_limit") rules[index].target = value;
  if (rules[index].type === "regex_task_name") rules[index].pattern = value;
  if (rules[index].type === "co_run") rules[index].tasks = value.split(",");
}

function saveRules() {
  const weights = {
    slot_limit: parseInt(document.getElementById("weight-slot_limit").value || 1),
    co_run: parseInt(document.getElementById("weight-co_run").value || 1),
    regex_task_name: parseInt(document.getElementById("weight-regex_task_name").value || 1)
  };

  fetch('/save_rules', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ rules, weights })
  }).then(res => res.json()).then(data => {
    alert("Rules saved!");
  });
}
// static/rules.js
window.addEventListener("DOMContentLoaded", () => {
  fetch("/load_rules")
    .then((res) => res.json())
    .then((data) => {
      const ruleList = document.getElementById("rule-list");
      if (!ruleList) return console.error("rule-list element not found!");
      ruleList.innerHTML = "";

      data.rules.forEach((rule, index) => {
        const li = document.createElement("li");
        li.textContent = `${index + 1}. ${JSON.stringify(rule)}`;
        ruleList.appendChild(li);
      });
    })
    .catch((err) => console.error("Error loading rules:", err));
});
function saveRules(rules) {
  fetch("/save_rules", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rules: rules })
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === "success") {
        alert("Rules saved successfully!");
      }
    });
}


function renderRules(rules) {
  const list = document.getElementById("rule-list");
  list.innerHTML = "";

  if (rules.length === 0) {
    list.innerHTML = "<li>No rules defined yet.</li>";
    return;
  }

  rules.forEach(rule => {
    const li = document.createElement("li");

    switch (rule.type) {
      case "coRun":
        li.textContent = `Co-run: ${rule.tasks.join(", ")}`;
        break;
      case "slotRestriction":
        li.textContent = `Slot Restriction: Group ${rule.group} → Min ${rule.minCommonSlots} slots`;
        break;
      case "loadLimit":
        li.textContent = `Load Limit: Worker Group ${rule.group} → Max ${rule.maxSlotsPerPhase} slots/phase`;
        break;
      case "phaseWindow":
        li.textContent = `Phase Window: Task ${rule.task} → Phases ${rule.allowedPhases.join(", ")}`;
        break;
      case "patternMatch":
        li.textContent = `Regex Rule: Pattern "${rule.regex}" → ${rule.template} (${JSON.stringify(rule.parameters)})`;
        break;
      default:
        li.textContent = `Unknown rule: ${JSON.stringify(rule)}`;
    }

    list.appendChild(li);
  });
}
function convertNLToRule() {
  const input = document.getElementById("nl-rule").value;

  fetch("/nl_to_rule", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: input })
  })
  .then(res => res.json())
  .then(data => {
    if (data.rule) {
      document.getElementById("nl-rule-result").innerText = "✔ Rule parsed and added!";
      addRule(data.rule);  // Optional: Immediately add to UI
    } else {
      document.getElementById("nl-rule-result").innerText = "❌ Couldn't understand the rule.";
    }
  });
}
