import { timeAgo } from "../config/Helper";

function Message({index,user,message}){
  const isSender = (user == message.sender);

  return <div key={index} className={`flex ${isSender ? "justify-end" : "justify-start" }`}>
              <div className={`my-2 ${isSender ? "bg-green-700" : "bg-blue-600" } p-2 max-w-xs rounded mx-2`}>
                  <div className="flex flex-row gap-2 items-center">
                    <div>
                      <img className="h-10 w-10" src="https://avatar.iran.liara.run/public" alt="avatar" />
                    </div>
                    <div className="flex flex-col gap-1">
                      <p className="text-sm font-bold">{message.sender}</p>
                      <p>{message.content}</p>
                      <p className="text-xs text-gray-300">{timeAgo(message.timeStamp)}</p>
                    </div>
                </div>
              </div>
            </div>
}

export default Message;