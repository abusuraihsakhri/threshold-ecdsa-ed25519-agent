# Threshold Telemetry Evaluator

This repository (`threshold-ecdsa-ed25519-agent`) contains **demonstration-only rule evaluators** for synthetic telemetry. It does **not** implement threshold ECDSA, Ed25519, FROST, GG20, multiparty key custody, zero-knowledge proofs, or post-quantum cryptography. Do not use it to secure wallets, make clinical decisions, or validate protocol conformance.

## What works

- **Python evaluator:** three deterministic workers in `agents/` check a primary metric (>25), a secondary metric (>12 or a critical flag), and status keywords. The results are merged into a dossier.
- **In-memory audit chain:** the Python evaluator computes linked HMAC-SHA256 entries. They are lost at process exit; this is not durable, independently attested logging.
- **Sensitive-pattern screening:** a limited regex guard rejects some common identifiers in the Python API and CLI. It does **not** guarantee de-identification or HIPAA compliance. Never input real sensitive records.
- **CLI and FastAPI:** audit individual or CSV records and query the deterministic mock response. API documentation is available at `/docs` when the server is running.
- **Separate wallet-named demo:** `threshold_mpc_wallet/` supplies another non-cryptographic threshold evaluator, accessible through a separate CLI command.
- **Browser demo:** `web/index.html` runs matching three-worker demonstration rules entirely in JavaScript, without a backend or network submission. Outputs can be downloaded as JSON.

## Install and use

Python 3.10–3.12 is exercised by CI. From a checkout:

```bash
python -m pip install -e ".[api,test]"
threshold-ecdsa-ed25519-engine audit --task-id DEMO-1 --target SAMPLE-1 --primary 29.4 --secondary 14.2 --status DISCORDANT
threshold-ecdsa-ed25519-engine batch --input sample.csv --output results.csv
threshold-ecdsa-ed25519-engine chat "What does this demo do?"
threshold-ecdsa-ed25519-engine verify-audit
threshold-ecdsa-ed25519-engine serve --host 127.0.0.1 --port 8000
```

A separate packaged entry point is available:

```bash
threshold-mpc-wallet audit --primary 30 --secondary 14
```

The root-level `cli.py` and `threshold_mpc_wallet/cli.py` produce distinct schema variants; they have been retained for compatibility.

### REST API

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/health` | Server status |
| GET | `/metrics` | Basic JSON counters (not Prometheus text) |
| POST | `/api/audit` | Evaluate a synthetic JSON task |
| POST | `/api/chat` | Deterministic mock response |
| GET | `/api/audit/logs` | In-memory audit snapshot and integrity status |

Example audit request:

```bash
curl -s http://127.0.0.1:8000/api/audit \
  -H 'Content-Type: application/json' \
  -d '{"task_id":"DEMO-1","target_identifier":"SAMPLE-1","primary_metric":29.4,"secondary_metric":14.2,"status_descriptor":"DISCORDANT","is_critical_flag":false}'
```

### Browser demo

Open `web/index.html` locally in a current desktop or mobile browser. The HTML uses no external libraries or API calls. Enter only synthetic data; no persistent state is stored and no server-side audit logging occurs. JavaScript, not Python/Pyodide, implements the browser-only rules.

### Container

The Docker service exposes port 8000. **Set an independent secret before starting Docker Compose**; no audit key is committed or generated as a fixed default:

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
```

Avoid binding the API to an untrusted public network: it has **no authentication**, no access control, and an unbounded in-memory registry. The audit key must remain private and stable for a running instance.

## Test

```bash
python -m pytest -q
python -m pip check
python simulator.py 100
```

GitHub Actions tests Python 3.10, 3.11, and 3.12, and checks the browser script's JavaScript syntax. All rule thresholds are example constants, **not** accepted cryptographic or clinical reference limits.

## License

MIT. See [LICENSE](LICENSE).
