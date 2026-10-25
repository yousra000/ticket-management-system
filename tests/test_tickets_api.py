def ticket_payload(**overrides):
    data = {
        "title": "Login page fails",
        "description": "Returns a 500 error after submit",
        "status": "open",
        "priority": "high",
        "assignee": "sara",
    }
    data.update(overrides)
    return data


# ---------- Health check ----------

def test_health_reports_database_ok(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


# ---------- Create ----------

def test_create_ticket_returns_201_with_all_fields(client):
    response = client.post("/api/tickets", json=ticket_payload())
    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["title"] == "Login page fails"
    assert body["description"] == "Returns a 500 error after submit"
    assert body["status"] == "open"
    assert body["priority"] == "high"
    assert body["assignee"] == "sara"
    assert body["created_at"].endswith("Z")


def test_create_applies_defaults(client):
    response = client.post("/api/tickets", json={"title": "Minimal ticket"})
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "open"
    assert body["priority"] == "medium"
    assert body["description"] is None
    assert body["assignee"] is None


def test_title_shorter_than_three_characters_is_rejected(client):
    response = client.post("/api/tickets", json={"title": "ab"})
    assert response.status_code == 422


def test_blank_title_is_rejected(client):
    response = client.post("/api/tickets", json={"title": "     "})
    assert response.status_code == 422


def test_missing_title_is_rejected(client):
    response = client.post("/api/tickets", json={"description": "no title here"})
    assert response.status_code == 422


def test_invalid_priority_is_rejected(client):
    response = client.post("/api/tickets", json=ticket_payload(priority="urgent"))
    assert response.status_code == 422


def test_invalid_status_is_rejected(client):
    response = client.post("/api/tickets", json=ticket_payload(status="done"))
    assert response.status_code == 422


def test_surrounding_spaces_are_trimmed(client):
    response = client.post("/api/tickets", json=ticket_payload(title="   Trim me   "))
    assert response.json()["title"] == "Trim me"


# ---------- Read / list ----------

def test_list_returns_newest_first(client):
    client.post("/api/tickets", json=ticket_payload(title="First ticket"))
    client.post("/api/tickets", json=ticket_payload(title="Second ticket"))
    titles = [t["title"] for t in client.get("/api/tickets").json()]
    assert titles == ["Second ticket", "First ticket"]


def test_list_filters_by_status(client):
    client.post("/api/tickets", json=ticket_payload(title="Open one"))
    client.post("/api/tickets", json=ticket_payload(title="Closed one", status="closed"))
    response = client.get("/api/tickets", params={"status": "closed"})
    assert [t["title"] for t in response.json()] == ["Closed one"]


def test_list_filters_by_priority(client):
    client.post("/api/tickets", json=ticket_payload(title="Routine", priority="low"))
    client.post("/api/tickets", json=ticket_payload(title="Urgent", priority="critical"))
    response = client.get("/api/tickets", params={"priority": "critical"})
    assert [t["title"] for t in response.json()] == ["Urgent"]


def test_invalid_filter_value_is_rejected(client):
    response = client.get("/api/tickets", params={"status": "bogus"})
    assert response.status_code == 422


def test_get_single_ticket(client):
    created = client.post("/api/tickets", json=ticket_payload()).json()
    response = client.get(f"/api/tickets/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Login page fails"


def test_get_missing_ticket_returns_404(client):
    response = client.get("/api/tickets/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket 9999 not found"


# ---------- Update ----------

def test_update_ticket_replaces_fields(client):
    created = client.post("/api/tickets", json=ticket_payload()).json()
    response = client.put(
        f"/api/tickets/{created['id']}",
        json=ticket_payload(title="Login page fixed", status="resolved", priority="low", assignee=None),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Login page fixed"
    assert body["status"] == "resolved"
    assert body["priority"] == "low"
    assert body["assignee"] is None

    fetched = client.get(f"/api/tickets/{created['id']}").json()
    assert fetched["status"] == "resolved"


def test_update_with_invalid_data_is_rejected_and_ticket_unchanged(client):
    created = client.post("/api/tickets", json=ticket_payload()).json()
    response = client.put(f"/api/tickets/{created['id']}", json=ticket_payload(priority="urgent"))
    assert response.status_code == 422
    fetched = client.get(f"/api/tickets/{created['id']}").json()
    assert fetched["priority"] == "high"


def test_update_missing_ticket_returns_404(client):
    response = client.put("/api/tickets/9999", json=ticket_payload())
    assert response.status_code == 404


# ---------- Delete ----------

def test_delete_ticket_then_it_is_gone(client):
    created = client.post("/api/tickets", json=ticket_payload()).json()
    response = client.delete(f"/api/tickets/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/api/tickets/{created['id']}").status_code == 404


def test_delete_missing_ticket_returns_404(client):
    response = client.delete("/api/tickets/9999")
    assert response.status_code == 404
