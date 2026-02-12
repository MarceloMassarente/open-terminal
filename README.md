# ⬛ Open Terminal

A lightweight API for remote command execution with streaming support.

## Quick Start

### Run Locally

```bash
pip install .
open-terminal run
```

### Docker

```bash
docker build -t open-terminal .
docker run -p 8000:8000 open-terminal
```

An API key is auto-generated on startup if not provided. To set your own:

```bash
# via CLI flag
open-terminal run --api-key my-secret

# via environment variable
docker run -p 8000:8000 -e OPEN_TERMINAL_API_KEY=my-secret open-terminal
```

## API

### `GET /health`

Health check — no auth required.

### `POST /execute`

Execute a command and return the result.

```bash
curl -X POST http://localhost:8000/execute \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"command": "echo hello", "timeout": 30}'
```

```json
{"exit_code": 0, "stdout": "hello\n", "stderr": ""}
```

### `POST /execute?stream=true`

Stream output as JSONL (`application/x-ndjson`):

```bash
curl -X POST "http://localhost:8000/execute?stream=true" \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"command": "for i in 1 2 3; do echo $i; sleep 1; done"}'
```

```jsonl
{"type": "stdout", "data": "1\n"}
{"type": "stdout", "data": "2\n"}
{"type": "stdout", "data": "3\n"}
{"type": "exit", "data": 0}
```

## License

MIT
