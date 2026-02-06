from flask import Blueprint, request
from psycopg2 import sql as pgsql
from jwt_utils import jwt_required
from uitils.db_query_utils import DBQueryUtils
from controllers.query_controller import query_execution

DB_TABLE = DB_TABLE = DBQueryUtils.DB_NAME  

most_frequent_repairs = Blueprint("most_frequent_repairs", __name__, url_prefix="/kpi")

@most_frequent_repairs.route("/most_frequent_repairs", methods=["GET"])
# @jwt_required
def get_most_frequent_repairs():
    """
    Top 5 Most Frequent Repairs
    """
    limit = DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS or request.args.get("limit", default=5, type=int)
    sql = pgsql.SQL("""
        SELECT
            damage_code,
            issue,
            COUNT(DISTINCT fin) AS unique_vins,
            COUNT(*) AS repair_count
        FROM {}
        GROUP BY 1, 2
        ORDER BY repair_count DESC
        LIMIT %s
    """).format(pgsql.Identifier(DB_TABLE))

    return query_execution(DB_TABLE, limit, sql)