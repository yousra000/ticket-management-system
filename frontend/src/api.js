// Base URL of the FastAPI backend. Override with VITE_API_URL in frontend/.env if needed.
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function formatError(data, status) {
  if (!data || !data.detail) {
    return `Request failed (HTTP ${status})`;
  }
  if (typeof data.detail === "string") {
    return data.detail;
  }
  // FastAPI validation errors arrive as a list of { loc, msg } objects.
  return data.detail
    .map((item) => {
      const field = (item.loc || []).slice(1).join(".");
      return field ? `${field}: ${item.msg}` : item.msg;
    })
    .join("; ");
}

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch {
    throw new Error(`Cannot reach the backend at ${BASE_URL}. Is it running?`);
  }

  if (response.status === 204) {
    return null;
  }

  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(formatError(data, response.status));
  }
  return data;
}

function toPayload(ticket) {
  return {
    title: ticket.title,
    description: ticket.description?.trim() || null,
    status: ticket.status,
    priority: ticket.priority,
    assignee: ticket.assignee?.trim() || null,
  };
}

export const api = {
  async health() {
    try {
      const response = await fetch(`${BASE_URL}/api/health`);
      const data = await response.json();
      return { ...data, httpStatus: response.status };
    } catch {
      return { status: "unreachable" };
    }
  },
  listTickets(status = "") {
    const query = status ? `?status=${encodeURIComponent(status)}` : "";
    return request(`/api/tickets${query}`);
  },
  createTicket(ticket) {
    return request("/api/tickets", { method: "POST", body: JSON.stringify(toPayload(ticket)) });
  },
  updateTicket(id, ticket) {
    return request(`/api/tickets/${id}`, { method: "PUT", body: JSON.stringify(toPayload(ticket)) });
  },
  deleteTicket(id) {
    return request(`/api/tickets/${id}`, { method: "DELETE" });
  },
};
