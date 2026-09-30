import { useState, useEffect } from 'react'

function App() {
  // 1. declare state to hold the message from the backend
  const [premise, setPremise] = useState(null)
  const [turns, setTurns] = useState([])
  const [loading, setLoading] = useState(true)

  // 2. useEffect to fetch from the backend once, when the component loads
  useEffect(() => {
      const socket = new WebSocket("ws://localhost:8000/ws/scene")
      socket.onmessage = (event) => {
        console.log(event.data)
        const data = JSON.parse(event.data)
        if(data.type == "premise"){
          setPremise(data.content)
        }
        else if (data.type == "turn") {
          setTurns(prevTurns => [...prevTurns, data])
        }
      }
      socket.onclose = () => {
          setLoading(false)
      }
      return () => {
        socket.close()
      }
    },[])

  return (
    <main>
      {premise && <h1>{premise}</h1>}
      {loading && <p>Loading...</p>}
      {turns.map((turn, index) => (
        <div className="turn" key={index}>
          <img src={`http://localhost:8000/portraits/${turn.portrait}`} alt={turn.name} />
          <div className="dialogue">
            <p className="speaker-name">{turn.name}</p>
            <p className="speaker-content">{turn.content}</p>
          </div>
        </div>
      ))}
    </main>
  )
}

export default App