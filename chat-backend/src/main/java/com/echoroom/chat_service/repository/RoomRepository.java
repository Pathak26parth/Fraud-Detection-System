package com.echoroom.chat_service.repository;

import com.echoroom.chat_service.entity.Room;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface RoomRepository extends MongoRepository<Room, String> {

    // get room using room id
    Room findByRoomId(String roomId);
}
