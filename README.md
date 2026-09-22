# spug-20260922-fastapi
Build Your First API with Python!
FastAPI examples for SPUG meetup on 2026-09-22

### Links
Meetup event: https://www.meetup.com/python-spokane/events/316344742/

Presentation slides: https://gamma.app/docs/Build-Your-First-API-with-Python-asi9obj15d8usum?following_id=lx18pr74ci53m9n&follow_on_start=true

<br/>

# FastAPI Task API

A small in-memory REST API for learning FastAPI. Tasks return to their initial state whenever the server restarts.


## Setup

From the repository root, create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
venv\Scripts\Activate.ps1
```

Install the project in editable mode so `task-api` uses changes made in this
repository:

```bash
pip install -e .
```

Start the server:

```bash
task-api
```

The API is available at http://127.0.0.1:5000

<br/>

## Git Branches

| Branch | Description |
| --- | --- |
| 01-intro | basic single endpoint example |
| 02-crud | endpoints for CRUD operations |
| 03-auth | adding auth with Bearer token |
| 04-docker | creating Dockerfile |

<br/>

## Running with Docker

From the repository root, build the image with the Dockerfile in `src/docker`:

```bash
docker build -f src/docker/Dockerfile -t spug-fastapi .
```

Run the API and publish it on port 5000:

```bash
docker run --rm -p 5000:5000 spug-fastapi
```

The API is available at http://127.0.0.1:5000 

<br/>

## Authentication

The welcome endpoint (`GET /`) is public. Every other endpoint requires an
`Authorization` header with a bearer token. The default token for this learning
example is `example-token`:

```bash
curl http://127.0.0.1:5000/tasks \
  -H "Authorization: Bearer example-token"
```

To use a different token, set `TASK_API_TOKEN` before starting the server:

```bash
TASK_API_TOKEN='my-local-token' task-api
```

This is deliberately a minimal example, not a production authentication system.
Use a secret manager and a complete authentication/authorization solution for a
real application.

<br/>

## API documentation

The app generates an OpenAPI document from its routes and docstrings. Start the
server, then open either documentation UI:

- Swagger UI: http://127.0.0.1:5000/docs
- ReDoc: http://127.0.0.1:5000/redoc
- OpenAPI JSON: http://127.0.0.1:5000/openapi.json

The documentation pages are public. The task operations they describe still
require `Authorization: Bearer example-token`. In Swagger UI, select
**Authorize** and enter `example-token` to use **Try it out**.

<br/>

## Try the API

```bash
# GET / -- welcome/health response
curl http://127.0.0.1:5000/
```
``` bash
# GET /tasks -- list all tasks
curl http://127.0.0.1:5000/tasks \
  -H "Authorization: Bearer example-token"
```
``` bash
# GET /tasks/<task_id> -- get one task
curl http://127.0.0.1:5000/tasks/1 \
  -H "Authorization: Bearer example-token"
```
``` bash
# POST /tasks -- create a task
curl -X POST http://127.0.0.1:5000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer example-token" \
  -d '{"title":"Write a FastAPI route","description":"Practice POST requests","completed":false}'
```
``` bash
# PATCH /tasks/<task_id> -- update part of a task
curl -X PATCH http://127.0.0.1:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer example-token" \
  -d '{"completed":true}'
```
``` bash
# DELETE /tasks/<task_id> -- delete a task
curl -X DELETE -i http://127.0.0.1:5000/tasks/1 \
  -H "Authorization: Bearer example-token"
```
