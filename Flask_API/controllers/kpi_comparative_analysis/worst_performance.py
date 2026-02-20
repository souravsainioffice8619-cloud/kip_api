from flask import Blueprint, request
from psycopg2 import sql as pgsql
from jwt_utils import jwt_required
from uitils.db_query_utils import DBQueryUtils
from controllers.query_controller import query_execution
from uitils.kpi_query_utils import get_kpi_query

DB_TABLE = DB_TABLE = DBQueryUtils.DB_NAME  

worst_performance = Blueprint("worst_performance", __name__, url_prefix="/kpi")

@worst_performance.route("/worst_performance", methods=["GET"])
@jwt_required
def get_worst_performance():
    """
    Retrieves the dealers with the worst performance based on cost per VIN.
    """
    limit = DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS or request.args.get("limit", default=5, type=int)
    sql = pgsql.SQL(get_kpi_query("worst_performance")).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit, sql)