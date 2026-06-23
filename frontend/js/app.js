/* =============================================
   PERSISTENT AI — Frontend Logic
   Clean, professional, no dependencies
============================================= */

'use strict';

// ─── State ───
const state = {
  messages: 0,
  memories: [],
  theme: localStorage.getItem('theme') || 'dark',
  isLoading: false,
  lastMode: 'novel interaction',
};

// ─── DOM refs (assigned after DOMContentLoaded) ───
let chatArea, userInput, sendBtn, typingEl, modeTopBadge;
let statMessages, statMemories;
let memoryFeed, toastContainer;
let sidebar, overlay;

// ─── Init ───
document.addEventListener('DOMContentLoaded', () => {
  chatArea     = document.getElementById('chat-area');
  userInput    = document.getElementById('user-input');
  sendBtn      = document.getElementById('send-btn');
  typingEl     = document.getElementById('typing-indicator');
  modeTopBadge = document.getElementById('mode-top-badge');
  statMessages = document.getElementById('stat-messages');
  statMemories = document.getElementById('stat-memories');
  memoryFeed   = document.getElementById('memory-feed');
  toastContainer = document.getElementById('toast-container');
  sidebar      = document.getElementById('sidebar');
  overlay      = document.getElementById('overlay');

  applyTheme(state.theme);
  setupListeners();
});

// ─── Listeners ───
function setupListeners() {
  // Send on Enter (Shift+Enter = newline)
  userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Auto-resize textarea
  userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 140) + 'px';
  });

  // Sidebar toggle (mobile)
  document.getElementById('mobile-toggle')?.addEventListener('click', () => {
    sidebar.classList.add('open');
    overlay.classList.add('show');
  });
  overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('show');
  });

  // Theme toggle
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

  // Clear chat
  document.getElementById('btn-clear').addEventListener('click', clearChat);
}

// ─── Send Message ───
async function sendMessage() {
  const msg = userInput.value.trim();
  if (!msg || state.isLoading) return;

  // Hide welcome screen if visible
  const welcome = document.getElementById('welcome-screen');
  if (welcome) welcome.remove();

  userInput.value = '';
  userInput.style.height = 'auto';

  appendUserBubble(msg);
  showTyping();
  setLoading(true);

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg }),
    });

    if (!res.ok) throw new Error(`Server error: ${res.status}`);

    const data = await res.json();

    hideTyping();
    appendAIBubble(data.reply, data.mode);
    updateMode(data.mode);
    updateStats(msg);

  } catch (err) {
    hideTyping();
    appendAIBubble('⚠ Connection error. Please check that the backend is running and try again.', 'error');
    showToast('Failed to connect to backend', 'error');
    console.error('Chat error:', err);
  } finally {
    setLoading(false);
  }
}

// ─── Bubble Builders ───
function appendUserBubble(text) {
  state.messages++;
  const time = formatTime();

  const row = document.createElement('div');
  row.className = 'msg-row user';
  row.innerHTML = `
    <div class="bubble-wrap">
      <div class="bubble user">${escapeHTML(text)}</div>
      <div class="bubble-meta">
        <span class="bubble-time">${time}</span>
      </div>
    </div>
    <div class="avatar user">U</div>
  `;
  chatArea.appendChild(row);
  scrollToBottom();
}

function appendAIBubble(text, mode) {
  const time = formatTime();
  const modeClass = getModeClass(mode);
  const modeLabel = formatModeLabel(mode);

  const row = document.createElement('div');
  row.className = 'msg-row ai';
  row.innerHTML = `
    <div class="avatar ai">✦</div>
    <div class="bubble-wrap">
      <div class="bubble ai">${formatAIText(text)}</div>
      <div class="bubble-meta">
        <span class="bubble-time">${time}</span>
        <span class="bubble-mode ${modeClass}">${modeLabel}</span>
      </div>
    </div>
  `;
  chatArea.appendChild(row);
  scrollToBottom();

  // Add to memory feed
  addMemoryItem(text);
}

// ─── Suggestion Chips ───
function sendSuggestion(text) {
  userInput.value = text;
  sendMessage();
}

