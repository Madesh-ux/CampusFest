import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import EventDetails from './pages/EventDetails'
import Signup from './pages/Signup'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/events/:id" element={<EventDetails />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  )
}

export default App