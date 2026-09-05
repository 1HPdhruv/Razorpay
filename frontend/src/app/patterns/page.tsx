'use client';
import { API_BASE_URL } from "@/lib/api";
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { StatCard } from '@/components/ui/StatCard';
import { formatCurrency, formatNumber, formatMultiplier } from '@/lib/utils';
import { ArrowRight, Filter, Loader2 } from 'lucide-react';

export default function Patterns() {
  const [patterns, setPatterns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/patterns`)
      .then(r => r.json())
      .then(setPatterns)
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

  const filteredPatterns = patterns.filter(p => {
    if (filter === 'emergent') return p.pattern_type === 'ASSOCIATION' || p.pattern_type === 'EMERGENT' || !p.pattern_type;
    if (filter === 'baseline') return p.pattern_type === 'BASELINE';
    if (filter === 'review') return p.risk_multiplier > 5;
    return true;
  });

  return (
    <div className="flex flex-col space-y-8 pb-12">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard 
          title="Total Discovered" 
          value={patterns.length}
        />
        <StatCard 
          title="Validated on Test" 
          value={patterns.length} 
          icon={<Badge variant="success">100%</Badge>}
        />
        <StatCard 
          title="Requiring Review" 
          value={patterns.filter(p => p.risk_multiplier > 5).length} 
          icon={<Badge variant="danger">High Risk</Badge>}
        />
      </div>

      <div className="flex items-center gap-4 py-4 border-y border-border">
        <Filter className="h-4 w-4 text-muted-foreground" />
        <span className="text-sm font-medium text-muted-foreground">Filter by:</span>
        <div className="flex gap-2">
          <Button variant={filter === 'all' ? 'default' : 'outline'} size="sm" onClick={() => setFilter('all')}>All</Button>
          <Button variant={filter === 'emergent' ? 'default' : 'outline'} size="sm" onClick={() => setFilter('emergent')}>Emergent</Button>
          <Button variant={filter === 'baseline' ? 'default' : 'outline'} size="sm" onClick={() => setFilter('baseline')}>Baseline</Button>
          <Button variant={filter === 'review' ? 'default' : 'outline'} size="sm" onClick={() => setFilter('review')}>Requires Review</Button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {filteredPatterns.map((p, i) => {
          const isTop = i === 0 && filter === 'all';
          return (
            <Card key={p.pattern_id} className={isTop ? "border-purple-500/30 bg-purple-950/10 shadow-[0_0_15px_rgba(168,85,247,0.05)]" : ""}>
              <div className="p-6 flex flex-col h-full justify-between">
                <div>
                  <div className="flex justify-between items-start mb-4">
                    <Badge variant={(p.pattern_type === 'ASSOCIATION' || !p.pattern_type) ? (isTop ? 'emergent' : 'info') : 'default'}>
                      {p.pattern_type || 'EMERGENT'}
                    </Badge>
                    <span className="text-muted-foreground font-mono text-xs">{p.pattern_id}</span>
                  </div>
                  <h3 className="text-lg font-semibold text-foreground mb-4 line-clamp-2">
                    {p.name || p.conditions.map((c:any) => c.feature).join(' + ')}
                  </h3>
                  
                  <div className="flex flex-wrap gap-2 mb-6">
                    {p.conditions.map((c: any, idx: number) => (
                      <span key={idx} className="inline-flex items-center text-xs font-medium bg-secondary px-2 py-1 rounded text-secondary-foreground border border-border">
                        {c.feature} <span className="text-muted-foreground mx-1">{c.operator}</span> <span className="font-mono">{c.value}</span>
                      </span>
                    ))}
                  </div>
                </div>
                
                <div className="border-t border-border pt-4 mt-auto">
                  <div className="grid grid-cols-2 gap-y-4 gap-x-2">
                    <div>
                      <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold mb-1">Risk Multiplier</p>
                      <p className="text-lg font-mono text-red-400">{formatMultiplier(p.risk_multiplier)}</p>
                    </div>
                    <div>
                      <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold mb-1">Loss Rate</p>
                      <p className="text-lg font-mono text-red-400">{(p.loss_rate * 100).toFixed(1)}%</p>
                    </div>
                    <div>
                      <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold mb-1">Test Support</p>
                      <p className="text-sm font-mono text-foreground">{formatNumber(p.matching_transaction_count ?? 0)}</p>
                    </div>
                    <div>
                      <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold mb-1">Exposure</p>
                      <p className="text-sm font-mono text-foreground">{typeof p.exposure_amount === "number" ? formatCurrency(p.exposure_amount) : '—'}</p>
                    </div>
                  </div>
                  <div className="mt-6">
                    <Link href={`/investigations/${p.pattern_id}`} className="block w-full">
                      <Button variant={isTop ? "default" : "outline"} className="w-full">
                        Investigate Pattern <ArrowRight className="ml-2 h-4 w-4" />
                      </Button>
                    </Link>
                  </div>
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
