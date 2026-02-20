from fastapi import APIRouter, Query, Request
from psycopg2 import sql as pgsql

from uitils.db_query_utils import DBQueryUtils
from .query_controller import query_execution

DB_TABLE = DBQueryUtils.DB_TABLE
DB_QUERY_LIMIT = DBQueryUtils.DB_QUERY_LIMIT

hrs_per_visit_router = APIRouter(prefix="/kpi")


@hrs_per_visit_router.get("/hours/visit")
def city(request: Request, limit: int | None = Query(default=None)):
    limit_value = limit or DB_QUERY_LIMIT
    sql = pgsql.SQL(
        """
        SELECT
            dealer_code,
            dealer_address,
            DATE_TRUNC('month', TO_DATE(repair_date, 'DD-MM-YYYY')) AS month,
            model_series,
            service_type,
            repair_date,
            SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) AS total_cost_sum,
            ROUND(
                SUM(CAST(REPLACE(op_time, ',', '') AS DECIMAL))
                / NULLIF(COUNT(DISTINCT fin || repair_date), 0),
                2
            ) AS hours_per_visit
        FROM {}
        GROUP BY dealer_code, dealer_address, month, model_series, service_type, repair_date
        ORDER BY dealer_code, month
        LIMIT %s
        """
    ).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit_value, sql, request.url.path)


@hrs_per_visit_router.get("/hours/visit/weekly")
def weekly(request: Request, limit: int | None = Query(default=None)):
    limit_value = limit or DB_QUERY_LIMIT
    sql = pgsql.SQL(
        """
        SELECT
            DATE_TRUNC('week', TO_DATE(repair_date, 'DD-MM-YYYY'))::DATE AS week_start,
            DATE_TRUNC('week', TO_DATE(repair_date, 'DD-MM-YYYY'))::DATE + 6 AS week_end,
            dealer_code,
            model_series,
            service_type,
            COUNT(DISTINCT fin) AS unique_vins,
            SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) AS total_cost_sum,
            ROUND(
                SUM(CAST(REPLACE(op_time, ',', '') AS DECIMAL))
                / NULLIF(COUNT(DISTINCT fin || repair_date), 0),
                2
            ) AS hours_per_visit
        FROM {}
        GROUP BY week_start, week_end, dealer_code, model_series, service_type
        ORDER BY week_start ASC, dealer_code
        LIMIT %s
        """
    ).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit_value, sql, request.url.path)
