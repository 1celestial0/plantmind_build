"""Upload team-share staging folder to Google Drive (uses local OAuth token)."""

from __future__ import annotations

import json
import mimetypes
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "continuity" / "drive-export-staging" / "team-share"
STATE_PATH = ROOT / "continuity" / "STATE.json"
CREDS_PATH = Path.home() / "AppData/Local/google-vscode-extension/auth/credentials.json"
GCLOUD = Path.home() / "AppData/Local/Google/Cloud SDK/google-cloud-sdk/bin/gcloud.cmd"
DRIVE_UPLOAD = "https://www.googleapis.com/upload/drive/v3/files"
DRIVE_API = "https://www.googleapis.com/drive/v3/files"


def _refresh_with_drive_scope() -> str | None:
    if not CREDS_PATH.exists():
        return None
    data = json.loads(CREDS_PATH.read_text(encoding="utf-8"))
    refresh = data.get("refreshToken") or data.get("credentials", {}).get("refresh_token")
    if not refresh:
        return None
    client_id = "681255809395-oo8oft2opprdrnp9e3aqf6av3hmdib135.apps.googleusercontent.com"
    resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": client_id,
            "refresh_token": refresh,
            "grant_type": "refresh_token",
            "scope": "https://www.googleapis.com/auth/drive",
        },
        timeout=30,
    )
    if resp.status_code != 200:
        return None
    return resp.json().get("access_token")


def load_token() -> str:
    token = _refresh_with_drive_scope()
    if token:
        return token
    if CREDS_PATH.exists():
        data = json.loads(CREDS_PATH.read_text(encoding="utf-8"))
        token = data.get("accessToken") or data.get("credentials", {}).get("access_token")
        if token:
            return token
    if GCLOUD.exists():
        try:
            proc = subprocess.run(
                [str(GCLOUD), "auth", "print-access-token"],
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            token = proc.stdout.strip()
            if token:
                return token
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            pass
    raise RuntimeError(
        "No Google Drive token. Run from Claude CLI with Drive MCP, or re-auth with drive scope."
    )


def folder_id() -> str:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8-sig"))
    return state["drive_folder_id"]


def list_files_in_folder(token: str, parent_id: str) -> dict[str, str]:
    q = f"'{parent_id}' in parents and trashed=false"
    resp = requests.get(
        DRIVE_API,
        headers={"Authorization": f"Bearer {token}"},
        params={"q": q, "fields": "files(id,name)", "pageSize": 200},
        timeout=60,
    )
    resp.raise_for_status()
    return {f["name"]: f["id"] for f in resp.json().get("files", [])}


def upload_or_update(token: str, parent_id: str, local_path: Path, existing: dict[str, str]) -> str:
    name = local_path.name
    mime, _ = mimetypes.guess_type(local_path)
    mime = mime or "application/octet-stream"

    if name in existing:
        file_id = existing[name]
        url = f"{DRIVE_UPLOAD}/{file_id}"
        params = {"uploadType": "media"}
        with local_path.open("rb") as fh:
            resp = requests.patch(
                url,
                headers={"Authorization": f"Bearer {token}", "Content-Type": mime},
                params=params,
                data=fh,
                timeout=300,
            )
        resp.raise_for_status()
        return f"updated:{name}"

    metadata = {"name": name, "parents": [parent_id]}
    with local_path.open("rb") as fh:
        resp = requests.post(
            DRIVE_UPLOAD,
            headers={"Authorization": f"Bearer {token}"},
            params={"uploadType": "multipart"},
            files={
                "metadata": ("metadata", json.dumps(metadata), "application/json"),
                "file": (name, fh, mime),
            },
            timeout=300,
        )
    resp.raise_for_status()
    return f"created:{name}"


def upload_tree(token: str, parent_id: str, local_dir: Path, rel_prefix: str = "") -> list[str]:
    results: list[str] = []
    existing = list_files_in_folder(token, parent_id)

    for item in sorted(local_dir.iterdir()):
        if item.name == "manifest.json":
            continue
        if item.is_file():
            results.append(upload_or_update(token, parent_id, item, existing))
        elif item.is_dir():
            sub_name = item.name
            if sub_name in existing:
                sub_id = existing[sub_name]
            else:
                meta = {"name": sub_name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]}
                r = requests.post(
                    DRIVE_API,
                    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                    json=meta,
                    timeout=60,
                )
                r.raise_for_status()
                sub_id = r.json()["id"]
                results.append(f"created-folder:{sub_name}")
            results.extend(upload_tree(token, sub_id, item, f"{rel_prefix}{sub_name}/"))
    return results


def main() -> int:
    if not CREDS_PATH.exists():
        print(f"Missing credentials: {CREDS_PATH}", file=sys.stderr)
        return 1
    if not STAGING.exists():
        print(f"Run sync-team-share-drive.ps1 first. Missing: {STAGING}", file=sys.stderr)
        return 1

    token = load_token()
    parent = folder_id()
    print(f"Uploading to Drive folder {parent} from {STAGING}")
    results = upload_tree(token, parent, STAGING)
    for line in results:
        print(f"  {line}")
    print(f"Done: {len(results)} operations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())