const API = "http://127.0.0.1:8000";


// =======================
// SIGNUP
// =======================
async function signup() {

    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;

    const response = await fetch(`${API}/auth/signup`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    alert(data.message);
    window.location.href = "login.html";
}


// =======================
// LOGIN
// =======================
async function login() {

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    const response = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "dashboard.html";
    } else {
        alert("Login failed");
    }
}


// =======================
// UPLOAD RESUME
// =======================
async function uploadResume() {

    const file = document.getElementById("resumeFile").files[0];
    const token = localStorage.getItem("token");

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API}/llm_analyze/analyze`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`
        },
        body: formData
    });

    const data = await response.json();

    // ✅ SAFE extraction (works for all backend formats)
    const aiText =
        data.result?.choices?.[0]?.message?.content ||
        data.result?.ai_response ||
        data.result ||
        "No response found";

    document.getElementById("result").innerText = aiText;
}


// =======================
// LOAD HISTORY
// =======================
async function loadHistory() {

    const token = localStorage.getItem("token");

    const res = await fetch(`${API}/llm_analyze/history`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await res.json();

    const container = document.getElementById("historyList");
    container.innerHTML = "";

    data.forEach(item => {

        const div = document.createElement("div");
        div.className = "history-item";

        div.innerText = item.filename;

        div.onclick = () => {

            const text =
                item.ai_response?.choices?.[0]?.message?.content ||
                item.ai_response ||
                "No data";

            document.getElementById("result").innerText = text;
        };

        container.appendChild(div);
    });
}


// =======================
// ON PAGE LOAD
// =======================
window.onload = () => {
    if (localStorage.getItem("token")) {
        loadHistory();
    }
};