import os

def write_file(path, content=""):
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

# CORE
write_file("backend/app/core/config.py", """
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Financial CSI"
    DATABASE_URL: str = "sqlite:///./financial_csi.db"
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
""")

write_file("backend/app/core/logging.py", """
import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO)
""")

write_file("backend/app/core/constants.py", """
# TODO: Define application constants
""")

write_file("backend/app/api/dependencies.py", """
def get_db():
    # TODO: Implement DB session dependency
    yield None
""")

# SERVICES PLACEHOLDERS
services = [
    ("backend/app/services/data/generator.py", "def generate_synthetic_data():\n    raise NotImplementedError"),
    ("backend/app/services/data/loader.py", "def load_data():\n    raise NotImplementedError"),
    ("backend/app/services/data/validator.py", "def validate_data():\n    raise NotImplementedError"),
    ("backend/app/services/lifecycle/builder.py", "def build_lifecycle():\n    raise NotImplementedError"),
    ("backend/app/services/lifecycle/state_machine.py", "class LifecycleStateMachine:\n    pass"),
    ("backend/app/services/lifecycle/transitions.py", "def define_transitions():\n    pass"),
    ("backend/app/services/features/extractor.py", "def extract_features():\n    raise NotImplementedError"),
    ("backend/app/services/features/temporal.py", "def extract_temporal_features():\n    raise NotImplementedError"),
    ("backend/app/services/features/behavioral.py", "def extract_behavioral_features():\n    raise NotImplementedError"),
    ("backend/app/services/features/financial.py", "def extract_financial_features():\n    raise NotImplementedError"),
    ("backend/app/services/discovery/miner.py", "def discover_patterns():\n    '''TODO: Implement unsupervised/candidate pattern discovery in a later phase.'''\n    raise NotImplementedError"),
    ("backend/app/services/discovery/clustering.py", "def cluster_patterns():\n    raise NotImplementedError"),
    ("backend/app/services/discovery/association.py", "def associate_patterns():\n    raise NotImplementedError"),
    ("backend/app/services/discovery/anomaly.py", "def detect_anomalies():\n    raise NotImplementedError"),
    ("backend/app/services/risk/scorer.py", "def calculate_risk_score():\n    raise NotImplementedError"),
    ("backend/app/services/risk/exposure.py", "def calculate_exposure():\n    raise NotImplementedError"),
    ("backend/app/services/risk/thresholds.py", "def evaluate_thresholds():\n    raise NotImplementedError"),
    ("backend/app/services/investigation/investigator.py", "def investigate_pattern():\n    raise NotImplementedError"),
    ("backend/app/services/investigation/evidence.py", "def gather_evidence():\n    raise NotImplementedError"),
    ("backend/app/services/investigation/explanation.py", "def generate_explanation():\n    raise NotImplementedError"),
    ("backend/app/services/simulation/intervention.py", "def simulate_intervention():\n    raise NotImplementedError"),
    ("backend/app/services/simulation/counterfactual.py", "def evaluate_counterfactual():\n    raise NotImplementedError"),
    ("backend/app/services/simulation/calculator.py", "def calculate_savings():\n    raise NotImplementedError"),
    ("backend/app/services/evaluation/metrics.py", "def calculate_metrics():\n    raise NotImplementedError"),
    ("backend/app/services/evaluation/holdout.py", "def validate_on_holdout():\n    raise NotImplementedError"),
    ("backend/app/services/evaluation/confusion.py", "def build_confusion_matrix():\n    raise NotImplementedError"),
    ("backend/app/services/evaluation/report.py", "def generate_report():\n    raise NotImplementedError"),
]

for path, content in services:
    write_file(path, content)

# REPOSITORIES
repos = [
    ("backend/app/repositories/transaction_repository.py", "class TransactionRepository:\n    pass"),
    ("backend/app/repositories/pattern_repository.py", "class PatternRepository:\n    pass"),
    ("backend/app/repositories/investigation_repository.py", "class InvestigationRepository:\n    pass"),
]
for path, content in repos:
    write_file(path, content)

