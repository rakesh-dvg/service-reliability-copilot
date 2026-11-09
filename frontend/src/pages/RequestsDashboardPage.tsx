import { useQuery } from "@tanstack/react-query";
import { listRequests } from "../api/client";

export default function RequestsDashboardPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["requests"],
    queryFn: listRequests,
    refetchInterval: 10000,
  });

  const requests = data || [];
  const open = requests.filter((r) => r.status === "open").length;
  const inProgress = requests.filter((r) => r.status === "in_progress").length;
  const completed = requests.filter((r) => r.status === "completed").length;

  return (
    <section className="panel">
      <h1>Service Request Dashboard</h1>
      <p className="lead">Recent submissions and status distribution.</p>
      <div className="grid-4" style={{ marginBottom: "1.2rem" }}>
        <div className="stat">
          <span className="label">Total</span>
          <span className="value">{requests.length}</span>
        </div>
        <div className="stat">
          <span className="label">Open</span>
          <span className="value">{open}</span>
        </div>
        <div className="stat">
          <span className="label">In progress</span>
          <span className="value">{inProgress}</span>
        </div>
        <div className="stat">
          <span className="label">Completed</span>
          <span className="value">{completed}</span>
        </div>
      </div>
      {isLoading && <p>Loading requests…</p>}
      {error && <p className="error">{(error as Error).message}</p>}
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Category</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {requests.map((request) => (
              <tr key={request.id}>
                <td>{request.title}</td>
                <td>{request.service_category}</td>
                <td>{request.priority}</td>
                <td>
                  <span className="badge">{request.status}</span>
                </td>
                <td>{new Date(request.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
