package com.echoroom.chat_service.controllers;


import com.echoroom.chat_service.entity.Message;
import com.echoroom.chat_service.payload.MessageRequest;
import com.echoroom.chat_service.repository.RoomRepository;
import com.echoroom.chat_service.service.ChatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestBody;

@Controller
public class ChatController {

    @Autowired
    ChatService chatService;

    private RoomRepository roomRepository;

    public ChatController(RoomRepository roomRepository){
        this.roomRepository = roomRepository;
    }

    @MessageMapping("/sendMessage/{roomId}")
    @SendTo("/topic/room/{roomId}")
    public Message sendMessage(@DestinationVariable String roomId ,@RequestBody MessageRequest request){
        return chatService.sendMessage(request);
    }

}
