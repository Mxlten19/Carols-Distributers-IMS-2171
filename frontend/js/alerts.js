async function loadAlerts() {
    let data = await apiGet("/alerts/");
    let table = document.getElementById("alert-table");

    table.innerHTML = "";

    if (!data || data.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="4" style="text-align:center;">No alerts</td>
            </tr>`;
        return;
    }

    data.forEach(a => {
        table.innerHTML += `
            <tr>
                <td>${a.product}</td>
                <td>${a.msg}</td>
                <td>${a.created_at || ""}</td>
                <td>${a.status}</td>
                <td>
                    ${
                        a.status === "RESOLVED"
                            ? `<button class="btn-secondary" onclick="deleteAlert(${a.id})">
                                   Delete
                               </button>`
                            : ""
                    }
                </td>
            </tr>
        `;
    });
}

async function deleteAlert(id) {
    if (!confirm("Are you sure you want to delete this alert?")) return;

    let res = await apiDelete(`/alerts/${id}`);

    if (res && res.error) {
        alert(res.error);
        return;
    }

    // reload table
    loadAlerts();
}

window.addEventListener("DOMContentLoaded", loadAlerts);


