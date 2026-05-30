const authPanel = document.getElementById('authPanel');
const trackerPage = document.getElementById('trackerPage');
const historyPage = document.getElementById('historyPage');
const profilePage = document.getElementById('profilePage');
const mainNav = document.getElementById('mainNav');
const logoutBtn = document.getElementById('logoutBtn');
const logoutProfileBtn = document.getElementById('logoutProfileBtn');
const authMessage = document.getElementById('authMessage');
const authTitle = document.getElementById('authTitle');
const authSubtitle = document.getElementById('authSubtitle');
const showLogin = document.getElementById('showLogin');
const showSignup = document.getElementById('showSignup');
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');
const expenseForm = document.getElementById('expenseForm');
const expenseTable = document.getElementById('expenseTable');
const historyTable = document.getElementById('historyTable');
const totalAmount = document.getElementById('totalAmount');
const profileName = document.getElementById('profileName');
const profileEmail = document.getElementById('profileEmail');
const profileSince = document.getElementById('profileSince');

const SESSION_KEY = 'expenseTrackerSession';

function getSession() {
    return JSON.parse(localStorage.getItem(SESSION_KEY) || 'null');
}

function setSession(session) {
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

function clearSession() {
    localStorage.removeItem(SESSION_KEY);
}

function showMessage(message, type = 'error') {
    authMessage.textContent = message;
    authMessage.style.color = type === 'error' ? '#f87171' : '#34d399';
}

function switchAuthTab(activeTab) {
    if (activeTab === 'login') {
        loginForm.classList.remove('hidden');
        signupForm.classList.add('hidden');
        showLogin.classList.add('active');
        showSignup.classList.remove('active');
        authTitle.textContent = 'Welcome Back';
        authSubtitle.textContent = 'Login to continue to your expense dashboard.';
        showMessage('');
    } else {
        loginForm.classList.add('hidden');
        signupForm.classList.remove('hidden');
        showLogin.classList.remove('active');
        showSignup.classList.add('active');
        authTitle.textContent = 'Create Account';
        authSubtitle.textContent = 'Sign up to save expenses and view your profile.';
        showMessage('');
    }
}

function showPage(page) {
    authPanel.classList.add('hidden');
    trackerPage.classList.add('hidden');
    historyPage.classList.add('hidden');
    profilePage.classList.add('hidden');

    document.querySelectorAll('.nav-link').forEach(btn => btn.classList.remove('active'));

    if (page === 'tracker') {
        trackerPage.classList.remove('hidden');
        mainNav.querySelector('[data-page="tracker"]').classList.add('active');
        loadExpenses();
    } else if (page === 'history') {
        historyPage.classList.remove('hidden');
        mainNav.querySelector('[data-page="history"]').classList.add('active');
        loadHistory();
    } else if (page === 'profile') {
        profilePage.classList.remove('hidden');
        mainNav.querySelector('[data-page="profile"]').classList.add('active');
        renderProfile();
    }
}

function renderProfile() {
    const session = getSession();
    if (!session) return;
    profileName.textContent = session.name;
    profileEmail.textContent = session.email;
    profileSince.textContent = session.joined;
}

function validateEmail(email) {
    return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
}

showLogin.addEventListener('click', () => switchAuthTab('login'));
showSignup.addEventListener('click', () => switchAuthTab('signup'));

async function authRequest(path, body) {
    const response = await fetch(path, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });

    const data = await response.json();
    if (!response.ok) {
        showMessage(data.message || 'Something went wrong.');
        return null;
    }
    return data;
}

loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('loginEmail').value.trim().toLowerCase();
    const password = document.getElementById('loginPassword').value.trim();

    if (!email || !password) {
        showMessage('Please enter email and password.');
        return;
    }
    if (!validateEmail(email)) {
        showMessage('Please enter a valid email address.');
        return;
    }

    const result = await authRequest('/auth/login', { email, password });
    if (!result) return;

    setSession(result.user);
    showMessage('Login successful!', 'success');
    setTimeout(() => initializeApp(), 400);
});

signupForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const name = document.getElementById('signupName').value.trim();
    const email = document.getElementById('signupEmail').value.trim().toLowerCase();
    const password = document.getElementById('signupPassword').value;
    const confirm = document.getElementById('signupConfirm').value;

    if (!name || !email || !password || !confirm) {
        showMessage('Please complete all fields.');
        return;
    }
    if (!validateEmail(email)) {
        showMessage('Please enter a valid email address.');
        return;
    }
    if (password !== confirm) {
        showMessage('Passwords do not match.');
        return;
    }

    const result = await authRequest('/auth/signup', { name, email, password });
    if (!result) return;

    setSession(result.user);
    showMessage('Account created successfully!', 'success');
    setTimeout(() => initializeApp(), 500);
});

expenseForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const session = getSession();
    if (!session) return;

    const expense = {
        title: document.getElementById('title').value.trim(),
        amount: parseFloat(document.getElementById('amount').value),
        category: document.getElementById('category').value,
        date: document.getElementById('date').value,
        user_email: session.email
    };

    if (!expense.title || !expense.amount || !expense.date) {
        showMessage('Please fill in all expense fields.');
        return;
    }

    const response = await fetch('/expenses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(expense)
    });

    const data = await response.json();
    if (!response.ok) {
        showMessage(data.message || 'Unable to save expense.');
        return;
    }

    expenseForm.reset();
    loadExpenses();
});

async function loadExpenses() {
    const session = getSession();
    if (!session) return;

    const response = await fetch(`/expenses?email=${encodeURIComponent(session.email)}`);
    if (!response.ok) {
        return;
    }

    const expenses = await response.json();
    expenseTable.innerHTML = '';
    let total = 0;

    expenses.slice().reverse().forEach(expense => {
        total += Number(expense.amount);
        expenseTable.innerHTML += `
            <tr>
                <td>${expense.title}</td>
                <td>₹${Number(expense.amount).toFixed(2)}</td>
                <td>${expense.category}</td>
                <td>${expense.date}</td>
                <td><button class="delete-btn" onclick="deleteExpense('${expense._id}')">Delete</button></td>
            </tr>
        `;
    });

    totalAmount.textContent = total.toFixed(2);
}

async function loadHistory() {
    const session = getSession();
    if (!session) return;

    const response = await fetch(`/expenses?email=${encodeURIComponent(session.email)}`);
    if (!response.ok) {
        return;
    }

    const expenses = await response.json();
    historyTable.innerHTML = '';

    expenses.slice().reverse().forEach(expense => {
        historyTable.innerHTML += `
            <tr>
                <td>${expense.date}</td>
                <td>${expense.title}</td>
                <td>${expense.category}</td>
                <td>₹${Number(expense.amount).toFixed(2)}</td>
            </tr>
        `;
    });
}

async function deleteExpense(id) {
    const session = getSession();
    if (!session) return;

    await fetch(`/expenses/${id}?email=${encodeURIComponent(session.email)}`, {
        method: 'DELETE'
    });

    loadExpenses();
    loadHistory();
}

function logout() {
    clearSession();
    initializeApp();
}

logoutBtn.addEventListener('click', logout);
logoutProfileBtn.addEventListener('click', logout);

mainNav.addEventListener('click', (event) => {
    if (!event.target.matches('.nav-link')) return;
    const page = event.target.dataset.page;
    if (page) showPage(page);
});

function initializeApp() {
    const currentUser = getSession();
    if (currentUser) {
        authPanel.classList.add('hidden');
        mainNav.classList.remove('hidden');
        showPage('tracker');
        renderProfile();
    } else {
        authPanel.classList.remove('hidden');
        trackerPage.classList.add('hidden');
        historyPage.classList.add('hidden');
        profilePage.classList.add('hidden');
        mainNav.classList.add('hidden');
        switchAuthTab('login');
    }
}

initializeApp();

window.deleteExpense = deleteExpense;
