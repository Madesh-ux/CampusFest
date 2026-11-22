import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api, { getApiError } from '../lib/api'
import '../App.css'

function Signup() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({ student_id: '', first_name: '', last_name: '', email: '', password: '', confirmPassword: '' })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const handleSubmit = async (e) => {
    e.preventDefault(); setError('')
    if (formData.password !== formData.confirmPassword) { setError('Passwords do not match.'); return }
    setSubmitting(true)
    try {
      await api.post('/accounts/register/', { student_id: formData.student_id.trim(), first_name: formData.first_name.trim(), last_name: formData.last_name.trim(), email: formData.email.trim(), password: formData.password })
      navigate('/login', { state: { registered: true } })
    } catch (err) { setError(getApiError(err, 'Registration failed. Please check your details.')) }
    finally { setSubmitting(false) }
  }
  return <main className="auth-page"><Link className="logo auth-logo" to="/">CampusFest<span>.</span></Link><section className="auth-card"><span className="eyebrow">YOUR CAMPUS STARTS HERE</span><h1>Make your<br />first move.</h1><p className="auth-intro">Create your account with the student ID issued by your college.</p>{error && <p className="form-error" role="alert">{error}</p>}<form onSubmit={handleSubmit}><div className="form-row"><label>Student ID<input required autoComplete="off" value={formData.student_id} onChange={(e) => setFormData({ ...formData, student_id: e.target.value })} /></label><label>First name<input required autoComplete="given-name" value={formData.first_name} onChange={(e) => setFormData({ ...formData, first_name: e.target.value })} /></label></div><label>Last name <span className="optional">(optional)</span><input autoComplete="family-name" value={formData.last_name} onChange={(e) => setFormData({ ...formData, last_name: e.target.value })} /></label><label>College email<input type="email" required autoComplete="email" value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} /></label><div className="form-row"><label>Password<input type="password" required minLength="8" autoComplete="new-password" value={formData.password} onChange={(e) => setFormData({ ...formData, password: e.target.value })} /></label><label>Confirm password<input type="password" required minLength="8" autoComplete="new-password" value={formData.confirmPassword} onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })} /></label></div><button className="button button-primary auth-submit" disabled={submitting}>{submitting ? 'Creating account…' : 'Create account'}</button></form><p className="auth-switch">Already registered? <Link to="/login">Log in</Link></p></section></main>
}
export default Signup
