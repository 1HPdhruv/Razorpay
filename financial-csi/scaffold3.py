import os

def write_file(path, content=""):
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

# MODELS (Pydantic / placeholders)
write_file("backend/app/models/transaction.py", """
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    transaction_id: str
    order_id: str
    customer_id: str
    merchant_id: str
    amount: float
    currency: str
    payment_method: str
    gateway: str
    created_at: datetime
    outcome: str
    loss_flag: bool
    loss_amount: float
    loss_type: Optional[str] = None
""")

write_file("backend/app/models/event.py", """
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventBase(BaseModel):
    event_id: str
    transaction_id: str
    event_type: str
    timestamp: datetime
    status: str
    amount: Optional[float] = None
    metadata: dict = {}
""")

write_file("backend/app/models/pattern.py", """
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PatternBase(BaseModel):
    pattern_id: str
    name: str
    description: str
    risk_level: str
    conditions: dict
    transaction_count: int
    loss_count: int
    loss_rate: float
    baseline_loss_rate: float
    risk_multiplier: float
    exposure_amount: float
    confidence: float
    discovery_method: str
    is_predefined: bool
    evidence_transaction_ids: List[str]
    created_at: datetime
""")

write_file("backend/app/models/investigation.py", """
from pydantic import BaseModel
from typing import List

class InvestigationBase(BaseModel):
    investigation_id: str
    pattern_id: str
    explanation: str
    evidence_events: List[dict]
""")

write_file("backend/app/models/simulation.py", """
from pydantic import BaseModel

class SimulationBase(BaseModel):
    simulation_id: str
    pattern_id: str
    intervention_type: str
    prevented_loss: float
""")

write_file("backend/app/models/evaluation.py", """
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
""")

# TESTS
write_file("backend/tests/test_health.py", """
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}
""")

# FRONTEND SCAFFOLD
write_file("frontend/package.json", """
{
  "name": "financial-csi-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "lucide-react": "^0.359.0",
    "next": "14.1.4",
    "react": "^18",
    "react-dom": "^18",
    "recharts": "^2.12.3"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "autoprefixer": "^10.0.1",
    "eslint": "^8",
    "eslint-config-next": "14.1.4",
    "postcss": "^8",
    "tailwindcss": "^3.3.0",
    "typescript": "^5"
  }
}
""")

write_file("frontend/tsconfig.json", """
{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
""")

write_file("frontend/next.config.ts", """
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;
""")

write_file("frontend/postcss.config.mjs", """
/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    tailwindcss: {},
  },
};

export default config;
""")

write_file("frontend/eslint.config.mjs", """
import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
];

export default eslintConfig;
""")

write_file("frontend/src/app/globals.css", """
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: #0f1115;
  --foreground: #e2e8f0;
}

body {
  color: var(--foreground);
  background: var(--background);
  font-family: Arial, Helvetica, sans-serif;
}
""")

write_file("frontend/src/app/layout.tsx", """
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Financial CSI | Risk Manager",
  description: "AI Risk Manager for discovering hidden payment-loss patterns",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="flex h-screen overflow-hidden">
          {/* Sidebar placeholder */}
          <aside className="w-64 border-r border-gray-800 bg-gray-900 p-4">
            <h1 className="text-xl font-bold tracking-wider text-blue-400">FINANCIAL CSI</h1>
          </aside>
          {/* Main Content */}
          <main className="flex-1 overflow-y-auto bg-gray-950 p-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
""")

write_file("frontend/src/app/page.tsx", """
export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center h-full">
      <h1 className="text-4xl font-bold mb-4">FINANCIAL CSI</h1>
      <p className="text-lg text-gray-400">AI Risk Manager for discovering hidden payment-loss patterns.</p>
      <div className="mt-8 p-4 bg-blue-900/20 border border-blue-500/30 rounded-lg text-blue-200">
        Module ready — implementation coming in the next development phase.
      </div>
    </div>
  );
}
""")

write_file("frontend/src/app/patterns/page.tsx", """
export default function Patterns() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Patterns</h1>
      <div className="p-4 bg-gray-900 border border-gray-800 rounded-lg text-gray-400">
        Module ready — implementation coming in the next development phase.
      </div>
    </div>
  );
}
""")

write_file("frontend/src/app/investigations/page.tsx", """
export default function Investigations() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Investigations</h1>
      <div className="p-4 bg-gray-900 border border-gray-800 rounded-lg text-gray-400">
        Module ready — implementation coming in the next development phase.
      </div>
    </div>
  );
}
""")

write_file("frontend/src/app/simulations/page.tsx", """
export default function Simulations() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Simulations</h1>
      <div className="p-4 bg-gray-900 border border-gray-800 rounded-lg text-gray-400">
        Module ready — implementation coming in the next development phase.
      </div>
    </div>
  );
}
""")

write_file("frontend/src/app/evaluation/page.tsx", """
export default function Evaluation() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Evaluation</h1>
      <div className="p-4 bg-gray-900 border border-gray-800 rounded-lg text-gray-400">
        Module ready — implementation coming in the next development phase.
      </div>
    </div>
  );
}
""")

