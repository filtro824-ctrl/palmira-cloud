#!/bin/sh

uv run src/agent.py start &
exec uv run python bridge_server.py
