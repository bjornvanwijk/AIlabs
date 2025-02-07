
document.addEventListener('DOMContentLoaded', function() {
    const analysisForm = document.getElementById('analysis-form');
    const resultsContainer = document.getElementById('results-container');

    analysisForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData(this);
        const userText = formData.get('input_text');
        
        // Add user message
        const userDiv = document.createElement('div');
        userDiv.className = 'message user-message';
        userDiv.innerHTML = `<strong>User:</strong><br>${userText}`;
        resultsContainer.appendChild(userDiv);

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.error) {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error';
                errorDiv.textContent = data.error;
                resultsContainer.appendChild(errorDiv);
                return;
            }

            // Add tool response
            const toolDiv = document.createElement('div');
            toolDiv.className = 'message tool-message';
            toolDiv.innerHTML = `<strong>Tool:</strong><br>${data.results.analysis}`;
            resultsContainer.appendChild(toolDiv);

            resultsContainer.scrollTop = resultsContainer.scrollHeight;

        } catch (error) {
            console.error('Error:', error);
            resultsContainer.innerHTML = `
                <div class="error">An error occurred: ${error.message}</div>`;
        }
    });
});
