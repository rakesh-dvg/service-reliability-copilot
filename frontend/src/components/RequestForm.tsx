import { FormEvent, useState } from "react";
import type { Priority, ServiceCategory, ServiceRequestCreate } from "../types";

const CATEGORIES: ServiceCategory[] = [
  "Equipment Maintenance",
  "Technical Support",
  "Installation",
  "General Service",
];

const PRIORITIES: Priority[] = ["low", "medium", "high", "urgent"];

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export interface RequestFormProps {
  onSubmit: (payload: ServiceRequestCreate) => Promise<void>;
  submitting?: boolean;
  apiError?: string | null;
}

export default function RequestForm({ onSubmit, submitting = false, apiError }: RequestFormProps) {
  const [customerName, setCustomerName] = useState("");
  const [customerEmail, setCustomerEmail] = useState("");
  const [serviceCategory, setServiceCategory] = useState<ServiceCategory>("General Service");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<Priority>("medium");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [success, setSuccess] = useState<string | null>(null);

  function validate(): boolean {
    const next: Record<string, string> = {};
    if (!customerName.trim()) next.customerName = "Customer name is required.";
    if (!customerEmail.trim()) next.customerEmail = "Email is required.";
    else if (!EMAIL_RE.test(customerEmail)) next.customerEmail = "Enter a valid email address.";
    if (title.trim().length < 3) next.title = "Title must be at least 3 characters.";
    if (description.trim().length < 5) next.description = "Description must be at least 5 characters.";
    if (!PRIORITIES.includes(priority)) next.priority = "Select a valid priority.";
    if (!CATEGORIES.includes(serviceCategory)) next.serviceCategory = "Select a valid category.";
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setSuccess(null);
    if (!validate()) return;
    await onSubmit({
      customer_name: customerName.trim(),
      customer_email: customerEmail.trim(),
      service_category: serviceCategory,
      title: title.trim(),
      description: description.trim(),
      priority,
    });
    setSuccess("Service request submitted successfully.");
    setCustomerName("");
    setCustomerEmail("");
    setTitle("");
    setDescription("");
    setPriority("medium");
    setServiceCategory("General Service");
  }

  return (
    <form className="panel" onSubmit={handleSubmit} noValidate>
      <h1>Customer Service Request</h1>
      <p className="lead">Submit a service request. Valid submissions are persisted to PostgreSQL.</p>
      <div className="grid-2">
        <label>
          Customer name
          <input value={customerName} onChange={(e) => setCustomerName(e.target.value)} maxLength={120} />
          {errors.customerName && <p className="error">{errors.customerName}</p>}
        </label>
        <label>
          Customer email
          <input
            type="email"
            value={customerEmail}
            onChange={(e) => setCustomerEmail(e.target.value)}
            maxLength={255}
          />
          {errors.customerEmail && <p className="error">{errors.customerEmail}</p>}
        </label>
        <label>
          Service category
          <select
            value={serviceCategory}
            onChange={(e) => setServiceCategory(e.target.value as ServiceCategory)}
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
          {errors.serviceCategory && <p className="error">{errors.serviceCategory}</p>}
        </label>
        <label>
          Priority
          <select value={priority} onChange={(e) => setPriority(e.target.value as Priority)}>
            {PRIORITIES.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
          {errors.priority && <p className="error">{errors.priority}</p>}
        </label>
      </div>
      <label style={{ marginTop: "1rem" }}>
        Request title
        <input value={title} onChange={(e) => setTitle(e.target.value)} maxLength={200} />
        {errors.title && <p className="error">{errors.title}</p>}
      </label>
      <label style={{ marginTop: "1rem" }}>
        Description
        <textarea value={description} onChange={(e) => setDescription(e.target.value)} maxLength={4000} />
        {errors.description && <p className="error">{errors.description}</p>}
      </label>
      <div className="form-actions">
        <button type="submit" disabled={submitting}>
          {submitting ? "Submitting…" : "Submit request"}
        </button>
      </div>
      {apiError && <p className="error">{apiError}</p>}
      {success && !apiError && <p className="success">{success}</p>}
    </form>
  );
}
