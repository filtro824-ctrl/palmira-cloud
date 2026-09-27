# Palmira — versão preparada para nuvem

Esta cópia foi preparada para um modelo de 2 serviços:

- `palmira-ui`: servidor web que entrega a interface e cria tokens LiveKit no servidor.
- `palmira-agent`: worker que executa o agente Palmira e aguarda jobs do LiveKit.

## Deploy recomendado

O arquivo `render.yaml` está preparado para Render. No painel do Render, crie um Blueprint a partir deste repositório.

Configure estes segredos nos dois serviços:

- `LIVEKIT_URL` — URL do projeto LiveKit Cloud, normalmente `wss://...`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`

Não coloque `LIVEKIT_API_SECRET` no código, no HTML ou no Git.

O serviço web usa a variável `PORT` fornecida pela plataforma. A interface é servida pelo próprio `bridge_server.py`, então o navegador usa `/token` no mesmo domínio e não precisa conhecer o segredo da API.

## Depois do deploy

Abra a URL HTTPS do serviço `palmira-ui` no celular.

1. Toque em CONNECT PALMIRA.
2. Permita o microfone.
3. O navegador pede um token ao `/token`.
4. O token despacha o agente `Palmira` para a sala.
5. O agente entra na sala e responde por voz.

## Importante

O worker e o servidor web são processos diferentes. Não tente executar os dois como um único processo de produção.

O Dockerfile foi ajustado para não depender de um `uv.lock` que não estava presente na cópia recebida. O ambiente de build resolve as dependências a partir do `pyproject.toml`.
