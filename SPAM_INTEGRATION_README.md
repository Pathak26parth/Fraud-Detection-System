# Fraud Detection System Integration

This project integrates an AI-powered spam detection model with a real-time chat application. The system detects spam messages and alerts receivers when spam level > 0.5.

## Architecture

- **Frontend**: React.js with WebSocket for real-time messaging
- **Backend**: Spring Boot with MongoDB and WebSocket support
- **AI Model**: FastAPI service with scikit-learn spam detection model

## Features

- Real-time spam detection for all messages
- Fraud alerts shown only to message receivers (not senders)
- Visual indicators for spam messages (red background, warning labels)
- Toast notifications for spam alerts
- Configurable spam threshold (default: 0.5)

## Setup Instructions

### 1. Start the AI Model Service

```bash
# Option 1: Use the batch script
start_ai_model.bat

# Option 2: Manual start
cd DAIICT_FinalModel
python serve.py
```

The AI service will run on `http://localhost:8000`

### 2. Start the Backend Service

```bash
cd chat-backend
mvn spring-boot:run
```

The backend will run on `http://localhost:8080`

### 3. Start the Frontend

```bash
cd frontend-chat
npm install
npm run dev
```

The frontend will run on `http://localhost:5173`

## How It Works

1. **Message Sending**: When a user sends a message, the backend calls the AI model to detect spam
2. **Spam Detection**: The AI model returns a spam probability score (0.0 to 1.0)
3. **Message Storage**: Messages are stored with spam level and spam flag
4. **Real-time Delivery**: Messages are broadcast to all room participants via WebSocket
5. **Receiver Alerts**: Only receivers see spam alerts and visual indicators

## Configuration

### Backend Configuration

Edit `chat-backend/src/main/resources/application.properties`:

```properties
spam.detection.api.url=http://localhost:8000
```

### Spam Threshold

The spam threshold is set to 0.5 (50%) in the `SpamDetectionService`. Messages with spam level > 0.5 are flagged as spam.

## API Endpoints

### AI Model Service (FastAPI)
- `POST /predict` - Detect spam in text
  - Request: `{"text": "message content"}`
  - Response: `{"spamLevel": 0.75}`

### Backend Service (Spring Boot)
- `POST /api/chat/send` - Send message with spam detection
- `GET /api/chat/messages/{roomId}` - Get room messages
- WebSocket: `/chat` - Real-time messaging

## Testing Spam Detection

Try sending messages with spam-like content:
- "Congratulations! You've won $1000!"
- "Click here for free money!"
- "Urgent: Verify your account now!"

These should trigger spam alerts for other users in the room.

## Troubleshooting

1. **AI Model not responding**: Ensure the Python service is running on port 8000
2. **No spam detection**: Check backend logs for API connection errors
3. **Frontend not showing alerts**: Verify WebSocket connection and message structure

## Dependencies

### Backend
- Spring Boot WebFlux (for HTTP client)
- Spring Boot WebSocket
- MongoDB

### Frontend
- React Hot Toast (for notifications)
- WebSocket client

### AI Model
- FastAPI
- scikit-learn
- joblib
