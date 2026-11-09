import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { disableDemoFailure, enableDemoFailure, getDemoFailureStatus } from "../api/client";

export default function DemoControlsPage() {
  const queryClient = useQueryClient();
  const demoMode = (import.meta.env.VITE_DEMO_MODE || "true").toLowerCase() === "true";
  const defaultToken = import.meta.env.VITE_ADMIN_API_TOKEN || "";
  const [adminToken, setAdminToken] = useState(defaultToken);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const statusQuery = useQuery({
    queryKey: ["demo-failure"],
    queryFn: getDemoFailureStatus,
    refetchInterval: 5000,
  });

  const enableMutation = useMutation({
    mutationFn: () => enableDemoFailure(adminToken),
    onSuccess: async () => {
      setError(null);
      setMessage("Controlled demo failure ENABLED. Submissions will return HTTP 503.");
      await queryClient.invalidateQueries({ queryKey: ["demo-failure"] });
    },
    onError: (err: Error) => setError(err.message),
  });

  const disableMutation = useMutation({
    mutationFn: () => disableDemoFailure(adminToken),
    onSuccess: async () => {
      setError(null);
      setMessage("Demo failure DISABLED. Submissions should succeed again.");
      await queryClient.invalidateQueries({ queryKey: ["demo-failure"] });
    },
    onError: (err: Error) => setError(err.message),
  });

  if (!demoMode) {
    return (
      <section className="panel">
        <h1>Demo Controls</h1>
        <p className="lead">Demo mode is disabled in this environment.</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <h1>Demo Incident Control</h1>
      <div className="notice">
        <strong>Controlled demo fault.</strong> Enabling this makes{" "}
        <code>POST /api/v1/requests</code> return HTTP 503. It does not execute arbitrary code or
        destroy data. Requires an admin token.
      </div>
      <p className="lead">
        Current state:{" "}
        <strong>
          {statusQuery.data?.demo_failure_mode_enabled ? "FAILURE MODE ON" : "FAILURE MODE OFF"}
        </strong>
      </p>
      <label>
        Admin API token
        <input
          type="password"
          value={adminToken}
          onChange={(e) => setAdminToken(e.target.value)}
          placeholder="Bearer token value"
        />
      </label>
      <div className="form-actions">
        <button
          className="danger"
          type="button"
          disabled={!adminToken || enableMutation.isPending}
          onClick={() => enableMutation.mutate()}
        >
          Simulate Request Submission Failure
        </button>
        <button
          className="secondary"
          type="button"
          disabled={!adminToken || disableMutation.isPending}
          onClick={() => disableMutation.mutate()}
        >
          Disable demo failure
        </button>
      </div>
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}
    </section>
  );
}
