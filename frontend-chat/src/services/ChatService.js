import { httpClient } from "../config/AxiosHelper";


export const getMessage = async(roomId)=>{
  const response = httpClient.get(`/rooms/${roomId}/message`);

  return (await response).data;
}