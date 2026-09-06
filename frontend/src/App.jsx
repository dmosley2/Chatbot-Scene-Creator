import { useState, useEffect } from 'react'

function App() {
  // 1. declare state to hold the message from the backend
  const [message, setMessage] = useState("")

  // 2. useEffect to fetch from the backend once, when the component loads
  useEffect(() => {
    async function loadMessage(){
      const response = await fetch("http://localhost:8000")
      const data = await response.json()
      setMessage(data.message)
    }
    loadMessage()
  }, [])

  return (
    <div>
      {message}
    </div>
  )
}

export default App