import pytest


class TestTaskCRUDIntegration:

    @pytest.mark.parametrize(
        "title, description, expected_status",
        [
            ("Test Task", "Test Description", "created"),
            ("Task without description", None, "created"),
        ]
    )
    @pytest.mark.asyncio
    async def test_create_task(self, async_integration_client, title, description, expected_status):
        payload = {"title": title}
        if description is not None:
            payload["description"] = description

        response = await async_integration_client.post("/tasks/", json=payload)
        assert response.status_code == 201

        sample_task = response.json()
        task_id = sample_task["id"]

        response = await async_integration_client.get(f"/tasks/{task_id}")
        assert response.status_code == 200

        sample_task = response.json()
        assert sample_task["title"] == title
        assert sample_task["description"] == description
        assert sample_task["status"] == expected_status

    @pytest.mark.asyncio
    async def test_get_task(self, async_integration_client):
        response = await async_integration_client.post("/tasks/", json={
            "title": "DB Retrieval Test",
            "description": "Testing retrieval from DB"
        })
        sample_task = response.json()
        task_id = sample_task["id"]

        response = await async_integration_client.get(f"/tasks/{task_id}")
        assert response.status_code == 200

        sample_task = response.json()
        assert sample_task["id"] == task_id
        assert sample_task["title"] == "DB Retrieval Test"
        assert sample_task["description"] == "Testing retrieval from DB"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "payload, expected_title, expected_description, expected_status",
        [
            ({"title": "Updated Title"}, "Updated Title", "Original Description", "created"),
            ({"description": "Updated Description"}, "Original Task", "Updated Description", "created"),
            ({"status": "in_progress"}, "Original Task", "Original Description", "in_progress"),
            ({"title": "New Title", "status": "completed"}, "New Title", "Original Description", "completed"),
            ({"description": None}, "Original Task", None, "created"),
            ({"title": "Full Update", "description": "Full Description Update", "status": "in_progress"},
             "Full Update", "Full Description Update", "in_progress"),
        ]
    )
    async def test_update_task(
            self,
            async_integration_client, payload, expected_title, expected_description, expected_status
    ):
        response = await async_integration_client.post("/tasks/", json={
            "title": "Original Task",
            "description": "Original Description"
        })
        sample_task = response.json()
        task_id = sample_task["id"]

        response = await async_integration_client.put(f"/tasks/{task_id}", json=payload)
        assert response.status_code == 200

        response = await async_integration_client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        sample_task = response.json()
        assert sample_task["title"] == expected_title
        assert sample_task["description"] == expected_description
        assert sample_task["status"] == expected_status

    @pytest.mark.asyncio
    async def test_delete_task(self, async_integration_client):
        response = await async_integration_client.post("/tasks/", json={
            "title": "Task to Delete",
            "description": "Will be deleted"
        })
        sample_task = response.json()
        task_id = sample_task["id"]

        response = await async_integration_client.get(f"/tasks/{task_id}")
        assert response.status_code == 200

        response = await async_integration_client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204

        response = await async_integration_client.get(f"/tasks/{task_id}")
        assert response.status_code == 404
