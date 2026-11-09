import type {
  ReliabilitySummary,
  ServiceRequest,
  ServiceRequestCreate,
  Incident,
} from "../types";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
    ...init,
  });

  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      detail = body.detail || detail;
    } catch {
      // ignore parse errors
    }
    throw new Error(detail);
  }

  if (response.status === 204) {
    return undefined as T;
  }
  return response.json() as Promise<T>;
}

export function listRequests(): Promise<ServiceRequest[]> {
  return request("/api/v1/requests");
}

export function createRequest(payload: ServiceRequestCreate): Promise<ServiceRequest> {
  return request("/api/v1/requests", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getReliabilitySummary(): Promise<ReliabilitySummary> {
  return request("/api/v1/reliability/summary");
}

export function listIncidents(): Promise<Incident[]> {
  return request("/api/v1/incidents");
}

export function getDemoFailureStatus(): Promise<{
  demo_mode: boolean;
  demo_failure_mode_enabled: boolean;
}> {
  return request("/api/v1/demo/failure/status");
}

export function enableDemoFailure(adminToken: string): Promise<{ demo_failure_mode_enabled: boolean }> {
  return request("/api/v1/demo/failure/enable", {
    method: "POST",
    headers: { Authorization: `Bearer ${adminToken}` },
  });
}

export function disableDemoFailure(adminToken: string): Promise<{ demo_failure_mode_enabled: boolean }> {
  return request("/api/v1/demo/failure/disable", {
    method: "POST",
    headers: { Authorization: `Bearer ${adminToken}` },
  });
}
