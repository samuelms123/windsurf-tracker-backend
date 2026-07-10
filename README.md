# Windsurf-Tracker API

This repository contains the backend API built with **FastAPI**. It handles basic user management, but its main purpose is to fetch users windsurf activities & stream data from Strava API and analyze them to provide windsurf specific metrics.

Note that currently in main is a single-user solution for my personal use only that requires dedicated VPN connection, because the backend and database are hosted on my home lab servers.

Please check out the project repositories here:
* **Overview** [Windsurf-Tracker Overview](https://github.com/samuelms123/windsurf-tracker)
* **Backend API:** [Windsurf-Tracker Backend](https://github.com/samuelms123/windsurf-tracker-backend)

### Backend Stack
* **[FastAPI](https://fastapi.tiangolo.com/)** Deployed locally inside an isolated Proxmox LXC.
* **[Uvicorn](https://www.uvicorn.org/)** – Deployed locally inside an isolated Proxmox LXC.
* **[MongoDB](https://www.mongodb.com/)** – Hosted within a dedicated Proxmox VM.
* **[Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)** - Data analysis
* **[HTTPX](https://www.python-httpx.org/)**
* **[Pytest](https://docs.pytest.org/)**

### Security & Authentication
* **Single-User Architecture** – Relies on an isolated **WireGuard VPN** server (deployed via PiVPN on a Proxmox LXC) as the primary cryptographic gateway.
* **Multi-User Architecture** *(Archived in `multi-user` branch)* – Implements full OAuth 2.0 (Strava) integration, standard JWT authentication, Argon2 password hashing, and Fernet symmetric encryption for long-lived refresh tokens.
