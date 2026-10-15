# STOS Security Verification Plan

Record date, operator, client OS/version, server image digest, test result, and evidence for every test. A successful `docker compose up` is not a security test.

## A. Exposure and host configuration

- [ ] From a network outside the home LAN, scan the home public IP. Confirm only intended control-plane HTTPS is reachable.
- [ ] Confirm TCP 9844 is not forwarded by the router and is not listening on the public host interface.
- [ ] Confirm dashboard port 8787 is bound only to `127.0.0.1`.
- [ ] Confirm Headscale's admin interface/API is not publicly exposed.
- [ ] Confirm host firewall denies unsolicited inbound traffic except the intentionally published control-plane port.
- [ ] Confirm DNS and TLS certificate validation work from outside the home network.

## B. Device identity and four-device cap

- [ ] Enroll one device each on macOS, Windows, Linux, and Android using unique device identities.
- [ ] Verify all four devices appear separately in the Headscale node inventory.
- [ ] Attempt a fifth enrollment. Confirm the operator workflow refuses it and document any manual enforcement needed.
- [ ] Verify an unapproved node cannot receive the `tag:stos-client` tag.
- [ ] Verify no device shares another device's private key or reusable device credential.
- [ ] Confirm an unapproved device cannot reach STOS TCP 9844.

## C. Encryption and reachability

- [ ] Confirm each client reports a connected tailnet and recent handshake.
- [ ] Capture traffic on the physical LAN/WAN interface while accessing STOS; verify application payload is not sent in cleartext outside the encrypted tunnel.
- [ ] Test clients on distinct external networks, including a restrictive NAT if available.
- [ ] Verify relay behavior when direct peer-to-peer paths fail.
- [ ] Verify no default route or unrelated LAN access is granted unintentionally.

## D. Default-deny policy

- [ ] Approved tagged client -> STOS tailnet IP TCP 9844: allowed.
- [ ] Approved tagged client -> STOS host SSH/administration ports: denied unless separately and deliberately authorized.
- [ ] Unapproved device -> STOS TCP 9844: denied.
- [ ] Approved device -> unrelated tailnet device/service: denied.
- [ ] Test IPv4 and IPv6 paths if IPv6 is enabled.
- [ ] Verify the actual STOS process binds only to the intended private interface or loopback gateway.

## E. Revocation

- [ ] Revoke one test device through Headscale's supported administrative interface.
- [ ] Verify it disappears/is disabled in node inventory according to version behavior.
- [ ] Verify it cannot establish a new tunnel or reach TCP 9844.
- [ ] Test an already-established connection and application session; confirm firewall/session termination and STOS session invalidation meet the required revocation window.
- [ ] Confirm the other three devices remain operational.
- [ ] Document propagation delay and any connection-tracking state that must be cleared.

## F. Independent STOS authentication

- [ ] Request STOS without a valid application session from an approved VPN device: expect 401/redirect/denial.
- [ ] Request STOS with a valid session: expect only authorized operations.
- [ ] Revoke/logout the STOS session and retry: expect denial.
- [ ] Confirm a VPN device identity alone never grants application-level access.
- [ ] Test CSRF protections if cookie-based browser sessions are used, plus session expiry and secure cookie flags.

## G. Live synchronization (application-layer tests)

- [ ] Make a change on device A and verify it appears on device B within the defined service-level target.
- [ ] Make concurrent edits on two devices; verify deterministic conflict handling and no silent data loss.
- [ ] Disconnect a client, change data on another device, reconnect the first client, and verify catch-up.
- [ ] Restart the STOS service and confirm persisted data and reconnect behavior.
- [ ] Test duplicate delivery, retries, and offline edits if supported by STOS.
- [ ] Verify authorization is enforced on sync endpoints, not just on the initial page load.

## Acceptance criteria

Do not label the deployment production-ready until all applicable checks pass, failures are remediated, and the evidence is reviewed. Mark unsupported or untested requirements explicitly rather than treating them as passed.
