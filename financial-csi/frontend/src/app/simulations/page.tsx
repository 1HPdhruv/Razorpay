'use client';
import { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { LoadingSkeleton } from '@/components/ui/LoadingSkeleton';
import { formatCurrency } from '@/lib/utils';
import { AlertTriangle, Activity, Settings2, BarChart3, Info } from 'lucide-react';

function SimulationsContent() {
  const searchParams = useSearchParams();
  const initialPatternId = searchParams.get('patternId') || '';
  
  const [patterns, setPatterns] = useState<any[]>([]);
  const [patternId, setPatternId] = useState(initialPatternId);
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [scenarioId, setScenarioId] = useState('');
  
  const [runs, setRuns] = useState(1000);
  const [seed, setSeed] = useState(42);
  
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    fetch('http://localhost:8000/api/patterns')
      .then(r => r.json())
      .then(setPatterns);
  }, []);
  
  useEffect(() => {
    if (patternId) {
      fetch(`http://localhost:8000/api/simulations/pattern/${patternId}`)
        .then(r => r.json())
        .then(data => {
          setScenarios(data.scenarios);
          if (data.scenarios.length > 0 && !scenarioId) {
            setScenarioId(data.scenarios[0].scenario_id);
          }
        });
    }
  }, [patternId]);
  
  useEffect(() => {
    if (patternId && scenarioId) {
      setLoading(true);
      fetch('http://localhost:8000/api/simulations/intervention', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pattern_id: patternId, scenario_id: scenarioId, runs, seed })
      })
      .then(r => r.json())
      .then(data => {
        setResult(data);
        setLoading(false);
      });
    }
  }, [patternId, scenarioId, runs, seed]);
  
  return (
    <div className="flex flex-col space-y-8 pb-12 max-w-6xl mx-auto">
      {/* Warning Banner */}
      <div className="flex items-center gap-3 bg-amber-500/10 border border-amber-500/20 text-amber-500 px-4 py-3 rounded-lg">
        <AlertTriangle className="h-5 w-5 shrink-0" />
        <p className="text-sm font-medium">
          <strong>SIMULATION ONLY.</strong> No payment action will be executed on live systems. 
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Left Column: Controls */}
        <div className="space-y-6">
          <Card className="p-5 space-y-5">
            <div>
              <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground block mb-2">
                Target Pattern
              </label>
              <select 
                className="w-full bg-secondary border border-border text-secondary-foreground text-sm rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/20"
                value={patternId}
                onChange={e => setPatternId(e.target.value)}
              >
                <option value="">Select a pattern</option>
                {patterns.slice(0, 10).map(p => (
                  <option key={p.pattern_id} value={p.pattern_id}>{p.pattern_id}: {p.name || p.conditions[0]?.feature}</option>
                ))}
              </select>
            </div>
            
            <div>
              <div className="flex items-center gap-2 mb-3">
                <Settings2 className="h-4 w-4 text-muted-foreground" />
                <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Interventions</h3>
              </div>
              <div className="space-y-3">
                {scenarios.map(s => (
                  <label 
                    key={s.scenario_id} 
                    className={`block p-4 border rounded-lg cursor-pointer transition-all ${
                      scenarioId === s.scenario_id 
                        ? 'border-blue-500/50 bg-blue-950/10 ring-1 ring-blue-500/20' 
                        : 'border-border hover:border-muted-foreground/30'
                    }`}
                  >
                    <div className="flex items-start space-x-3">
                      <div className="mt-0.5">
                        <input 
                          type="radio" 
                          name="scenario" 
                          value={s.scenario_id} 
                          checked={scenarioId === s.scenario_id} 
                          onChange={() => setScenarioId(s.scenario_id)}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded-full"
                        />
                      </div>
                      <div>
                        <span className="text-sm font-semibold text-foreground block">{s.name}</span>
                        <span className="text-xs text-muted-foreground block mt-1">{s.intervention.name}</span>
                        <Badge variant="info" className="mt-2 text-[10px]">{s.effectiveness * 100}% Effective</Badge>
                      </div>
                    </div>
                  </label>
                ))}
              </div>
            </div>
            
            <div className="pt-4 border-t border-border">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">Parameters</h3>
              <div className="flex space-x-3">
                <div className="flex-1">
                  <label className="text-[10px] text-muted-foreground uppercase mb-1 block">Runs</label>
                  <input 
                    type="number" 
                    value={runs} 
                    onChange={e => setRuns(parseInt(e.target.value))} 
                    className="w-full bg-secondary border border-border text-secondary-foreground text-sm rounded-md px-2 py-1.5 focus:outline-none" 
                  />
                </div>
                <div className="flex-1">
                  <label className="text-[10px] text-muted-foreground uppercase mb-1 block">Seed</label>
                  <input 
                    type="number" 
                    value={seed} 
                    onChange={e => setSeed(parseInt(e.target.value))} 
                    className="w-full bg-secondary border border-border text-secondary-foreground text-sm rounded-md px-2 py-1.5 focus:outline-none" 
                  />
                </div>
              </div>
            </div>
          </Card>
        </div>
        
        {/* Right Column: Results */}
        <div className="lg:col-span-3 space-y-6">
          {!patternId ? (
            <Card className="h-64 flex flex-col items-center justify-center border-dashed bg-transparent">
               <Activity className="h-10 w-10 text-muted-foreground/50 mb-4" />
               <p className="text-muted-foreground font-medium">Select a pattern to run simulations</p>
            </Card>
          ) : loading ? (
             <div className="space-y-6 animate-pulse">
                <Card className="p-8 space-y-4">
                  <div className="h-6 bg-muted rounded w-1/4 mb-8"></div>
                  <div className="h-24 bg-muted rounded w-full"></div>
                </Card>
                <div className="grid grid-cols-2 gap-6">
                   <Card className="h-48 bg-muted"></Card>
                   <Card className="h-48 bg-muted"></Card>
                </div>
             </div>
          ) : result ? (
             <>
                {/* Decision Card */}
                <Card className={`p-6 sm:p-8 border-2 shadow-lg ${
                  result.recommendation === 'RECOMMEND_INTERVENTION' ? 'border-emerald-500/30 bg-emerald-950/10' : 
                  result.recommendation === 'DO_NOT_INTERVENE' ? 'border-red-500/30 bg-red-950/10' : 
                  'border-amber-500/30 bg-amber-950/10'
                }`}>
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                    <div>
                      <Badge variant={
                        result.recommendation === 'RECOMMEND_INTERVENTION' ? 'success' : 
                        result.recommendation === 'DO_NOT_INTERVENE' ? 'danger' : 'warning'
                      } className="mb-3 uppercase tracking-wider text-xs">
                        Simulation Decision
                      </Badge>
                      <h2 className={`text-2xl font-bold mb-2 ${
                        result.recommendation === 'RECOMMEND_INTERVENTION' ? 'text-emerald-400' : 
                        result.recommendation === 'DO_NOT_INTERVENE' ? 'text-red-400' : 'text-amber-400'
                      }`}>
                         {result.recommendation.replace(/_/g, ' ')}
                      </h2>
                      <p className="text-muted-foreground text-sm max-w-xl leading-relaxed">
                        {result.recommendation === 'RECOMMEND_INTERVENTION' && "The estimated net benefit is positive. Counterfactual simulation indicates that this intervention would statistically reduce loss without exceeding operational costs."}
                        {result.recommendation === 'DO_NOT_INTERVENE' && "The expected operational cost and friction exceed the estimated preventable loss. Recommendation is to monitor only."}
                        {result.recommendation === 'REQUIRE_MANUAL_REVIEW' && "Insufficient statistical confidence or marginal net benefit requires manual review before automated deployment."}
                      </p>
                    </div>
                    <div className="text-left sm:text-right bg-card/50 p-4 rounded-lg border border-border shrink-0">
                      <p className="text-[10px] uppercase tracking-wider font-semibold text-muted-foreground mb-1">Net Estimated Benefit</p>
                      <p className={`text-2xl font-mono font-bold ${result.net_estimated_benefit_paise >= 0 ? "text-emerald-500" : "text-red-500"}`}>
                        {result.net_estimated_benefit_paise >= 0 ? "+" : "-"} {formatCurrency(Math.abs(result.net_estimated_benefit_paise))}
                      </p>
                    </div>
                  </div>
                </Card>
                
                {/* Before/After Visualizer */}
                <Card className="p-6 sm:p-8">
                   <div className="flex items-center gap-2 mb-8">
                     <BarChart3 className="h-5 w-5 text-muted-foreground" />
                     <h3 className="text-lg font-semibold text-foreground">Observed vs Counterfactual</h3>
                   </div>
                   
                   <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                      <div className="relative">
                         <div className="flex justify-between items-end mb-4 border-b border-border pb-4">
                           <div>
                             <h4 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-1">Observed Loss</h4>
                             <p className="text-xs text-muted-foreground">Historical data</p>
                           </div>
                           <p className="text-3xl font-mono font-bold text-red-400">{formatCurrency(result.observed_loss_paise)}</p>
                         </div>
                         <div className="h-8 bg-red-500/20 rounded-md overflow-hidden border border-red-500/30">
                           <div className="h-full bg-red-500/60 w-full" />
                         </div>
                         <p className="text-xs text-muted-foreground mt-3 flex items-center">
                           <Info className="h-3 w-3 mr-1" /> All matches resulted in loss
                         </p>
                      </div>
                      
                      <div className="relative">
                         <div className="flex justify-between items-end mb-4 border-b border-border pb-4">
                           <div>
                             <h4 className="text-sm font-semibold uppercase tracking-wider text-blue-400 mb-1">Counterfactual</h4>
                             <p className="text-xs text-blue-400/70">Estimated residual</p>
                           </div>
                           <p className="text-3xl font-mono font-bold text-amber-500">{formatCurrency(result.estimated_residual_loss_paise)}</p>
                         </div>
                         
                         <div className="h-8 bg-secondary rounded-md overflow-hidden flex border border-border">
                           <div className="h-full bg-amber-500/60 transition-all duration-1000" style={{ width: `${(result.estimated_residual_loss_paise / result.observed_loss_paise) * 100}%` }} />
                           <div className="h-full flex-1 bg-[repeating-linear-gradient(45deg,transparent,transparent_10px,rgba(16,185,129,0.1)_10px,rgba(16,185,129,0.1)_20px)] border-l border-emerald-500/30 flex items-center justify-center">
                             <span className="text-[10px] font-bold text-emerald-500 tracking-wider">PREVENTED</span>
                           </div>
                         </div>
                         <p className="text-xs font-semibold text-emerald-500 mt-3 text-right">
                           {formatCurrency(result.estimated_prevented_loss_paise)} potentially prevented
                         </p>
                      </div>
                   </div>
                </Card>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Cost Benefit Analysis */}
                  <Card className="p-6">
                    <h3 className="text-sm font-semibold text-foreground mb-6">Financial Unit Economics</h3>
                    <div className="space-y-4">
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-muted-foreground">Estimated Prevented Loss</span>
                        <span className="text-emerald-400 font-mono">+ {formatCurrency(result.estimated_prevented_loss_paise)}</span>
                      </div>
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-muted-foreground">Intervention Cost (Assumed)</span>
                        <span className="text-red-400 font-mono">- {formatCurrency(result.intervention_cost_paise)}</span>
                      </div>
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-muted-foreground">False-Positive Friction Cost</span>
                        <span className="text-red-400 font-mono">- {formatCurrency(result.false_positive_cost_paise)}</span>
                      </div>
                      <div className="flex justify-between items-center font-bold pt-4 border-t border-border">
                        <span className="text-foreground">Net Estimated Benefit</span>
                        <span className={`font-mono ${result.net_estimated_benefit_paise >= 0 ? "text-emerald-500" : "text-red-500"}`}>
                          {result.net_estimated_benefit_paise >= 0 ? "+" : "-"} {formatCurrency(Math.abs(result.net_estimated_benefit_paise))}
                        </span>
                      </div>
                    </div>
                  </Card>
                  
                  {/* Uncertainty & Assumptions */}
                  <Card className="p-6">
                    <h3 className="text-sm font-semibold text-foreground mb-6">Simulation Uncertainty</h3>
                    <div className="flex justify-between text-center items-end mb-4">
                      <div>
                        <p className="text-[10px] uppercase text-muted-foreground mb-1 font-semibold">Worst Case (P10)</p>
                        <p className="font-mono text-sm text-foreground">{formatCurrency(result.confidence_interval.p10)}</p>
                      </div>
                      <div className="flex-1 px-6 pb-2">
                        <div className="w-full h-1.5 bg-secondary rounded-full relative">
                          <div className="absolute h-full bg-blue-500/40 rounded-full" style={{ left: '10%', right: '10%' }} />
                          <div className="absolute w-1.5 h-3 bg-blue-500 rounded-full top-1/2 -translate-y-1/2" style={{ left: '50%' }} />
                        </div>
                      </div>
                      <div>
                        <p className="text-[10px] uppercase text-muted-foreground mb-1 font-semibold">Best Case (P90)</p>
                        <p className="font-mono text-sm text-foreground">{formatCurrency(result.confidence_interval.p90)}</p>
                      </div>
                    </div>
                    <p className="text-center font-mono font-bold text-blue-400 text-sm mt-4">
                      Median: {formatCurrency(result.confidence_interval.median)}
                    </p>
                    
                    <div className="mt-6 pt-4 border-t border-border">
                      <h4 className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-2">Assumptions</h4>
                      <ul className="space-y-1">
                        {result.limitations.map((lim: string, idx: number) => (
                          <li key={idx} className="text-xs text-muted-foreground flex items-start">
                            <span className="mr-1.5 mt-1 h-1 w-1 shrink-0 rounded-full bg-muted-foreground" />
                            {lim}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </Card>
                </div>
             </>
          ) : null}
        </div>
      </div>
    </div>
  );
}

export default function SimulationsPage() {
  return (
    <Suspense fallback={<div className="p-8 flex justify-center"><LoadingSkeleton className="h-64 w-full" /></div>}>
      <SimulationsContent />
    </Suspense>
  );
}
