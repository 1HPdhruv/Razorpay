'use client';
import { useEffect, useState } from 'react';
import { StatCard } from "@/components/ui/StatCard";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { formatCurrency, formatNumber, formatMultiplier, classNames } from "@/lib/utils";
import { ArrowRight, AlertTriangle, CheckCircle2, Search, Zap, Loader2 } from "lucide-react";
import Link from 'next/link';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function Home() {
  const [health, setHealth] = useState<any>(null);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [patterns, setPatterns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    Promise.all([
      fetch('http://localhost:8000/api/health').then(r => r.json()),
      fetch('http://localhost:8000/api/transactions').then(r => r.json()),
      fetch('http://localhost:8000/api/patterns').then(r => r.json())
    ])
    .then(([healthData, txData, patternsData]) => {
      setHealth(healthData);
      setTransactions(txData);
      setPatterns(patternsData);
    })
    .catch(console.error)
    .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  const topPatterns = patterns.slice(0, 5);
  const maxNetBenefitPaise = health?.evaluation?.simulation?.length > 0 
    ? Math.max(...health.evaluation.simulation.map((s:any) => s.net_benefit_paise)) 
    : 0;

  const chartData = topPatterns.map(p => {
    const exposurePaise = typeof p.exposure_amount === "number" ? p.exposure_amount : null;
    return {
      name: p.pattern_id,
      exposure: exposurePaise !== null ? exposurePaise / 100 : null,
      exposureFormatted: exposurePaise !== null ? formatCurrency(exposurePaise) : '—'
    };
  });

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-popover border border-border p-3 rounded-lg shadow-lg">
          <p className="text-sm font-semibold text-foreground">{label}</p>
          <p className="text-sm text-red-400">Exposure: {payload[0].payload.exposureFormatted}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="flex flex-col space-y-8">
      {/* KPI Cards */}
      {health && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard 
            title="Transactions" 
            value={formatNumber(health.transaction_count)}
            subtitle="Analyzed"
            icon={<Search className="h-4 w-4" />}
          />
          <StatCard 
            title="Patterns" 
            value={health.pattern_count}
            subtitle="Discovered"
            icon={<NetworkIcon className="h-4 w-4 text-blue-500" />}
          />
          <StatCard 
            title="Validated" 
            value={health.evaluation?.discovery?.pattern_count || 0}
            subtitle="On held-out test data"
            icon={<CheckCircle2 className="h-4 w-4 text-emerald-500" />}
          />
          <StatCard 
            title="Potential Loss" 
            value={formatCurrency(maxNetBenefitPaise)}
            subtitle="Estimated preventable loss"
            icon={<AlertTriangle className="h-4 w-4 text-amber-500" />}
          />
        </div>
      )}

      {/* Discovery Insights */}
      {health?.evaluation?.discovery && (
        <Card className="p-6 bg-blue-950/20 border-blue-900/50">
          <div className="flex items-start gap-4">
            <div className="p-2 bg-blue-900/50 rounded-lg">
              <Zap className="h-6 w-6 text-blue-400" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-blue-400 mb-1">WHAT THE SYSTEM FOUND</h3>
              <p className="text-sm text-muted-foreground max-w-4xl leading-relaxed">
                The discovery engine identified previously unspecified payment-event combinations associated with elevated loss. 
                <strong className="text-foreground font-medium"> {health.evaluation.discovery.pattern_count} patterns </strong> 
                remained elevated on held-out data. The strongest pattern exhibits a risk multiplier of 
                <strong className="text-foreground font-medium"> {formatMultiplier(health.evaluation.discovery.top_pattern_risk_multiplier)} </strong> 
                with support across {health.evaluation.discovery.top_pattern_test_support} transactions.
              </p>
            </div>
          </div>
        </Card>
      )}

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Top Patterns */}
        <div className="col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Top Emergent Patterns</h2>
            <Link href="/patterns" className="text-sm text-primary hover:underline font-medium flex items-center">
              View all <ArrowRight className="ml-1 h-4 w-4" />
            </Link>
          </div>
          
          <div className="space-y-4">
            {topPatterns.map((pattern, i) => (
              <Card key={pattern.pattern_id} className={classNames("p-5 transition-all hover:border-muted-foreground/30", i === 0 ? "border-purple-500/30 bg-purple-950/10 shadow-[0_0_15px_rgba(168,85,247,0.05)]" : "")}>
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-center gap-2">
                    <Badge variant={i === 0 ? "emergent" : "default"}>
                      {pattern.pattern_id}
                    </Badge>
                    {i === 0 && <span className="text-xs font-semibold text-purple-400 uppercase tracking-widest">Top Risk Candidate</span>}
                  </div>
                  <Badge variant="success">✓ Validated</Badge>
                </div>
                
                <div className="flex flex-wrap items-center gap-2 mb-6">
                  {pattern.conditions.map((cond: any, idx: number) => (
                    <div key={idx} className="flex items-center">
                      <span className="text-sm font-medium bg-secondary px-2.5 py-1 rounded-md text-secondary-foreground border border-border">
                        {cond.feature}
                      </span>
                      {idx < pattern.conditions.length - 1 && (
                        <span className="text-muted-foreground mx-2 text-xs font-bold">+</span>
                      )}
                    </div>
                  ))}
                </div>

                <div className="grid grid-cols-3 gap-4 py-4 border-t border-border">
                  <div>
                    <p className="text-xs text-muted-foreground mb-1 uppercase font-semibold">Risk Multiplier</p>
                    <p className="text-lg font-mono text-red-400">{formatMultiplier(pattern.risk_multiplier)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground mb-1 uppercase font-semibold">Test Support</p>
                    <p className="text-lg font-mono text-foreground">{formatNumber(pattern.matching_transaction_count ?? 0)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground mb-1 uppercase font-semibold">Exposure</p>
                    <p className="text-lg font-mono text-foreground">{typeof pattern.exposure_amount === "number" ? formatCurrency(pattern.exposure_amount) : '—'}</p>
                  </div>
                </div>

                <div className="mt-4 flex justify-end">
                  <Link href={`/investigations/${pattern.pattern_id}`}>
                    <Button variant={i === 0 ? "default" : "outline"} size="sm">
                      Investigate Pattern <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Right Column: Chart & Decisions */}
        <div className="space-y-6">
          <h2 className="text-lg font-semibold">Loss Exposure by Pattern</h2>
          <Card className="p-6 h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} layout="vertical" margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                <XAxis type="number" hide />
                <YAxis dataKey="name" type="category" width={60} axisLine={false} tickLine={false} tick={{fill: '#a1a1aa', fontSize: 12}} />
                <Tooltip content={<CustomTooltip />} cursor={{fill: '#27272a', opacity: 0.4}} />
                <Bar dataKey="exposure" fill="#f87171" radius={[0, 4, 4, 0]} maxBarSize={32} />
              </BarChart>
            </ResponsiveContainer>
          </Card>

          <h2 className="text-lg font-semibold pt-4">Decision Summary</h2>
          <Card className="divide-y divide-border">
            <div className="p-4 flex justify-between items-center">
              <span className="text-sm font-medium text-muted-foreground">Patterns requiring review</span>
              <span className="text-lg font-mono text-foreground">{patterns.filter(p => p.risk_multiplier > 5 && p.risk_multiplier <= 10).length}</span>
            </div>
            <div className="p-4 flex justify-between items-center">
              <span className="text-sm font-medium text-muted-foreground">Recommended interventions</span>
              <span className="text-lg font-mono text-red-400">{patterns.filter(p => p.risk_multiplier > 10).length}</span>
            </div>
            <div className="p-4 flex justify-between items-center">
              <span className="text-sm font-medium text-muted-foreground">Do not intervene</span>
              <span className="text-lg font-mono text-emerald-500">{patterns.filter(p => p.risk_multiplier <= 5).length}</span>
            </div>
          </Card>
        </div>
      </div>

      {/* Transaction Table */}
      <div className="pt-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Transaction Stream</h2>
          <Badge variant="default" className="text-xs font-mono">{transactions.length} rows preview</Badge>
        </div>
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="bg-secondary/50 text-muted-foreground text-xs uppercase font-semibold">
                <tr>
                  <th className="px-6 py-4">Transaction</th>
                  <th className="px-6 py-4 text-right">Amount</th>
                  <th className="px-6 py-4">Gateway</th>
                  <th className="px-6 py-4">Method</th>
                  <th className="px-6 py-4">Outcome</th>
                  <th className="px-6 py-4">Loss</th>
                  <th className="px-6 py-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {transactions.map((tx) => (
                  <tr key={tx.transaction_id} className="hover:bg-muted/50 transition-colors group">
                    <td className="px-6 py-4 font-mono text-muted-foreground group-hover:text-foreground transition-colors">{tx.transaction_id}</td>
                    <td className="px-6 py-4 text-right font-medium">{formatCurrency(tx.amount_paise)}</td>
                    <td className="px-6 py-4">
                       <Badge variant="default">{tx.gateway}</Badge>
                    </td>
                    <td className="px-6 py-4 text-muted-foreground">{tx.payment_method}</td>
                    <td className="px-6 py-4">
                      <Badge variant={tx.outcome === 'SUCCESS' ? 'success' : 'danger'}>
                        {tx.outcome}
                      </Badge>
                    </td>
                    <td className="px-6 py-4">
                      {tx.loss_flag ? (
                        <Badge variant="danger">Yes</Badge>
                      ) : (
                        <span className="text-muted-foreground">—</span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Button variant="ghost" size="sm" className="h-8 px-2 text-muted-foreground group-hover:text-primary">
                        View DNA
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>

    </div>
  );
}

function NetworkIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect x="16" y="16" width="6" height="6" rx="1" />
      <rect x="2" y="16" width="6" height="6" rx="1" />
      <rect x="9" y="2" width="6" height="6" rx="1" />
      <path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3" />
      <path d="M12 12V8" />
    </svg>
  )
}
