import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def welcome() -> dict[str, str]:
    return {"message": "Welcome to the Task API"}


def main() -> None:
    """Run the Task API development server."""
    uvicorn.run("app.app:app", host="127.0.0.1", port=5000, reload=True)


if __name__ == "__main__":
    main()
