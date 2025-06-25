import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './Chatbot.css';

export default function Chatbot() {
  const navigate = useNavigate();
  const [expanded, setExpanded] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [hasStarted, setHasStarted] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const sendMessage = async () => {
    if (inputText.trim() === '') return;

    const userMsg = { sender: 'user', text: inputText.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setHasStarted(true);

    let promptType = 'overall_analysis';
    const lowerInput = inputText.toLowerCase();
    if (lowerInput.includes('anomaly')) promptType = 'anomalies';
    else if (lowerInput.includes('hypothesis')) promptType = 'hypothesis';
    else if (lowerInput.includes('financial')) promptType = 'financials';
    else if (lowerInput.includes('taapi')) promptType = 'taapi';
    else if (lowerInput.includes('stock')) promptType = 'stock_data';
    else if (lowerInput.includes('historical')) promptType = 'historical_features';

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt_type: promptType,
          ticker: 'AAP' // Hardcoded or modify to extract from input
        }),
      });
      const data = await res.json();
      const botMsg = { sender: 'bot', text: data.reply };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: 'Error: Could not reach backend.' }
      ]);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setHasStarted(false);
    setInputText('');
  };

  return (
    <div className="chatbot-page">
      {/* Sidebar */}
      <aside className={`sidebar ${expanded ? 'expanded' : ''}`}>
        <div className="sidebar-top">
          <button onClick={() => setExpanded(!expanded)}>
            ☰ {expanded && <span className="btn-text">Menu</span>}
          </button>
          <button onClick={handleNewChat}>
            ＋ {expanded && <span className="btn-text">New Chat</span>}
          </button>
        </div>
        <div className="sidebar-bottom">
          <button>
            ⚙ {expanded && <span className="btn-text">Settings</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="chatbot-header">
          <h2 className="valora-link" onClick={() => navigate('/')}>
            Valora
          </h2>
          <button className="profiles-button" onClick={() => navigate('/companyprofile')}>
            Company Profiles
          </button>
        </header>

        <section className="chatbot-body">
          {!hasStarted && <h1>Hello, User</h1>}

          <div className="chat-scroll-container">
            {messages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.sender === 'user' ? 'user-msg' : 'bot-msg'}`}>
                {msg.text}
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>

          {/* Input Box */}
          <div className="input-box">
            <input
              type="text"
              placeholder="Ask me anything..."
              className="chat-input"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button className="send-button" onClick={sendMessage}>Send</button>
          </div>
        </section>
      </main>
    </div>
  );
}
