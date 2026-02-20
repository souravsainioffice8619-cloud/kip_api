from fastapi import APIRouter, Query, Request
from psycopg2 import sql as pgsql

from uitils.db_query_utils import DBQueryUtils
from .query_controller import query_execution

DB_TABLE = DBQueryUtils.DB_TABLE
DB_QUERY_LIMIT = DBQueryUtils.DB_QUERY_LIMIT

cost_per_damage_router = APIRouter(prefix="/kpi")


@cost_per_damage_router.get("/cost/damage")
def city(request: Request, limit: int | None = Query(default=None)):
    limit_value = limit or DB_QUERY_LIMIT
    sql = pgsql.SQL("SELECT * FROM {} LIMIT %s").format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit_value, sql, request.url.path)