# UTILS
utils = [
    ("backend/app/utils/money.py", "def format_money(amount: float) -> str:\n    return f'₹{amount}'"),
    ("backend/app/utils/dates.py", "def format_date():\n    pass"),
    ("backend/app/utils/ids.py", "def generate_id():\n    pass"),
]
for path, content in utils:
    write_file(path, content)

# TESTS PLACEHOLDERS
tests = [
    ("backend/tests/test_lifecycle.py", "def test_lifecycle():\n    pass"),
    ("backend/tests/test_features.py", "def test_features():\n    pass"),
    ("backend/tests/test_discovery.py", "def test_discovery():\n    pass"),
    ("backend/tests/test_risk.py", "def test_risk():\n    pass"),
    ("backend/tests/test_evaluation.py", "def test_evaluation():\n    pass"),
]
for path, content in tests:
    write_file(path, content)

# SCRIPTS
write_file("scripts/setup.sh", "#!/bin/bash\necho 'Setup script coming soon.'")
write_file("scripts/generate_data.py", "def main():\n    pass\n\nif __name__ == '__main__':\n    main()")
write_file("scripts/run_demo.sh", "#!/bin/bash\necho 'Demo script coming soon.'")

# Set executable perms
os.chmod("scripts/setup.sh", 0o755)
os.chmod("scripts/run_demo.sh", 0o755)

# FRONTEND MISC COMPONENT PLACEHOLDERS
frontend_components = [
    "frontend/src/components/layout/Sidebar.tsx",
    "frontend/src/components/layout/Header.tsx",
    "frontend/src/components/layout/PageContainer.tsx",
    "frontend/src/components/dashboard/MetricCard.tsx",
    "frontend/src/components/dashboard/RiskOverview.tsx",
    "frontend/src/components/dashboard/PatternList.tsx",
    "frontend/src/components/dashboard/ExposureChart.tsx",
    "frontend/src/components/patterns/PatternCard.tsx",
    "frontend/src/components/patterns/PatternDetails.tsx",
    "frontend/src/components/patterns/PatternTimeline.tsx",
    "frontend/src/components/patterns/RiskBadge.tsx",
    "frontend/src/components/investigations/InvestigationPanel.tsx",
    "frontend/src/components/investigations/EvidenceList.tsx",
    "frontend/src/components/investigations/TransactionGraph.tsx",
    "frontend/src/components/investigations/AIExplanation.tsx",
    "frontend/src/components/simulations/InterventionCard.tsx",
    "frontend/src/components/simulations/BeforeAfter.tsx",
    "frontend/src/components/simulations/PreventedLossCard.tsx",
    "frontend/src/components/evaluation/MetricsGrid.tsx",
    "frontend/src/components/evaluation/ConfusionMatrix.tsx",
    "frontend/src/components/evaluation/EvaluationTable.tsx",
]
for p in frontend_components:
    name = os.path.basename(p).replace(".tsx", "")
    write_file(p, f"export function {name}() {{\n  return <div>{name}</div>;\n}}")

frontend_types = [
    ("frontend/src/types/transaction.ts", "export interface Transaction { id: string; }"),
    ("frontend/src/types/pattern.ts", "export interface Pattern { id: string; }"),
    ("frontend/src/types/investigation.ts", "export interface Investigation { id: string; }"),
    ("frontend/src/types/simulation.ts", "export interface Simulation { id: string; }"),
    ("frontend/src/types/evaluation.ts", "export interface Evaluation { id: string; }"),
]
for p, content in frontend_types:
    write_file(p, content)

frontend_lib = [
    ("frontend/src/lib/api.ts", "export const api = {};"),
    ("frontend/src/lib/formatters.ts", "export const formatters = {};"),
    ("frontend/src/lib/constants.ts", "export const constants = {};"),
]
for p, content in frontend_lib:
    write_file(p, content)

frontend_hooks = [
    ("frontend/src/hooks/usePatterns.ts", "export function usePatterns() {}"),
    ("frontend/src/hooks/useInvestigation.ts", "export function useInvestigation() {}"),
    ("frontend/src/hooks/useSimulation.ts", "export function useSimulation() {}"),
    ("frontend/src/hooks/useEvaluation.ts", "export function useEvaluation() {}"),
]
for p, content in frontend_hooks:
    write_file(p, content)
