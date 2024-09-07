
function appendUrls(data, resultsContainer, query)
{   
    resultsContainer.innerHTML = ''; // Clear previous results

    Object.entries(data).forEach(([key, value]) => {
        
        if(value.length > 0)
        {   
            if(key !== 'tag'){
                const header = document.createElement('p');
                header.className = 'search-header';
                header.innerText = capitalize(key);
                resultsContainer.appendChild(header);
            }
            

            value.forEach(result => {
                const resultLink = document.createElement('a');
                resultLink.href = `/${key}/${result.name}`; // Example: replace with actual URL

                // Check if result name contains the search query
                 // Replace with the actual search query
                const name = capitalize(result.name); // Assuming capitalize function makes the text capitalized

                // Highlight matching text with <strong> tags
                if (name.toLowerCase().includes(query.toLowerCase())) {
                    const index = name.toLowerCase().indexOf(query.toLowerCase());
                    const matchedText = name.substring(index, index + query.length);
                    resultLink.innerHTML = `<p>${name.substring(0, index)}<strong>${matchedText}</strong>${name.substring(index + query.length)}</p>`;
                } else {
                    resultLink.innerHTML = `<p>${name}</p>`;
                }

                resultsContainer.appendChild(resultLink);

                // resultsContainer.appendChild(document.createElement('br')); // Optional: line break
            });
            
        }
            
    });
    resultsContainer.style.display = 'block';
    
    
}
            // Function to fetch data from backend and update search results
function fetchSearchResults(query, ele) 
{
    const backendUrl = '/search/suggestions';
    
    
    // Example: Replace 'GET' with appropriate method if different
    fetch(`${backendUrl}/${query}`, {
        method: 'GET',
    })
    .then(response => response.json()) // Assuming JSON response; adjust as needed
    .then(data => {
        appendUrls(data, ele, query);
    })
    .catch(error => console.error('Error fetching search results:', error));
}
        
const searchInputUpper = document.getElementById('searchInputUpper');
var upperContainer = document.getElementById('searchContainerUpper');
const searchInputLower = document.getElementById('searchInputLower');
var lowerContainer = document.getElementById('searchContainerLower');
searchInputUpper.addEventListener('input', function() {
    
    const query = this.value.trim();
    if (query.length > 0) {
        fetchSearchResults(query, upperContainer);
    } else {
        // Clear results if search input is empty
        
        upperContainer.innerHTML = '';
        upperContainer.style.display = 'none';
    }
});


searchInputLower.addEventListener('input', function() {
    const query = this.value.trim();
    if (query.length > 0) {
        fetchSearchResults(query, lowerContainer);
    } else {    
        lowerContainer.innerHTML = '';
        lowerContainer.style.display = 'none';
    }
});


document.addEventListener('click', function(event) {    
    if (!lowerContainer.contains(event.target)) {
        lowerContainer.style.display = 'none';
    }
    if (!upperContainer.contains(event.target)) {
        upperContainer.style.display = 'none';
    }
});