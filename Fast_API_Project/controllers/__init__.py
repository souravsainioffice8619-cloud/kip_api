from fastapi import FastAPI

from .auth_controller import auth_router
from .cost_per_damage_controller import cost_per_damage_router
from .cost_per_vin_controller import cost_per_vin_router
from .cost_per_visit_controller import cost_per_visit_router
from .damage_cost_per_vin_controller import damage_cost_per_vin_router
from .damages_per_vin_controller import damages_per_vin_router
from .db_controller import db_router
from .device_controller import device_router
from .hours_per_vin_controller import hours_per_vin_router
from .hrs_per_visit_controller import hrs_per_visit_router
from .info_controller import info_router
from .kpi_comparative_analysis.best_performance import best_performance_router
from .kpi_comparative_analysis.highest_warranty_issues_by_models import (
    highest_warranty_issues_by_models_router,
)
from .kpi_comparative_analysis.least_frequent_repairs import least_frequent_repairs_router
from .kpi_comparative_analysis.lowest_warranty_issues_by_models import (
    lowest_warranty_issues_by_models_router,
)
from .kpi_comparative_analysis.most_costly_repairs import most_costly_repairs_router
from .kpi_comparative_analysis.most_frequent_repairs import most_frequent_repairs_router
from .kpi_comparative_analysis.worst_performance import worst_performance_router
from .log_controller import log_router
from .main_controller import main_router


def register_routers(app: FastAPI) -> None:
    """Register all routers on the FastAPI app."""
    app.include_router(auth_router)
    app.include_router(device_router)
    app.include_router(main_router)
    app.include_router(db_router)
    app.include_router(cost_per_visit_router)
    app.include_router(cost_per_vin_router)
    app.include_router(damages_per_vin_router)
    app.include_router(cost_per_damage_router)
    app.include_router(hours_per_vin_router)
    app.include_router(hrs_per_visit_router)
    app.include_router(damage_cost_per_vin_router)
    app.include_router(log_router)
    app.include_router(best_performance_router)
    app.include_router(worst_performance_router)
    app.include_router(highest_warranty_issues_by_models_router)
    app.include_router(lowest_warranty_issues_by_models_router)
    app.include_router(most_frequent_repairs_router)
    app.include_router(least_frequent_repairs_router)
    app.include_router(most_costly_repairs_router)
    app.include_router(info_router)
