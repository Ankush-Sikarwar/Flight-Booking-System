function search() {
    // Get the search term from the input field
    const searchTerm = document
        .getElementById("search-input")
        .value.toLowerCase();
    console.log("Search term:", searchTerm);
    // Get the list of dynamic data elements
    const dynamicDataList = document.querySelectorAll(".dynamic-data");

    // Get the "no results" message element
    const noResultsMsg = document.getElementById("no-results-msg");

    // Keep track of whether any search results were found
    let searchResultsFound = false;

    // Loop through the dynamic data elements and check if they match the search term
    dynamicDataList.forEach((data) => {
        const textContent = data.textContent.toLowerCase();
        if (textContent.includes(searchTerm)) {
            data.style.display = "block";
            searchResultsFound = true;
        } else {
            data.style.display = "none";
        }
    });

    // Toggle the visibility of the dynamic data container based on whether search results were found
    const dynamicDataContainer = document.getElementById(
        "dynamic-data-container"
    );
    dynamicDataContainer.style.display = searchResultsFound ? "block" : "none";

    // Toggle the visibility of the "no results" message based on whether search results were found
    noResultsMsg.style.display = searchResultsFound ? "none" : "block";
}

// Get the search button and input field
const searchButton = document.getElementById("search-button");
const searchInput = document.getElementById("search-input");

// Add an event listener to the search button
searchButton.addEventListener("click", search);

// Add an event listener to the search input field to handle the Enter key
searchInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        search();
    }
});

// Add an event listener to the search input field to handle input changes
searchInput.addEventListener("input", search);
