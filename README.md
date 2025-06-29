# Valora

Valora is a full-stack application for financial data analysis and chatbot interaction developed by TCS BFSI Data Lab Interns, built with FastAPI (backend) and React (frontend).
 
## Project Structure

- `backend/`: FastAPI server for data processing, analysis, and chatbot services.
- `frontend/`: React app for user interface and interaction.

## Backend

- **Tech Stack:** Python, FastAPI, Pandas, Scikit-learn, yFinance, Google Generative AI.
- **Key Features:**
  - Financial data ingestion and ratio analysis.
  - Company data APIs.
  - Chatbot service for financial queries.
- **Setup:**
  1. Navigate to `backend/`.
  2. Install dependencies:
     ```
     pip install -r requirements.txt
     ```
  3. Run the server:
     ```
     uvicorn main:app --reload
     ```

## Frontend

- **Tech Stack:** React, Tailwind CSS, Vite.
- **Setup:**
  1. Navigate to `frontend/`.
  2. Install dependencies:
     ```
     npm install
     ```
  3. Start the development server:
     ```
     npm run dev
     ```

## Development

- Backend endpoints are defined in `backend/services/api/`.
- Data processing modules are in `backend/services/` and `backend/data_ingestion/`.
- Frontend pages are in `frontend/src/pages/`.
- Acess the full deployed application at [Valora](https://valoranalytics-995650517009.europe-west1.run.app/).

## License

This project is for educational and internal use.
