from flask import Blueprint, request
from psycopg2 import sql as pgsql
from jwt_utils import jwt_required
from uitils.db_query_utils import DBQueryUtils
from controllers.query_controller import query_execution
from uitils.kpi_query_utils import get_kpi_query

DB_TABLE = DBQueryUtils.DB_NAME  

least_frequent_repairs = Blueprint("least_frequent_repairs", __name__, url_prefix="/kpi")

@least_frequent_repairs.route("/least_frequent_repairs", methods=["GET"])
# @jwt_required
def get_least_frequent_repairs():
    """
    Top 5 least Frequent Repair Types
    """
    limit =DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS or  request.args.get("limit", default=5, type=int)
    sql = pgsql.SQL(get_kpi_query("least_frequent_repairs")).format(pgsql.Identifier(DB_TABLE))

    return query_execution(DB_TABLE, limit, sql)
