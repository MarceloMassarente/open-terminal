# ⚡ Open Terminal

A lightweight API for running shell commands remotely — designed for AI agents and automation.

The container ships with a full toolkit (Python, git, jq, curl, build tools, and more) and runs as a non-root user with passwordless `sudo`.

## Getting Started

### Docker (recommended)

```bash
docker run -d --name open-terminal --restart unless-stopped -p 8000:8000 -v open-terminal:/home/user -e OPEN_TERMINAL_API_KEY=your-secret-key ghcr.io/open-webui/open-terminal
```

If no API key is provided, one is auto-generated and printed on startup (`docker logs open-terminal`).

### Build from Source

```bash
docker build -t open-terminal .
docker run -p 8000:8000 open-terminal
```

### Bare Metal

```bash
# One-liner with uvx (no install needed)
uvx open-terminal run --host 0.0.0.0 --port 8000 --api-key your-secret-key

# Or install globally with pip
pip install open-terminal
open-terminal run --host 0.0.0.0 --port 8000 --api-key your-secret-key
```

## Quick Examples

**Run a command:**

```bash
curl -X POST http://localhost:8000/execute?wait=5 \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"command": "echo hello"}'
```

**Upload a file:**

```bash
curl -X POST "http://localhost:8000/files/upload?directory=/home/user&url=https://example.com/data.csv" \
  -H "Authorization: Bearer <api-key>"
```

## API Docs

Full interactive API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

## License

MIT — see [LICENSE](LICENSE) for details.
