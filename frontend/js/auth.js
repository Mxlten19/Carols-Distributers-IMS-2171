async function login() {
    let username = document.getElementById("username").value.trim();
    let password = document.getElementById("password").value.trim();
    let errorBox = document.getElementById("login-error");
    let timerBox = document.getElementById("lock-timer"); // add <div id="lock-timer"></div> under form

    errorBox.innerText = "";
    if (timerBox) timerBox.innerText = "";

    let res = await apiPost("/auth/login", { username, password });

    if (res.token) {
        // save token + role
        localStorage.setItem("token", res.token);
        localStorage.setItem("role", res.role);
        localStorage.setItem("username", res.username);
        localStorage.setItem("user_id", res.user_id);
        window.location.href = "dashboard.html";
        return;
    }

    // handle errors / lockout
    if (res.locked && res.seconds_left) {
        errorBox.innerText = res.error || "Account locked.";

        let remaining = res.seconds_left;
        if (timerBox) {
            timerBox.innerText = `Please wait ${remaining}s before trying again.`;
            let interval = setInterval(() => {
                remaining--;
                if (remaining <= 0) {
                    clearInterval(interval);
                    timerBox.innerText = "";
                    errorBox.innerText = "";
                } else {
                    timerBox.innerText = `Please wait ${remaining}s before trying again.`;
                }
            }, 1000);
        }
    } else if (res.attempts_left !== undefined) {
        errorBox.innerText = `${res.error} You have ${res.attempts_left} attempt(s) left.`;
    } else if (res.error) {
        errorBox.innerText = res.error;
    } else {
        errorBox.innerText = "Login failed. Please try again.";
    }
}


function startLockCountdown(seconds) {

    let errorBox = document.getElementById("login-error");
    let timeLeft = seconds;

    errorBox.innerText = `Too many failed attempts. Try again in ${timeLeft}s`;

    let timer = setInterval(() => {

        timeLeft--;

        if (timeLeft <= 0) {
            clearInterval(timer);
            errorBox.innerText = "You may now try logging in again.";
            return;
        }

        errorBox.innerText =
            `Too many failed attempts. Try again in ${timeLeft}s`;

    }, 1000);
}
