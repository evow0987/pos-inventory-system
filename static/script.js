// Fetch and display inventory data dynamically
fetch('/inventory')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('#inventoryTable tbody');
        tableBody.innerHTML = '';  // Clear existing rows
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.name}</td>
                <td>${item.description}</td>
                <td>${item.price}</td>
                <td>${item.quantity}</td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => console.error('Error fetching inventory:', error));
