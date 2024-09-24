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
                    <table class="dietinfo">
        <tr>
            <th>Dish</th>
            <td>${data.recipeName}</td>
        </tr>
        <tr>
            <th>Calories</th>
            <td>${data.calories}</td>
        </tr>
        <tr>
            <th>Fat</th>
            <td>${data.fat}</td>
        </tr>
        <tr>
            <th>Carbs</th>
            <td>${data.carbs}</td>
        </tr>
        <tr>
            <th>Protein</th>
            <td>${data.protein}</td>
        </tr>
    </table>
                    <div class="img">
                    <img src="${data.image}" alt="${data.recipeName} image">
                    </div>
                `;
            }
        })
        .catch(error => {
            document.getElementById('result').innerHTML = `<p>Error fetching data. Please try again.</p>`;
        });
});