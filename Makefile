start:
	uvicorn app.api.api:app --host 0.0.0.0 --port 8080 --workers 1