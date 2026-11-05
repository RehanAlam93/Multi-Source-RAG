function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.input-section').forEach(sec => sec.style.display = 'none');

    if (tab === 'youtube') {
        event.target.classList.add('active');
        document.getElementById('youtube-section').style.display = 'flex';
    } else if (tab === 'pdf') {
        event.target.classList.add('active');
        document.getElementById('pdf-section').style.display = 'flex';
    } else if (tab === 'web') {
        event.target.classList.add('active');
        document.getElementById('web-section').style.display = 'flex';
    }
}

function showStatus(message, isError = false) {
    const statusDiv = document.getElementById('status-message');
    statusDiv.style.backgroundColor = isError ? '#7f1d1d' : '#065f46';
    statusDiv.style.color = '#ffffff';
    statusDiv.innerText = message;
}

async function processYouTube() {
    const videoId = document.getElementById('youtube-id').value.trim();
    if (!videoId) {
        showStatus('Please enter a valid YouTube Video ID', true);
        return;
    }
    showStatus('Processing YouTube video transcript...');

    const response = await fetch('/process-youtube', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_id: videoId })
    });
    const data = await response.json();

    if (data.status === 'success') {
        showStatus('YouTube processed successfully!');
        document.getElementById('active-source-badge').innerText = 'Source: YouTube (' + videoId + ')';
        appendBotMessage('YouTube video loaded and processed successfully! You can now ask questions.');
    } else {
        showStatus('Error: ' + data.message, true);
    }
}

async function processPDF() {
    const fileInput = document.getElementById('pdf-file');
    if (fileInput.files.length === 0) {
        showStatus('Please select a PDF file', true);
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    showStatus('Uploading and parsing PDF...');

    const response = await fetch('/process-pdf', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();

    if (data.status === 'success') {
        showStatus('PDF processed successfully!');
        document.getElementById('active-source-badge').innerText = 'Source: PDF (' + fileInput.files[0].name + ')';
        appendBotMessage('PDF document processed successfully! You can now ask questions.');
    } else {
        showStatus('Error: ' + data.message, true);
    }
}

async function processWeb() {
    const url = document.getElementById('web-url').value.trim();
    if (!url) {
        showStatus('Please enter a valid website URL', true);
        return;
    }
    showStatus('Scraping and processing website content...');

    const response = await fetch('/process-web', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    });
    const data = await response.json();

    if (data.status === 'success') {
        showStatus('Website processed successfully!');
        document.getElementById('active-source-badge').innerText = 'Source: Website';
        appendBotMessage('Website content indexed successfully! You can now ask questions.');
    } else {
        showStatus('Error: ' + data.memory, true);
    }
}

async function sendQuery() {
    const queryInput = document.getElementById('user-query');
    const query = queryInput.value.trim();
    if (!query) return;

    appendUserMessage(query);
    queryInput.value = '';

    const chatBox = document.getElementById('chat-box');
    const loadingId = 'loading-' + Date.now();
    chatBox.innerHTML += `<div class="message bot-msg" id="${loadingId}">Thinking...</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query })
    });
    const data = await response.json();

    document.getElementById(loadingId).remove();

    if (data.status === 'success') {
        appendBotMessage(data.answer);
    } else {
        appendBotMessage('Error: ' + data.message);
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendQuery();
    }
}

function appendUserMessage(text) {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<div class="message user-msg">${text}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendBotMessage(text) {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<div class="message bot-msg">${text}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}