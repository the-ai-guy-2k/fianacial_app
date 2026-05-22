# Docker Usage for Financial Nebula Node

This document explains how to build, run, and pull the Financial Nebula Node application from Docker.

## Docker Hub Image

The Financial Nebula Node is automatically published to Docker Hub:

```
taig2k/financial-nebula-node
```

### Pull the latest image from Docker Hub

```powershell
docker pull taig2k/financial-nebula-node:latest
```

### Pull a specific version by commit SHA

```powershell
docker pull taig2k/financial-nebula-node:<commit-sha>
```

## What Docker Adds

- Consistent local runtime environment for the Flask application
- Isolation from host Python installations
- Support for mounting configuration and secret files at runtime
- Automated publishing to Docker Hub on deployable branch commits
- Easy portability across machines

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

## Docker Hub Image Tags

- **`latest`**: Points to the most recent image published from the deployable branch
- **Commit SHA**: Each deployment creates a tag with the commit SHA for full traceability

Example:
```powershell
docker run -p 5000:5000 taig2k/financial-nebula-node:latest
```

## CI/CD Publishing Behavior

- **Feature branches**: Docker image is built and validated in CI but NOT pushed to Docker Hub
- **Deployable branch**: Docker image is built, validated, and automatically pushed to Docker Hub with `latest` and commit SHA tags

This ensures only validated, tested code is published to Docker Hub.

## Config file and secret handling

- Do not bake `config.json` or any API key file into the Docker image
- Mount `config.docker.json` to `/app/config.json` inside the container
- Mount the OpenAI key file to `/run/secrets/openai_key.txt` inside the container
- The app also supports environment variables `CONFIG_FILE` and `OPENAI_API_KEY_FILE`

### Example `config.docker.json`

Use the provided `config.docker.example.json` as a starting point, or mount your own config with the API key path set to `/run/secrets/openai_key.txt`.

## Troubleshooting

- If the app still fails to start, check the container logs for configuration or API key errors
- If the app cannot bind, confirm the container exposes port `5000` and the host port is available
- Do not commit mounted secret file paths or API keys to source control
- Check Docker Hub repo for available images and tags: `https://hub.docker.com/r/taig2k/financial-nebula-node`

## Why secrets are not baked into images

- Docker images are often shared across environments; embedding secrets would risk accidental exposure
- Use mounts or environment variables so credentials remain on the host and are injected only at runtime
- This keeps the image reusable and secure across all users and environments
