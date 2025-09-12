import { IoMdSend } from "react-icons/io";
import { CgAttachment } from "react-icons/cg";
import { useContext, useEffect, useRef, useState } from "react";
import Message from "./Message";
import { ChatContext } from "../store/ChatContext";
import { useNavigate } from "react-router";
import SockJS from "sockjs-client";
import { URL } from "../config/AxiosHelper";
import { Stomp } from "@stomp/stompjs";
import toast from "react-hot-toast";
import { getMessage } from "../services/ChatService";

function Chat(){

  const {currUser , roomId , connected , setConnected , setRoomId , setCurrUser} = useContext(ChatContext);

  const navigate = useNavigate();

  useEffect(
    ()=>{
      if(!connected) navigate("/");
    },[connected,navigate]);

  const [message,setMessage] = useState([]);

  const inputRef = useRef();
  const chatBoxRef = useRef();
  const [stompClient,setStompClient] = useState();

  //load message
  useEffect(()=>{
    async function loadMessage(){
      try{
        const response = await getMessage(roomId);
        
        // setMessage(response);
        setMessage(Array.isArray(response) ? response : []);
      }
      catch(error){
        toast.error(error);
      }
    }

    if(connected) loadMessage();

  },[roomId,connected]);


  // auto scroll
  useEffect(()=>{
    if(chatBoxRef.current){
      chatBoxRef.current.scroll({
        top : chatBoxRef.current.scrollHeight,
        behavior : "smooth"
      })
    }


  },[message]);


  // stomp client init
  useEffect(()=>{
    const connectWebSocket = ()=>{

      // SockJs
      const sock = new SockJS(`${URL}/chat`);

      const client = Stomp.over(sock);

      client.connect({}, () => {
        setStompClient(client);

        toast.success("connected");

        client.subscribe(`/topic/room/${roomId}`, (message) => {

          const newMessage = JSON.parse(message.body);

          setMessage((prev) => [...prev, newMessage]);
          
        })
      }
      )
    }

    if(connected) connectWebSocket();


  },[roomId,connected]);



  // Send Message
  const sendMessage = async()=>{
    if(stompClient && connected && inputRef.current.value.trim()){
      const message = {
        "sender" : currUser,
        "content" : inputRef.current.value,
        "roomId" : roomId
      }
      stompClient.send(`/app/sendMessage/${roomId}`,{},JSON.stringify(message));
      inputRef.current.value = "";
    }
  }

  // Logout

  const handleLogout = ()=>{
    stompClient.disconnect();
    setConnected(false);
    setRoomId("");
    setCurrUser("");
    navigate("/");
  }


  return <div>
    {/* Header  */}
    <header className="py-5 fixed w-full dark:bg-gray-900 shadow flex justify-around">
      {/* room name container  */}
      <div>
        <h1 className="text-3xl font-semibold">
          Room : <span>{roomId}</span> 
        </h1>
      </div>

      {/* user name container  */}
      <div>
        <h1 className="text-3xl font-semibold">
          User : <span>{currUser}</span> 
        </h1>
      </div>

      {/* leave btn  */}
      <div>
        <button onClick={handleLogout} className="dark:bg-red-500 hover:bg-red-800 px-3 py-2 rounded-lg">Leave Room</button>
      </div>

    </header>

    {/* main  */}
    <main ref={chatBoxRef} className="py-20 w-2/3 dark:bg-slate-800 h-screen overflow-auto mx-auto">
      <div className="message-container">
        {message.map((message,index)=><Message index={index} user={currUser} message={message}/>)}
      </div>
    </main>

    {/* input message  */}
    <div className="fixed bottom-2 w-full h-16">
      <div className="h-full w-1/2 mx-auto rounded flex gap-5 items-center">
      
       <input type="text" ref={inputRef} onKeyDown={(e)=>{
          if(e.key === "Enter") sendMessage();
       }} placeholder="Type your message here..." className="w-full dark:bg-gray-900 border dark:border-gray-700 px-3 py-2 h-full focus:outline-none focus:ring-2 focus:ring-blue-400 rounded-lg"/>

       <button className="dark:bg-purple-600 h-13 w-15 flex rounded-full justify-center items-center"><CgAttachment /></button>

        <button onClick = {sendMessage} className="dark:bg-green-600 h-13 w-15 flex rounded-full justify-center items-center"><IoMdSend size={27}/></button>
      </div>
    </div>
    
  </div>
}
export default Chat;