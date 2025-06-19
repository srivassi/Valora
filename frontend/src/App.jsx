import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Chatbot from './pages/Chatbot/Chatbot'
import Landing from './pages/Landing/Landing'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/chatbot" element={<Chatbot />} />
      </Routes>
    </Router>
  )
}

export default App
