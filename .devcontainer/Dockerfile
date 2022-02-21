# Microsoft image (contains a lot of useful extras)
FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.10-bullseye

WORKDIR /service
COPY . /service

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# Debug asyncio
# ENV PYTHONASYNCIODEBUG=1

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# To be able to use absolute import paths
ENV PYTHONPATH=/service

# Use latest version of pip
RUN pip install --upgrade pip
