# STOS Private Network Manager (SPNM)

A self-hosted deployment scaffold for private access to a home-hosted STOS service. It uses Headscale as the self-hosted coordination server and WireGuard-based Tailscale clients for encrypted transport. It does **not** implement its own cryptography.

## Security status: scaffold, not yet production-verified

This repository provides configuration, an operator checklist, a policy starting point, and a small local dashboard/API for viewing deployment guidance. It does not claim that the network is operational or secure until you deploy it, adapt it to your Headscale version, and complete the verification checklist.

The dashboard is intentionally **not** an authentication authority and does not issue or revoke VPN credentials. Perform enrollment, approval, and revocation through the installed Headscale CLI/API, then verify the resulting node and policy state. This avoids presenting a decorative UI as a security control.

## Important network constraint

A home-hosted control plane must be reachable by roaming devices somehow. This scaffold expects a DNS name and an inbound HTTPS path to the **control plane only** (typically TCP 443 forwarded to Caddy). It does **not** publish or forward STOS port 9844. If you do not want any inbound home-router ports at all, you need a separate reachable rendezvous/relay design; a fully self-hosted control plane entirely behind NAT cannot generally be reached by remote devices without an outbound tunnel or another reachable endpoint.

Headscale coordination reachability is not the same as direct peer reachability. Some networks may require DERP relaying. Review the Headscale documentation for the exact version deployed.

## Included

- `compose.yaml`: Headscale, Caddy, and a local status dashboard.
- `config/headscale.yaml`: starter Headscale config (review against pinned release).
- `config/policy.hujson`: default-deny ACL policy permitting only explicitly tagged STOS clients to reach the STOS host on TCP 9844.
- `Caddyfile`: HTTPS reverse proxy for the control plane and dashboard.
- `dashboard/`: minimal FastAPI status/instructions page, bound to localhost by default.
- `scripts/`: host firewall examples and a preflight checklist.
- `tests/`: policy and configuration sanity checks (not a substitute for integration testing).

## Deployment outline

1. Choose a DNS name such as `vpn.example.net`; configure its A/AAAA records to your home public IP.
2. On the home router, forward **TCP 443 only** to the host running Caddy. Do not forward TCP 9844. Ensure the ISP permits inbound HTTPS. If not, use an alternative externally reachable control-plane design.
3. Copy `.env.example` to `.env`, set a strong unique `DASHBOARD_SECRET`, and set `CONTROL_FQDN`.
4. Review `config/headscale.yaml` for the selected Headscale release. Pin the image tag to a release you have reviewed; do not use `latest`.
5. Replace the example `STOS_TAILNET_IP` in `config/policy.hujson` with the STOS server's stable tailnet IP or use a supported host alias strategy. Ensure only authorized devices receive the `tag:stos-client` tag.
6. Review TLS, DNS, firewall, backup, and admin-access arrangements before starting.
7. Start services with `docker compose up -d`; inspect logs and health manually.
8. Enroll each of the four devices using the supported Headscale CLI/API for your chosen release. Approve only the four intended devices. Do not share one device key between devices.
9. Use platform-supported Tailscale clients configured to use your Headscale server. Android, macOS, Windows, and Linux clients are available, but client compatibility and enrollment steps should be verified against current vendor documentation.
10. Configure the STOS application to bind only to its tailnet interface or loopback behind a controlled gateway. Keep application authentication enabled.
11. Run the test plan in `docs/SECURITY-VERIFICATION.md` from each platform and record evidence.

## Device limit

The four-device maximum is an operational policy in this scaffold, not a magical hard limit enforced by the WireGuard protocol. Enforce it by maintaining an allowlist of four active device identities, preventing unapproved enrollments, reviewing the node inventory, and revoking extras immediately. If you require a cryptographically enforced automated cap, implement and test an authenticated enrollment broker against the exact Headscale version before relying on it.

## STOS authentication and synchronization

VPN membership does not authenticate a user to STOS. STOS must independently authenticate every session and authorize each request. Use secure cookies or short-lived tokens, TLS where applicable, CSRF protections for cookie-based browser sessions, rate limits, and audit logs.

Live synchronization is an application-layer property. Test reconnect, simultaneous updates, conflict resolution, persistence, and recovery after network loss separately.

## Local dashboard

The dashboard is a local operator landing page only. It deliberately does not expose credential creation or revocation actions. Run it locally and access it at `http://127.0.0.1:8787`. Do not expose it to the internet. A future integration should use the version-matched Headscale API with strong admin authentication, CSRF protection, audit logging, and explicit confirmation for destructive actions.

## Quick checks

```bash
cp .env.example .env
# Edit .env before starting.
docker compose config
docker compose up -d
docker compose ps
docker compose logs --tail=100 headscale caddy dashboard
python -m unittest discover -s tests -v
```

These commands validate configuration or service startup only; they do not prove the tunnel, access policy, revocation, application authentication, or synchronization work correctly.

## Security caveats

- This scaffold is not an audited security product.
- Do not use the example secrets or sample domain in production.
- Pin and review image versions; monitor security advisories and back up Headscale state securely.
- Restrict access to Docker, the host OS, Headscale's Unix/CLI administration, and the dashboard.
- Do not put Headscale's admin API or dashboard on an unrestricted public interface.
- A compromised home host can compromise the control plane.
- Do not add `9844:9844` to Compose or a router forwarding rule.
