from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_login_valid_credentials():
    res = client.post("/auth/login", data={"username": "admin", "password": "admin123"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["role"] == "Admin"
    assert "dashboard" in data["user"]["permissions"]


def test_login_wrong_password():
    res = client.post("/auth/login", data={"username": "admin", "password": "wrong"})
    assert res.status_code == 401


def test_login_unknown_user():
    res = client.post("/auth/login", data={"username": "ghost", "password": "pass"})
    assert res.status_code == 401


def test_me_with_valid_token():
    token = _get_token("manager", "manager123")
    res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["username"] == "manager"
    assert res.json()["role"] == "Manager"


def test_me_without_token():
    res = client.get("/auth/me")
    assert res.status_code == 401


def test_me_with_invalid_token():
    res = client.get("/auth/me", headers={"Authorization": "Bearer invalidtoken"})
    assert res.status_code == 401


def test_roles_endpoint():
    res = client.get("/auth/roles")
    assert res.status_code == 200
    data = res.json()
    assert "Admin" in data["roles"]
    assert "Manager" in data["roles"]
    assert "Planner" in data["roles"]


def test_all_demo_accounts_work():
    accounts = [
        ("admin", "admin123"),
        ("manager", "manager123"),
        ("planner", "planner123"),
        ("technician", "tech123"),
        ("executive", "exec123"),
    ]
    for username, password in accounts:
        res = client.post("/auth/login", data={"username": username, "password": password})
        assert res.status_code == 200, f"Login failed for {username}"


def test_planner_role_permissions():
    token = _get_token("planner", "planner123")
    res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    perms = res.json()["permissions"]
    assert "dashboard" in perms
    assert "upload" in perms
    assert "executive" not in perms  # Planner should not see Executive dashboard


def test_executive_role_permissions():
    token = _get_token("executive", "exec123")
    res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    perms = res.json()["permissions"]
    assert "executive" in perms
    assert "upload" not in perms  # Executive should not upload


# ── helpers ────────────────────────────────────────────────────────────────

def _get_token(username: str, password: str) -> str:
    res = client.post("/auth/login", data={"username": username, "password": password})
    return res.json()["access_token"]
