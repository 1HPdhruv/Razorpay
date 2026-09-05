import pytest
from app.services.ai.provider import AIProvider
from app.services.investigation.evidence_pack import EvidencePack
from app.models.pattern import Pattern, PatternCondition
from app.services.investigation.evidence import EvidenceItem

@pytest.mark.asyncio
async def test_investigator_fallback():
    p = Pattern(
        pattern_id="P1", name="P1", description="Test", pattern_type="ASSOCIATION",
        conditions=[PatternCondition(feature="atomic_gateway", operator="==", value="G1")],
        support=0.5, matching_transaction_count=2, loss_count=1, loss_rate=0.5,
        baseline_loss_rate=0.25, risk_multiplier=2.0, lift=2.0, p_value=0.01,
        exposure_amount=1000, average_loss_amount=1000, discovery_method="test",
        feature_importance={}, evidence_transaction_ids=[], is_predefined=False
    )
    
    ev_pack = EvidencePack(
        pattern=p,
        pattern_statistics={},
        supporting_loss_examples=[{'transaction_id': 'T1', 'loss_amount': 100}],
        contrasting_non_loss_examples=[],
        baseline_examples=[],
        evidence_items=[EvidenceItem(evidence_id="EV-001", transaction_id="T1", evidence_type="LOSS_OUTCOME", claim="loss", observed_value="100", source_field="x")]
    )
    
    # Ensure OPENAI_API_KEY is not set or handle mock
    import os
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
        
    provider = AIProvider()
    report = await provider.generate_investigation(ev_pack)
    
    assert report.pattern_id == "P1"
    assert "deterministic" in report.headline
    assert "EV-001" in report.supporting_evidence[0].evidence_ids
