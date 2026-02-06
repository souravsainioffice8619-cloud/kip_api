from flask import Blueprint, request
from psycopg2 import sql as pgsql
from jwt_utils import jwt_required
from uitils.db_query_utils import DBQueryUtils
from controllers.query_controller import query_execution

DB_TABLE = DB_TABLE = DBQueryUtils.DB_NAME  

worst_performance = Blueprint("worst_performance", __name__, url_prefix="/kpi")

@worst_performance.route("/worst_performance", methods=["GET"])
@jwt_required
def get_worst_performance():
    """
    Retrieves the dealers with the worst performance based on cost per VIN.
    """
    limit = DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS or request.args.get("limit", default=5, type=int)
    sql = pgsql.SQL("""
        SELECT 
            dealer_code, 
            dealer_address,
            COUNT(DISTINCT fin) AS unique_vins,
            SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) AS total_cost_sum,
            ROUND(SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) / NULLIF(COUNT(DISTINCT fin), 0), 2) AS cost_per_vin
        FROM {}
        GROUP BY 1, 2
        ORDER BY cost_per_vin DESC
        LIMIT %s
    """).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit, sql)