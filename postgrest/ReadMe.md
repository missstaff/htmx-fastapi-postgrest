# PostgREST Setup Guide

This directory contains the configuration and Docker setup for running **PostgREST**. PostgREST is a tool that serves as a RESTful API for a PostgreSQL database, making it easy to expose your database tables as HTTP endpoints.

## Directory Structure

```
/postgrest
│
├── Dockerfile           # Dockerfile for building the PostgREST container
├── postgrest.conf       # Configuration file for PostgREST
└── README.md            # This file
```

## Requirements

- **Docker** (for running PostgREST in a containerized environment)
- **PostgreSQL** (either locally or within a Docker container, depending on your setup)

## Configuration Overview

The `postgrest.conf` file is where you define your PostgreSQL connection settings and configure PostgREST. It allows you to set the PostgreSQL connection URI, the schema, and the role configurations that PostgREST will use.

- **db-uri**: Defines the connection URI for your PostgreSQL instance.
- **db-schema**: The PostgreSQL schema that PostgREST will expose as an API.
- **db-anon-role**: The PostgreSQL role that PostgREST uses for unauthenticated requests.

### Example `postgrest.conf`:

```ini
# PostgreSQL connection settings

# For Docker environment (PostgreSQL running in Docker)
db-uri = "postgres://postgres:mysecretpassword@postgres:5432/postgrest_db"

# For local development (uncomment when running locally)
# db-uri = "postgres://postgres:mysecretpassword@localhost:5432/postgrest_db"

# Schema and role configurations
db-schema = "public"
db-anon-role = "web_anon"

# PostgREST URL settings

# For Docker environment (PostgREST will be accessible from within the Docker network)
POSTGREST_URL = "http://postgrest:3000"

# For local development (uncomment when running locally)
# POSTGREST_URL = "http://localhost:3000"
```

## How to Run PostgREST

### Running with Docker

1. **Build the Docker image**:
   In the `postgrest` directory, build the Docker image using the following command:

   ```bash
   docker build -t postgrest .
   ```

2. **Run the Docker container**:
   After building the Docker image, run the container:

   ```bash
   docker run -d -p 3000:3000 --name postgrest --env-file .env postgrest
   ```

   This will start PostgREST on port `3000` and use the environment variables defined in the `.env` file (if available). Ensure that PostgreSQL is accessible from the Docker network using the configured `db-uri`.

### Running Locally

If you prefer to run PostgREST locally (not in Docker), you'll need to have **PostgreSQL** and **PostgREST** installed on your machine.

1. **Install PostgREST**:
   Follow the [PostgREST installation instructions](https://postgrest.org/en/stable/install.html) for your operating system.

2. **Configure PostgreSQL**:
   Ensure that PostgreSQL is running locally on your machine and that the database and schema exist. You can use the connection string:

   ```
   postgres://postgres:mysecretpassword@localhost:5432/postgrest_db
   ```

3. **Run PostgREST**:
   Start PostgREST using the following command (assuming the `postgrest.conf` file is in the same directory):

   ```bash
   postgrest postgrest.conf
   ```

   This will start PostgREST locally on `http://localhost:3000`.

### Environment Variables

You can specify environment variables by creating a `.env` file in the `postgrest` directory. These variables will be used by Docker or PostgREST if needed.

Example `.env` file:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=postgrest_db
POSTGREST_URL=http://localhost:3000
```

## Notes

- **Docker Networking**: If you are running both PostgREST and PostgreSQL in Docker, ensure that the Docker network is set up correctly, and the `db-uri` is configured to connect to the PostgreSQL container (e.g., `postgres://postgres:mysecretpassword@postgres:5432/postgrest_db`).
  
- **Local Development**: When running locally, ensure PostgreSQL is running on `localhost` and the database exists before starting PostgREST. Update the `postgrest.conf` file to use `localhost` for local connections.

- **Rate Limiting and API Security**: The configuration provided is a starting point. You can extend this with authentication, authorization, and rate limiting as needed.
