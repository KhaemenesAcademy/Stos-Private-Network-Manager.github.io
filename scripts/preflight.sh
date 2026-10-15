#!/usr/bin/env sh
set -eu
echo "STOS Private Network Manager preflight"
[ -f .env ] || { echo "ERROR: .env missing; copy .env.example and edit it."; exit 1; }
grep -q '^CONTROL_FQDN=.' .env || { echo "ERROR: CONTROL_FQDN missing"; exit 1; }
if grep -q 'REPLACE_WITH_A_LONG_RANDOM_SECRET' .env; then
  echo "ERROR: replace the example dashboard secret"; exit 1
fi
if grep -q 'vpn.example.net' config/headscale.yaml; then
  echo "WARNING: update server_url in config/headscale.yaml"
fi
if grep -q '100.64.0.10:9844' config/policy.hujson; then
  echo "WARNING: confirm STOS tailnet IP in config/policy.hujson"
fi
if grep -Eq '"9844:9844|9844:.*9844' compose.yaml; then
  echo "ERROR: STOS port must not be published by Compose"; exit 1
fi
echo "Basic preflight complete. This does NOT test VPN connectivity or security."
