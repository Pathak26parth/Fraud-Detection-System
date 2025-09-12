package com.echoroom.chat_service.entity;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor

public class Message {
    private String sender;
    private String content;
    private LocalDateTime timeStamp;
    private Double spamLevel;
    private Boolean isSpam;

    public Message(String sender , String content) {
        this.sender = sender;
        this.content = content;
        this.timeStamp = LocalDateTime.now();
        this.spamLevel = 0.0;
        this.isSpam = false;
    }

    public Message(String sender, String content, Double spamLevel, Boolean isSpam) {
        this.sender = sender;
        this.content = content;
        this.timeStamp = LocalDateTime.now();
        this.spamLevel = spamLevel;
        this.isSpam = isSpam;
    }
}
