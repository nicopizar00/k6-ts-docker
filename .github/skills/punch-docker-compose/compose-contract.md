# Compose Service Contract Template

Every service in `docker-compose.yml` must declare the following fields.
If a field is genuinely not applicable, document the reason in a comment.

```yaml
services:
  <service-name>:                       # CONTRACT: stable, lowercase, kebab-case
    image: <name>:<pinned-tag>          # CONTRACT: never `:latest`
    container_name: <service-name>      # optional but recommended for log clarity
    build:                              # optional; if present, points at a Dockerfile
      context: .
      dockerfile: docker/<service>.Dockerfile
    ports:                              # CONTRACT: explicit, never random
      - "<host>:<container>"            # only when the host needs reachability
    environment:                        # CONTRACT: every env var is part of the surface
      VAR_NAME: ${VAR_NAME:-default}    # default makes it work without env files
    depends_on:                         # CONTRACT: only ordering mechanism
      <other-service>:
        condition: service_healthy      # CONTRACT: never service_started for deps
    healthcheck:                        # CONTRACT: every service has one
      test: ["CMD", "<lightweight-check>"]
      interval: 5s
      timeout: 3s
      retries: 10
      start_period: 5s                  # tune per service
    volumes:                            # CONTRACT: read-only by default
      - ./<host-path>:<container-path>:ro
    networks:                           # CONTRACT: explicit network membership
      - punch-net                       # default project network
```

## Field-by-field rules

| Field | Required | Notes |
|---|---|---|
| `image` | yes | Pin to a specific version. Never `:latest`. |
| `container_name` | recommended | Improves log readability and matches grep patterns in `.github/workflows/k6.yml`. |
| `build` | when service is local | Use multi-stage builds; runtime stage carries artifacts only. |
| `ports` | only when host access needed | Internal traffic uses service-name DNS, no port mapping. |
| `environment` | yes (even if empty) | Every variable is part of the contract. Document defaults. |
| `depends_on` with `condition: service_healthy` | yes if depending on others | Replaces `sleep` loops. |
| `healthcheck` | yes | Without it, `depends_on` cannot gate startup. |
| `volumes` | yes (`./reports:/reports` writable, others `:ro`) | Writable mounts must be justified in the Plan. |
| `networks` | yes (`punch-net`) | All services share the project network so k6 can resolve hostnames. |

## What changes break the contract

These changes are *contract changes* and require a Plan with a dependents
cascade (see [`docs/ai/maintenance-matrix.md`](../../../docs/ai/maintenance-matrix.md)):

- Renaming a service.
- Changing an exposed port (host-side).
- Removing or weakening a healthcheck.
- Adding a writable volume.
- Changing the image tag in a way that bumps a major version.
- Removing or renaming an env var that another service or `src/tests/`
  reads.

## What changes are within contract

These do **not** require a Plan beyond the normal Build:

- Patch-level image bumps (within the same major).
- Tightening a healthcheck interval/timeout.
- Adding an env var with a backwards-compatible default.
- Adding a new service that follows the template above (still requires a
  Plan because of the cascade into `bin/punch` and possibly tests).
