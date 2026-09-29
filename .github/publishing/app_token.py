#!/usr/bin/env python3
"""Print a one-hour installation token for the organization's publishing App.

Reads `app_id` and `private-key.pem` from $ICRA_PSF_APP_DIR
(default ~/.config/icra-2027-psf-publisher). Pushes made with the token are
credited to icra-2027-psf-publisher[bot].
"""
import json
import os
import time
import urllib.request

import jwt

D = os.path.expanduser(os.environ.get("ICRA_PSF_APP_DIR", "~/.config/icra-2027-psf-publisher"))
ORG = "icra-2027-psf"


def api(method, path, bearer):
    req = urllib.request.Request(
        f"https://api.github.com{path}", method=method,
        headers={"Authorization": f"Bearer {bearer}",
                 "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


now = int(time.time())
app_jwt = jwt.encode({"iat": now - 60, "exp": now + 540,
                      "iss": open(os.path.join(D, "app_id")).read().strip()},
                     open(os.path.join(D, "private-key.pem")).read(), algorithm="RS256")
inst = api("GET", f"/orgs/{ORG}/installation", app_jwt)
print(api("POST", f"/app/installations/{inst['id']}/access_tokens", app_jwt)["token"])
