from fastapi import APIRouter, Depends, Query, Request
from psycopg2 import sql as pgsql

from controllers.query_controller import query_execution
from jwt_utils import jwt_required
from uitils.db_query_utils import DBQueryUtils

DB_TABLE = DBQueryUtils.DB_TABLE

best_performance_router = APIRouter(prefix="/kpi")


@best_performance_router.get("/best_performance")
def get_best_performance(
    request: Request,
    limit: int | None = Query(default=5),
    _: dict = Depends(jwt_required),
):
    """Retrieve dealers with the best performance based on cost per VIN."""
    limit_value = DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS or limit or 5
    sql = pgsql.SQL(
        """
        SELECT
            dealer_code,
            dealer_address,
            COUNT(DISTINCT fin) AS unique_vins,
            SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) AS total_cost_sum,
            ROUND(
                SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL))
                / NULLIF(COUNT(DISTINCT fin), 0),
                2
            ) AS cost_per_vin
        FROM {}
        GROUP BY 1, 2
        HAVING COUNT(DISTINCT fin) > 5
        ORDER BY cost_per_vin ASC
        LIMIT %s
        """
    ).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit_value, sql, request.url.path)
