document.addEventListener('DOMContentLoaded', function () {
    const countySelect = document.getElementById('countySelect');
    const constituencySelect = document.getElementById('constituencySelect');
    const filterForm = document.getElementById('filterForm');
    const resultsContainer = document.getElementById('resultsContainer');

    // Function to fetch counties and populate dropdown
    async function fetchCounties() {
        try {
            const response = await axios.get('/counties'); // Replace with actual endpoint
            const counties = response.data;

            counties.forEach(county => {
                const option = document.createElement('option');
                option.value = county;
                option.textContent = county;
                countySelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching counties:', error);
        }
    }

    // Function to fetch constituencies for selected county
    async function fetchConstituencies(county) {
        try {
            const response = await axios.get(`/constituencies/${county}`); // Replace with actual endpoint
            const constituencies = response.data;

            // Clear previous options
            constituencySelect.innerHTML = '<option value="">Select Constituency</option>';

            constituencies.forEach(constituency => {
                const option = document.createElement('option');
                option.value = constituency;
                option.textContent = constituency;
                constituencySelect.appendChild(option);
            });
        } catch (error) {
            console.error(`Error fetching constituencies for ${county}:`, error);
        }
    }

    // Event listener for county selection change
    countySelect.addEventListener('change', function () {
        const selectedCounty = countySelect.value;
        if (selectedCounty) {
            fetchConstituencies(selectedCounty);
        } else {
            // Clear constituency dropdown if no county selected
            constituencySelect.innerHTML = '<option value="">Select Constituency</option>';
        }
    });


    // Event listener for form submission (filtering)
    filterForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const selectedCounty = countySelect.value;
    const selectedConstituency = constituencySelect.value;

    try {
        const response = await axios.get(`/filter?county=${selectedCounty}&constituency=${selectedConstituency}`); // Replace with actual endpoint
        const filteredResults = response.data;

        // Clear previous results
        resultsContainer.innerHTML = '';

        filteredResults.forEach(result => {
            // Create a clickable result div
            const resultDiv = document.createElement('div');
            resultDiv.classList.add('bg-white', 'p-6', 'rounded-lg', 'shadow-md', 'cursor-pointer', 'mb-4');
            resultDiv.innerHTML = `
            <a href="/profile/{{ profile.id }}" class="profile-card bg-white rounded-lg shadow-md p-6 block">
                <h3 class="text-xl font-semibold text-gray-800">${result.name}</h3>
                <p class="text-gray-600">County: ${result.county}, Constituency: ${result.constituency}</p>
                <img src="${result.image}" alt="${result.name} photo" class="w-32 h-32 rounded-full mx-auto mt-4">
                <p class="text-gray-600 mt-2">Party: ${result.party}</p>
            </a>
            `;

            // Append resultDiv to resultsContainer
            resultsContainer.appendChild(resultDiv);
        });
    } catch (error) {
        console.error('Error filtering results:', error);
    }
});


    // Initialize by fetching counties
    fetchCounties();
});
