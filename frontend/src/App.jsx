import { useState } from 'react'
import './App.css'

const API = 'http://127.0.0.1:8000'

function App() {
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState('')

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

  return (
    <div>
      <h1>DocuMind</h1>
      <h2>Upload a document</h2>
      <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
      <p>{message}</p>
    </div>
  )
}

export default App