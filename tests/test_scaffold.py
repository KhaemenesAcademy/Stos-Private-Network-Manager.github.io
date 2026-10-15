from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ScaffoldTests(unittest.TestCase):
    def test_stos_port_not_published_by_compose(self):
        compose = (ROOT / "compose.yaml").read_text()
        self.assertNotIn('"9844:9844', compose)
        self.assertNotIn("'9844:9844", compose)

    def test_dashboard_binds_loopback(self):
        compose = (ROOT / "compose.yaml").read_text()
        self.assertIn('127.0.0.1:8787:8787', compose)

    def test_policy_has_specific_destination(self):
        policy = (ROOT / "config/policy.hujson").read_text()
        self.assertIn('100.64.0.10:9844', policy)
        self.assertIn('"src": ["tag:stos-client"]', policy)

    def test_docs_do_not_claim_verified(self):
        readme = (ROOT / "README.md").read_text().lower()
        self.assertIn('not yet production-verified', readme)
        self.assertIn('does not authenticate a user to stos', readme)

if __name__ == "__main__":
    unittest.main()
