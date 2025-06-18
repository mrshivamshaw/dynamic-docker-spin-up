from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import docker
import random

app = FastAPI()
client = docker.from_env()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows only specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/run")
def run_container():
    try:
        frontend_port = random.randint(4000, 5000)
        backend_port = random.randint(5001, 6000)

        container = client.containers.run(
            "fullstack-base",
            volumes={
                "/home/thecoderguy/fullstack-runner/template-app": {
                    'bind': '/app', 'mode': 'rw'
                }
            },
            ports={
                '3000/tcp': frontend_port,
                '8000/tcp': backend_port
            },
            detach=True
        )

        return {
            "frontend_url": f"http://localhost:{frontend_port}",
            "backend_url": f"http://localhost:{backend_port}/api/hello"
        }

    except Exception as e:
        return {"error": str(e)}
