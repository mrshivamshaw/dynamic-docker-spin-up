from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import docker
import random
import uuid

app = FastAPI()
client = docker.from_env()
container_map = {}  # key: run_id, value: container_id

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

        run_id = str(uuid.uuid4())
        container_map[run_id] = container.id
        print(container_map)
        return {
            "run_id": run_id,
            "frontend_url": f"http://localhost:{frontend_port}",
            "backend_url": f"http://localhost:{backend_port}/api/hello",
        }

    except Exception as e:
        return {"error": str(e)}

@app.post("/stop")
async def stop_container(request: Request):
    try:
        data = await request.json()
        run_id = data.get("run_id")
        if not run_id or run_id not in container_map:
            return {"error": "Invalid run_id"}

        container_id = container_map[run_id]
        container = client.containers.get(container_id)
        container.kill()
        del container_map[run_id]

        return {"message": f"Container with run_id {run_id} stopped successfully"}

    except Exception as e:
        return {"error": str(e)}
