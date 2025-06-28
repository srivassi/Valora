import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './CompanyProfile.css';
import companyData from '../../data/useful_database/company_bubbles.json';

const industries = ["All", ...Array.from(new Set(companyData.map(c => c.industry)))];

function ReturnsLineGraph({ returns }) {
    const periods = ['1y', '3y', '5y'];
    const values = periods.map(p => returns?.[p] ?? 0);
    const minY = Math.min(...values, 0);
    const maxY = Math.max(...values, 0);
    const width = 220, height = 200, padding = 40;
    const x = i => padding + i * ((width - 2 * padding) / (periods.length - 1));
    const y = v => height - padding - ((v - minY) / (maxY - minY || 1)) * (height - 2 * padding);

    const [progress, setProgress] = useState(0);
    const rafRef = useRef();

    useEffect(() => {
        setProgress(0);
        let start;
        function animate(ts) {
            if (!start) start = ts;
            const elapsed = ts - start;
            const duration = 1200; // ms
            const p = Math.min(1, elapsed / duration);
            setProgress(p);
            if (p < 1) rafRef.current = requestAnimationFrame(animate);
        }
        rafRef.current = requestAnimationFrame(animate);
        return () => cancelAnimationFrame(rafRef.current);
    }, [returns]);

    // Interpolate line and points
    const totalLength = periods.length - 1;
    const current = progress * totalLength;
    const linePoints = [];
    for (let i = 0; i < periods.length; i++) {
        if (i < current) {
            linePoints.push([x(i), y(values[i])]);
        } else if (i - 1 < current && i > 0) {
            // Interpolate between last and current
            const frac = current - (i - 1);
            const xPrev = x(i - 1), yPrev = y(values[i - 1]);
            const xCurr = x(i), yCurr = y(values[i]);
            linePoints.push([
                xPrev + (xCurr - xPrev) * frac,
                yPrev + (yCurr - yPrev) * frac
            ]);
            break;
        }
    }

    return (
        <svg width={width} height={height}>
            {/* Y axis */}
            <line x1={padding} y1={padding} x2={padding} y2={height - padding} stroke="#aaa" />
            {/* X axis */}
            <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="#aaa" />

            {/* Y axis labels and ticks */}
            {[minY, maxY].map((v, i) => (
                <g key={i}>
                    <text x={padding - 10} y={y(v) + 4} fontSize="12" textAnchor="end" fill="#888">{v.toFixed(0)}%</text>
                    <line x1={padding - 5} y1={y(v)} x2={padding} y2={y(v)} stroke="#aaa" />
                </g>
            ))}

            {/* X axis labels and ticks */}
            {periods.map((p, i) => (
                <g key={p}>
                    <text x={x(i)} y={height - padding + 20} fontSize="12" textAnchor="middle">{p}</text>
                    <line x1={x(i)} y1={height - padding} x2={x(i)} y2={height - padding + 5} stroke="#aaa" />
                </g>
            ))}

            {/* Axis labels */}
            <text x={width / 2} y={height - 5} fontSize="13" textAnchor="middle" fill="#333">Period</text>
            <text x={padding - 30} y={height / 2} fontSize="13" textAnchor="middle" fill="#333" transform={`rotate(-90,${padding - 30},${height / 2})`}>Return (%)</text>

            {/* Animated returns line */}
            {linePoints.length > 1 && (
                <polyline
                    fill="none"
                    stroke="#735a8c"
                    strokeWidth="3"
                    points={linePoints.map(([px, py]) => `${px},${py}`).join(' ')}
                />
            )}
            {/* Animated points */}
            {linePoints.map(([px, py], i) => (
                <circle key={i} cx={px} cy={py} r={5} fill="#735a8c" />
            ))}
        </svg>
    );
}

function CompanyProfiles() {
    const [selectedCompany, setSelectedCompany] = useState(null);
    const [selectedIndustry, setSelectedIndustry] = useState("All");
    const navigate = useNavigate();

    const filteredCompanies = selectedIndustry === "All"
        ? companyData
        : companyData.filter(company => company.industry === selectedIndustry);

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
                    Discover financial summaries and insights from leading NYSE companies.
                    Click to view additional financial information
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
                {filteredCompanies.map((company, idx) => (
                    <div
                        key={company.ticker}
                        className={`profile-card ${selectedCompany === idx ? 'expanded' : ''}`}
                        onClick={() =>
                            setSelectedCompany(selectedCompany === idx ? null : idx)
                        }
                    >
                        <h3>{company.company} ({company.ticker})</h3>
                        <ReturnsLineGraph returns={company.returns} />
                        <p className="industry-label"><strong>Industry:</strong> {company.industry}</p>
                        {selectedCompany === idx && (
                            <div className="company-details">
                                <p><strong>Price:</strong> ${company.price}</p>
                                <p><strong>Revenue:</strong> ${company.revenue}B</p>
                                <p><strong>Market Cap:</strong> ${company.market_cap}B</p>
                                <p><strong>P/E Ratio:</strong> {isNaN(company.pe_ratio) ? 'N/A' : company.pe_ratio}</p>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default CompanyProfiles;
