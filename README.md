# MeetFlow AI MVP

MVP funcional para transformar reunioes em:

- Ata Formal
- Resumo Executivo
- Tarefas acionaveis
- Decisoes consolidadas
- Riscos detectados
- Chat com a reuniao

## Stack

- `backend`: FastAPI + SQLite local + Whisper + LLM (OpenAI opcional)
- `frontend`: Next.js + React + Tailwind CSS
- `desktop-ready`: empacotamento desktop via Tauri + sidecar FastAPI

## Fluxo principal

1. Login local simples (usuario bootstrap)
2. Nova reuniao por texto/manual ou upload de audio/video
3. Pipeline de IA com status visual:
   - Transcrevendo
   - Analisando
   - Gerando ata
   - Finalizando insights
4. Visualizacao em abas e chat contextual
5. Exportacao em PDF, DOCX e Markdown

## Credenciais bootstrap

- email: `admin@meetflow.app`
- senha: `admin123`

## Como rodar (desenvolvimento)

Backend:

```bash
cd backend
python -m pip install -r requirements.txt
python -m alembic upgrade head
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:3000`
Backend: `http://localhost:8000`

## Build desktop com Tauri (Windows)

Pré-requisitos:

- Rust/Cargo instalados ([rustup.rs](https://rustup.rs/))
- Python no PATH
- Node.js + npm
- PyInstaller (`python -m pip install pyinstaller`)

Comandos:

```bash
cd frontend
npm install
npm run tauri:build
```

O instalador/app será gerado em `frontend/src-tauri/target/release/bundle`.

## Variaveis de ambiente (backend)

Use `backend/.env.example` como base:

- `APP_SECRET_KEY`
- `OPENAI_API_KEY` (opcional)
- `MEETFLOW_LLM_MODEL` (default `gpt-4o-mini`)
- `WHISPER_MODEL` (default `base`)

## Endpoint principais

- `POST /api/auth/login`
- `GET /api/dashboard`
- `GET /api/meetings`
- `POST /api/meetings/process-text`
- `POST /api/meetings/process-upload`
- `POST /api/meetings/{id}/chat`
- `GET /api/meetings/{id}/export/{pdf|docx|md}`
