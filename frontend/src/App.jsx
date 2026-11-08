import { useState } from 'react'
import './App.css'

const API = 'http://127.0.0.1:8000'

function App() {
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState('')
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleUpload() {
    if (!file) {
      setMessage('Choose a PDF first')
      return
    }
    const formData = new FormData()
    formData.append('file', file)

    setMessage('Uploading...')
    try {
      const response = await fetch(API + '/upload', {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      if (response.ok) {
        setMessage(data.message + ': ' + data.filename)
      } else {
        setMessage(data.detail)
      }
    } catch (err) {
      setMessage('Could not reach the server. Is the backend running?')
    }
  }

  async function handleAsk(e) {
    e.preventDefault()
    if (question.trim() === '') {
      return
    }
    setResult(null)
    setError('')
    setLoading(true)
    try {
      const response = await fetch(API + '/query?q=' + encodeURIComponent(question))
      if (response.ok) {
        const data = await response.json()
        setResult(data)
      } else {
        setError('Something went wrong on the server. Please try again.')
      }
    } catch (err) {
      setError('Could not reach the server. Is the backend running?')
    }
    setLoading(false)
  }

  return (
    <div className="page">
      <h1>DocuMind</h1>
      <p className="subtitle">Ask questions about your company documents</p>

      <div className="card">
        <h2>1. Upload a document</h2>
        <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Upload</button>
        <p className="note">{message}</p>
      </div>

      <div className="card">
        <h2>2. Ask a question</h2>
        <form onSubmit={handleAsk}>
          <input
            className="question"
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask something about your documents"
          />
          <button type="submit">Ask</button>
        </form>

        {loading && <p className="note">Thinking...</p>}
        {error && <p className="error">{error}</p>}

        {result && (
          <div>
            <h3>Answer</h3>
            <p className="answer">{result.answer}</p>
            {result.sources.length > 0 && (
              <div className="sources">
                <h3>Sources</h3>
                <ul>
                  {result.sources.map((s, i) => (
                    <li key={i}>{s.filename}, chunk {s.chunk_index}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App