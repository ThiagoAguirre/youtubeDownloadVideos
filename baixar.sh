#!/usr/bin/env bash
# Atualiza o yt-dlp (o YouTube muda com frequência) e baixa os links de links.txt
cd "$(dirname "$0")"
.venv/bin/pip install -q -U "yt-dlp[default]" deno imageio-ffmpeg
.venv/bin/python baixar.py
