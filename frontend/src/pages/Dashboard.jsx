import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api, { getApiError } from '../lib/api'
import '../App.css'

function Dashboard() {
  const navigate = useNavigate()
  const [student, setStudent] = useState(null)
  const [registrations, setRegistrations] = useState({ individual_registrations: [], team_registrations: [] })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  useEffect(() => {
    if (!localStorage.getItem('access_token')) { navigate('/login', { replace: true }); return }
    Promise.all([api.get('/accounts/profile/'), api.get('/accounts/my-registrations/')])
      .then(([profile, history]) => { setStudent(profile.data); setRegistrations(history.data) })
      .catch((err) => { if (err.response?.status === 401) { localStorage.removeItem('access_token'); navigate('/login', { replace: true }) } else setError(getApiError(err, 'Unable to load your dashboard.')) })
      .finally(() => setLoading(false))
  }, [navigate])
  const logout = () => { localStorage.removeItem('access_token'); localStorage.removeItem('refresh_token'); navigate('/') }
  if (loading) return <main className="page-shell"><p className="state-card">Loading your dashboard…</p></main>
  return <><nav className="navbar"><Link className="logo" to="/">CampusFest<span>.</span></Link><div className="nav-buttons"><Link className="button button-outline" to="/">Browse events</Link><button className="button button-primary" onClick={logout}>Log out</button></div></nav><main className="dashboard-shell"><header className="dashboard-welcome"><div><span className="eyebrow">YOUR CAMPUS, YOUR CALENDAR</span><h1>Hey{student?.first_name ? `, ${student.first_name}` : ''}.</h1><p>Here's what you've signed up for.</p></div><div className="student-chip"><span>STUDENT ID</span><strong>{student?.student_id}</strong></div></header>{error && <p className="form-error">{error}</p>}<section className="registration-section"><div className="section-heading compact"><div><span className="eyebrow">YOUR SIGN UPS</span><h2>Individual events</h2></div><span className="count-badge">{registrations.individual_registrations.length}</span></div>{registrations.individual_registrations.length ? <div className="registration-list">{registrations.individual_registrations.map((item, index) => <article className="registration-item" key={`${item.event}-${index}`}><div><h3>{item.event}</h3><p>{item.date} <span>·</span> {item.venue}</p></div><span className="pill">Registered</span></article>)}</div> : <div className="empty-state"><p>No individual registrations yet.</p><Link className="text-link" to="/#events">Find an event →</Link></div>}</section><section className="registration-section"><div className="section-heading compact"><div><span className="eyebrow">YOUR SIGN UPS</span><h2>Team events</h2></div><span className="count-badge">{registrations.team_registrations.length}</span></div>{registrations.team_registrations.length ? <div className="registration-list">{registrations.team_registrations.map((item, index) => <article className="registration-item" key={`${item.team}-${index}`}><div><h3>{item.event}</h3><p>{item.team} <span>·</span> Captain: {item.captain}</p><p>{item.date} <span>·</span> {item.venue}</p></div><span className="pill">Team member</span></article>)}</div> : <div className="empty-state"><p>No team registrations yet.</p><Link className="text-link" to="/#events">Find a team event →</Link></div>}</section></main></>
}
export default Dashboard
