from typing import Any

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

app = FastAPI(title="Task API", description="A small in-memory API for learning FastAPI.")


# A dictionary is our temporary in-memory data store. Restarting the server resets it.
tasks: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "title": "Learn FastAPI",
        "description": "Build a simple REST API",
        "completed": False,
    },
    2: {
        "id": 2,
        "title": "Try the API",
        "description": "Send a request with curl",
        "completed": False,
    },
}
next_task_id = 3


def error(message: str, status_code: int) -> JSONResponse:
    """Return the same small JSON error format from each endpoint."""
    return JSONResponse({"error": message}, status_code=status_code)


async def request_json(request: Request) -> dict[str, Any] | JSONResponse:
    """Read a JSON object, returning a concise 400 response when it is invalid."""
    try:
        data: Any = await request.json()
    except ValueError:
        return error("Request body must be valid JSON", 400)

    if not isinstance(data, dict):
        return error("Request body must be valid JSON", 400)
    return data


@app.get("/")
async def welcome() -> dict[str, str]:
    return {"message": "Welcome to the Task API"}


@app.get("/tasks")
def get_tasks() -> list[dict[str, Any]]:
    return list(tasks.values())


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        return error("Task not found", 404)
    return task


@app.post("/tasks", status_code=201)
async def create_task(request: Request):
    global next_task_id

    data = await request_json(request)
    if isinstance(data, JSONResponse):
        return data

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return error("'title' is required", 400)

    task = {
        "id": next_task_id,
        "title": title,
        "description": data.get("description", ""),
        "completed": data.get("completed", False),
    }
    tasks[next_task_id] = task
    next_task_id += 1
    return task


@app.patch("/tasks/{task_id}")
async def update_task(task_id: int, request: Request):
    task = tasks.get(task_id)
    if task is None:
        return error("Task not found", 404)

    data = await request_json(request)
    if isinstance(data, JSONResponse):
        return data

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return error("'title' must be a non-empty string", 400)
        task["title"] = data["title"]

    # PATCH changes only fields supplied by the client.
    for field in ("description", "completed"):
        if field in data:
            task[field] = data[field]

    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> Response:
    if task_id not in tasks:
        return error("Task not found", 404)

    del tasks[task_id]
    return Response(status_code=204)


def main() -> None:
    """Run the Task API development server."""
    uvicorn.run("app.app:app", host="127.0.0.1", port=5000, reload=True)


if __name__ == "__main__":
    main()
