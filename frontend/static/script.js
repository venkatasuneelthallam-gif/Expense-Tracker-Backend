const form = document.getElementById("expenseForm");
const table = document.getElementById("expenseTable");
const totalAmount = document.getElementById("totalAmount");

async function loadExpenses() {

    const response = await fetch("/expenses");

    const expenses = await response.json();

    table.innerHTML = "";

    let total = 0;

    expenses.forEach(expense => {

        total += Number(expense.amount);

        table.innerHTML += `
        <tr>
            <td>${expense.title}</td>
            <td>₹${expense.amount}</td>
            <td>${expense.category}</td>
            <td>${expense.date}</td>
            <td>
                <button
                class="delete-btn"
                onclick="deleteExpense('${expense._id}')">
                    Delete
                </button>
            </td>
        </tr>
        `;
    });

    totalAmount.innerText = total;
}

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const expense = {

        title: document.getElementById("title").value,

        amount: parseFloat(
            document.getElementById("amount").value
        ),

        category: document.getElementById("category").value,

        date: document.getElementById("date").value
    };

    await fetch("/expenses", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(expense)

    });

    form.reset();

    loadExpenses();
});

async function deleteExpense(id) {

    await fetch(`/expenses/${id}`, {

        method: "DELETE"

    });

    loadExpenses();
}

loadExpenses();