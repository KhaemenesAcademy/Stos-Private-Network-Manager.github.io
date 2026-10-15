import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="STOS Private Network Manager", docs_url=None, redoc_url=None)
CONTROL_FQDN = os.getenv("CONTROL_FQDN", "not-configured")
SECRET_SET = bool(os.getenv("DASHBOARD_SECRET")) and os.getenv("DASHBOARD_SECRET") != "REPLACE_WITH_A_LONG_RANDOM_SECRET"

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>STOS Private Network Manager</title>
<style>
:root{color-scheme:dark;--bg:#10151d;--panel:#182230;--line:#2d3b4c;--text:#edf2f7;--muted:#a8b6c7;--gold:#d7bd83}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at top,#202c3b,var(--bg) 55%);color:var(--text);font:16px/1.6 Arial,sans-serif}
main{max-width:1000px;margin:auto;padding:36px 20px 70px}header{text-align:center;padding:24px 0 30px;border-bottom:1px solid var(--line)}
.kicker{letter-spacing:.18em;text-transform:uppercase;color:var(--gold);font-size:.76rem}h1{font:normal clamp(1.8rem,4vw,3rem)/1.2 Georgia,serif;margin:12px 0}h2{font:normal 1.3rem Georgia,serif;margin-top:0}.sub{color:var(--muted);max-width:680px;margin:auto}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:24px 0}.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px}.label{color:var(--muted);font-size:.85rem}.value{font-size:1.1rem;margin-top:5px}.warning{border-color:#806a3d}.pill{display:inline-block;border:1px solid var(--line);border-radius:99px;padding:3px 10px;font-size:.8rem;color:var(--gold)}
li{margin:.55rem 0;color:#d9e1ea}code{color:#e7d5a8;background:#111923;padding:2px 5px;border-radius:4px}.foot{color:var(--muted);font-size:.88rem;margin-top:25px}
</style></head><body><main><header><div class="kicker">Private infrastructure · operator console</div>
<h1>STOS Private Network Manager</h1><p class="sub">A self-hosted control-plane deployment scaffold for private STOS access.</p></header>
<div class="grid">
<section class="card"><div class="label">Control-plane hostname</div><div class="value">__HOST__</div></section>
<section class="card"><div class="label">Credential / tunnel status</div><div class="value">Not verified by this dashboard</div></section>
<section class="card warning"><div class="label">Security verification</div><div class="value">Deployment and tests required</div></section>
</div>
<section class="card"><h2>Operator checklist</h2><ol>
<li>Enroll devices using the version-matched Headscale CLI/API.</li>
<li>Approve only the four intended device identities; inspect node inventory after every enrollment.</li>
<li>Assign <code>tag:stos-client</code> only to approved devices and verify policy evaluation.</li>
<li>Keep STOS port <code>9844</code> off public interfaces and router forwarding rules.</li>
<li>Confirm STOS independently authenticates sessions.</li>
<li>Run every test in <code>docs/SECURITY-VERIFICATION.md</code> and preserve results.</li>
</ol></section>
<section class="card" style="margin-top:14px"><h2>Trust boundary</h2><p>This page is informational. It does not create keys, approve devices, change ACLs, or revoke access. Use the secured host and Headscale administration interface for those actions. Do not expose this dashboard publicly.</p></section>
<p class="foot">A private tunnel is not proof of application authentication or live synchronization. Those controls require independent testing.</p>
</main></body></html>"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(PAGE.replace("__HOST__", CONTROL_FQDN))

@app.get("/health")
def health():
    # Reports only dashboard process readiness, not VPN or STOS health.
    return JSONResponse({"dashboard": "running", "control_fqdn_configured": CONTROL_FQDN != "not-configured",
                         "secret_configured": SECRET_SET,
                         "vpn_status": "not_checked", "stos_authentication": "not_checked",
                         "live_synchronization": "not_checked"})
