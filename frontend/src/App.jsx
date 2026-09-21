import { useRef, useState } from 'react'
import './index.css'

const API_URL = (import.meta.env.VITE_API_URL || 'https://resume-analyzer-1-l0rv.onrender.com').replace(/\/$/, '')
const emptyResume = { name: '', email: '', skills: [], education: [], work_experience: [] }

function Icon({ children, size = 18 }) {
  return <span className="icon" style={{ fontSize: size }} aria-hidden="true">{children}</span>
}

function Field({ label, value }) {
  return <div className="detail-field"><span>{label}</span><strong>{value || 'Not detected'}</strong></div>
}

function normalizeList(value) {
  if (!value) return []
  return Array.isArray(value) ? value : [value]
}

function App() {
  const inputRef = useRef(null)
  const [file, setFile] = useState(null)
  const [resume, setResume] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const selectFile = (nextFile) => {
    if (!nextFile) return
    if (nextFile.type !== 'application/pdf' && !['image/jpeg', 'image/png'].includes(nextFile.type)) {
      setError('Please choose a PDF, JPG, or PNG file.')
      return
    }
    setFile(nextFile)
    setResume(null)
    setError('')
  }

  const parseResume = async () => {
    if (!file) {
      setError('Choose a resume before starting the analysis.')
      return
    }
    setLoading(true)
    setError('')
    try {
      const body = new FormData()
      body.append('file', file)
      const response = await fetch(`${API_URL}/parse-resume`, { method: 'POST', body })
      const payload = await response.json().catch(() => ({}))
      if (!response.ok) throw new Error(payload.detail || 'The resume could not be analyzed.')
      setResume({ ...emptyResume, ...payload })
    } catch (requestError) {
      setError(requestError.message || 'Something went wrong while analyzing the resume.')
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setFile(null)
    setResume(null)
    setError('')
    if (inputRef.current) inputRef.current.value = ''
  }

  const education = normalizeList(resume?.education)
  const work = normalizeList(resume?.work_experience)

  return (
    <main className="app-shell">
      <nav className="topbar">
        <div className="brand"><div className="brand-mark"><Icon>✦</Icon></div><div><strong>Resume Analyzer</strong><small>AI-powered resume parsing</small></div></div>
        <div className="status"><i /> No login required</div>
      </nav>

      {!resume ? (
        <section className="hero-panel">
          <div className="eyebrow"><Icon size={14}>✧</Icon> Smart resume parser</div>
          <h1>Turn your resume into<br /><em>structured data.</em></h1>
          <p className="intro">Upload your resume and let our parser extract your personal details,<br className="desktop-only" /> skills, education, and work experience.</p>

          <div className={`dropzone ${file ? 'has-file' : ''}`} onDrop={(event) => { event.preventDefault(); selectFile(event.dataTransfer.files[0]) }} onDragOver={(event) => event.preventDefault()} onClick={() => inputRef.current?.click()} role="button" tabIndex="0" onKeyDown={(event) => event.key === 'Enter' && inputRef.current?.click()}>
            <input ref={inputRef} type="file" accept=".pdf,.jpg,.jpeg,.png" onChange={(event) => selectFile(event.target.files[0])} />
            {file ? <div className="file-row" onClick={(event) => event.stopPropagation()}><div className="file-icon"><Icon>▤</Icon></div><div className="file-copy"><strong>{file.name}</strong><span>{(file.size / 1024).toFixed(1)} KB</span></div><button className="remove-button" type="button" aria-label="Remove file" onClick={reset}>×</button></div> : <><div className="upload-icon"><Icon size={26}>↑</Icon></div><strong>Drop your resume here</strong><span>or click to browse your files</span><small>PDF, JPG or PNG · up to 10 MB</small></>}
          </div>

          {error && <div className="error-message"><Icon>!</Icon>{error}</div>}
          <button className="primary-button" type="button" onClick={parseResume} disabled={loading}><Icon>{loading ? '◌' : '✧'}</Icon>{loading ? 'Analyzing resume...' : 'Analyze resume'}<span className="button-arrow">→</span></button>

          <div className="feature-grid"><div><span className="feature-icon">ϟ</span><div><strong>Fast processing</strong><small>Extract resume information quickly.</small></div></div><div><span className="feature-icon">⌑</span><div><strong>Simple & private</strong><small>No account or login required.</small></div></div><div><span className="feature-icon">▤</span><div><strong>Structured output</strong><small>Clear and consistent JSON.</small></div></div></div>
          <p className="formats"><Icon size={13}>ⓘ</Icon> Supported formats: PDF, JPG and PNG</p>
        </section>
      ) : (
        <section className="results-panel">
          <div className="results-heading"><div><div className="eyebrow"><Icon size={14}>✧</Icon> Analysis complete</div><h1>Resume <em>insights.</em></h1><p>Structured information extracted from your document.</p></div><button className="secondary-button" type="button" onClick={reset}>＋ Analyze another</button></div>
          <div className="source-strip"><span className="file-icon small"><Icon size={16}>▤</Icon></span><div><strong>{file?.name}</strong><small>Parsed just now</small></div><span className="success-pill"><i /> Ready</span></div>
          <div className="summary-card"><div className="avatar">{(resume.name || 'R').charAt(0).toUpperCase()}</div><div><span className="section-kicker">Candidate</span><h2>{resume.name || 'Name not detected'}</h2><p>{resume.email || 'Email not detected'}</p></div></div>

          <div className="result-grid">
            <section className="result-card"><div className="card-heading"><span className="section-icon">◎</span><div><span className="section-kicker">01 · Contact</span><h2>Personal details</h2></div></div><div className="details-grid"><Field label="Full name" value={resume.name} /><Field label="Email address" value={resume.email} /></div></section>
            <section className="result-card"><div className="card-heading"><span className="section-icon">✦</span><div><span className="section-kicker">02 · Expertise</span><h2>Skills</h2></div></div><div className="skill-list">{resume.skills?.length ? resume.skills.map((skill) => <span key={skill}>{skill}</span>) : <p className="empty-state">No skills detected.</p>}</div></section>
            <section className="result-card wide-card"><div className="card-heading"><span className="section-icon">▣</span><div><span className="section-kicker">03 · Background</span><h2>Work experience</h2></div></div>{work.length ? <div className="timeline">{work.map((item, index) => <article className="timeline-item" key={`${item.company}-${index}`}><div className="timeline-dot" /><div><div className="item-topline"><h3>{item.position || 'Position not detected'}</h3><span>{item.years || 'Dates not detected'}</span></div><strong>{item.company || 'Company not detected'}</strong>{item.description && <p>{item.description}</p>}</div></article>)}</div> : <p className="empty-state">No work experience detected.</p>}</section>
            <section className="result-card wide-card"><div className="card-heading"><span className="section-icon">⌂</span><div><span className="section-kicker">04 · Education</span><h2>Education</h2></div></div>{education.length ? <div className="education-list">{education.map((item, index) => <article key={`${item.degree}-${index}`}><div className="school-badge">⌂</div><div><h3>{item.degree || 'Degree not detected'}</h3><strong>{item.college || item.school || 'Institution not detected'}</strong><p>{[item.start_year, item.end_year].filter(Boolean).join(' — ') || 'Dates not detected'}</p></div></article>)}</div> : <p className="empty-state">No education details detected.</p>}</section>
          </div>
        </section>
      )}
      <footer>Resume Analyzer <span>·</span> Built for resume parsing assessment</footer>
    </main>
  )
}

export default App
