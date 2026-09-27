#!/bin/sh

uv run src/agent.py start &
exec uv run python servidor_ponte.py
