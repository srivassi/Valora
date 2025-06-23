import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './companyprofile.css';

const companies = [
    { id: 1, name: "Apple Inc." },
    { id: 2, name: "Amazon" },
    { id: 3, name: "Google" },
    { id: 4, name: "Tesla" },
    { id: 5, name: "Meta" }
];

function CompanyProfiles() {
    const [selectedCompany, setSelectedCompany] = useState(null);
    const navigate = useNavigate();

    return (
        <div className="profiles-page">
            <header className="chatbot-header">
                <h2 className="valora-link" onClick={() => navigate('/')}>
                    Valora
                </h2>
                <button
                    className="profiles-button"
                    onClick={() => navigate('/chatbot')}
                >
                    Chatbot
                </button>
            </header>

            {/*introduction*/}
            <div className="profiles-intro">
                <h1 className="profiles-title">Explore Company Financial Profiles</h1>
                <p className="profiles-description">
                    Discover financial summaries and insights from leading NYSE companies. Click on a company to view key financial info and trends (placeholder data).
                </p>
            </div>

            <div className="profiles-grid">
                {companies.map(company => (
                    <div
                        key={company.id}
                        className={`profile-card ${selectedCompany === company.id ? 'expanded' : ''}`}
                        onClick={() =>
                            setSelectedCompany(selectedCompany === company.id ? null : company.id)
                        }
                    >
                        <h3>{company.name}</h3>
                        {selectedCompany === company.id && (
                            <div className="company-details">
                                <p>📊 Placeholder for financial metrics and insights...</p>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default CompanyProfiles;
