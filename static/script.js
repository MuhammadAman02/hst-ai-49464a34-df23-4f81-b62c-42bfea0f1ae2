document.querySelector('form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch('/api/analyze-image', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    document.getElementById('results').innerHTML = `
        <h2>Results:</h2>
        <p>Skin Tone: RGB(${data.skin_tone.join(', ')})</p>
        <h3>Recommended Colors:</h3>
        <ul>
            ${data.color_palette.map(color => `<li style="color: rgb(${color.join(',')})">RGB(${color.join(', ')})</li>`).join('')}
        </ul>
    `;
});