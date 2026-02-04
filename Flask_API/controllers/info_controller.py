from flask import Blueprint, current_app

info_bp = Blueprint('info', __name__)


@info_bp.route('/routes.html')
def routes_html():
    """Simple HTML view of the registered routes."""
    routes = []
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint == 'static':
            continue
        methods = sorted([m for m in rule.methods if m not in ('HEAD', 'OPTIONS')])
        routes.append((str(rule), methods, rule.endpoint))
    html = ['<h1>Registered Routes</h1>', '<ul>']
    for r, methods, endpoint in sorted(routes):
        html.append(f'<li><b>{r}</b> — {methods} — <code>{endpoint}</code></li>')
    html.append('</ul>')
    return '\n'.join(html)
