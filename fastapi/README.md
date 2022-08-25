# Simple FastAPI boilerplate

---

This is a basic FastAPI application that can be used to start off a new project. 

The application will run as is, but note it is not secure. Please implement your own
database logic and utilize more secure user handling methods. 

Any password or secret that exists within this repository is **NOT SECURE**. Only use for example and demonstration purposes. 

---
### Using the application

1. Ensure Poetry is installed to your local environment `pip install poetry`
2. Install dependencies using poetry `poetry install`
3. Run application `uvicorn src.app.main:app`
4. You can access the swagger page via `http://localhost:8000/docs`
