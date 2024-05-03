<script>
    let question = '';
    let answer = '';

    async function askQuestion() {
        try {
            const response = await fetch('http://localhost:9999', {
                method: 'POST',
                headers: {
                    'Content-Type': 'text/plain',
                },
                body: question
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            answer = await response.text();
        } catch (error) {
            console.error('Error:', error);
            answer = 'Failed to fetch answer.';
        }
    }
</script>

<main>
    <h1>Fråga om bygglovsregler</h1>
    <input type="text" bind:value={question} placeholder="Type your question here" />
    <button on:click={askQuestion}>Ask</button>
    <pre>{answer}</pre>
</main>

<style>
    main {
        text-align: center;
        padding: 50px;
        font-family: Arial, sans-serif;
    }
    input, button {
        font-size: 1.2rem;
        padding: 0.5rem;
        margin: 0.5rem;
    }
    input {
        width: 400px;
    }
    button {
        cursor: pointer;
    }
    pre {
        max-width: 100%;
        white-space: break-spaces;
        text-align: left;
    }
</style>