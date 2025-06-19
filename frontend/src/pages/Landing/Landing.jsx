import { Link } from 'react-router-dom';

export default function Landing() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-gray-100 to-white text-gray-800">
      <h1 className="text-4xl font-bold mb-4">Welcome to Gemini Chat Demo</h1>
      <p className="mb-8 text-lg text-center max-w-md">
        This simple chatbot interface connects to Google's Gemini 2.5 Flash model via FastAPI.
        Click below to start chatting!
      </p>
      <Link
        to="/chatbot"
        className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
      >
        Go to Chatbot
      </Link>
    </div>
  );
}
