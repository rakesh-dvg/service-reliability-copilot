export type ServiceCategory =
  | "Equipment Maintenance"
  | "Technical Support"
  | "Installation"
  | "General Service";

export type Priority = "low" | "medium" | "high" | "urgent";
export type RequestStatus = "open" | "in_progress" | "completed" | "cancelled";

export interface ServiceRequest {
  id: string;
  customer_name: string;
  customer_email: string;
  service_category: ServiceCategory;
  title: string;
  description: string;
  priority: Priority;
  status: RequestStatus;
  created_at: string;
  updated_at: string;
}

export interface ServiceRequestCreate {
  customer_name: string;
  customer_email: string;
  service_category: ServiceCategory;
  title: string;
  description: string;
  priority: Priority;
}

export interface Remediation {
  id: string;
  action_type: string;
  status: string;
  started_at: string;
  finished_at: string | null;
  diagnostic_summary: string | null;
  verification_result: string | null;
}

export interface Incident {
  id: string;
  alert_fingerprint: string;
  incident_type: string;
  severity: string;
  status: string;
  detected_at: string;
  acknowledged_at: string | null;
  resolved_at: string | null;
  root_cause: string | null;
  recovery_verified: boolean;
  remediations: Remediation[];
}

export interface ReliabilitySummary {
  total_requests: number;
  open_requests: number;
  in_progress_requests: number;
  completed_requests: number;
  submission_success_count: number;
  submission_failure_count: number;
  submission_success_rate: number;
  active_incidents: number;
  recent_incidents: Incident[];
}
