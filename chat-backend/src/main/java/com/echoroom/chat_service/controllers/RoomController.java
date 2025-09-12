package com.echoroom.chat_service.controllers;

import com.echoroom.chat_service.entity.Message;
import com.echoroom.chat_service.service.RoomService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/rooms")
public class RoomController {

    @Autowired
    RoomService roomService;

    @PostMapping
    public ResponseEntity<?> createRoom(@RequestBody String roomId){
        return roomService.createRoom(roomId);
    }

    @GetMapping("/{roomId}")
    public ResponseEntity<?> joinRoom(@PathVariable String roomId){
        return roomService.joinRoom(roomId);
    }

    @GetMapping("/{roomId}/message")
    public ResponseEntity<List<Message>> getMessage(@PathVariable String roomId){
        return roomService.getMessages(roomId);
    }

}
