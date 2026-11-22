import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import api, { getApiError } from '../lib/api'
import '../App.css'

function Login() {
  const navigate = useNavigate()
  const location = useLocation()
  const [formData, setFormData] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const handleSubmit = async (e) => {
    e.preventDefault(); setError(''); setSubmitting(true)
    try {
      const { data } = await api.post('/accounts/login/', formData)
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      navigate(location.state?.from || '/dashboard', { replace: true })
    } catch (err) { setError(getApiError(err, 'Login failed. Check your email and password.')) }
    finally { setSubmitting(false) }
  }
  return <main className="auth-page"><Link className="logo auth-logo" to="/">CampusFest<span>.</span></Link><section className="auth-card"><span className="eyebrow">WELCOME BACK</span><h1>Pick up where<br />the fun starts.</h1><p className="auth-intro">Log in to manage your campus registrations.</p>{location.state?.registered && <p className="notice" role="status">Account created. Log in to continue.</p>}{error && <p className="form-error" role="alert">{error}</p>}<form onSubmit={handleSubmit}><label>Email address<input type="email" autoComplete="email" required value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} /></label><label>Password<input type="password" autoComplete="current-password" required value={formData.password} onChange={(e) => setFormData({ ...formData, password: e.target.value })} /></label><button className="button button-primary auth-submit" disabled={submitting}>{submitting ? 'Logging in…' : 'Log in'}</button></form><p className="auth-switch">New around here? <Link to="/signup">Create an account</Link></p></section></main>
}
export default Login
