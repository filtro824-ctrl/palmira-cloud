# Como testar a Palmira com a interface

## 1. Preparar credenciais
Cria `.env.local` na raiz, com:

LIVEKIT_URL=wss://SEU-PROJETO.livekit.cloud
LIVEKIT_API_KEY=SUA_API_KEY
LIVEKIT_API_SECRET=SEU_API_SECRET
PALMIRA_UI_PORT=8080

Nunca coloques `LIVEKIT_API_SECRET` dentro do HTML.

## 2. Instalar dependências

uv sync

## 3. Terminal 1 — iniciar o agente

uv run python src/agent.py dev

## 4. Terminal 2 — iniciar a ponte/interface

uv run python bridge_server.py

## 5. Abrir no navegador

http://localhost:8080

Clica em `CONNECT PALMIRA`, permite o microfone e fala.

A interface deve:
- conectar à sala LiveKit;
- enviar o microfone;
- disparar o agente Palmira;
- receber a voz da Palmira;
- mudar entre IDLE/LISTENING/THINKING/SPEAKING.
