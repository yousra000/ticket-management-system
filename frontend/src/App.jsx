import { useCallback, useEffect, useState } from "react";
import { api } from "./api.js";
import TicketForm from "./components/TicketForm.jsx";
import TicketList from "./components/TicketList.jsx";

export default function App() {
  const [tickets, setTickets] = useState([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [health, setHealth] = useState(null);
  const [editingTicket, setEditingTicket] = useState(null);

  const loadTickets = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setTickets(await api.listTickets(statusFilter));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [statusFilter]);

  useEffect(() => {
    loadTickets();
  }, [loadTickets]);

  useEffect(() => {
    api.health().then(setHealth);
  }, []);

  async function handleSave(ticket) {
    // Errors are thrown so the form can display them next to the fields.
    if (editingTicket) {
      await api.updateTicket(editingTicket.id, ticket);
      setEditingTicket(null);
    } else {
      await api.createTicket(ticket);
    }
    await loadTickets();
  }

  async function handleDelete(id) {
    if (!window.confirm("Delete this ticket? This cannot be undone.")) return;
    try {
      await api.deleteTicket(id);
      if (editingTicket?.id === id) setEditingTicket(null);
      await loadTickets();
    } catch (err) {
      setError(err.message);
    }
  }

  const healthy = health?.status === "ok";

  return (
    <div className="app">
      <header className="app-header">
        <h1>Ticket Management System</h1>
        <div className={`health ${healthy ? "health-ok" : "health-bad"}`}>
          {health === null && "Checking backend..."}
          {health && healthy && "Backend and database connected"}
          {health && !healthy && `Backend status: ${health.status}${health.httpStatus ? ` (HTTP ${health.httpStatus})` : ""}`}
        </div>
      </header>

      <main className="layout">
        <section className="panel">
          <h2>{editingTicket ? `Edit ticket #${editingTicket.id}` : "New ticket"}</h2>
          <TicketForm
            key={editingTicket ? editingTicket.id : "new"}
            editingTicket={editingTicket}
            onSave={handleSave}
            onCancel={() => setEditingTicket(null)}
          />
        </section>

        <section className="panel">
          <div className="list-header">
            <h2>Tickets</h2>
            <label>
              Status:{" "}
              <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
                <option value="">All</option>
                <option value="open">Open</option>
                <option value="in_progress">In progress</option>
                <option value="resolved">Resolved</option>
                <option value="closed">Closed</option>
              </select>
            </label>
          </div>

          {error && <div className="error-banner">{error}</div>}
          {loading && <p>Loading tickets...</p>}
          {!loading && (
            <TicketList tickets={tickets} onEdit={setEditingTicket} onDelete={handleDelete} />
          )}
        </section>
      </main>
    </div>
  );
}
