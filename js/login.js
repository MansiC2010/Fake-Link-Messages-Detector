// Login form handling
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const errorDiv = document.getElementById('login-error');
    const loginBtn = document.getElementById('login-btn');
    
    // Clear previous errors
    errorDiv.style.display = 'none';
    errorDiv.innerHTML = '';
    
    // Validate inputs
    if (!username || !password) {
        errorDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i> Please enter both username and password.';
        errorDiv.style.display = 'block';
        return;
    }
    
    // Disable button and show loading
    loginBtn.disabled = true;
    loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing in...';
    
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Redirect to main page
            window.location.href = '/';
        } else {
            // Show error message
            errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${data.error || 'Invalid username or password.'}`;
            errorDiv.style.display = 'block';
            loginBtn.disabled = false;
            loginBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Sign In';
        }
    } catch (error) {
        errorDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i> Network error. Please try again.';
        errorDiv.style.display = 'block';
        loginBtn.disabled = false;
        loginBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Sign In';
    }
});

// Enter key support
document.getElementById('password').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('login-form').dispatchEvent(new Event('submit'));
    }
});

