'use client';

import { API_BASE_URL } from '@/lib/api';
import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { LoadingSkeleton } from '@/components/ui/LoadingSkeleton';
import { formatCurrency, formatMultiplier } from '@/lib/utils';
import { ArrowRight, FileSearch, Loader2, Search, ShieldAlert } from 'lucide-react';

export default function Investigations() {
  const [patterns, setPatterns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/patterns`)
      .then(async (r) => {
        if (!r.ok) throw new Error(`Unable to load patterns (${r.status})`);
        return r.json();
      })
      .then(setPatterns)
      .catch((e) => setError(e.message || 'Unable to load investigations'))
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return patterns;
    return patterns.filter((p) =>
      [p.pattern_id, p.name, p.pattern_type, ...(p.conditions || []).map((c: any) => `${c.feature} ${c.operator} ${c.value}`)]
        .filter(Boolean)
        .join(' ')
        .toLowerCase()
        .includes(q)
    );
  }, [patterns, query]);

  if (loading) {
    return (
      <div className="space-y-8 max-w-6xl mx-auto">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Investigations</h1>
          <p className="mt-2 text-muted-foreground">Evidence-backed investigation of discovered loss patterns.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => <LoadingSkeleton key={i} className="h-64 w-full" />)}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <Card className="max-w-3xl mx-auto p-8 text-center space-y-4">
        <ShieldAlert className="h-10 w-10 mx-auto text-red-400" />
        <h2 className="text-xl font-bold text-foreground">Investigations failed to load</h2>
        <p className="text-muted-foreground">{error}</p>
        <Button variant="outline" onClick={() => window.location.reload()}>Retry</Button>
      </Card>
    );
  }

  return (
    <div className="flex flex-col space-y-8 pb-12 max-w-6xl mx-auto">
      <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <FileSearch className="h-6 w-6 text-blue-400" />
            <h1 className="text-3xl font-bold tracking-tight text-foreground">Investigations</h1>
          </div>
          <p className="mt-2 text-muted-foreground">Turn discovered patterns into evidence-backed risk investigations.</p>
        </div>
        <div className="relative w-full md:w-80">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search pattern or condition..."
            className="w-full rounded-md border border-border bg-secondary pl-9 pr-3 py-2 text-sm text-white placeholder:text-muted-foreground outline-none focus:ring-2 focus:ring-blue-500/30"
          />
        </div>
      </div>

      <div className="flex items-center justify-between text-sm text-muted-foreground">
        <span>{filtered.length} pattern{filtered.length === 1 ? '' : 's'} available for investigation</span>
        {query && <button className="hover:text-foreground" onClick={() => setQuery('')}>Clear search</button>}
      </div>

      {filtered.length === 0 ? (
        <Card className="p-12 text-center">
          <Loader2 className="h-8 w-8 mx-auto mb-3 text-muted-foreground" />
          <p className="text-foreground font-medium">No matching patterns</p>
          <p className="text-sm text-muted-foreground mt-1">Try another search term.</p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {filtered.map((p) => (
            <Card key={p.pattern_id} className="p-6 flex flex-col h-full hover:border-blue-500/40 transition-colors">
              <div className="flex items-start justify-between gap-3 mb-4">
                <Badge variant="emergent">{p.pattern_type || 'EMERGENT'}</Badge>
                <span className="font-mono text-xs text-muted-foreground">{p.pattern_id}</span>
              </div>
              <h2 className="text-lg font-semibold text-foreground mb-3">{p.name || (p.conditions || []).map((c: any) => c.feature).join(' + ') || 'Loss pattern'}</h2>
              <div className="space-y-2 mb-6">
                {(p.conditions || []).slice(0, 3).map((c: any, i: number) => (
                  <div key={i} className="text-xs rounded border border-border bg-secondary px-2 py-1.5 text-secondary-foreground">
                    <span className="font-medium">{c.feature}</span> <span className="text-muted-foreground">{c.operator}</span> <span className="font-mono">{c.value}</span>
                  </div>
                ))}
              </div>
              <div className="grid grid-cols-2 gap-4 border-t border-border pt-4 mt-auto mb-5">
                <div><p className="text-[10px] uppercase text-muted-foreground">Risk multiplier</p><p className="font-mono text-red-400">{formatMultiplier(p.risk_multiplier)}</p></div>
                <div><p className="text-[10px] uppercase text-muted-foreground">Exposure</p><p className="font-mono text-foreground">{typeof p.exposure_amount === 'number' ? formatCurrency(p.exposure_amount) : '—'}</p></div>
              </div>
              <Link href={`/investigations/${p.pattern_id}`}>
                <Button className="w-full" variant="outline">Open Investigation <ArrowRight className="ml-2 h-4 w-4" /></Button>
              </Link>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
