from fastapi import APIRouter, Query, Request
from psycopg2 import sql as pgsql

from controllers.query_controller import query_execution
from uitils.db_query_utils import DBQueryUtils

DB_TABLE = DBQueryUtils.DB_TABLE

most_frequent_repairs_router = APIRouter(prefix="/kpi")


@most_frequent_repairs_router.get("/most_frequent_repairs")
def get_most_frequent_repairs(request: Request, limit: int | None = Query(default=5)):
    """Top most frequent repair types."""
    limit_value = DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS or limit or 5
    sql = pgsql.SQL(
        """
        SELECT
            damage_code,
            issue,
            COUNT(DISTINCT fin) AS unique_vins,
            COUNT(*) AS repair_count
        FROM {}
        GROUP BY 1, 2
        ORDER BY repair_count DESC
        LIMIT %s
        """
    ).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit_value, sql, request.url.path)
