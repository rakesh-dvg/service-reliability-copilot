import { NavLink, Route, Routes } from "react-router-dom";
import RequestFormPage from "./pages/RequestFormPage";
import RequestsDashboardPage from "./pages/RequestsDashboardPage";
import ReliabilityDashboardPage from "./pages/ReliabilityDashboardPage";
import DemoControlsPage from "./pages/DemoControlsPage";

export default function App() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand-block">
          <p className="brand">Service Reliability Copilot</p>
          <p className="tagline">From User-Impact Detection to AI-Assisted Incident Recovery</p>
        </div>
        <nav className="nav">
          <NavLink to="/" end>
            Submit Request
          </NavLink>
          <NavLink to="/requests">Requests</NavLink>
          <NavLink to="/reliability">Reliability</NavLink>
          <NavLink to="/demo">Demo Controls</NavLink>
        </nav>
      </header>
      <main className="content">
        <Routes>
          <Route path="/" element={<RequestFormPage />} />
          <Route path="/requests" element={<RequestsDashboardPage />} />
          <Route path="/reliability" element={<ReliabilityDashboardPage />} />
          <Route path="/demo" element={<DemoControlsPage />} />
        </Routes>
      </main>
      <footer className="footer">
        <span>Local stack · Docker Compose</span>
        <a href={import.meta.env.VITE_GRAFANA_URL || "http://localhost:3000"} target="_blank" rel="noreferrer">
          Open Grafana
        </a>
      </footer>
    </div>
  );
}
