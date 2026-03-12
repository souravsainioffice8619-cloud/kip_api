from flask import Blueprint, request
from psycopg2 import sql as pgsql
from jwt_utils import jwt_required
from uitils.db_query_utils import DBQueryUtils
from controllers.query_controller import query_execution
from uitils.kpi_query_utils import get_kpi_query


DB_TABLE = DBQueryUtils.DB_NAME  

most_costly_repairs = Blueprint("most_costly_repairs", __name__, url_prefix="/kpi")

@most_costly_repairs.route("/most_costly_repairs", methods=["GET"])
# @jwt_required
def get_most_costly_repairs():
    """
    Top 5 Most Costly Repair Types
    """
    limit =  request.args.get("limit", default=5, type=int) or DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS  
    sql = pgsql.SQL(get_kpi_query("most_costly_repairs")).format(pgsql.Identifier(DB_TABLE))

    return query_execution(DB_TABLE, limit, sql)

@most_costly_repairs.route("/least_costly_repairs", methods=["GET"])
# @jwt_required
def get_least_costly_repairs():
    """
    Top 5 Least Costly Repair Types
    """
    limit =  request.args.get("limit", default=5, type=int) or DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS  
    sql_query = get_kpi_query("most_costly_repairs").replace("DESC", "ASC")
    sql = pgsql.SQL(sql_query).format(pgsql.Identifier(DB_TABLE))

    return query_execution(DB_TABLE, limit, sql)