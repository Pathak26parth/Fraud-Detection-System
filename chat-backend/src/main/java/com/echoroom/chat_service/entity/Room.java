package com.echoroom.chat_service.entity;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.ArrayList;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor

@Document(collection = "rooms")
public class Room {
    @Id
    private String id;

    private String roomId;

    private List<Message> message = new ArrayList<>();
}
