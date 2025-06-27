import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './Chatbot.css';
import { marked } from 'marked';

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function Chatbot() {
  const navigate = useNavigate();
  const [expanded, setExpanded] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [hasStarted, setHasStarted] = useState(false);
  const chatEndRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(true);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const fetchSuggestions = async () => {
    try {
      const res = await fetch('http://localhost:8000/chat/suggestions');
      const data = await res.json();
      setSuggestions(data.suggestions || []);
      setShowSuggestions(true);
    } catch {
      setSuggestions([]);
    }
  };

  const sendMessage = async () => {
    if (inputText.trim() === '') return;

    const userMsg = { sender: 'user', text: inputText.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setHasStarted(true);
    setLoading(true);

    let promptType = 'overall_analysis';
    const lowerInput = inputText.toLowerCase();
    if (lowerInput.includes('anomaly')) promptType = 'anomalies';
    else if (lowerInput.includes('hypothesis')) promptType = 'hypothesis';
    else if (lowerInput.includes('financial')) promptType = 'financials';
    else if (lowerInput.includes('taapi')) promptType = 'taapi';
    else if (lowerInput.includes('stock')) promptType = 'stock_data';
    else if (lowerInput.includes('historical')) promptType = 'historical_features';

    try {
      const res = await fetch(`${apiUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt_type: promptType,
          ticker: '',
          question: inputText.trim()
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
    } finally{
      setLoading(false);
    }
  };

  const renderMessage = (msg) => {
    if (msg.sender === 'bot') {
      return (
        <div
          className="chat-message bot-msg"
          dangerouslySetInnerHTML={{ __html: marked.parse(msg.text) }}
        />
      );
    }
    return <div className="chat-message user-msg">{msg.text}</div>;
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      console.log("Sending:", inputText)
      sendMessage();
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setHasStarted(false);
    setInputText('');
    fetchSuggestions();
  };

  // Hide suggestions when user types
  const handleInputChange = (e) => {
    setInputText(e.target.value);
    if (showSuggestions) setShowSuggestions(false);
  };

  // Fill input when suggestion is clicked
  const handleSuggestionClick = (s) => {
    setInputText(s.example);
    setShowSuggestions(false);
  };

  // Fetch suggestions on first mount
  useEffect(() => {
    fetchSuggestions();
  }, []);

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
               <React.Fragment key={index}>
                 {renderMessage(msg)}
               </React.Fragment>
            ))}
            {loading && (
              <div className="chat-message bot-msg">
                <em>🔎 Analysing your request...</em>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

           {/* Suggestions Bubble */}
          {showSuggestions && suggestions.length > 0 && (
            <div className="suggestions-bubble">
              {suggestions.map((s, i) => (
                <div
                  key={i}
                  className="suggestion-btn"
                  onClick={() => handleSuggestionClick(s)}
                >
                  {s.label} <span className="example">{s.example}</span>
                </div>
              ))}
            </div>
          )}

          {/* Input Box */}
          <div className="input-box">
            <input
              type="text"
              placeholder="Ask me anything..."
              className="chat-input"
              value={inputText}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
            />
            <button className="send-button" onClick={sendMessage}>Send</button>
          </div>
        </section>
      </main>
    </div>
  );
}
