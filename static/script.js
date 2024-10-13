document.getElementById('searchForm').addEventListener('submit', async function (event) {
    event.preventDefault();  // Prevent page reload on form submit

    // Get the query from the input field
    const query = document.getElementById('query').value;

    // Send query to Flask backend using POST request
    const response = await fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query }),
    });

    const results = await response.json();

    // Check for errors
    if (results.error) {
        document.getElementById('results').innerHTML = `<p>Error: ${results.error}</p>`;
        return;
    }

    // Display the top documents and their similarity scores
    let resultHTML = '<ol>';
    results.forEach((result) => {
        resultHTML += `<li><strong>Similarity:</strong> ${result.similarity.toFixed(4)}<br>
                       <strong>Document Preview:</strong> ${result.document}...</li>`;
    });
    resultHTML += '</ol>';
    document.getElementById('results').innerHTML = resultHTML;

    // Visualize cosine similarity using a bar chart
    visualizeSimilarity(results);
});

function visualizeSimilarity(results) {
    const ctx = document.getElementById('similarityChart').getContext('2d');
    const labels = results.map((result, index) => `Doc ${index + 1}`);
    const data = results.map(result => result.similarity);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Cosine Similarity',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
            }],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
}
