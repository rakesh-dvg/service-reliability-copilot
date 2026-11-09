import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import ReliabilityDashboardPage from "./ReliabilityDashboardPage";

vi.mock("../api/client", () => ({
  getReliabilitySummary: vi.fn().mockResolvedValue({
    total_requests: 4,
    open_requests: 2,
    in_progress_requests: 1,
    completed_requests: 1,
    submission_success_count: 3,
    submission_failure_count: 1,
    submission_success_rate: 0.75,
    active_incidents: 1,
    recent_incidents: [
      {
        id: "1",
        alert_fingerprint: "fp",
        incident_type: "DEMO_FAILURE_MODE",
        severity: "high",
        status: "remediating",
        detected_at: new Date().toISOString(),
        acknowledged_at: null,
        resolved_at: null,
        root_cause: "demo",
        recovery_verified: false,
        remediations: [
          {
            id: "r1",
            action_type: "DISABLE_DEMO_FAILURE_MODE",
            status: "started",
            started_at: new Date().toISOString(),
            finished_at: null,
            diagnostic_summary: null,
            verification_result: null,
          },
        ],
      },
    ],
  }),
}));

describe("ReliabilityDashboardPage", () => {
  it("renders incident status and success rate", async () => {
    const client = new QueryClient();
    render(
      <QueryClientProvider client={client}>
        <ReliabilityDashboardPage />
      </QueryClientProvider>,
    );

    await waitFor(() => {
      expect(screen.getByText("75.0%")).toBeInTheDocument();
    });
    expect(screen.getByText("DEMO_FAILURE_MODE")).toBeInTheDocument();
    expect(screen.getByText("DISABLE_DEMO_FAILURE_MODE")).toBeInTheDocument();
  });
});
