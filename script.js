document.getElementById('recipeForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const recipeName = document.getElementById('recipeName').value;
    const selectedCuisine = document.getElementById('cuisine').value; // Get selected cuisine
    const apiKey = '593818f809bd4c47a2c69ca54da00978'; // Replace with your Spoonacular API key

    try {
        // Step 1: Search for the recipe by name (with optional cuisine filter)
        let searchUrl = `https://api.spoonacular.com/recipes/complexSearch?query=${recipeName}&apiKey=${apiKey}`;
        
        // If a specific cuisine is selected, add the cuisine parameter to the URL
        if (selectedCuisine) {
            searchUrl += `&cuisine=${selectedCuisine}`;
        }

        const searchResponse = await fetch(searchUrl);
        const searchData = await searchResponse.json();

        if (searchData.results.length === 0) {
            document.getElementById('result').innerHTML = `<p>No recipe found for "${recipeName}".</p>`;
            return;
        }

        // Get the first recipe's ID and image URL
        const recipe = searchData.results[0];
        const recipeId = recipe.id;
        const recipeImage = recipe.image;

        // Step 2: Get the nutritional information for the recipe
        const nutritionUrl = `https://api.spoonacular.com/recipes/${recipeId}/nutritionWidget.json?apiKey=${apiKey}`;
        const nutritionResponse = await fetch(nutritionUrl);
        const nutritionData = await nutritionResponse.json();

        // Display recipe image, calorie and other relevant information
        document.getElementById('result').innerHTML = `
            <p><strong>Recipe:</strong> ${recipeName}</p>
            <p><strong>Calories:</strong> ${nutritionData.calories}</p>
            <p><strong>Fat:</strong> ${nutritionData.fat}</p>
            <p><strong>Carbs:</strong> ${nutritionData.carbs}</p>
            <p><strong>Protein:</strong> ${nutritionData.protein}</p>
            <img src="${recipeImage}" alt="${recipeName} image">
        `;
    } catch (error) {
        console.error('Error fetching data:', error);
        document.getElementById('result').innerHTML = `<p>Error fetching data. Please try again.</p>`;
    }
});
