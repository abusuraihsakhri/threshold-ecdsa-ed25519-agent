# Threshold Ecdsa Ed25519 Agent

> **Domain:** Clinical Decision Support & Biomedical Computing / Post-Quantum Cryptography & Zero-Knowledge

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## Overview

**Threshold Ecdsa Ed25519 Agent** is an advanced analytical and computational platform implementing Gennaro-Goldfeder (GG20) and FROST threshold MPC wallet custody supervision. The system provides multi-agent consensus evaluation with tamper-evident audit logging and PHI (Protected Health Information) outbound protection.

### Architecture

The project consists of two main modules:

1. **`agents/`** - Clinical & Biomedical AI evaluation engine with PHI guard and HMAC-SHA256 audit trail
2. **`threshold_mpc_wallet/`** - Post-Quantum Cryptography & Zero-Knowledge MPC wallet custody supervisor

---

## Key Features

- **Multi-Agent Consensus**: Three specialized workers evaluate tasks with configurable thresholds
- **PHI Outbound Guard**: Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers
- **Tamper-Evident Audit Trail**: Chained HMAC-SHA256 cryptographically signed logs with integrity verification
- **FastAPI REST API**: OpenAPI 3.1 REST endpoints for programmatic access
- **Prometheus Metrics**: Operational telemetry export for monitoring
- **Active Learning Engine**: Bayesian calibration for worker reliability weighting
- **CLI Interface**: Command-line tools for single and batch processing

---

## Installation

```bash
pip install -e .
```

### Optional Dependencies

```bash
pip install fastapi uvicorn  # For REST API server
pip install pytest           # For running tests
```

---

## Usage

### CLI Commands

#### 1. Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

#### 2. Batch Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

#### 3. System Chat
```bash
python cli.py chat "What is the system status?"
```

#### 4. Verify Audit Integrity
```bash
python cli.py verify-audit
```

#### 5. Start REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### REST API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/metrics` | GET | Prometheus-style metrics |
| `/api/audit` | POST | Submit task for evaluation |
| `/api/chat` | POST | Query supervisory chat |
| `/api/audit/logs` | GET | Retrieve audit trail |

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AUDIT_SECRET_KEY` | Secret key for HMAC-SHA256 audit signing | Auto-generated secure random key |

---

## Testing

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 100
```

---

## Security Features

- **Audit Trail**: Cryptographic chain verification with HMAC-SHA256 signatures
- **PHI Protection**: Regex-based detection and blocking of protected health information
- **Input Validation**: Numeric bounds checking and NaN/Infinity rejection
- **Secure Defaults**: Auto-generated cryptographic keys when not explicitly configured

---

## Container Deployment

```bash
docker build -t threshold-ecdsa-ed25519-agent .
docker run -p 8000:8000 threshold-ecdsa-ed25519-agent
```

---

## License

MIT License - see [LICENSE](LICENSE) for details.
