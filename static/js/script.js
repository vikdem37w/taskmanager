console.log("HEY KRIS, I HAVE NO IDEA WHAT THAT [Little Slime] WROTE, [Approach with Caution]!!!");
// Store tokens in localStorage
function storeTokens(accessToken, refreshToken) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
}

// Get access token
function getAccessToken() {
    return localStorage.getItem('access_token');
}

// Make authenticated requests
async function makeAuthenticatedRequest(url, options = {}) {
    const token = getAccessToken();
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(url, {
        ...options,
        headers
    });
    
    if (response.status === 401) {
        // Token expired, try to refresh
        const refreshed = await refreshToken();
        if (refreshed) {
            return makeAuthenticatedRequest(url, options);
        }
    }
    
    return response;
}

// Refresh token
async function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return false;
    
    try {
        const response = await fetch('/users/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                refresh: refreshToken
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            storeTokens(data.access, refreshToken);
            return true;
        }
    } catch (error) {
        console.error('Token refresh failed:', error);
    }
    
    // Clear tokens if refresh failed
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    return false;
}

// Login function
async function login(username, password) {
    try {
        const response = await fetch('/users/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            storeTokens(data.access_token, data.refresh_token);
            return data;
        } else {
            const error = await response.json();
            throw new Error(error.error || 'Login failed');
        }
    } catch (error) {
        throw error;
    }
}

// Register function
async function register(username, password, email = '') {
    try {
        const response = await fetch('/users/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
                email: email
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            storeTokens(data.access_token, data.refresh_token);
            return data;
        } else {
            const error = await response.json();
            throw new Error(error.error || 'Registration failed');
        }
    } catch (error) {
        throw error;
    }
}