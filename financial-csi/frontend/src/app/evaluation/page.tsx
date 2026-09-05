'use client';
import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { StatCard } from '@/components/ui/StatCard';
import { formatCurrency, formatNumber, formatMultiplier } from '@/lib/utils';
import { ShieldCheck, LineChart, FileWarning, Search, BarChart3, Database } from 'lucide-react';
import { LoadingSkeleton } from '@/components/ui/LoadingSkeleton';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts';

export default function EvaluationPage() {
  const [report, setReport] = useState<any>(null);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/evaluation')
      .then(r => {
        if (!r.ok) throw new Error('Evaluation data not found.');
        return r.json();
      })
      .then(setReport)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (error) {
    return (
      <Card className="flex flex-col h-64 max-w-5xl mx-auto items-center justify-center p-8 text-center space-y-4">
        <FileWarning className="h-10 w-10 text-destructive" />
        <h2 className="text-xl font-bold text-foreground">Evaluation Failed to Load</h2>
        <p className="text-muted-foreground">{error}</p>
        <span className="text-sm bg-muted text-muted-foreground px-4 py-2 rounded-md font-mono mt-2">
          Run `python scripts/run_final_evaluation.py` to generate the report.
        </span>
      </Card>
    );
  }

  if (loading || !report) {
    return (
      <div className="max-w-6xl mx-auto space-y-8">
        <LoadingSkeleton className="h-64 w-full" />
        <div className="grid grid-cols-3 gap-6">
          <LoadingSkeleton className="h-32 w-full" />
          <LoadingSkeleton className="h-32 w-full" />
          <LoadingSkeleton className="h-32 w-full" />
        </div>
      </div>
    );
  }

  const isLeakageSafe = report.holdout.overlap_count === 0;

  const datasetSplitData = [
    { name: 'Training Set', value: report.holdout.train_count, color: '#3b82f6' },
    { name: 'Testing Set', value: report.holdout.test_count, color: '#10b981' }
  ];

  return (
    <div className="flex flex-col space-y-8 pb-12 max-w-6xl mx-auto">
      {/* Holdout Integrity Card */}
      <Card className={`p-8 border-2 ${isLeakageSafe ? 'border-emerald-500/30 bg-emerald-950/5' : 'border-red-500/30 bg-red-950/5'}`}>
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div className="flex items-center gap-4">
            <div className={`p-3 rounded-full ${isLeakageSafe ? 'bg-emerald-500/20 text-emerald-500' : 'bg-red-500/20 text-red-500'}`}>
              <ShieldCheck className="h-8 w-8" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-foreground">Data Separation Integrity</h2>
              <p className="text-muted-foreground mt-1 text-sm max-w-xl">
                Ensures patterns discovered in the training phase generalize to unseen transactions without memorization.
              </p>
            </div>
          </div>
          <Badge variant={isLeakageSafe ? 'success' : 'danger'} className="text-sm px-4 py-1.5 uppercase tracking-wider">
            {isLeakageSafe ? 'No Leakage Detected' : 'Data Leakage Detected'}
          </Badge>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8 pt-8 border-t border-border">
          <div className="flex flex-col">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Training Set</span>
            <span className="text-3xl font-mono font-bold text-blue-500">{formatNumber(report.holdout.train_count)}</span>
          </div>
          <div className="flex flex-col">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Held-out Test Set</span>
            <span className="text-3xl font-mono font-bold text-emerald-500">{formatNumber(report.holdout.test_count)}</span>
          </div>
          <div className="flex flex-col">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Overlap</span>
            <span className={`text-3xl font-mono font-bold ${isLeakageSafe ? 'text-emerald-500' : 'text-red-500'}`}>
              {report.holdout.overlap_count}
            </span>
          </div>
        </div>
        
        {/* Simple visual bar for train/test split */}
        <div className="mt-8 flex h-4 w-full rounded-full overflow-hidden border border-border">
          <div className="bg-blue-500/80" style={{ width: `${(report.holdout.train_count / (report.holdout.train_count + report.holdout.test_count)) * 100}%` }} title="Training Data"></div>
          <div className="bg-emerald-500/80" style={{ width: `${(report.holdout.test_count / (report.holdout.train_count + report.holdout.test_count)) * 100}%` }} title="Test Data"></div>
        </div>
        <div className="flex justify-between mt-2 text-[10px] uppercase font-semibold text-muted-foreground">
          <span>80% Train</span>
          <span>20% Test</span>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column */}
        <div className="lg:col-span-1 space-y-6">
          <Card className="p-6">
            <div className="flex items-center gap-2 mb-6">
              <Search className="h-5 w-5 text-muted-foreground" />
              <h3 className="text-lg font-semibold text-foreground">Discovery Metrics</h3>
            </div>
            <div className="space-y-6">
              <div>
                <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">Emergent Patterns Found</p>
                <p className="text-3xl font-mono font-bold text-foreground">{report.discovery.pattern_count}</p>
              </div>
              <div className="pt-4 border-t border-border">
                <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">Strongest Pattern</p>
                <Badge variant="emergent" className="mb-2 text-xs">{report.discovery.top_pattern_id}</Badge>
                <div className="flex justify-between items-center mt-2">
                  <span className="text-sm text-muted-foreground">Validation Support</span>
                  <span className="font-mono text-foreground">{formatNumber(report.discovery.top_pattern_test_support)}</span>
                </div>
                <div className="flex justify-between items-center mt-2">
                  <span className="text-sm text-muted-foreground">Risk Multiplier</span>
                  <span className="font-mono text-red-400 font-bold">{formatMultiplier(report.discovery.top_pattern_risk_multiplier)}</span>
                </div>
              </div>
            </div>
          </Card>
          
          <Card className="p-6">
            <div className="flex items-center gap-2 mb-6">
              <Database className="h-5 w-5 text-muted-foreground" />
              <h3 className="text-lg font-semibold text-foreground">Reproducibility</h3>
            </div>
            <div className="space-y-4 text-sm">
              <div className="flex justify-between border-b border-border pb-2">
                <span className="text-muted-foreground">Random Seed</span>
                <span className="font-mono text-foreground">42</span>
              </div>
              <div className="flex justify-between border-b border-border pb-2">
                <span className="text-muted-foreground">Dataset Split</span>
                <span className="font-mono text-foreground">80% / 20%</span>
              </div>
              <div className="flex justify-between border-b border-border pb-2">
                <span className="text-muted-foreground">Simulation Runs</span>
                <span className="font-mono text-foreground">1,000 / Scenario</span>
              </div>
              <div className="flex justify-between pt-1">
                <span className="text-muted-foreground">Evaluation Version</span>
                <span className="font-mono text-foreground">v0.2.0</span>
              </div>
            </div>
          </Card>
        </div>

        {/* Right Column */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-6 h-full">
            <div className="flex items-center gap-2 mb-6">
              <BarChart3 className="h-5 w-5 text-muted-foreground" />
              <h3 className="text-lg font-semibold text-foreground">Intervention Efficacy & Decisions</h3>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm whitespace-nowrap">
                <thead className="bg-secondary/50 text-muted-foreground text-xs uppercase font-semibold">
                  <tr>
                    <th className="px-4 py-3 rounded-tl-md">Scenario</th>
                    <th className="px-4 py-3">Intervention Action</th>
                    <th className="px-4 py-3">Assumed Efficacy</th>
                    <th className="px-4 py-3 text-right">Net Estimated Benefit</th>
                    <th className="px-4 py-3 text-right rounded-tr-md">Decision Engine</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {report.simulation.map((sim: any, idx: number) => (
                    <tr key={idx} className="hover:bg-muted/30 transition-colors">
                      <td className="px-4 py-4 font-semibold text-foreground">{sim.scenario}</td>
                      <td className="px-4 py-4 text-muted-foreground">{sim.intervention}</td>
                      <td className="px-4 py-4">
                        <Badge variant="info" className="font-mono text-[10px]">{(sim.effectiveness * 100).toFixed(0)}%</Badge>
                      </td>
                      <td className="px-4 py-4 text-right">
                        <span className={`font-mono font-bold ${sim.net_benefit_paise >= 0 ? 'text-emerald-500' : 'text-red-500'}`}>
                          {sim.net_benefit_paise >= 0 ? '+' : '-'}{formatCurrency(Math.abs(sim.net_benefit_paise))}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-right">
                        <Badge variant={
                          sim.recommendation === 'RECOMMEND_INTERVENTION' ? 'success' :
                          sim.recommendation === 'DO_NOT_INTERVENE' ? 'danger' : 'warning'
                        } className="text-[10px]">
                          {sim.recommendation.replace(/_/g, ' ')}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            
            <div className="mt-8 pt-6 border-t border-border">
              <p className="text-xs text-muted-foreground leading-relaxed">
                <strong className="text-foreground">Methodology:</strong> Decision engine recommendations are generated strictly from the evaluation holdout set (20% unseen data) using Monte Carlo simulations (1,000 runs per scenario, standard normal deviation on effectiveness assumption). Results estimate net benefit minus operational and false-positive friction costs.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
