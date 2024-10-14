// Save data function (works with Django POST request)
function saveData() {
    const message = document.getElementById("inputMessage").value;

    // Make POST request to Django backend
    fetch('/api/save/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            message: message
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display the response message on the webpage
        document.getElementById("response").innerHTML = data.response;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


// Download file function
function downloadFile() {
    window.location.href = '/download/';
}

// Run code function (for real-time code execution)
function runCode() {
    const userCode = editor.getValue();

    fetch('/run_stream/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            code: userCode
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.body.getReader();
    })
    .then(reader => {
        const outputElement = document.getElementById('output');
        outputElement.textContent = '';  // Clear previous output

        const decoder = new TextDecoder();
        function readChunk() {
            reader.read().then(({ done, value }) => {
                if (done) return;  // Stop reading when finished
                const chunk = decoder.decode(value);
                outputElement.textContent += chunk;
                readChunk();  // Keep reading chunks
            });
        }

        readChunk();
    })
    .catch(error => {
        console.error('Error running code:', error);
    });
}
