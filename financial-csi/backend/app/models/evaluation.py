from pydantic import BaseModel
from datetime import datetime

class EvaluationBase(BaseModel):
    dataset_size: int
    positive_cases: int
    negative_cases: int
    true_positives: int
    true_negatives: int
    false_positives: int
    false_negatives: int
    precision: float
    recall: float
    f1: float
    false_positive_rate: float
    total_loss: float
    detected_loss: float
    potentially_prevented_loss: float
    false_positive_cost: float
    evaluation_timestamp: datetime
