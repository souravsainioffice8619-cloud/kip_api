from fastapi import APIRouter, Depends, Query, Request
from psycopg2 import sql as pgsql

from controllers.query_controller import query_execution
from jwt_utils import jwt_required
from uitils.db_query_utils import DBQueryUtils

DB_TABLE = DBQueryUtils.DB_TABLE

highest_warranty_issues_by_models_router = APIRouter(prefix="/kpi")


@highest_warranty_issues_by_models_router.get("/highest_warranty_issues_by_models")
def get_highest_warranty_issues_by_models(
    request: Request,
    limit: int | None = Query(default=5),
    _: dict = Depends(jwt_required),
):
    """Retrieve models with highest warranty claim counts."""
    limit_value = DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS or limit or 5
    sql = pgsql.SQL(
        """
        SELECT
            model_series,
            COUNT(*) AS total_claims,
            COUNT(DISTINCT fin) AS unique_vins,
            SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) AS total_cost,
            ROUND(
                SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL))
                / NULLIF(COUNT(DISTINCT fin), 0),
                2
            ) AS cost_per_vin
        FROM {}
        GROUP BY 1
        ORDER BY total_claims DESC
        LIMIT %s
        """
    ).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit_value, sql, request.url.path)
