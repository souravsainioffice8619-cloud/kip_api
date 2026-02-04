from typing import Callable
from .auth_controller import auth_bp
from .device_controller import device_bp
from .main_controller import main_bp
from .db_controller import db_bp
from .cost_per_visit_controller import cost_per_visit
from .cost_per_vin_controller import cost_per_vin
from .damages_per_vin_controller import damages_per_vin
from .cost_per_damage_controller import cost_per_damage
from .hours_per_vin_controller import hours_per_vin
from .hrs_per_visit_controller import hrs_per_visit
from .damage_cost_per_vin_controller import damage_cost_per_vin
from .log_controller import log_bp


def register_blueprints(app) -> None:
    """Register all controller blueprints on the Flask app."""
    # Import here to avoid circular imports at package import time
    app.register_blueprint(auth_bp)
    app.register_blueprint(device_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(db_bp)
    app.register_blueprint(cost_per_visit)
    app.register_blueprint(cost_per_vin)
    app.register_blueprint(damages_per_vin)
    app.register_blueprint(cost_per_damage)
    app.register_blueprint(hours_per_vin)
    app.register_blueprint(hrs_per_visit)
    app.register_blueprint(damage_cost_per_vin)
    app.register_blueprint(log_bp)


    
