import { useEffect, useState } from "react";
const incidents = [
  {
    id: "INC-1024",
    title: "Payment service unavailable",
    service: "Payment API",
    severity: "SEV-1",
    status: "Investigating",
    time: "2 min ago",
  },
  {
    id: "INC-1023",
    title: "High database latency",
    service: "MongoDB",
    severity: "SEV-2",
    status: "Identified",
    time: "14 min ago",
  },
  {
    id: "INC-1022",
    title: "Authentication failures",
    service: "Auth Service",
    severity: "SEV-3",
    status: "Monitoring",
    time: "32 min ago",
  },
]

const severityStyle = {
  "SEV-1": "bg-red-500/15 text-red-400",
  "SEV-2": "bg-orange-500/15 text-orange-400",
  "SEV-3": "bg-yellow-500/15 text-yellow-400",
}

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking...");

useEffect(() => {
  fetch("http://127.0.0.1:8000/health")
    .then((response) => {
      if (!response.ok) throw new Error("Backend unavailable");
      return response.json();
    })
    .then(() => setBackendStatus("Connected"))
    .catch(() => setBackendStatus("Offline"));
}, []);
  return (
    <div className="min-h-screen bg-[#080d18] text-slate-200 flex">

      {/* Sidebar */}
      <aside className="hidden md:flex w-64 flex-col border-r border-slate-800 bg-[#0c1422] p-6">
        <div className="mb-10">
          <h1 className="text-xl font-bold text-white">
            <span className="text-emerald-400">◆</span> IncidentAI
          </h1>
          <p className="mt-2 text-xs text-slate-500">
            Intelligent Incident Management
          </p>
        </div>

        <p className="mb-3 text-xs uppercase tracking-widest text-slate-500">
          Workspace
        </p>

        <nav className="space-y-2">
          {[
            ["▦", "Overview"],
            ["◉", "Incidents"],
            ["⌘", "AI Diagnosis"],
            ["▤", "Runbooks"],
            ["◷", "Incident History"],
          ].map(([icon, name], index) => (
            <div
              key={name}
              className={`flex items-center gap-3 rounded-lg px-4 py-3 text-sm ${
                index === 0
                  ? "bg-emerald-500/10 text-emerald-400"
                  : "text-slate-400 hover:bg-slate-800"
              }`}
            >
              <span>{icon}</span>
              {name}
            </div>
          ))}
        </nav>

        <div className="mt-auto rounded-xl border border-slate-800 bg-slate-900 p-4">
          <p className="text-sm font-semibold text-white">
            AI Engine
          </p>
          <p className="mt-2 text-xs text-emerald-400">
            ● Ready for integration
          </p>
          <p className="mt-2 text-xs text-slate-500">
            Grok API connection will be configured in the backend.
          </p>
        </div>
      </aside>

      {/* Main content */}
      <main className="min-w-0 flex-1 p-5 md:p-8">

        {/* Header */}
        <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm text-slate-500">
              Workspace / Overview
            </p>
            <h2 className="mt-2 text-2xl font-bold text-white">
              Incident Command Center
            </h2>
            <p className="mt-1 text-sm text-slate-400">
              Monitor, investigate and resolve production incidents.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <span className={`rounded-full border px-3 py-2 text-xs ${
  backendStatus === "Connected"
    ? "border-emerald-500/20 bg-emerald-500/10 text-emerald-400"
    : "border-yellow-500/20 bg-yellow-500/10 text-yellow-400"
}`}>
  ● Backend {backendStatus}
</span>
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-700 font-bold text-white">
              IR
            </div>
          </div>
        </header>

        {/* Statistics */}
        <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {[
            ["Active Incidents", "12", "+3 today", "text-blue-400"],
            ["Critical Incidents", "02", "Requires attention", "text-red-400"],
            ["Resolved Today", "18", "+12% this week", "text-emerald-400"],
            ["Mean Resolution", "14m", "-8% this week", "text-purple-400"],
          ].map(([label, value, detail, color]) => (
            <div
              key={label}
              className="rounded-xl border border-slate-800 bg-[#101a2b] p-5"
            >
              <p className="text-sm text-slate-400">{label}</p>
              <h3 className={`mt-3 text-3xl font-bold ${color}`}>
                {value}
              </h3>
              <p className="mt-2 text-xs text-slate-500">{detail}</p>
            </div>
          ))}
        </section>

        {/* Incident list and AI panel */}
        <section className="mt-8 grid grid-cols-1 gap-6 xl:grid-cols-3">

          <div className="xl:col-span-2 rounded-xl border border-slate-800 bg-[#101a2b]">
            <div className="flex items-center justify-between border-b border-slate-800 p-5">
              <div>
                <h3 className="font-semibold text-white">
                  Active Incidents
                </h3>
                <p className="mt-1 text-xs text-slate-500">
                  Current production alerts
                </p>
              </div>
              <button className="rounded-lg bg-emerald-500 px-4 py-2 text-xs font-semibold text-slate-950">
                + New Incident
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="text-xs text-slate-500">
                  <tr>
                    <th className="p-4">Incident</th>
                    <th className="p-4">Severity</th>
                    <th className="p-4">Status</th>
                    <th className="p-4">Time</th>
                  </tr>
                </thead>
                <tbody>
                  {incidents.map((incident) => (
                    <tr
                      key={incident.id}
                      className="border-t border-slate-800"
                    >
                      <td className="p-4">
                        <p className="font-medium text-white">
                          {incident.title}
                        </p>
                        <p className="mt-1 text-xs text-slate-500">
                          {incident.id} · {incident.service}
                        </p>
                      </td>
                      <td className="p-4">
                        <span className={`rounded-md px-2 py-1 text-xs ${severityStyle[incident.severity]}`}>
                          {incident.severity}
                        </span>
                      </td>
                      <td className="p-4 text-xs text-slate-300">
                        {incident.status}
                      </td>
                      <td className="p-4 text-xs text-slate-500">
                        {incident.time}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* AI Diagnosis */}
          <div className="rounded-xl border border-emerald-500/20 bg-[#101a2b] p-5">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-500/10 text-xl text-emerald-400">
                ✦
              </div>
              <div>
                <h3 className="font-semibold text-white">AI Diagnosis</h3>
                <p className="text-xs text-slate-500">Grok-powered analysis</p>
              </div>
            </div>

            <div className="mt-6 rounded-lg bg-slate-900 p-4">
              <p className="text-xs font-semibold uppercase tracking-wider text-emerald-400">
                Latest insight
              </p>
              <p className="mt-3 text-sm leading-6 text-slate-300">
                Payment API is experiencing elevated response times.
                Database connection saturation is a potential cause.
              </p>
              <p className="mt-4 text-xs text-yellow-400">
                Hypothesis only — awaiting diagnostic evidence.
              </p>
            </div>

            <div className="mt-5">
              <p className="text-sm font-semibold text-white">
                Suggested next steps
              </p>
              <ul className="mt-3 space-y-3 text-xs text-slate-400">
                <li>→ Inspect payment service logs</li>
                <li>→ Check MongoDB connection pool</li>
                <li>→ Review API latency metrics</li>
              </ul>
            </div>

            <button className="mt-6 w-full rounded-lg border border-emerald-500/40 py-3 text-sm font-medium text-emerald-400">
              Open AI Analysis →
            </button>
          </div>
        </section>

        {/* Footer */}
        <footer className="mt-8 border-t border-slate-800 pt-5 text-xs text-slate-600">
          IncidentAI · Incident Response and Reliability Platform
          <span className="float-right">Development Preview</span>
        </footer>

      </main>
    </div>
  )
}

export default App
