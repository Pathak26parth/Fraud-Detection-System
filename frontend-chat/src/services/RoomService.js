import { httpClient } from "../config/AxiosHelper"

export const createRoomService = async(roomId)=>{
  const response = await httpClient.post("/rooms",roomId,{
    headers : {
      "Content-Type" : "text/plain"
    }
  });
  return response.data;
}

export const joinRoomService = async(roomId)=>{
  const api =  `/rooms/${roomId}`;

  const response = await httpClient.get(api);

  return response.data;
}