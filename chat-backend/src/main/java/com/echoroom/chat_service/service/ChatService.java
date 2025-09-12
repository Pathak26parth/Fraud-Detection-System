package com.echoroom.chat_service.service;

import com.echoroom.chat_service.entity.Message;
import com.echoroom.chat_service.entity.Room;
import com.echoroom.chat_service.payload.MessageRequest;
import com.echoroom.chat_service.repository.RoomRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class ChatService {
    @Autowired
    RoomRepository roomRepository;
    
    @Autowired
    SpamDetectionService spamDetectionService;

    public Message sendMessage(MessageRequest request){
        Room room = roomRepository.findByRoomId(request.getRoomId());

        // Detect spam before creating message
        SpamDetectionService.SpamDetectionResult spamResult = 
            spamDetectionService.detectSpam(request.getContent());

        Message message = new Message();
        message.setContent(request.getContent());
        message.setSender(request.getSender());
        message.setTimeStamp(LocalDateTime.now());
        message.setSpamLevel(spamResult.getSpamLevel());
        message.setIsSpam(spamResult.isSpam());

        if(room != null){
            room.getMessage().add(message);
            roomRepository.save(room);
        }
        else{
            throw  new RuntimeException("Room Not Found");
        }

        return message;
    }
}
