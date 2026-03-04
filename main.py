"""
Cortex KB – Web server
Serves the rich dark-academia UI and JSON API endpoints.
Uses only the stdlib so there are zero extra runtime dependencies.
"""

import json
import os
import sys
import mimetypes
import tempfile
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Ensure the project root is importable
sys.path.insert(0, str(Path(__file__).parent))

from cortex.cortex import CortexKB

# ── Paths ──
ROOT      = Path(__file__).resolve().parent
STATIC    = ROOT / "web" / "static"
TEMPLATES = ROOT / "web" / "templates"

# ── Cortex instance (created once) ──
DATA_DIR    = os.getenv("DATA_DIR", "./cortex_data")
DISCOVERY   = os.getenv("ENABLE_WEB_SEARCH", "true").lower() == "true"
THRESHOLD   = float(os.getenv("RELEVANCE_THRESHOLD", "0.7"))
LLM_PROV    = os.getenv("LLM_PROVIDER")
LLM_KEY     = os.getenv("LLM_API_KEY")

cortex = CortexKB(
    storage_path=DATA_DIR,
    enable_external_sources=DISCOVERY,
    relevance_threshold=THRESHOLD,
    llm_provider=LLM_PROV,
    llm_api_key=LLM_KEY,
)


# ══════════════════════════════════════════════════
#  Request Handler
# ══════════════════════════════════════════════════

