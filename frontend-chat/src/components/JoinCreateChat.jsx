import { useContext, useRef} from "react";
import toast from "react-hot-toast";
import { createRoomService, joinRoomService } from "../services/RoomService";
import { ChatContext } from "../store/ChatContext";
import { useNavigate } from "react-router";

function JoinCreateChat(){

  const nameRef = useRef();
  const roomRef = useRef();

  const { setRoomId , setCurrUser , setConnected} = useContext(ChatContext);

  const navigate = useNavigate();

  function validate(){
    if(nameRef.current.value == "" || roomRef.current.value == ""){
      toast.error("Invalid Input");
      return false;
    }
    return true;
  }

  async function joinRoom(){
    if(validate()){
      try{
        await joinRoomService(roomRef.current.value);
        
        setRoomId(roomRef.current.value);
        setCurrUser(nameRef.current.value);

        setConnected(true);

        toast.success("Joined Room");

        navigate("/chat");
      }
      catch(error){
        if(error.status == 400){
          toast.error("Room Does Not Exists");
        }
        else{
          toast.error("Error in joining Room");
        }
      }
    }
  }

  async function createRoom(){
    if(validate()){
      try{
        await createRoomService(roomRef.current.value);
        
        setRoomId(roomRef.current.value);
        setCurrUser(nameRef.current.value);

        setConnected(true);

        toast.success("Room Created Sucessfully");

        navigate("/chat");
      }
      catch(error){
        if(error.status == 400){
          toast.error("Room Already Exsists");
        }
        else{
          toast.error("Error in Creating Room");
        }
      }
    }
  }


  return <div className="min-h-screen flex items-center justify-center">
    <div className="p-8 w-full max-w-md dark:bg-gray-900 shadow rounded flex flex-col gap-5">
      <h1 className="text-2xl font-semibold text-center">Join Room / Create Room</h1>

      {/* name div  */}
      <div>
        <label htmlFor="name" className="block font-medium mb-2">Your Name</label>
        <input type="text" id="name" ref={nameRef}  placeholder="Enter Room Name" className="w-full dark:bg-gray-600 px-4 py-2 border dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"/>
      </div>

      {/* room Id div  */}
      <div>
        <label htmlFor="room-id" className="block font-medium mb-2">Room ID</label>
        <input type="text" id="room-id" ref={roomRef} placeholder="Enter Room Id" className="w-full dark:bg-gray-600 px-4 py-2 border dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"/>
      </div>

      {/* buttons  */}
      <div className="flex justify-around mt-5">
        <button className="px-3 py-2 dark:bg-green-500 hover:bg-green-800 rounded-lg" onClick={joinRoom}>Join Room</button>
        <button className="px-3 py-2 dark:bg-blue-500 hover:bg-blue-800 rounded-lg" onClick={createRoom}>Create Room</button>
      </div>

    </div>
  </div>
}

export default JoinCreateChat;