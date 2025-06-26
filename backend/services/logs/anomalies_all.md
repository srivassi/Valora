# Prompt Type: anomalies
## Identifier: all

### Prompt:
```

You are a financial analyst reviewing anomalies in company financials.

Detected anomalies:
- AAL (2015-12-31): ROA=1.2762797166693247, D/E=3.550929227825881
- ABBV (2013-12-31): ROA=1.0519098832221028, D/E=2.213508795503248
- ABC (2013-09-30): ROA=-0.6298857460489029, D/E=3.271944702120092
- ADI (2013-11-02): ROA=0.5429718642375414, D/E=-1.081404818697005
- ADI (2014-11-01): ROA=0.3471626216973197, D/E=-1.0204955788747718


Instructions:
- Bullet each anomaly (≤10 words)
- Note likely cause (e.g. market vs mismanagement)
- Finish with 2 investor recommendations
- Use concise, clear professional tone

```

### Gemini Response:
Here's an analysis of the detected anomalies:

*   **AAL (2015-12-31): Exceptionally high ROA with elevated leverage.**
    *   **Likely Cause:** Highly probable data error or a one-off, non-recurring accounting event; an ROA over 100% is not sustainable for a typical airline.
    *   **Recommendations:**
        1.  Verify the accuracy of the reported ROA against audited financial statements.
        2.  If confirmed, analyze specific non-operating items driving such extraordinary profitability.

*   **ABBV (2013-12-31): Extreme ROA and high initial leverage post-spin-off.**
    *   **Likely Cause:** Accounting distortions due to the company's spin-off from Abbott, potentially non-cash gains or asset revaluations impacting early ROA.
    *   **Recommendations:**
        1.  Examine detailed financial statements from the spin-off period for one-time accounting adjustments.
        2.  Focus analysis on normalized performance and trends in subsequent periods.

*   **ABC (2013-09-30): Significant net loss with substantial leverage.**
    *   **Likely Cause:** Indicates operational challenges or a large one-time write-off/impairment, eroding profitability while maintaining high debt.
    *   **Recommendations:**
        1.  Investigate specific drivers of the net loss, distinguishing operational issues from non-recurring charges.
        2.  Assess the company's liquidity position and ability to service debt given the significant loss.

*   **ADI (2013-11-02): Unusual negative D/E ratio despite strong ROA.**
    *   **Likely Cause:** Negative shareholder equity, likely due to accumulated losses or aggressive capital return strategies (e.g., share buybacks) exceeding retained earnings.
    *   **Recommendations:**
        1.  Conduct a thorough balance sheet analysis to understand factors leading to negative equity.
        2.  Evaluate the company's long-term solvency and capital structure sustainability.

*   **ADI (2014-11-01): Continued negative D/E ratio.**
    *   **Likely Cause:** Persistence of negative shareholder equity, indicating a structural balance sheet issue requiring investigation into capital management.
    *   **Recommendations:**
        1.  Analyze cash flow statements for insights into financing activities and capital sources.
        2.  Monitor management actions to restore positive equity and improve financial stability.
