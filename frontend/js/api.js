const API_BASE = "http://127.0.0.1:5000";

async function apiRequest(url, method="GET", data=null) {

    let token = localStorage.getItem("token");

    let headers = {
        "Content-Type": "application/json"
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    let options = {
        method,
        headers
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    let response = await fetch(API_BASE + url, options);

    // UPDATE TOKEN IF BACKEND SENT A REFRESH
    let refreshed = response.headers.get("X-Auth-Refresh");

    if (refreshed) {
        localStorage.setItem("token", refreshed);
    }

    // Auto logout only on REAL auth failure
    if (response.status === 401) {
        localStorage.clear();
        window.location.href = "index.html";
        return;
    }

    return response.json();
}

// WRAPPERS
const apiGet    = (url) => apiRequest(url, "GET");
const apiPost   = (url, data) => apiRequest(url, "POST", data);
const apiPut    = (url, data) => apiRequest(url, "PUT", data);
const apiDelete = (url) => apiRequest(url, "DELETE");
