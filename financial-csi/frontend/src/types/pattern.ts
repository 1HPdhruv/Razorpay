export interface PatternCondition {
  feature: string;
  operator: string;
  value: string;
}

export interface Pattern {
  pattern_id: string;
  name?: string;
  description?: string;
  pattern_type?: string;
  conditions: PatternCondition[];
  support?: number;
  matching_transaction_count?: number;
  loss_count?: number;
  loss_rate?: number;
  baseline_loss_rate?: number;
  risk_multiplier: number;
  lift?: number;
  p_value?: number;
  confidence_interval?: any;
  exposure_amount?: number;
  average_loss_amount?: number;
  discovery_method?: string;
  feature_importance?: any;
  evidence_transaction_ids?: string[];
}
