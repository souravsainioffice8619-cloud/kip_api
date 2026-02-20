from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

info_router = APIRouter()


@info_router.get("/routes.html")
def routes_html(request: Request):
    """Simple HTML view of registered routes."""
    rows = []
    for route in request.app.routes:
        path = getattr(route, "path", None)
        methods = getattr(route, "methods", None)
        name = getattr(route, "name", "")
        if not path or path == "/openapi.json":
            continue
        method_list = sorted([m for m in (methods or []) if m not in {"HEAD", "OPTIONS"}])
        rows.append((path, method_list, name))

    html = ["<h1>Registered Routes</h1>", "<ul>"]
    for path, method_list, name in sorted(rows):
        html.append(f"<li><b>{path}</b> - {method_list} - <code>{name}</code></li>")
    html.append("</ul>")
    return HTMLResponse("\n".join(html))
