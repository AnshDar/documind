import { useState } from 'react'
import './App.css'

const API = 'http://127.0.0.1:8000'

function App() {
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState('')
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleUpload() {
    if (!file) {
      setMessage('Choose a PDF first')
      return
    }
    const formData = new FormData()
    formData.append('file', file)

    setMessage('Uploading...')
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
  }

  async function handleAsk() {
    if (question.trim() === '') {
      return
    }
    setResult(null)
    setLoading(true)
    const response = await fetch(API + '/query?q=' + encodeURIComponent(question))
    const data = await response.json()
    setResult(data)
    setLoading(false)
  }

  return (
    <div>
      <h1>DocuMind</h1>

      <h2>Upload a document</h2>
      <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
      <p>{message}</p>

      <h2>Ask a question</h2>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask something about your documents"
      />
      <button onClick={handleAsk}>Ask</button>

      {loading && <p>Thinking...</p>}

      {result && (
        <div>
          <h3>Answer</h3>
          <p>{result.answer}</p>
          {result.sources.length > 0 && (
            <div>
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
  )
}

export default App