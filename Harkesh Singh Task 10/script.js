// Address of your FastAPI server. Change this after you deploy the API.
const API_URL = "http://127.0.0.1:8000";

// Dropdown choices (the same categories the model was trained on)
const options = {
  "workclass": ["Federal-gov", "Local-gov", "Never-worked", "Private", "Self-emp-inc", "Self-emp-not-inc", "State-gov", "Unknown", "Without-pay"],
  "education": ["Preschool", "1st-4th", "5th-6th", "7th-8th", "9th", "10th", "11th", "12th", "HS-grad", "Some-college", "Assoc-voc", "Assoc-acdm", "Bachelors", "Masters", "Prof-school", "Doctorate"],
  "marital_status": ["Divorced", "Married-AF-spouse", "Married-civ-spouse", "Married-spouse-absent", "Never-married", "Separated", "Widowed"],
  "occupation": ["Adm-clerical", "Armed-Forces", "Craft-repair", "Exec-managerial", "Farming-fishing", "Handlers-cleaners", "Machine-op-inspct", "Other-service", "Priv-house-serv", "Prof-specialty", "Protective-serv", "Sales", "Tech-support", "Transport-moving", "Unknown"],
  "relationship": ["Husband", "Not-in-family", "Other-relative", "Own-child", "Unmarried", "Wife"],
  "race": ["Amer-Indian-Eskimo", "Asian-Pac-Islander", "Black", "Other", "White"],
  "sex": ["Female", "Male"],
  "native_country": ["Cambodia", "Canada", "China", "Columbia", "Cuba", "Dominican-Republic", "Ecuador", "El-Salvador", "England", "France", "Germany", "Greece", "Guatemala", "Haiti", "Holand-Netherlands", "Honduras", "Hong", "Hungary", "India", "Iran", "Ireland", "Italy", "Jamaica", "Japan", "Laos", "Mexico", "Nicaragua", "Outlying-US(Guam-USVI-etc)", "Peru", "Philippines", "Poland", "Portugal", "Puerto-Rico", "Scotland", "South", "Taiwan", "Thailand", "Trinadad&Tobago", "United-States", "Unknown", "Vietnam", "Yugoslavia"]
};

// The model needs the education level as a number as well
const educationNum = {
  "Preschool": 1, "1st-4th": 2, "5th-6th": 3, "7th-8th": 4, "9th": 5, "10th": 6,
  "11th": 7, "12th": 8, "HS-grad": 9, "Some-college": 10, "Assoc-voc": 11,
  "Assoc-acdm": 12, "Bachelors": 13, "Masters": 14, "Prof-school": 15, "Doctorate": 16
};

// Starting values shown in the form
const defaults = {
  age: 39,
  workclass: "Private",
  fnlwgt: 189778,
  education: "Bachelors",
  marital_status: "Never-married",
  occupation: "Adm-clerical",
  relationship: "Not-in-family",
  race: "White",
  sex: "Male",
  capital_gain: 0,
  capital_loss: 0,
  hours_per_week: 40,
  native_country: "United-States"
};

const form = document.getElementById("predict-form");
const submitBtn = document.getElementById("submit-btn");
const resultBox = document.getElementById("result");
const resultLabel = document.getElementById("result-label");
const resultDetail = document.getElementById("result-detail");
const barFill = document.getElementById("bar-fill");
const errorBox = document.getElementById("error");
const statusBox = document.getElementById("status");
const statusText = document.getElementById("status-text");

// 1) Fill the dropdowns
for (const field in options) {
  const select = document.getElementById(field);
  options[field].forEach(function (value) {
    const opt = document.createElement("option");
    opt.value = value;
    opt.textContent = value;
    select.appendChild(opt);
  });
}

// 2) Fill the starting values
for (const field in defaults) {
  document.getElementById(field).value = defaults[field];
}

// 3) Check whether the API is running
async function checkApi() {
  try {
    const response = await fetch(API_URL + "/");
    if (!response.ok) throw new Error("bad status");
    statusBox.className = "status online";
    statusText.textContent = "API online";
  } catch (err) {
    statusBox.className = "status offline";
    statusText.textContent = "API offline - start it with: uvicorn main:app --reload";
  }
}
checkApi();

// 4) Send the form to the API
form.addEventListener("submit", async function (event) {
  event.preventDefault();
  errorBox.hidden = true;
  resultBox.hidden = true;

  // Names here must match the fields of the Person class in main.py
  const person = {
    age: Number(document.getElementById("age").value),
    workclass: document.getElementById("workclass").value,
    fnlwgt: Number(document.getElementById("fnlwgt").value),
    education: document.getElementById("education").value,
    education_num: educationNum[document.getElementById("education").value],
    marital_status: document.getElementById("marital_status").value,
    occupation: document.getElementById("occupation").value,
    relationship: document.getElementById("relationship").value,
    race: document.getElementById("race").value,
    sex: document.getElementById("sex").value,
    capital_gain: Number(document.getElementById("capital_gain").value),
    capital_loss: Number(document.getElementById("capital_loss").value),
    hours_per_week: Number(document.getElementById("hours_per_week").value),
    native_country: document.getElementById("native_country").value
  };

  submitBtn.disabled = true;
  submitBtn.textContent = "Predicting...";

  try {
    const response = await fetch(API_URL + "/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(person)
    });

    if (!response.ok) {
      throw new Error("The API returned an error (status " + response.status + ").");
    }

    const data = await response.json();
    showResult(data);
  } catch (err) {
    errorBox.textContent = err instanceof TypeError
      ? "Could not reach the API at " + API_URL + ". Is the server running?"
      : err.message;
    errorBox.hidden = false;
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Predict income";
  }
});

// 5) Show the answer
function showResult(data) {
  const percent = Math.round(data.probability_above_50k * 100);
  const isHigh = data.prediction === ">50K";

  resultBox.className = "result " + (isHigh ? "high" : "low");
  resultLabel.textContent = isHigh
    ? "Likely earns more than $50K per year"
    : "Likely earns $50K or less per year";
  resultDetail.textContent = "Chance of earning more than $50K: " + percent + "%";
  barFill.style.width = percent + "%";
  resultBox.hidden = false;
}
