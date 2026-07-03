import pytest


@pytest.mark.asyncio
async def test_create_payment_success(client):
    response = await client.post(
        "/payments",
        json={
            "amount": 100,
            "currency": "USD",
        },
        headers={
            "Idempotency-Key": "test-key-001",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 100
    assert data["currency"] == "USD"
    assert data["status"] == "approved"
    assert data["provider_reference"] is not None
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_payment_idempotency(client):
    # First request
    response1 = await client.post(
        "/payments",
        json={
            "amount": 100,
            "currency": "USD",
        },
        headers={
            "Idempotency-Key": "test-key-002",
        },
    )

    assert response1.status_code == 201
    data1 = response1.json()
    payment_id = data1["id"]

    # Second request with same idempotency key
    response2 = await client.post(
        "/payments",
        json={
            "amount": 200,  # Different amount
            "currency": "EUR",  # Different currency
        },
        headers={
            "Idempotency-Key": "test-key-002",
        },
    )

    assert response2.status_code == 201
    data2 = response2.json()
    assert data2["id"] == payment_id
    assert data2["amount"] == 100  # Original amount
    assert data2["currency"] == "USD"  # Original currency


@pytest.mark.asyncio
async def test_create_payment_card_declined(client):
    response = await client.post(
        "/payments",
        json={
            "amount": 400,
            "currency": "USD",
        },
        headers={
            "Idempotency-Key": "test-key-003",
        },
    )

    assert response.status_code == 402
    assert response.json()["detail"] == "Card declined"


@pytest.mark.asyncio
async def test_create_payment_insufficient_funds(client):
    response = await client.post(
        "/payments",
        json={
            "amount": 600,
            "currency": "USD",
        },
        headers={
            "Idempotency-Key": "test-key-004",
        },
    )

    assert response.status_code == 402
    assert response.json()["detail"] == "Insufficient funds"


@pytest.mark.asyncio
async def test_create_payment_provider_timeout(client):
    response = await client.post(
        "/payments",
        json={
            "amount": 500,
            "currency": "USD",
        },
        headers={
            "Idempotency-Key": "test-key-005",
        },
    )

    assert response.status_code == 504
    assert response.json()["detail"] == "Provider timeout"


@pytest.mark.asyncio
async def test_create_payment_invalid_amount(client):
    response = await client.post(
        "/payments",
        json={
            "amount": -100,
            "currency": "USD",
        },
        headers={
            "Idempotency-Key": "test-key-006",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_payment_invalid_currency(client):
    response = await client.post(
        "/payments",
        json={
            "amount": 100,
            "currency": "US",  # Too short
        },
        headers={
            "Idempotency-Key": "test-key-007",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_payment_success(client):
    # First create a payment
    create_response = await client.post(
        "/payments",
        json={
            "amount": 100,
            "currency": "USD",
        },
        headers={
            "Idempotency-Key": "test-key-008",
        },
    )

    payment_id = create_response.json()["id"]

    # Then retrieve it
    response = await client.get(f"/payments/{payment_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == payment_id
    assert data["amount"] == 100
    assert data["currency"] == "USD"
    assert data["status"] == "approved"


@pytest.mark.asyncio
async def test_get_payment_not_found(client):
    response = await client.get("/payments/non-existent-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"


@pytest.mark.asyncio
async def test_refund_payment_success(client):
    # First create an approved payment
    create_response = await client.post(
        "/payments",
        json={
            "amount": 100,
            "currency": "USD",
        },
        headers={
            "Idempotency-Key": "test-key-009",
        },
    )

    payment_id = create_response.json()["id"]

    # Then refund it
    refund_response = await client.post(
        f"/payments/{payment_id}/refund",
        json={
            "amount": 100,
        },
    )

    assert refund_response.status_code == 200
    data = refund_response.json()
    assert data["id"] == payment_id
    assert data["status"] == "refunded"


@pytest.mark.asyncio
async def test_refund_payment_not_found(client):
    response = await client.post(
        "/payments/non-existent-id/refund",
        json={
            "amount": 100,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"


@pytest.mark.asyncio
async def test_refund_payment_invalid_amount(client):
    # First create an approved payment
    create_response = await client.post(
        "/payments",
        json={
            "amount": 100,
            "currency": "USD",
        },
        headers={
            "Idempotency-Key": "test-key-010",
        },
    )

    payment_id = create_response.json()["id"]

    # Try to refund more than the original amount
    response = await client.post(
        f"/payments/{payment_id}/refund",
        json={
            "amount": 200,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid refund"


@pytest.mark.asyncio
async def test_refund_payment_negative_amount(client):
    # First create an approved payment
    create_response = await client.post(
        "/payments",
        json={
            "amount": 100,
            "currency": "USD",
        },
        headers={
            "Idempotency-Key": "test-key-011",
        },
    )

    payment_id = create_response.json()["id"]

    # Try to refund a negative amount
    response = await client.post(
        f"/payments/{payment_id}/refund",
        json={
            "amount": -50,
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
