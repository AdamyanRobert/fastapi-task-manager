import uuid
import pytest


@pytest.mark.parametrize(
    "method",
    ("get", "put", "delete")
)
class TestUUID:
    def test_invalid_uuid(self, client, method):
        response = getattr(client, method)("/tasks/invalid-uuid")
        assert response.status_code == 422

    def test_task_not_found(self, client, mock_repository, method):
        repo_methods = {
            "get": "select_task",
            "put": "update_task",
            "delete": "delete_task",
        }
        getattr(mock_repository, repo_methods[method]).return_value = None
        task_id = uuid.uuid4()

        if method == "put":
            response = getattr(client, method)(f"/tasks/{task_id}", json={
                "title": "Title"
            })

        else:
            response = getattr(client, method)(f"/tasks/{task_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"


@pytest.mark.parametrize(
    "payload, expected_status, expected_title, expected_description",
    [
        ({"title": "Test Task", "description": "Test Description"}, 201, "Test Task", "Test Description"),
        ({"title": "Only Title Task"}, 201, "Only Title Task", None),
        ({"title": "", "description": "Description"}, 422, None, None),
        ({"title": "a" * 256, "description": "Description"}, 422, None, None),
        ({"title": "Test Task", "description": "a" * 1024}, 422, None, None),
    ]
)
class TestCreateTask:

    def test_create_task(
        self, client, mock_repository, sample_task,
        payload, expected_status, expected_title, expected_description
    ):

        if expected_status == 201:
            sample_task.title = expected_title
            sample_task.description = expected_description
            mock_repository.create_task.return_value = sample_task

        response = client.post("/tasks/", json=payload)

        assert response.status_code == expected_status

        if expected_status == 201:
            data = response.json()
            assert data["title"] == expected_title
            assert data["description"] == expected_description
            assert data["status"] == "created"
            assert "id" in data

            mock_repository.create_task.assert_called_once_with(
                payload.get("title"),
                payload.get("description")
            )


class TestGetTasks:

    def test_get_tasks_empty_list(self, client, mock_repository):
        mock_repository.select_tasks.return_value = []

        response = client.get("/tasks/")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_tasks_with_data(self, client, multiple_tasks, mock_repository):
        mock_repository.select_tasks.return_value = multiple_tasks

        response = client.get("/tasks/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["title"] == "Task 1"
        assert data[1]["status"] == "in_progress"


class TestGetTask:

    def test_get_task_success(self, client, mock_repository, sample_task):
        mock_repository.select_task.return_value = sample_task

        response = client.get(f"/tasks/{sample_task.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(sample_task.id)
        assert data["title"] == sample_task.title


@pytest.mark.parametrize(
    "payload, expected_status, expected_title, expected_status_value, expected_detail",
    [
        ({"title": "Updated Title", "status": "in_progress"}, 200, "Updated Title", "in_progress", None),
        ({"status": "completed"}, 200, None, "completed", None),
        ({}, 400, None, None, "No fields to update"),
        ({"status": "invalid_status"}, 422, None, None, None),
    ]
)
class TestUpdateTask:

    def test_update_task(self, client, mock_repository, sample_task, payload,
                         expected_status, expected_title, expected_status_value, expected_detail):

        if expected_status == 200:
            if "title" in payload:
                sample_task.title = payload.get("title", sample_task.title)
            if "status" in payload:
                sample_task.status = payload.get("status", sample_task.status)
            mock_repository.update_task.return_value = sample_task

        task_id = sample_task.id if expected_status != 400 else uuid.uuid4()

        response = client.put(f"/tasks/{task_id}", json=payload)
        assert response.status_code == expected_status

        if expected_status == 200:
            data = response.json()
            if expected_title is not None:
                assert data["title"] == expected_title
            if expected_status_value is not None:
                assert data["status"] == expected_status_value
            mock_repository.update_task.assert_called_once_with(
                task_id, **payload
            )
        elif expected_status == 400:
            assert response.json()["detail"] == expected_detail


class TestDeleteTask:

    def test_delete_task_success(self, client, mock_repository):
        mock_repository.delete_task.return_value = True

        task_id = uuid.uuid4()
        response = client.delete(f"/tasks/{task_id}")

        assert response.status_code == 204
        mock_repository.delete_task.assert_called_once_with(task_id)
