import pytest
from fastapi.testclient import TestClient
from main import app
from schema import CreateEmployee, UpdateEmployee

client = TestClient(app)

# Test employee creation
def test_create_employee():
    response = client.post("/api/employees", json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "department": "Engineering",
        "role": "Developer"
    })
    assert response.status_code == 201
    assert response.json().get("email") == "johndoe@example.com"

# Test duplicate employee email
def test_create_employee_with_existing_email():
    client.post("/api/employees", json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "department": "Engineering",
        "role": "Developer"
    })
    response = client.post("/api/employees", json={
        "name": "Jane Doe",
        "email": "johndoe@example.com",
        "department": "HR",
        "role": "Manager"
    })
    assert response.status_code == 400
    assert response.json().get("detail") == "emailid already exist"

# Test list employees
def test_get_employee_list():
    response = client.get("/api/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test get employee by ID
def test_get_employee_by_id():
    response = client.post("/api/employees", json={
        "name": "Jane Doe",
        "email": "janedoe@example.com",
        "department": "Finance",
        "role": "Analyst"
    })
    emp_id = response.json().get("id")
    response = client.get(f"/api/employees/{emp_id}")
    assert response.status_code == 200
    assert response.json().get("name") == "Jane Doe"

# Test update employee
def test_update_employee():
    response = client.post("/api/employees", json={
        "name": "Mike Johnson",
        "email": "mikejohnson@example.com",
        "department": "Marketing",
        "role": "Executive"
    })
    emp_id = response.json().get("id")
    response = client.put(f"/api/employees/{emp_id}", json={
        "name": "Michael Johnson",
        "email": "michaeljohnson@example.com",
        "department": "Sales",
        "role": "Senior Executive"
    })
    assert response.status_code == 200
    assert response.json().get("name") == "Michael Johnson"

# Test updating a non-existent employee
def test_update_employee_not_found():
    response = client.put("/api/employees/999", json={
        "name": "Non Existent",
        "email": "nonexistent@example.com",
        "department": "Engineering",
        "role": "Developer"
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Employee not exist with this id"

# Test delete employee
def test_delete_employee():
    response = client.post("/api/employees", json={
        "name": "Lisa Taylor",
        "email": "lisataylor@example.com",
        "department": "Support",
        "role": "Support Specialist"
    })
    emp_id = response.json().get("id")
    response = client.delete(f"/api/employees/{emp_id}")
    assert response.status_code == 204
    response = client.get(f"/api/employees/{emp_id}")
    assert response.status_code == 404