// ─── Typing Indicator ───
function showTyping() {
  typingEl.style.display = 'flex';
  scrollToBottom();
}

function hideTyping() {
  typingEl.style.display = 'none';
}

// ─── Loading State ───
function setLoading(val) {
  state.isLoading = val;
  sendBtn.disabled = val;
  userInput.disabled = val;
}

// ─── Stats Update ───
function updateStats(userMsg) {
  statMessages.textContent = state.messages;
  state.memories++;
  statMemories.textContent = state.memories;
}

// ─── Mode Badge Update ───
function updateMode(mode) {
  state.lastMode = mode;
  const modeClass = getModeClass(mode);
  const modeLabel = formatModeLabel(mode);

  modeTopBadge.className = `mode-badge ${modeClass}`;
  modeTopBadge.textContent = modeLabel;
}

// ─── Memory Feed ───
function addMemoryItem(text) {
  const truncated = text.length > 80 ? text.slice(0, 80) + '…' : text;
  const item = document.createElement('div');
  item.className = 'memory-item';
  item.innerHTML = `
    <div class="memory-item-text">${escapeHTML(truncated)}</div>
    <div class="memory-item-meta">${formatTime()}</div>
  `;
  memoryFeed.insertBefore(item, memoryFeed.firstChild);

  // Limit feed to 20 items
  while (memoryFeed.children.length > 20) {
    memoryFeed.removeChild(memoryFeed.lastChild);
  }
}

// ─── Toast ───
function showToast(msg, type = 'info') {
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = msg;
  toastContainer.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}

// ─── Theme ───
function toggleTheme() {
  state.theme = state.theme === 'dark' ? 'light' : 'dark';
  applyTheme(state.theme);
  localStorage.setItem('theme', state.theme);
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const btn = document.getElementById('theme-toggle');
  if (btn) btn.innerHTML = theme === 'dark' ? '☀' : '☾';
}

// ─── Clear Chat ───
function clearChat() {
  chatArea.innerHTML = '';
  state.messages = 0;
  if (statMessages) statMessages.textContent = '0';

  // Re-insert welcome screen
  chatArea.innerHTML = buildWelcomeScreen();
  showToast('Chat cleared');
}

function buildWelcomeScreen() {
  return `
  <div class="welcome-screen" id="welcome-screen">
    <div class="welcome-icon">✦</div>
    <div>
      <div class="welcome-title">Persistent AI</div>
      <div class="welcome-subtitle" style="margin-top:10px">
        A conversational system with semantic memory, affect-weighted recall, and trace-based reconstruction. Context beyond time and identity.
      </div>
    </div>
    <div class="suggestion-chips">
      <button class="chip" onclick="sendSuggestion('What do you remember about our previous conversations?')">What do you remember?</button>
      <button class="chip" onclick="sendSuggestion('Tell me about memory reconstruction')">Memory reconstruction</button>
      <button class="chip" onclick="sendSuggestion('How does your persistent memory work?')">How memory works</button>
      <button class="chip" onclick="sendSuggestion('What is context beyond time and identity?')">Context beyond time</button>
    </div>
  </div>`;
}

// ─── Helpers ───
function escapeHTML(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

function formatAIText(text) {
  // Basic markdown-style formatting
  return escapeHTML(text)
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, `<code style="font-family:var(--font-mono);font-size:0.9em;background:var(--bg-elevated);padding:1px 5px;border-radius:4px;">$1</code>`)
    .replace(/\n/g, '<br>');
}

function formatTime() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function getModeClass(mode) {
  if (!mode) return 'novel';
  const m = mode.toLowerCase();
  if (m.includes('recall')) return 'recall';
  if (m.includes('reconstruction')) return 'reconstruction';
  return 'novel';
}

function formatModeLabel(mode) {
  if (!mode) return 'Novel';
  const m = mode.toLowerCase();
  if (m.includes('recall')) return '⟳ Direct Recall';
  if (m.includes('reconstruction')) return '⟡ Reconstruction';
  return '◈ Novel';
}

function scrollToBottom() {
  requestAnimationFrame(() => {
    chatArea.scrollTop = chatArea.scrollHeight;
  });
}
