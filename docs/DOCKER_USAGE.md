# Docker Usage for Financial Nebula Node

This document explains how to build and run the Financial Nebula Node application inside a Docker container.

## What Docker Adds

- Consistent local runtime environment for the Flask application
- Isolation from host Python installations
- Support for mounting configuration and secret files at runtime
- Validation of container builds in CI without pushing images to Docker Hub

## Build the image locally

From the repository root:
```powershell
docker build -t financial-nebula-node:local .
```

## Run the container locally

### Run without OpenAI configured

This starts the app with no mounted config or API key. It is useful to confirm the container runs and responds on port 5000.

```powershell
docker run --rm -p 5000:5000 financial-nebula-node:local
```

### Run with mounted config and API key

Mount a local Docker-friendly config file and the OpenAI key file into the container.

```powershell
docker run --rm -p 5000:5000 `
  -v "%cd%\config.docker.json:/app/config.json" `
  -v "C:\Users\tim\Desktop\openai_key_for_financial_app.txt:/run/secrets/openai_key.txt" `
  financial-nebula-node:local
```

Then open:

```
http://127.0.0.1:5000
```

## Config file and secret handling

- Do not bake `config.json` or any API key file into the Docker image.
- Mount `config.docker.json` to `/app/config.json` inside the container.
- Mount the OpenAI key file to `/run/secrets/openai_key.txt` inside the container.
- The app also supports the environment variables `CONFIG_FILE` and `OPENAI_API_KEY_FILE`.

### Example `config.docker.json`

Use the provided `config.docker.example.json` as a starting point.

### Using an environment variable for OpenAI key location

If you prefer to mount the key file elsewhere, set:

```powershell
docker run --rm -p 5000:5000 `
  -v "%cd%\config.docker.json:/app/config.json" `
  -v "C:\Users\tim\Desktop\openai_key_for_financial_app.txt:/run/secrets/openai_key.txt" `
  -e OPENAI_API_KEY_FILE=/run/secrets/openai_key.txt `
  financial-nebula-node:local
```

## Troubleshooting

- If the app still fails to start, check the container logs for configuration or API key errors.
- If the app cannot bind, confirm the container exposes port `5000` and the host port is available.
- Do not commit mounted secret file paths or API keys to source control.

## Why secrets are not baked into the image

- Docker images are often shared across environments; embedding secrets would risk accidental exposure.
- Use mounts or environment variables so credentials remain on the host and are injected only at runtime.
- This keeps the image reusable and secure.
