const API_BASE = 'http://localhost:5002';

const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const typingIndicator = document.getElementById('typingIndicator');

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addUserMessage(message);
    userInput.value = '';
    showTypingIndicator();
    scrollToBottom();

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        hideTypingIndicator();
        
        if (data.response) {
            addBotMessage(data.response);
        } else {
            addBotMessage('Sorry, I encountered an error. Please try again.');
        }
    } catch (error) {
        hideTypingIndicator();
        addBotMessage('Unable to connect to the server. Please make sure the backend is running on port 5000.');
        console.error('Error:', error);
    }

    scrollToBottom();
}

function quickAsk(question) {
    userInput.value = question;
    sendMessage();
}

function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-user"></i>
        </div>
        <div class="message-content">
            <p>${escapeHtml(message)}</p>
            <span class="timestamp">${getTimestamp()}</span>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addBotMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <p>${formatMessage(message)}</p>
            <span class="timestamp">${getTimestamp()}</span>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function formatMessage(text) {
    text = escapeHtml(text);
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\n/g, '<br>');
    return text;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showTypingIndicator() {
    typingIndicator.style.display = 'block';
    scrollToBottom();
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getTimestamp() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function clearChat() {
    chatMessages.innerHTML = `
        <div class="message bot-message">
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <p>Chat cleared! How can I help you today?</p>
                <span class="timestamp">${getTimestamp()}</span>
            </div>
        </div>
    `;
}

document.getElementById('recommendationForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const profile = {
        country: document.getElementById('country').value,
        field: document.getElementById('field').value,
        budget: document.getElementById('budget').value,
        ielts: document.getElementById('ielts').value,
        gpa: document.getElementById('gpa').value
    };

    try {
        const response = await fetch(`${API_BASE}/recommend-university`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(profile)
        });

        const data = await response.json();
        
        if (data.recommendations && data.recommendations.length > 0) {
            displayRecommendations(data.recommendations);
        } else {
            alert('No universities match your criteria. Try adjusting your preferences.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Unable to get recommendations. Please make sure the backend is running.');
    }
});

function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations');
    const list = document.getElementById('recommendationList');
    
    container.style.display = 'block';
    
    list.innerHTML = recommendations.map(rec => `
        <div class="recommendation-item">
            <h4>${rec.university} <span class="score-badge">${rec.score}% Match</span></h4>
            <div class="university-meta">
                ${rec.country} • ${rec.course}<br>
                IELTS: ${rec.ielts} • Deadline: ${rec.deadline}<br>
                Tuition: ${rec.tuition_fee} • GPA: ${rec.gpa_requirement}
            </div>
            <div class="reasons">
                <i class="fas fa-check-circle"></i> ${rec.reasons.join(' • ')}
            </div>
        </div>
    `).join('');

    container.scrollIntoView({ behavior: 'smooth' });
}

async function showVisaDetails(country) {
    try {
        const response = await fetch(`${API_BASE}/visa-info/${country}`);
        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById('modalTitle').textContent = data.name;
        
        document.getElementById('modalContent').innerHTML = `
            <p style="margin-bottom: 20px;">${data.description}</p>
            
            <div class="modal-section">
                <h3><i class="fas fa-file-alt"></i> Requirements</h3>
                <ul>
                    ${data.requirements.map(req => `<li>${req}</li>`).join('')}
                </ul>
            </div>
            
            <div class="modal-section">
                <h3><i class="fas fa-steps"></i> Application Process</h3>
                <ol style="padding-left: 20px;">
                    ${data.process.map(step => `<li style="margin: 6px 0;">${step}</li>`).join('')}
                </ol>
            </div>
            
            <div class="modal-section">
                <h3><i class="fas fa-clock"></i> Processing Time</h3>
                <p>${data.processing_time}</p>
            </div>
        `;

        document.getElementById('visaModal').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        alert('Unable to load visa information. Please make sure the backend is running.');
    }
}

function closeModal() {
    document.getElementById('visaModal').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('visaModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}
