"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { StatCard } from "@/components/ui/StatCard";
import { AlertTriangle, CheckCircle, XCircle, RefreshCw, Activity, ShieldAlert, FileText } from "lucide-react";

interface IntegrationStatus {
  enabled: boolean;
  mode: string;
  credentials_configured: boolean;
  webhook_secret_configured: boolean;
  events_received: number;
  events_processed: number;
  events_failed: number;
  events_duplicate: number;
  unmatched_events: number;
  last_webhook_received_at: string | null;
}

interface AuditEvent {
  provider: string;
  provider_event_id: string;
  event_type: string;
  received_at: string;
  verification_status: string;
  processing_status: string;
  internal_event_id: string | null;
}

export default function RazorpayIntegrationPage() {
  const [status, setStatus] = useState<IntegrationStatus | null>(null);
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<{success: boolean; message: string} | null>(null);
  const [simulating, setSimulating] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [statusRes, eventsRes] = await Promise.all([
        fetch('http://localhost:8000/api/integrations/razorpay/status'),
        fetch('http://localhost:8000/api/integrations/razorpay/events')
      ]);
      if (statusRes.ok) {
        setStatus(await statusRes.json());
      }
      if (eventsRes.ok) {
        setEvents(await eventsRes.json());
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleTestConnection = async () => {
    setTesting(true);
    try {
      const res = await fetch('http://localhost:8000/api/integrations/razorpay/test-connection', {
        method: 'POST'
      });
      const data = await res.json();
      setTestResult({
        success: res.ok && data.success,
        message: data.detail || data.message || "Connection failed"
      });
    } catch (e) {
      setTestResult({ success: false, message: "Network error" });
    } finally {
      setTesting(false);
      fetchData();
    }
  };

  const simulateWebhook = async (fixtureId: string) => {
    setSimulating(true);
    try {
      await fetch(`http://localhost:8000/api/webhooks/razorpay/simulate?fixture_id=${fixtureId}`, {
        method: 'POST'
      });
      await fetchData();
    } catch (e) {
      console.error(e);
    } finally {
      setSimulating(false);
    }
  };

  if (loading && !status) return <div className="animate-pulse flex space-x-4"><div className="h-4 bg-muted rounded w-1/4"></div></div>;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Razorpay Integration</h1>
          <p className="text-muted-foreground mt-2">
            Connect Razorpay Test Mode to safely ingest webhook events for pattern observation.
          </p>
        </div>
        <Button onClick={fetchData} variant="outline">
          <RefreshCw className="mr-2 h-4 w-4" /> Refresh
        </Button>
      </div>

      {/* Safety Notice */}
      <div className="bg-destructive/10 border border-destructive/20 text-destructive-foreground p-4 rounded-lg flex items-start space-x-3">
        <ShieldAlert className="h-5 w-5 text-destructive mt-0.5" />
        <div>
          <h3 className="font-semibold text-destructive text-sm">Test Mode Only</h3>
          <p className="text-sm mt-1 opacity-90">
            This integration operates strictly in Test Mode for observation and analytics. Financial interventions remain simulation-only. Real payments, refunds, and captures will NEVER be initiated automatically.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left Col: Config & Status */}
        <div className="md:col-span-1 space-y-6">
          <Card className="p-6 space-y-6">
            <h2 className="text-lg font-semibold flex items-center">
              <Activity className="mr-2 h-5 w-5 text-primary" /> Configuration
            </h2>
            
            <div className="space-y-4">
              <div className="flex justify-between items-center pb-4 border-b border-border">
                <span className="text-sm text-muted-foreground">Mode</span>
                {status?.mode === 'test' ? (
                  <Badge variant="default" className="bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500/20">Test Mode</Badge>
                ) : (
                  <Badge variant="danger">Invalid Mode</Badge>
                )}
              </div>
              <div className="flex justify-between items-center pb-4 border-b border-border">
                <span className="text-sm text-muted-foreground">API Credentials</span>
                {status?.credentials_configured ? (
                  <span className="flex items-center text-emerald-500 text-sm font-medium"><CheckCircle className="mr-1 h-4 w-4" /> Configured</span>
                ) : (
                  <span className="flex items-center text-muted-foreground text-sm"><XCircle className="mr-1 h-4 w-4" /> Not configured</span>
                )}
              </div>
              <div className="flex justify-between items-center pb-4 border-b border-border">
                <span className="text-sm text-muted-foreground">Webhook Secret</span>
                {status?.webhook_secret_configured ? (
                  <span className="flex items-center text-emerald-500 text-sm font-medium"><CheckCircle className="mr-1 h-4 w-4" /> Verified</span>
                ) : (
                  <span className="flex items-center text-muted-foreground text-sm"><XCircle className="mr-1 h-4 w-4" /> Unverified</span>
                )}
              </div>
              
              <div className="pt-2">
                <Button 
                  className="w-full" 
                  onClick={handleTestConnection} 
                  disabled={testing || !status?.credentials_configured}
                >
                  {testing ? "Testing..." : "Test Connection"}
                </Button>
                
                {testResult && (
                  <div className={`mt-3 text-sm p-3 rounded-md flex items-start ${testResult.success ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20' : 'bg-destructive/10 text-destructive border border-destructive/20'}`}>
                    {testResult.success ? <CheckCircle className="h-4 w-4 mr-2 mt-0.5 flex-shrink-0" /> : <AlertTriangle className="h-4 w-4 mr-2 mt-0.5 flex-shrink-0" />}
                    <span>{testResult.message}</span>
                  </div>
                )}
              </div>
            </div>
          </Card>

          <Card className="p-6 space-y-4">
             <h2 className="text-lg font-semibold flex items-center">
              <FileText className="mr-2 h-5 w-5 text-primary" /> Simulate Events
            </h2>
            <p className="text-sm text-muted-foreground">
              Send synthetic fixtures through the webhook pipeline.
            </p>
            <div className="space-y-2 pt-2">
              <Button variant="outline" className="w-full justify-start text-xs h-9" onClick={() => simulateWebhook('capture')} disabled={simulating}>
                payment.captured
              </Button>
              <Button variant="outline" className="w-full justify-start text-xs h-9" onClick={() => simulateWebhook('failed')} disabled={simulating}>
                payment.failed
              </Button>
              <Button variant="outline" className="w-full justify-start text-xs h-9" onClick={() => simulateWebhook('refund')} disabled={simulating}>
                refund.created
              </Button>
            </div>
          </Card>
        </div>

        {/* Right Col: Metrics & Log */}
        <div className="md:col-span-2 space-y-6">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard title="Received" value={status?.events_received || 0} />
            <StatCard title="Processed" value={status?.events_processed || 0} />
            <StatCard title="Duplicates" value={status?.events_duplicate || 0} />
            <StatCard title="Failed/Unmatched" value={(status?.events_failed || 0) + (status?.unmatched_events || 0)} />
          </div>

          <Card className="p-0 overflow-hidden">
            <div className="p-6 border-b border-border">
              <h2 className="text-lg font-semibold">Webhook Event Log</h2>
            </div>
            
            {events.length === 0 ? (
              <div className="p-12 text-center text-muted-foreground text-sm">
                No events received yet. Configure webhook in Razorpay Test Mode or use the simulation tools.
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm text-left whitespace-nowrap">
                  <thead className="text-xs text-muted-foreground bg-muted/50 uppercase border-b border-border">
                    <tr>
                      <th className="px-6 py-3 font-medium">Time</th>
                      <th className="px-6 py-3 font-medium">Event</th>
                      <th className="px-6 py-3 font-medium">Status</th>
                      <th className="px-6 py-3 font-medium">Source</th>
                    </tr>
                  </thead>
                  <tbody>
                    {events.map((evt, idx) => (
                      <tr key={idx} className="border-b border-border/50 hover:bg-muted/20 transition-colors">
                        <td className="px-6 py-4 text-muted-foreground">
                          {new Date(evt.received_at).toLocaleTimeString()}
                        </td>
                        <td className="px-6 py-4 font-medium font-mono text-xs">
                          {evt.event_type}
                        </td>
                        <td className="px-6 py-4">
                          {evt.processing_status === 'processed' ? (
                            <Badge variant="default" className="bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500/10">Processed</Badge>
                          ) : evt.processing_status === 'duplicate' ? (
                            <Badge variant="default" className="bg-transparent border border-border text-muted-foreground">Duplicate</Badge>
                          ) : (
                            <Badge variant="danger">{evt.processing_status}</Badge>
                          )}
                        </td>
                        <td className="px-6 py-4 text-muted-foreground text-xs flex items-center">
                          {evt.provider === 'razorpay' ? 'Razorpay Test' : evt.provider}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}
