import { useEffect, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import api, { getApiError } from '../lib/api'
import '../App.css'

function EventDetails() {
  const navigate = useNavigate()
  const { id } = useParams()
  const [event, setEvent] = useState(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [team, setTeam] = useState({ team_name: '', captain_student_id: '', member_student_ids: '' })

  useEffect(() => {
    let active = true
    api.get(`/events/${id}/`)
      .then(({ data }) => { if (active) setEvent(data) })
      .catch((err) => { if (active) setError(getApiError(err, 'Unable to load event details.')) })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [id])

  const handleRegister = async (e) => {
    e.preventDefault()
    setError('')
    setNotice('')
    if (!localStorage.getItem('access_token')) {
      navigate('/login', { state: { from: `/events/${id}` } })
      return
    }
    setSubmitting(true)
    setNotice('')
    try {
      if (event.registration_type === 'TEAM') {
        const member_student_ids = team.member_student_ids.split(/[\n,]+/).map((value) => value.trim()).filter(Boolean)
        await api.post('/events/register/team/', { ...team, member_student_ids, event_id: Number(id) })
      } else {
        await api.post('/events/register/individual/', { event_id: Number(id) })
      }
      setNotice('Registration successful. You can view it in your dashboard.')
    } catch (err) {
      setError(getApiError(err, 'Registration failed.'))
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <main className="page-shell"><p className="state-card">Loading event details…</p></main>
  if (error && !event) return <main className="page-shell"><p className="state-card error-text">{error}</p><Link className="text-link" to="/">Back to events</Link></main>

  return (
    <main className="page-shell">
      <Link className="text-link back-link" to="/">← All events</Link>
      <article className="detail-card">
        <div className="detail-heading"><span className="eyebrow">{event.category}</span><span className="pill">{event.registration_type === 'TEAM' ? 'Team event' : 'Individual event'}</span></div>
        <h1>{event.name}</h1>
        <p className="detail-description">{event.description}</p>
        <div className="detail-facts"><div><span>Date</span><strong>{event.date}</strong></div><div><span>Venue</span><strong>{event.venue}</strong></div>{event.registration_type === 'TEAM' && <div><span>Team size</span><strong>{event.min_team_size}–{event.max_team_size} members</strong></div>}</div>
        {notice && <p className="notice" role="status">{notice}</p>}
        {error && <p className="form-error" role="alert">{error}</p>}
        {event.registration_type === 'TEAM' ? (
          <form className="registration-form" onSubmit={handleRegister}>
            <h2>Register your team</h2>
            <label>Team name<input required maxLength="100" value={team.team_name} onChange={(e) => setTeam({ ...team, team_name: e.target.value })} /></label>
            <label>Team member student IDs<textarea required rows="3" placeholder="Separate IDs with commas or new lines" value={team.member_student_ids} onChange={(e) => setTeam({ ...team, member_student_ids: e.target.value })} /></label>
            <label>Captain student ID<input required value={team.captain_student_id} onChange={(e) => setTeam({ ...team, captain_student_id: e.target.value })} /></label>
            <button className="button button-primary" disabled={submitting}>{submitting ? 'Submitting…' : 'Register team'}</button>
          </form>
        ) : <button className="button button-primary" onClick={handleRegister} disabled={submitting}>{submitting ? 'Submitting…' : 'Register for event'}</button>}
      </article>
    </main>
  )
}

export default EventDetails
