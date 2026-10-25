import { useState } from "react";

const STATUSES = [
  ["open", "Open"],
  ["in_progress", "In progress"],
  ["resolved", "Resolved"],
  ["closed", "Closed"],
];

const PRIORITIES = [
  ["low", "Low"],
  ["medium", "Medium"],
  ["high", "High"],
  ["critical", "Critical"],
];

const EMPTY_TICKET = {
  title: "",
  description: "",
  status: "open",
  priority: "medium",
  assignee: "",
};

function fromTicket(ticket) {
  if (!ticket) return EMPTY_TICKET;
  return {
    title: ticket.title,
    description: ticket.description || "",
    status: ticket.status,
    priority: ticket.priority,
    assignee: ticket.assignee || "",
  };
}

function validate(form) {
  const errors = {};
  const title = form.title.trim();
  if (title.length < 3) errors.title = "Title must be at least 3 characters";
  if (title.length > 200) errors.title = "Title must be 200 characters or fewer";
  if (form.description.length > 5000) errors.description = "Description must be 5000 characters or fewer";
  if (form.assignee.length > 100) errors.assignee = "Assignee must be 100 characters or fewer";
  return errors;
}

export default function TicketForm({ editingTicket, onSave, onCancel }) {
  const [form, setForm] = useState(() => fromTicket(editingTicket));
  const [fieldErrors, setFieldErrors] = useState({});
  const [submitError, setSubmitError] = useState("");
  const [saving, setSaving] = useState(false);

  function updateField(name, value) {
    setForm((current) => ({ ...current, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const errors = validate(form);
    setFieldErrors(errors);
    setSubmitError("");
    if (Object.keys(errors).length > 0) return;

    setSaving(true);
    try {
      await onSave({ ...form, title: form.title.trim() });
      if (!editingTicket) setForm(EMPTY_TICKET);
    } catch (err) {
      setSubmitError(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="ticket-form" onSubmit={handleSubmit} noValidate>
      <label>
        Title *
        <input
          value={form.title}
          onChange={(e) => updateField("title", e.target.value)}
          placeholder="e.g. Login page returns 500"
        />
        {fieldErrors.title && <span className="field-error">{fieldErrors.title}</span>}
      </label>

      <label>
        Description
        <textarea
          rows={4}
          value={form.description}
          onChange={(e) => updateField("description", e.target.value)}
        />
        {fieldErrors.description && <span className="field-error">{fieldErrors.description}</span>}
      </label>

      <div className="row">
        <label>
          Status
          <select value={form.status} onChange={(e) => updateField("status", e.target.value)}>
            {STATUSES.map(([value, label]) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </select>
        </label>

        <label>
          Priority
          <select value={form.priority} onChange={(e) => updateField("priority", e.target.value)}>
            {PRIORITIES.map(([value, label]) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </select>
        </label>
      </div>

      <label>
        Assignee
        <input
          value={form.assignee}
          onChange={(e) => updateField("assignee", e.target.value)}
          placeholder="e.g. sara"
        />
        {fieldErrors.assignee && <span className="field-error">{fieldErrors.assignee}</span>}
      </label>

      {submitError && <div className="error-banner">{submitError}</div>}

      <div className="actions">
        <button type="submit" disabled={saving}>
          {saving ? "Saving..." : editingTicket ? "Update ticket" : "Create ticket"}
        </button>
        {editingTicket && (
          <button type="button" className="secondary" onClick={onCancel} disabled={saving}>
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
