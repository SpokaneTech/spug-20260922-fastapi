FROM python:3.13-alpine

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src/app ./src/app
RUN pip install --no-cache-dir .

EXPOSE 5000

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5000"]
