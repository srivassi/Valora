import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './companyprofile.css';

const companies = [
    { id: 1, name: "Apple", industry: "Technology" },
    { id: 2, name: "Eli Lilly", industry: "Healthcare" },
    { id: 3, name: "Phillips 66", industry: "Energy" },
    { id: 4, name: "Boeing", industry: "Defense" },
    { id: 5, name: "Pepsi", industry: "Consumer Goods" },
    { id: 6, name: "Mastercard", industry: "Finance" },
];

const industries = ["All", ...Array.from(new Set(companies.map(c => c.industry)))];

function CompanyProfiles() {
    const [selectedCompany, setSelectedCompany] = useState(null);
    const [selectedIndustry, setSelectedIndustry] = useState("All");
    const navigate = useNavigate();

    const filteredCompanies = selectedIndustry === "All"
        ? companies
        : companies.filter(company => company.industry === selectedIndustry);

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

            {/* filter */}
            <div className="filter-section">
                <label htmlFor="industry-filter">Filter by Industry:</label>
                <select
                    id="industry-filter"
                    value={selectedIndustry}
                    onChange={(e) => setSelectedIndustry(e.target.value)}
                >
                    {industries.map(ind => (
                        <option key={ind} value={ind}>{ind}</option>
                    ))}
                </select>
            </div>

            <div className="profiles-grid">
                {filteredCompanies.map(company => (
                    <div
                        key={company.id}
                        className={`profile-card ${selectedCompany === company.id ? 'expanded' : ''}`}
                        onClick={() =>
                            setSelectedCompany(selectedCompany === company.id ? null : company.id)
                        }
                    >
                        <h3>{company.name}</h3>
                        <p className="industry-label"><strong>Industry:</strong> {company.industry}</p>
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
