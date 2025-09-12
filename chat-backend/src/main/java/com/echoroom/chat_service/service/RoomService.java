package com.echoroom.chat_service.service;

import com.echoroom.chat_service.entity.Message;
import com.echoroom.chat_service.entity.Room;
import com.echoroom.chat_service.repository.RoomRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RoomService {

    @Autowired
    RoomRepository roomRepository;


    // create room

    public ResponseEntity<?> createRoom(String roomId){
        if(roomRepository.findByRoomId(roomId) != null){
            // room is already there
            return new ResponseEntity<>("Room Already Exists",HttpStatus.BAD_REQUEST);
        }
        // create new room
        else{
            Room room = new Room();
            room.setRoomId(roomId);
            Room savedRoom = roomRepository.save(room);

            return new ResponseEntity<>(savedRoom,HttpStatus.CREATED);
        }

    }

    // Join Room

    public ResponseEntity<?> joinRoom(String roomId){
        Room room = roomRepository.findByRoomId(roomId);

        // room exsists
        if(room != null){
            return new ResponseEntity<>(room,HttpStatus.OK);
        }
        else{
            return new ResponseEntity<>("Room Does Not Exists",HttpStatus.BAD_REQUEST);
        }
    }

    // Get Message of Room
    public ResponseEntity<List<Message>> getMessages(String roomId){
        Room room = roomRepository.findByRoomId(roomId);

        if(roomId != null){
            List<Message> messages = room.getMessage();
            return new ResponseEntity<>(messages,HttpStatus.OK);
        }
        else{
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        }
    }
}