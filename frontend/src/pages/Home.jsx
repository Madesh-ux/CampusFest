import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api, { getApiError } from '../lib/api'
import '../App.css'

function Home() {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  useEffect(() => {
    let active = true
    setLoading(true)
    api.get('/events/', { params: { search: search || undefined, category: category || undefined } })
      .then(({ data }) => { if (active) setEvents(data) })
      .catch((err) => { if (active) setError(getApiError(err, 'Unable to load events. Please try again later.')) })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [search, category])

  return (
    <>
      <nav className="navbar">
        <Link className="logo" to="/">CampusFest<span>.</span></Link>
        <div className="nav-links"><a href="#events">Events</a><a href="#about">About</a></div>
        <div className="nav-buttons">{localStorage.getItem('access_token') ? <Link className="button button-outline" to="/dashboard">My dashboard</Link> : <><Link className="button button-outline" to="/login">Log in</Link><Link className="button button-primary" to="/signup">Sign up</Link></>}</div>
      </nav>
      <main>
        <section className="hero">
          <span className="eyebrow">YOUR CAMPUS, IN MOTION</span>
          <h1>Make room for<br /><em>something memorable.</em></h1>
          <p>Find your next competition, show, workshop, or campus tradition. Your people are already there.</p>
          <a className="button button-primary hero-cta" href="#events">Explore events <span>↓</span></a>
          <div className="hero-orbit orbit-one" /><div className="hero-orbit orbit-two" />
        </section>
        <section className="events-section" id="events">
          <div className="section-heading"><div><span className="eyebrow">WHAT'S HAPPENING</span><h2>Find your kind of event.</h2></div><p>Pick a date. Bring your people. Make it count.</p></div>
          <div className="event-filters"><input aria-label="Search events" placeholder="Search events…" value={search} onChange={(e) => setSearch(e.target.value)} /><select aria-label="Filter by category" value={category} onChange={(e) => setCategory(e.target.value)}><option value="">All categories</option>{[...new Set(events.map((event) => event.category))].sort().map((item) => <option key={item} value={item}>{item}</option>)}</select></div>
          {loading ? <p className="state-card">Loading events…</p> : error ? <p className="state-card error-text">{error}</p> : events.length === 0 ? <p className="state-card">No events match your search yet.</p> : <div className="events-container">{events.map((event, index) => <article className="event-card" key={event.id}><div className={`event-art art-${index % 4}`}><span>{event.category}</span><b>{String(index + 1).padStart(2, '0')}</b></div><div className="event-card-body"><div className="event-meta"><span>{event.date}</span><span>{event.registration_type === 'TEAM' ? 'Team' : 'Individual'}</span></div><h3>{event.name}</h3><p>{event.description}</p><div className="card-footer"><span>{event.venue}</span><Link to={`/events/${event.id}`} aria-label={`View ${event.name}`}>View event <span>↗</span></Link></div></div></article>)}</div>}
        </section>
        <section className="about-section" id="about"><span className="eyebrow">CAMPUSFEST</span><h2>Good things happen<br />when we show up.</h2><p>A home for campus events and the people who make them unforgettable. Browse what's on and sign up in a few clicks.</p><Link className="text-link" to="/signup">Join the community →</Link></section>
      </main>
      <footer className="site-footer"><Link className="logo" to="/">CampusFest<span>.</span></Link><span>Made for campus life.</span><a href="#events">Back to events ↑</a></footer>
    </>
  )
}

export default Home
