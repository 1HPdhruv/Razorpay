'use client';
import { API_BASE_URL } from "@/lib/api";
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { formatCurrency } from '@/lib/utils';
import { ArrowLeft, BrainCircuit, Search, Info, ShieldAlert, FileText, ChevronRight, ArrowRight } from 'lucide-react';
import { LoadingSkeleton } from '@/components/ui/LoadingSkeleton';

export default function InvestigationDetail({ params }: { params: { patternId: string } }) {
  const [report, setReport] = useState<any>(null);
  const [error, setError] = useState('');
  
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/investigations/${params.patternId}`)
      .then(async r => {
        if (!r.ok) throw new Error(await r.text());
        return r.json();
      })
      .then(setReport)
      .catch(e => setError(e.message));
  }, [params.patternId]);

  if (error) {
    return (
      <Card className="p-8 max-w-3xl mx-auto flex flex-col items-center justify-center text-center space-y-4">
        <ShieldAlert className="h-10 w-10 text-destructive" />
        <h2 className="text-xl font-bold text-foreground">Unable to load investigation</h2>
        <p className="text-muted-foreground">{error}</p>
        <Button onClick={() => window.location.reload()} variant="outline">Retry</Button>
      </Card>
    );
  }

  if (!report) {
    return (
      <div className="max-w-5xl mx-auto space-y-8">
        <div className="space-y-4">
          <LoadingSkeleton className="h-8 w-64" />
          <LoadingSkeleton className="h-4 w-32" />
        </div>
        <Card className="p-8 space-y-4">
          <LoadingSkeleton className="h-8 w-3/4" />
          <LoadingSkeleton className="h-4 w-1/2" />
        </Card>
      </div>
    );
  }

  return (
    <div className="flex flex-col space-y-8 pb-12 max-w-5xl mx-auto">
      <div className="flex flex-col space-y-4 sm:flex-row sm:items-center sm:justify-between sm:space-y-0">
        <div>
          <Link href="/patterns" className="inline-flex items-center text-sm font-medium text-muted-foreground hover:text-foreground mb-4">
            <ArrowLeft className="mr-2 h-4 w-4" /> Back to Patterns
          </Link>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight text-foreground">{report.pattern_id}</h1>
            <Badge variant="emergent">EMERGENT LOSS PATTERN</Badge>
          </div>
        </div>
      </div>

      {/* AI Finding */}
      <Card className="p-6 bg-blue-950/20 border-blue-900/50 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-4 opacity-10">
          <BrainCircuit className="h-24 w-24 text-blue-400" />
        </div>
        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-3">
            <Badge variant="info" className="uppercase tracking-widest text-[10px]">AI-Generated Interpretation</Badge>
            <span className="text-xs text-muted-foreground flex items-center">
              <Info className="h-3 w-3 mr-1" /> Evidence-backed
            </span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-semibold leading-tight text-blue-100 max-w-3xl">
            {report.headline}
          </h2>
        </div>
      </Card>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column */}
        <div className="space-y-8">
          <Card className="p-6 space-y-4">
            <div className="flex items-center gap-2 mb-2">
              <Search className="h-5 w-5 text-muted-foreground" />
              <h3 className="text-lg font-semibold text-foreground">Observed Evidence</h3>
            </div>
            <ul className="space-y-3">
              {report.observations.map((obs: string, idx: number) => (
                <li key={idx} className="flex items-start text-sm text-muted-foreground">
                  <span className="mr-2 mt-1 flex h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" />
                  {obs}
                </li>
              ))}
            </ul>
          </Card>
          
          <Card className="p-6 space-y-4 bg-muted/30">
            <div className="flex items-center gap-2 mb-2">
              <BrainCircuit className="h-5 w-5 text-muted-foreground" />
              <h3 className="text-lg font-semibold text-foreground">Possible Mechanism</h3>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              <span className="font-semibold text-foreground mr-2">Hypothesis:</span>
              {report.possible_mechanism}
            </p>
          </Card>
        </div>
        
        {/* Right Column */}
        <div className="space-y-8">
          <Card className="p-6">
            <h3 className="text-lg font-semibold text-foreground mb-6">Financial Impact</h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <p className="text-[10px] text-muted-foreground uppercase tracking-widest font-semibold mb-2">Observed Loss</p>
                <p className="text-3xl font-mono font-bold text-red-400">
                  {formatCurrency(report.financial_exposure.observed_loss)}
                </p>
              </div>
              <div>
                <p className="text-[10px] text-muted-foreground uppercase tracking-widest font-semibold mb-2">Potential Exposure</p>
                <p className="text-3xl font-mono font-bold text-red-400">
                  {formatCurrency(report.financial_exposure.potential_exposure)}
                </p>
                <p className="text-xs text-muted-foreground mt-1">Not realized savings</p>
              </div>
            </div>
          </Card>
          
          <Card className="p-6 border-blue-900/50 bg-blue-950/10">
            <h3 className="text-lg font-semibold text-blue-400 mb-2">Recommended Control</h3>
            <p className="text-sm text-muted-foreground mb-6">{report.recommended_control}</p>
            <Link href={`/simulations?patternId=${report.pattern_id}`}>
              <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white shadow-none">
                Simulate Control <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </Card>
        </div>
      </div>

      {/* Vertical Timeline */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold text-foreground mb-6">Event Timeline</h3>
        <div className="relative border-l border-border ml-3 space-y-8 pb-4">
          <div className="relative pl-6">
            <span className="absolute -left-1.5 top-1.5 h-3 w-3 rounded-full bg-primary ring-4 ring-card" />
            <div className="flex flex-col">
              <span className="text-sm font-semibold text-foreground">Payment Attempt</span>
            </div>
          </div>
          <div className="relative pl-6">
            <span className="absolute -left-1.5 top-1.5 h-3 w-3 rounded-full bg-muted-foreground ring-4 ring-card" />
            <div className="flex flex-col">
              <span className="text-sm font-medium text-muted-foreground">Gateway Latency / Timeout</span>
            </div>
          </div>
          <div className="relative pl-6">
            <span className="absolute -left-1.5 top-1.5 h-3 w-3 rounded-full bg-amber-500 ring-4 ring-card" />
            <div className="flex flex-col">
              <span className="text-sm font-medium text-amber-500">Rapid Retry / Duplicate Capture</span>
            </div>
          </div>
          <div className="relative pl-6">
            <span className="absolute -left-1.5 top-1.5 h-3 w-3 rounded-full bg-red-500 ring-4 ring-card" />
            <div className="flex flex-col">
              <span className="text-sm font-bold text-red-500">Merchant Loss Recorded</span>
            </div>
          </div>
        </div>
      </Card>
      
      {/* Evidence Cards */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <FileText className="h-5 w-5 text-muted-foreground" />
          <h3 className="text-lg font-semibold text-foreground">Supporting Evidence</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {report.supporting_evidence.map((cit: any, idx: number) => (
            <Card key={idx} className="p-5 flex flex-col justify-between">
              <div>
                <p className="text-sm text-foreground font-medium mb-4">{cit.claim}</p>
                <div className="flex flex-wrap gap-2">
                  {cit.evidence_ids.map((id: string) => (
                    <Badge key={id} variant="default" className="font-mono text-[10px] text-muted-foreground">
                      {id}
                    </Badge>
                  ))}
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
      
      {report.limitations.length > 0 && (
        <Card className="p-6 border-dashed border-border bg-transparent">
          <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-4">Limitations & Assumptions</h3>
          <ul className="space-y-2">
            {report.limitations.map((lim: string, idx: number) => (
              <li key={idx} className="flex items-start text-xs text-muted-foreground">
                <ChevronRight className="mr-1 h-4 w-4 shrink-0 text-muted-foreground" />
                {lim}
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}
