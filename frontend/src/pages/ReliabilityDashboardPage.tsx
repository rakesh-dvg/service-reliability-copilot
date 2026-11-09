import { useQuery } from "@tanstack/react-query";
import { getReliabilitySummary } from "../api/client";

export default function ReliabilityDashboardPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["reliability"],
    queryFn: getReliabilitySummary,
    refetchInterval: 8000,
  });

  const grafanaUrl = import.meta.env.VITE_GRAFANA_URL || "http://localhost:3000";

  return (
    <section className="panel">
      <h1>Reliability Dashboard</h1>
      <p className="lead">
        Submission journey health, incidents, and recovery status.{" "}
        <a href={grafanaUrl} target="_blank" rel="noreferrer">
          Open Grafana dashboards
        </a>
      </p>
      {isLoading && <p>Loading reliability summary…</p>}
      {error && <p className="error">{(error as Error).message}</p>}
      {data && (
        <>
          <div className="grid-4" style={{ marginBottom: "1.2rem" }}>
            <div className="stat">
              <span className="label">Success rate</span>
              <span className="value">{(data.submission_success_rate * 100).toFixed(1)}%</span>
            </div>
            <div className="stat">
              <span className="label">Failures</span>
              <span className="value">{data.submission_failure_count}</span>
            </div>
            <div className="stat">
              <span className="label">Active incidents</span>
              <span className="value">{data.active_incidents}</span>
            </div>
            <div className="stat">
              <span className="label">Total requests</span>
              <span className="value">{data.total_requests}</span>
            </div>
          </div>
          <h2>Recent incidents</h2>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Severity</th>
                  <th>State</th>
                  <th>Detected</th>
                  <th>Resolved</th>
                  <th>Action</th>
                  <th>Verified</th>
                </tr>
              </thead>
              <tbody>
                {data.recent_incidents.map((incident) => {
                  const lastAction = incident.remediations?.[0];
                  return (
                    <tr key={incident.id}>
                      <td>{incident.incident_type}</td>
                      <td>{incident.severity}</td>
                      <td>
                        <span
                          className={`badge ${
                            incident.status === "resolved"
                              ? "ok"
                              : incident.status === "escalated"
                                ? "fail"
                                : "warn"
                          }`}
                        >
                          {incident.status}
                        </span>
                      </td>
                      <td>{new Date(incident.detected_at).toLocaleString()}</td>
                      <td>
                        {incident.resolved_at
                          ? new Date(incident.resolved_at).toLocaleString()
                          : "—"}
                      </td>
                      <td>{lastAction?.action_type || "—"}</td>
                      <td>{incident.recovery_verified ? "yes" : "no"}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </>
      )}
    </section>
  );
}
