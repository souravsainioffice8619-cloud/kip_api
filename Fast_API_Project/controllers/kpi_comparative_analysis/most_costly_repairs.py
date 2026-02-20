from fastapi import APIRouter, Query, Request
from psycopg2 import sql as pgsql

from controllers.query_controller import query_execution
from uitils.db_query_utils import DBQueryUtils

DB_TABLE = DBQueryUtils.DB_TABLE

most_costly_repairs_router = APIRouter(prefix="/kpi")


@most_costly_repairs_router.get("/most_costly_repairs")
def get_most_costly_repairs(request: Request, limit: int | None = Query(default=5)):
    """Top most costly repair types."""
    limit_value = DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS or limit or 5
    sql = pgsql.SQL(
        """
        SELECT
            damage_code,
            issue,
            COUNT(DISTINCT fin) AS unique_vins,
            SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) AS total_repair_cost
        FROM {}
        GROUP BY 1, 2
        ORDER BY total_repair_cost DESC
        LIMIT %s
        """
    ).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit_value, sql, request.url.path)
