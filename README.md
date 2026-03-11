# mcp-helix

Servidor MCP local para Trellix Helix/XDR. Ele autentica na API da Trellix e expõe operações do Helix como tools MCP via `stdio`.

## Como rodar

```bash
git clone <seu-repositorio.git>
cd <nome-do-repositorio>
cp .env.example .env
```

Preencha o `.env` com:

- `TRELLIX_CLIENT_ID`
- `TRELLIX_CLIENT_SECRET`
- `TRELLIX_API_KEY`
- `TRELLIX_TOKEN_ENDPOINT`
- `API_BASE_URL`

Depois instale e execute.

Com `uv`:

```bash
uv venv
. .venv/bin/activate
uv pip install -e .
mcp-helix
```

Com `pip`:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
mcp-helix
```