class Handler(BaseHTTPRequestHandler):
    """Routes for static files, HTML template, and JSON API."""

    # ── silence per-request logs in production ──
    def log_message(self, fmt, *args):
        if os.getenv("LOG_REQUESTS"):
            super().log_message(fmt, *args)

    # ────────────────────────────────────
    #  GET
    # ────────────────────────────────────
    def do_GET(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/") or "/"
        qs     = parse_qs(parsed.query)

        # ── Pages ──
        if path in ("/", "/index.html"):
            return self._serve_file(TEMPLATES / "index.html", "text/html; charset=utf-8")

        # ── Static assets ──
        if path.startswith("/static/"):
            rel  = path[len("/static/"):]
            fpath = (STATIC / rel).resolve()
            # prevent directory traversal
            if fpath.is_file() and str(fpath).startswith(str(STATIC)):
                mime = mimetypes.guess_type(str(fpath))[0] or "application/octet-stream"
                return self._serve_file(fpath, mime)
            return self._not_found()

        # ── Health check ──
        if path in ("/health", "/healthz"):
            return self._json(200, {"status": "ok"})

        # ── API ──
        if path == "/api/stats":
            return self._json(200, cortex.get_statistics())

        if path == "/api/documents":
            docs = cortex.graph.get_all_nodes()
            return self._json(200, self._sanitise_docs(docs))

        if path == "/api/search":
            q = qs.get("q", [""])[0]
            k = int(qs.get("k", ["10"])[0])
            if not q:
                return self._json(400, {"error": "Missing ?q= parameter"})
            results = cortex.search(q, top_k=k)
            return self._json(200, self._sanitise_docs(results))

        if path.startswith("/api/document/"):
            doc_id = path.split("/api/document/", 1)[1]
            doc = cortex.get_document(doc_id)
            if not doc:
                return self._json(404, {"error": "Document not found"})
            return self._json(200, self._sanitise_doc(doc))

        if path.startswith("/api/related/"):
            doc_id = path.split("/api/related/", 1)[1]
            related = cortex.get_related_documents(doc_id)
            return self._json(200, self._sanitise_docs(related))

        if path == "/api/graph":
            return self._json(200, self._build_graph())

        return self._not_found()

    # ────────────────────────────────────
    #  POST
    # ────────────────────────────────────
    def do_POST(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")

        if path == "/api/add-text":
            body = self._read_json()
            if body is None:
                return
            text = body.get("text", "").strip()
            if not text:
                return self._json(400, {"error": "text is required"})
            meta = {}
            if body.get("name"):
                meta["name"] = body["name"]
            discover = body.get("discover", True)
            try:
                doc_id = cortex.add_text(text, meta, discover_sources=discover)
                return self._json(201, {"id": doc_id})
            except Exception as exc:
                traceback.print_exc()
                return self._json(500, {"error": str(exc)})

        if path == "/api/add-file":
            return self._handle_file_upload()

        return self._not_found()

    # ────────────────────────────────────
    #  File upload (multipart)
    # ────────────────────────────────────
    def _handle_file_upload(self):
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            return self._json(400, {"error": "Expected multipart/form-data"})

        # Parse boundary
        boundary = None
        for part in content_type.split(";"):
            part = part.strip()
            if part.startswith("boundary="):
                boundary = part.split("=", 1)[1].strip('"')
        if not boundary:
            return self._json(400, {"error": "Missing boundary"})

        length = int(self.headers.get("Content-Length", 0))
        body   = self.rfile.read(length)

        # Very simple multipart parser – good enough for single-file uploads
        sep        = f"--{boundary}".encode()
        parts      = body.split(sep)
        file_data  = None
        file_name  = "upload.txt"
        discover   = True

        for part in parts:
            if b"Content-Disposition" not in part:
                continue
            header_end = part.find(b"\r\n\r\n")
            if header_end < 0:
                continue
            headers_raw = part[:header_end].decode(errors="replace")
            payload     = part[header_end + 4:].rstrip(b"\r\n--")

            if 'name="file"' in headers_raw:
                file_data = payload
                for h in headers_raw.split("\r\n"):
                    if "filename=" in h:
                        file_name = h.split("filename=")[1].strip('"').strip()
            elif 'name="discover"' in headers_raw:
                discover = payload.strip().lower() not in (b"false", b"0")

        if file_data is None:
            return self._json(400, {"error": "No file uploaded"})

        # Write to temp file so the ingestion pipeline can read it
        suffix = Path(file_name).suffix or ".txt"
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file_data)
                tmp_path = tmp.name
            doc_id = cortex.add_document(tmp_path, discover_sources=discover)
            # Patch the name to the original filename
            cortex.graph.update_node(doc_id, {"name": file_name})
            return self._json(201, {"id": doc_id})
        except Exception as exc:
            traceback.print_exc()
            return self._json(500, {"error": str(exc)})
        finally:
            if tmp_path:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

    # ────────────────────────────────────
    #  Graph builder (for the canvas viz)
    # ────────────────────────────────────
    def _build_graph(self):
        nodes = [
            {"id": n.get("id", ""), "name": n.get("name", ""), "category": n.get("category", "")}
            for n in cortex.graph.get_all_nodes()
        ]
        edges = [
            {"source": e["source"], "target": e["target"], "relationship": e.get("relationship", "")}
            for e in cortex.graph.edges
        ]
        return {"nodes": nodes, "edges": edges}

    # ────────────────────────────────────
    #  Helpers
    # ────────────────────────────────────
    @staticmethod
    def _sanitise_doc(d):
        """Return a JSON-safe copy of a document dict."""
        try:
            import numpy as np
            has_numpy = True
        except ImportError:
            has_numpy = False

        clean = {}
        for k, v in d.items():
            if isinstance(v, (str, int, float, bool, type(None))):
                clean[k] = v
            elif isinstance(v, (list, tuple)):
                clean[k] = [
                    str(x) if not isinstance(x, (str, int, float, bool, type(None))) else x
                    for x in v
                ]
            elif isinstance(v, dict):
                clean[k] = {str(kk): str(vv) for kk, vv in v.items()}
            elif has_numpy and isinstance(v, np.ndarray):
                continue  # skip embeddings
            else:
                clean[k] = str(v)
        return clean

    @classmethod
    def _sanitise_docs(cls, docs):
        return [cls._sanitise_doc(d) for d in docs]

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(length))
        except Exception:
            self._json(400, {"error": "Invalid JSON body"})
            return None

    def _json(self, status, payload):
        data = json.dumps(payload, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _serve_file(self, fpath, mime):
        try:
            data = fpath.read_bytes()
        except FileNotFoundError:
            return self._not_found()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "public, max-age=3600")
        self.end_headers()
        self.wfile.write(data)

    def _not_found(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Not found")


# ══════════════════════════════════════════════════
#  Entrypoint
# ══════════════════════════════════════════════════

def main():
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"🧠 Cortex KB running on http://0.0.0.0:{port}")
    print(f"   Data directory: {DATA_DIR}")
    server.serve_forever()


if __name__ == "__main__":
    main()
