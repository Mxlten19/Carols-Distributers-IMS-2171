document.addEventListener("DOMContentLoaded", () => {
    insertSidebar();
    insertTopbar();
    highlightActiveLink();
    applyRoleRestrictions();
});

function insertSidebar() {
    const sidebar = document.getElementById("sidebar");
    if (!sidebar) return;

    sidebar.innerHTML = `
        <h2 class="sidebar-title">Inventory Management System</h2>

        <a href="dashboard.html" data-page="dashboard">Dashboard</a>
        <a href="inventory.html" data-page="inventory">Inventory</a>
        <a href="sales.html" data-page="sales">Sales</a>
        <a href="alerts.html" data-page="alerts">Alerts</a>
        <a href="reports.html" data-page="reports">Reports</a>
        <a id="users-link" href="users.html" data-page="users">User Management</a>

    `;
}

function insertTopbar() {
    const topbar = document.getElementById("topbar");
    if (!topbar) return;

    topbar.innerHTML = `
        <div class="topbar-right">
            <span id="usernameLabel"></span>
            <button class="btn" onclick="logout()">Logout</button>
        </div>
    `;

    let username = localStorage.getItem("username");
    if (username) {
        document.getElementById("usernameLabel").innerText =
            "Logged in as: " + username;
    }
}

function highlightActiveLink() {
    const page = location.pathname.split("/").pop().replace(".html", "");
    const links = document.querySelectorAll("#sidebar a");

    links.forEach(link => {
        if (link.dataset.page === page) {
            link.classList.add("active");
        }
    });
}

function applyRoleRestrictions() {
    const page = location.pathname.split("/").pop();
    if (page === "index.html" || page === "") return;  // skip on login

    let token = localStorage.getItem("token");
    let role = localStorage.getItem("role");

    if (!token) {
        logout();
        return;
    }

    if (role !== "OWNER") {
        let users = document.getElementById("users-link");
        if (users) users.style.display = "none";
    }
}


function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}
