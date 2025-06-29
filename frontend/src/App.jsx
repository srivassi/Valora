import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import ChatbotPage from './pages/Chatbot/Chatbot';
import CompanyProfile from './pages/CompanyProfile/CompanyProfile';
import './App.css';

function LandingPage() {
    const navigate = useNavigate();

    return (
        <div className="app">
            <nav className="navbar">
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About Us</a></li>
                    <li><a href="#chatbot">Chatbot</a></li>
                </ul>
            </nav>

            <div className="content">
                <section id="home" className="section">
                    <h1>Valora</h1>
                    <h3>A financial analyst AI chatbot powered by TCS Spring Interns</h3>
                </section>

                <section id="about" className="section about-section">
                    <h1 className="about-title">What are we?</h1>
                    <h3 className="about-subtitle">About Information</h3>
                    <p className="about-description">
                        We’re exploring how far large language models can go when it comes to financial statement analysis. Inspired by research from AWS, our project investigates whether GPT-4 can analyse standardised, anonymised financial data and predict the direction of future earnings - without relying on industry context or narrative explanations.
                        <br/> <br/>The ambition doesn’t stop there. We also aim to connect these predictions with actual stock performance over time, helping us assess each company’s future potential - or as we like to call it, its “bankability.”
                    </p>

                    <h3 className="our-services">Our Services</h3>

                    <div className="services-container">
                        <div className="service-box">
                            <h4>Company Profile Information</h4>
                            <p>
                                 In this section, you'll find a curated set of anonymised company profiles, each built from real financial statements. The data has been standardised and stripped of any identifying or contextual information to keep things fair - and focused purely on performance. These profiles are the foundation for both human and AI analysis.
                            </p>
                            <button className="profile-btn" onClick={() => navigate('/companyprofile')}>
                                &#10140; More Company Profiles
                            </button>
                        </div>

                        <div className="service-box">
                            <h4>Chatbot Information</h4>
                            <p>
                                Our custom-built chatbot, powered by Google Gemini, analyses the company data with surprising clarity. Using just the numbers, it forecasts earnings direction and provides insight into each company’s financial outlook.Add commentMore actions
                                <br/><br/>It's part analyst, part predictor - and all data-driven. Think of it as a quiet overachiever with a sharp eye for trends (and no need for coffee breaks).
                            </p>
                        </div>
                    </div>
                </section>

                <section id="chatbot" className="section chatbot-section">
                    <h1 className="chatbot-title">Ready to get started?</h1>
                    <p className="chatbot-subtitle">
                        Give your data a voice, narrate the numbers,<br />
                        and drive strategic action
                    </p>

                    <div className="chatbot-card">
                        <div className="chatbot-card-header">
                            <span className="dot">●</span>
                            <strong>Valora</strong>
                            <button className="close-btn">×</button>
                        </div>
                        <p className="chatbot-card-text">
                            Your NYSE stock analysis report (Q1–Q3 2025) is ready.
                        </p>
                    </div>

                    <button className="chatbot-button" onClick={() => navigate('/chatbot')}>
                        Talk to Valora
                    </button>

                    <footer className="chatbot-footer">
                        <a
                            href="https://valoranalytics-995650517009.europe-west1.run.app">Look Under the Hood</a>
                        <a href="https://www.tcs.com/what-we-do/products-platforms/tcs-bfsi-platforms" target="_blank"
                           rel="noopener noreferrer">
                            About TCS
                        </a>
                    </footer>
                </section>
            </div>
        </div>
    );
}

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/chatbot" element={<ChatbotPage />} />
                <Route path="/companyprofile" element={<CompanyProfile />} />
            </Routes>
        </Router>
    );
}

export default App;
