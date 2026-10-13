"""Regression tests for privacy, failure modes, and both evaluator entry points."""
import math

import pytest
from fastapi.testclient import TestClient

from agents.api import app
from agents.base import AuditTrail
from agents.llm_factory import MockLLM
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor
from threshold_mpc_wallet.agents import ThresholdWalletCoordinator
from threshold_mpc_wallet.models import FrontierPayload

client = TestClient(app)


def test_api_rejects_identifiers_in_attributes():
    response = client.post("/api/audit", json={
        "task_id": "T-01",
        "target_identifier": "SAMPLE-01",
        "primary_metric": 2,
        "attributes": {"notes": "MRN: 123456"}
    })
    assert response.status_code == 422
    assert "Sensitive identifier" in response.json()["detail"]


def test_api_chat_rejects_sensitive_data():
    response = client.post("/api/chat", json={"query": "Please check MRN: 123456"})
    assert response.status_code == 422


def test_api_normal_evaluation():
    response = client.post("/api/audit", json={
        "task_id": "T-02",
        "target_identifier": "SAMPLE-02",
        "primary_metric": 25,
        "secondary_metric": 12,
        "is_critical_flag": False,
        "status_descriptor": "NOMINAL"
    })
    assert response.status_code == 200
    dossier = response.json()
    assert dossier["overall_urgency"] == "ROUTINE"
    assert dossier["total_alerts"] == 0
    assert dossier["standard_reference"] == "Demonstration rules only"


def test_api_rejects_nonfinite_metrics():
    response = client.post("/api/audit", json={
        "task_id": "T-03",
        "target_identifier": "SAMPLE-03",
        "primary_metric": "NaN"
    })
    assert response.status_code == 422


def test_audit_trail_exposes_snapshot_not_internal_mutable_entries():
    trail = AuditTrail(secret_key="regression-test-secret")
    trail.log("test", "unit", "EVENT", {"status": "ok"})
    snapshot = trail.get_trail()
    snapshot[0]["actor"] = "ATTACK"
    snapshot.append({})
    assert len(trail.get_trail()) == 1
    assert trail.verify_integrity()


def test_audit_trail_rejects_phi_in_actor_fields():
    trail = AuditTrail(secret_key="regression-test-secret")
    with pytest.raises(Exception, match="Sensitive identifier"):
        trail.log("MRN 123456", "unit", "EVENT", {"status": "ok"})
    assert trail.get_trail() == []


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf"), "not-a-number"])
def test_wallet_payload_finite_numeric(bad):
    with pytest.raises(ValueError, match="primary_metric must be finite"):
        FrontierPayload("t", "sample", bad, 0, "NOMINAL")
    with pytest.raises(ValueError, match="secondary_metric must be finite"):
        FrontierPayload("t", "sample", 0, bad, "NOMINAL")


def test_wallet_coordinator_demo_thresholds():
    coordinator = ThresholdWalletCoordinator()
    data = coordinator.process(FrontierPayload("t", "sample", 25, 10, "NOMINAL"))
    assert data["overall_status"] == "NOMINAL_OPTIMAL"
    assert data["total_alerts"] == 0
    assert data["standard_specification"] == "Demonstration rules only"


def test_mock_llm_does_not_claim_verification():
    response = MockLLM().invoke("sample task")
    assert "no clinical, cryptographic, or standards verification" in response.lower()
