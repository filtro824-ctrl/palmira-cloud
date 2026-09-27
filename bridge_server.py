import json
import os
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from dotenv import load_dotenv
from livekit import api

load_dotenv('.env.local')

ROOT = Path(__file__).resolve().parent
WEB_DIR = ROOT / 'web'
HOST = '0.0.0.0'
PORT = int(os.getenv('PORT', os.getenv('PALMIRA_UI_PORT', '8080')))
AGENT_NAME = 'Palmira'

LIVEKIT_URL = os.getenv('LIVEKIT_URL', '').strip()
API_KEY = os.getenv('LIVEKIT_API_KEY', '').strip()
API_SECRET = os.getenv('LIVEKIT_API_SECRET', '').strip()


class Handler(BaseHTTPRequestHandler):
    def _headers(self, content_type='application/json', status=200):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()

    def do_OPTIONS(self):
        self._headers(status=204)

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            data = (WEB_DIR / 'index.html').read_bytes()
            self._headers('text/html; charset=utf-8')
            self.wfile.write(data)
            return

        if self.path == '/health':
            self._headers()
            self.wfile.write(json.dumps({'ok': True, 'agent': AGENT_NAME}).encode())
            return

        self._headers(status=404)
        self.wfile.write(b'{"error":"not found"}')

    def do_POST(self):
        if self.path != '/token':
            self._headers(status=404)
            self.wfile.write(b'{"error":"not found"}')
            return

        if not all((LIVEKIT_URL, API_KEY, API_SECRET)):
            self._headers(status=500)
            self.wfile.write(json.dumps({
                'error': 'LIVEKIT_URL, LIVEKIT_API_KEY and LIVEKIT_API_SECRET must be set in .env.local'
            }).encode())
            return

        try:
            length = int(self.headers.get('Content-Length', '0'))
            body = json.loads(self.rfile.read(length) or '{}')
        except (ValueError, json.JSONDecodeError):
            self._headers(status=400)
            self.wfile.write(b'{"error":"invalid JSON"}')
            return

        room_name = body.get('room_name') or f'palmira-{uuid.uuid4().hex[:12]}'
        identity = body.get('participant_identity') or f'user-{uuid.uuid4().hex[:12]}'

        token = (
            api.AccessToken(API_KEY, API_SECRET)
            .with_identity(identity)
            .with_name('Palmira User')
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
            ))
            .with_room_config(
                api.RoomConfiguration(
                    agents=[api.RoomAgentDispatch(agent_name=AGENT_NAME)]
                )
            )
            .to_jwt()
        )

        self._headers(status=201)
        self.wfile.write(json.dumps({
            'server_url': LIVEKIT_URL,
            'participant_token': token,
            'room_name': room_name,
        }).encode())


if __name__ == '__main__':
    print(f'Palmira UI listening on 0.0.0.0:{PORT}')
    print(f'LiveKit: {LIVEKIT_URL or "NOT CONFIGURED"}')
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
