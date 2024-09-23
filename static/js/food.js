document.getElementById('recipeForm').addEventListener('submit', function (event) {
    event.preventDefault();
    fetch('/get_recipe', {
        method: 'POST',
        body: new FormData(this),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('result').innerHTML = `<p>${data.error}</p>`;
            } else {
                document.getElementById('result').innerHTML = `
                    <p><strong>Recipe:</strong> ${data.recipeName}</p>
                    <p><strong>Calories:</strong> ${data.calories}</p>
                    <p><strong>Fat:</strong> ${data.fat}</p>
                    <p><strong>Carbs:</strong> ${data.carbs}</p>
                    <p><strong>Protein:</strong> ${data.protein}</p>
                    <img src="${data.image}" alt="${data.recipeName} image">
                `;
            }
        })
        .catch(error => {
            document.getElementById('result').innerHTML = `<p>Error fetching data. Please try again.</p>`;
        });
});