# Chat Server

Web-based chat app built with FastAPI + WebSockets + asyncio.
Runs as a Docker container on AWS alongside portfolio/ and auth-system/

## Features

### Core
- Authentication via auth-system
- Friends system (add by email, requires confirmation)
- 1-on-1 chats with users on friends list
- Group chats (create, add/remove members)
- Chat history (persisted)

### Real-time
- Online/offline presence
- Typing indicator
- Delivered vs seen (read receipts)

### Media & Search
- File/image sharing
- Message search

## Tech Stack
- **Backend:** FastAPI, WebSockets, asyncio
- **Database:** PostgreSQL (chat history, relationships)
- **Cache/Pub-Sub:** Redis (presence, typing indicators, WebSocket scaling)
- **Auth:** auth-system (JWT)
- **Deployment:** Docker, Nginx (reverse proxy from portfolio)