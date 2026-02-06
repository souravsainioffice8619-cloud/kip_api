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
from .kpi_comparative_analysis.best_performance import best_performance
from .kpi_comparative_analysis.worst_performance import worst_performance
from .kpi_comparative_analysis.highest_warranty_issues_by_models import highest_warranty_issues_by_models
from .kpi_comparative_analysis.lowest_warranty_issues_by_models import lowest_warranty_issues_by_models
from .kpi_comparative_analysis.most_frequent_repairs import most_frequent_repairs
from .kpi_comparative_analysis.least_frequent_repairs import least_frequent_repairs
from .kpi_comparative_analysis.most_costly_repairs import most_costly_repairs

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
    app.register_blueprint(best_performance)
    app.register_blueprint(worst_performance)
    app.register_blueprint(highest_warranty_issues_by_models)
    app.register_blueprint(lowest_warranty_issues_by_models)
    app.register_blueprint(most_frequent_repairs)
    app.register_blueprint(least_frequent_repairs)
    app.register_blueprint(most_costly_repairs)


    
