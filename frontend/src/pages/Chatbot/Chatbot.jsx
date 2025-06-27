import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './chatbot.css';
import { marked } from 'marked';

export default function Chatbot() {
  const navigate = useNavigate();
  const [expanded, setExpanded] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [hasStarted, setHasStarted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Detect prompt type based on keywords
  const detectPromptType = (text) => {
    const msg = text.toLowerCase();
    if (msg.includes('compare') || msg.includes('vs')) return 'compare';
    if (msg.includes('anomal')) return 'anomalies';
    if (msg.includes('enhanced hypothesis') || msg.includes('signal')) return 'enhanced_hypothesis';
    if (msg.includes('hypothesis')) return 'hypothesis';
    if (msg.includes('pros') || msg.includes('cons')) return 'pros_cons';
    if (msg.includes('score')) return 'score';
    if (msg.includes('trend')) return 'stock_trend';
    if (msg.includes('financial')) return 'financials';
    if (msg.includes('taapi')) return 'taapi';
    if (msg.includes('feature')) return 'historical_features';
    if (msg.includes('stock')) return 'stock_data';
    if (msg.includes('overall')) return 'overall_analysis';
    return 'ratios'; // fallback
  };

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
    const cleanedInput = inputText.trim();
    if (!cleanedInput) return;

    const userMsg = { sender: 'user', text: cleanedInput };
    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setHasStarted(true);
    setLoading(true);

    const promptType = detectPromptType(cleanedInput);

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt_type: promptType,
          ticker: cleanedInput,
          persona: 'general',
          question: cleanedInput
        }),
      });

      const data = await res.json();
      const botMsg = { sender: 'bot', text: data.reply || '⚠️ No response received.' };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error('Backend error:', err);
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: '❌ Error: Could not reach backend.' }
      ]);
    } finally {
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
    if (e.key === 'Enter') sendMessage();
  };

  const handleNewChat = () => {
    setMessages([]);
    setHasStarted(false);
    setInputText('');
    fetchSuggestions();
  };

  const handleInputChange = (e) => {
    setInputText(e.target.value);
    if (showSuggestions) setShowSuggestions(false);
  };

  const handleSuggestionClick = (s) => {
    setInputText(s.example);
    setShowSuggestions(false);
  };

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

      {/* Main Chat Section */}
      <main className="main-content">
        <header className="chatbot-header">
          <h2 className="valora-link" onClick={() => navigate('/')}>Valora</h2>
          <button className="profiles-button" onClick={() => navigate('/companyprofile')}>
            Company Profiles
          </button>
        </header>

        <section className="chatbot-body">
          {!hasStarted && <h1>Hello, User</h1>}

          <div className="chat-scroll-container">
            {messages.map((msg, index) => (
              <React.Fragment key={index}>{renderMessage(msg)}</React.Fragment>
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
              placeholder="Ask me anything about a company..."
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
