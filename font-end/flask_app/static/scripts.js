document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            if (username === 'admin' && password === 'admin123') {
                window.location.href = 'dashboard.html';
            } else {
                alert('Invalid credentials');
            }
        });
    }

    const presentCount = document.getElementById('presentCount');
    const absentCount = document.getElementById('absentCount');

    if (presentCount && absentCount) {
        // Fetch data from API to update counts (dummy values here)
        presentCount.innerText = 30; // Sample value
        absentCount.innerText = 5;   // Sample value
    }
});

function viewAttendance() {
    window.location.href = 'attendance.html';
}
