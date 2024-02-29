import { useEffect, useState } from 'react'
import useWebSocket from 'react-use-websocket';

export const useArtifactChecker = (filename, readyToConnect) => {

  const { sendJsonMessage, lastMessage, readyState } = useWebSocket(readyToConnect ? '/socket' : null);
  const [ imageUrl, setImageUrl ] = useState("")
  const [ resend, setResend ] = useState(true)
  

  const msgToWs = {
    action: 'onCheck',
    filename
  }

  useEffect(() => {
    if (readyState === 1 && resend) {
      sendJsonMessage(msgToWs)
      setResend(false)
    } 
  }, [readyState, resend])

  useEffect(() => {
    (
      async () =>{
          if (readyToConnect && lastMessage) {

            const response = JSON.parse(lastMessage.data)

            if (typeof response !== 'string') {
              await new Promise(res => setTimeout(res, 5000))
              setResend(true)
            } else {
              await new Promise((res) => res(setImageUrl(response)))
              setResend(false)
            }
        }
      }
    )()
  }, [lastMessage])

  return imageUrl
}

