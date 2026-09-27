# Pedido para Claude — Revisão da ponte Palmira ↔ LiveKit

Estamos a trabalhar numa cópia do projeto Palmira. NÃO alteres o ZIP original.

## Objetivo
Integrar a interface `web/index.html` ao agente existente em `src/agent.py` através do LiveKit.

## O que já existe
- `src/agent.py`: agente LiveKit com `@server.rtc_session(agent_name="Palmira")`.
- Pipeline do agente: STT → LLM → TTS.
- `room_io.RoomOptions` já é usado no `session.start()`.
- `web/index.html`: interface futurista da Palmira.
- `bridge_server.py`: servidor local que serve a interface e cria tokens LiveKit com dispatch para o agente `Palmira`.

## Implementação feita
O `bridge_server.py`:
1. lê `LIVEKIT_URL`, `LIVEKIT_API_KEY` e `LIVEKIT_API_SECRET` de `.env.local`;
2. cria um nome de sala único;
3. cria um JWT de participante;
4. inclui `RoomAgentDispatch(agent_name="Palmira")` no token;
5. devolve `server_url`, `participant_token` e `room_name` em `/token`;
6. serve `web/index.html` em `http://localhost:8080`.

A interface usa `livekit-client` no navegador, conecta à sala, publica o microfone, recebe o áudio do agente e acompanha o atributo `lk.agent.state` para atualizar IDLE/LISTENING/THINKING/SPEAKING.

## O que quero que verifiques
- compatibilidade das APIs com a versão atual do LiveKit Agents instalada pelo `pyproject.toml`;
- se `livekit-api` precisa realmente ser uma dependência explícita;
- se a criação do token e `RoomAgentDispatch` estão corretos;
- se os eventos do `livekit-client` usados no HTML estão corretos;
- se existe uma forma mais simples/recomendada de fazer a ponte;
- não reescrever a personalidade da Palmira;
- não substituir a interface por React: manter HTML/CSS/JS por enquanto.

## Regra importante
Não inventar uma arquitetura nova sem necessidade. Se alguma alteração for necessária, explicar exatamente qual arquivo e por quê.
