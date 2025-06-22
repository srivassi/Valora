import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './chatbot.css';

export default function Chatbot() {
  const navigate = useNavigate();
  const [expanded, setExpanded] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [hasStarted, setHasStarted] = useState(false);

  const handleKeyDown = async (e) => {
      if (e.key === 'Enter' && inputText.trim() !== '') {
          const userMsg = { sender: 'user', text: inputText.trim() };
          setMessages((prev) => [...prev, userMsg]);
          setInputText('');
          setHasStarted(true);

          // Determine prompt_type based on user input
            let promptType = 'overall_analysis'; // Default
            const lowerInput = inputText.toLowerCase();
            if (lowerInput.includes('anomaly')) {
                promptType = 'anomalies';
            } else if (lowerInput.includes('hypothesis')) {
                promptType = 'hypothesis';
            } else if (lowerInput.includes('financial')) {
                promptType = 'financials';
            } else if (lowerInput.includes('taapi')) {
                promptType = 'taapi';
            } else if (lowerInput.includes('stock')) {
                promptType = 'stock_data';
            } else if (lowerInput.includes('historical')) {
                promptType = 'historical_features';
            }

          try {
              const res = await fetch('http://localhost:8000/chat', {
                  method: 'POST',
                  headers: {'Content-Type': 'application/json'},
                  body: JSON.stringify({
                      prompt_type: promptType,
                      ticker: inputText.trim()
                  }),
              });
              const data = await res.json();
              const botMsg = {sender: 'bot', text: data.reply};
              setMessages((prev) => [...prev, botMsg]);
          } catch (err) {
              setMessages((prev) => [
                  ...prev,
                  {sender: 'bot', text: 'Error: Could not reach backend.'}
              ]);
          }
      }
  };

  // new chat btn + reset everything
    const handleNewChat = () => {
        setMessages([]);
        setHasStarted(false);
        setInputText('');
    };


  return (
        <div className="chatbot-page">

            {/* sidebar */}
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

            {/* main content */}
            <main className="main-content">
                <header className="chatbot-header">
                    <h2 className="valora-link" onClick={() => navigate('/')}>
                        Valora
                    </h2>
                    <button className="profiles-button">Company Profiles</button>
                </header>

                <section className="chatbot-body">
                    {!hasStarted && <h1>Hello, User</h1>}

                    {/* show chat display if started */}
                    {hasStarted && (
                        <div className="chat-display">
                            {messages.map((msg, index) => (
                                <div
                                    key={index}
                                    className={`chat-message ${msg.sender === 'user' ? 'user-msg' : 'bot-msg'}`}
                                >
                                    {msg.text}
                                </div>
                            ))}
                        </div>
                    )}

                    {/* input box */}
                    <div className="input-box">
                        <input
                            type="text"
                            placeholder="Ask me anything..."
                            className="chat-input"
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            onKeyDown={handleKeyDown}
                        />
                    </div>
                </section>
            </main>
        </div>
    );
}
