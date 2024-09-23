document.getElementById('calorieForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/calculate', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('results').innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                let resultHTML = '<h2>Calorie Results</h2><ul>';
                data.calories_result.forEach(result => {
                    resultHTML += `<li>${result.label}: ${result.calories} Calories/day (${result.percentage})</li>`;
                });
                resultHTML += '</ul>';

                resultHTML += `<h2>Sample Diet Plan</h2><div>${data.diet_plan_html}</div>`;
                document.getElementById('results').innerHTML = resultHTML;
            }
        })
        .catch(error => {
            document.getElementById('results').innerHTML = `<p>Error: ${error.message}</p>`;
        });
});