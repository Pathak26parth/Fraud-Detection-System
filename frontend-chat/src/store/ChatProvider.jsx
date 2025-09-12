import { useState } from "react";
import { ChatContext } from "./ChatContext";

function ChatProvider({children}){
  const [roomId,setRoomId] = useState("");
  const [currUser,setCurrUser] = useState('');
  const [connected,setConnected] = useState(false);

  return (
  <ChatContext.Provider value={{roomId , setRoomId , currUser , setCurrUser , connected , setConnected}}>
    {children}
  </ChatContext.Provider>
  )
}

export default ChatProvider;