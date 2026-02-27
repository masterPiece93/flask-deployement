from flask import (
    render_template,
    request,
    jsonify,
    Blueprint,
    current_app
)
from markupsafe import escape

__module__ = 'misc'

misc_bp = Blueprint(
    __module__,
    f"{__name__}.{__module__}"
)

@misc_bp.route('/site-map')
def site_map():
    output = []
    for rule in current_app.url_map.iter_rules():
        # You may want to filter out rules that are not meant to be browsable,
        # such as the 'static' route, or those requiring parameters you can't provide.
        methods = ','.join(rule.methods)
        line = f"Endpoint: {rule.endpoint} | Methods: {methods} | Rule: {escape(rule.rule)}"
        output.append(line)
    
    # Return as a simple HTML list or formatted string
    return "<br/>".join(sorted(output))
