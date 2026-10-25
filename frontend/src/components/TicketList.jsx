const LABELS = {
  open: "Open",
  in_progress: "In progress",
  resolved: "Resolved",
  closed: "Closed",
  low: "Low",
  medium: "Medium",
  high: "High",
  critical: "Critical",
};

export default function TicketList({ tickets, onEdit, onDelete }) {
  if (tickets.length === 0) {
    return <p className="empty">No tickets yet. Create one using the form.</p>;
  }

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Status</th>
            <th>Priority</th>
            <th>Assignee</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {tickets.map((ticket) => (
            <tr key={ticket.id}>
              <td>{ticket.id}</td>
              <td>
                <strong>{ticket.title}</strong>
                {ticket.description && <div className="muted">{ticket.description}</div>}
              </td>
              <td><span className={`badge status-${ticket.status}`}>{LABELS[ticket.status]}</span></td>
              <td><span className={`badge priority-${ticket.priority}`}>{LABELS[ticket.priority]}</span></td>
              <td>{ticket.assignee || "-"}</td>
              <td>{new Date(ticket.created_at).toLocaleString()}</td>
              <td className="actions">
                <button className="secondary" onClick={() => onEdit(ticket)}>Edit</button>
                <button className="danger" onClick={() => onDelete(ticket.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
