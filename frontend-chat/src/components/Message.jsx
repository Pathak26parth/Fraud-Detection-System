import { timeAgo } from "../config/Helper";
import { useEffect } from "react";
import toast from "react-hot-toast";

function Message({index,user,message}){
  const isSender = (user == message.sender);
  const isSpam = message.isSpam && !isSender; // Only show spam alert to receivers

  // Show spam alert to receiver when message is spam
  useEffect(() => {
    if (isSpam && message.spamLevel > 0.5) {
      toast.error(`⚠️ Fraud Alert: Message from ${message.sender} detected as spam (${(message.spamLevel * 100).toFixed(1)}% spam level)`, {
        duration: 6000,
        position: 'top-right',
        style: {
          background: '#ff4444',
          color: 'white',
          fontWeight: 'bold'
        }
      });
    }
  }, [isSpam, message.spamLevel, message.sender]);

  return <div key={index} className={`flex ${isSender ? "justify-end" : "justify-start" }`}>
              <div className={`my-2 ${isSender ? "bg-green-700" : isSpam ? "bg-red-600" : "bg-blue-600" } p-2 max-w-xs rounded mx-2 ${isSpam ? "border-2 border-red-400" : ""}`}>
                  <div className="flex flex-row gap-2 items-center">
                    <div>
                      <img className="h-10 w-10" src="https://avatar.iran.liara.run/public" alt="avatar" />
                    </div>
                    <div className="flex flex-col gap-1">
                      <p className="text-sm font-bold">{message.sender}</p>
                      <p>{message.content}</p>
                      {isSpam && (
                        <div className="text-xs text-red-200 font-bold bg-red-800 px-2 py-1 rounded">
                          ⚠️ SPAM DETECTED ({(message.spamLevel * 100).toFixed(1)}%)
                        </div>
                      )}
                      <p className="text-xs text-gray-300">{timeAgo(message.timeStamp)}</p>
                    </div>
                </div>
              </div>
            </div>
}

export default Message;