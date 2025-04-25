document.addEventListener('DOMContentLoaded', function() {
    fetch('results.csv')
        .then(response => response.text())
        .then(data => {
            const rows = data.trim().split('\n');
            const tableHeader = document.getElementById('tableHeader');
            const tableBody = document.getElementById('tableBody');

            if (rows.length > 0) {
                // Assuming the first row contains headers
                const headers = rows[0].split(',');
                headers.forEach(header => {
                    const th = document.createElement('th');
                    th.textContent = header;
                    tableHeader.appendChild(th);
                });

                // Process the rest of the rows
                for (let i = 1; i < rows.length; i++) {
                    const row = rows[i].split(',');
                    const tr = document.createElement('tr');

                    for (let j = 0; j < row.length; j++) {
                        const td = document.createElement('td');
                        td.textContent = row[j];

                        // Apply color based on cell value
                        const cellValue = parseFloat(row[j].trim());
                        if (!isNaN(cellValue)) {

                            // Highlight the bigger number in adjacent even-odd column pairs as red
                            if (j > 1 && j % 2 === 0) { // Skip the first column and compare only when j is even (2, 4, 6, ...)
                                const prevCellValue = parseFloat(row[j - 1].trim());
                                if (!isNaN(prevCellValue)) {
                                    if (cellValue > prevCellValue) {
                                        td.style.color = 'red';
                                        tr.children[j - 1].style.color = 'green';
                                    } else if (cellValue < prevCellValue) {
                                        tr.children[j - 1].style.color = 'red';
                                        td.style.color = 'green';
                                    }
                                }
                            }

                            if (cellValue === -1) {
                                td.style.color = 'lightblue';
                            } else if (cellValue === -2) {
                                td.style.color = 'lavender';
                            }
                        }

                        tr.appendChild(td);
                    }
                    tableBody.appendChild(tr);
                }
            }
        })
        .catch(error => console.error('Error fetching the CSV file:', error));
});