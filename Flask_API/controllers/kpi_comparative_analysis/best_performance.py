from flask import Blueprint, request
from psycopg2 import sql as pgsql
from jwt_utils import jwt_required
from uitils.db_query_utils import DBQueryUtils
from controllers.query_controller import query_execution
from uitils.kpi_query_utils import get_kpi_query

DB_TABLE = DBQueryUtils.DB_NAME  

best_performance = Blueprint("best_performance", __name__, url_prefix="/kpi")

@best_performance.route("/best_performance", methods=["GET"])
# @jwt_required
def get_best_performance():
    """
    Retrieves the dealers with the best performance based on cost per VIN.
    """
    limit = DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS or request.args.get("limit", default=5, type=int)
    sql = pgsql.SQL(get_kpi_query("best_performance")).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit, sql)


@best_performance.route("/model_vs_issue_analysis/highest", methods=["GET"])
# @jwt_required
def model_vs_issue_analysis():
    """
    Retrieves the model vs issue analysis based on warranty data.
    """
    limit = request.args.get("limit", default=5, type=int) or DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS 
    sql = pgsql.SQL(get_kpi_query("model_vs_issue_analysis")).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit, sql)


@best_performance.route("/model_vs_issue_analysis/lowest", methods=["GET"])
# @jwt_required
def model_vs_issue_analysis_lowest():
    """
    Retrieves the model vs issue analysis based on warranty data.
    """
    limit = request.args.get("limit", default=5, type=int) or DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS 
    sql_query = get_kpi_query("model_vs_issue_analysis").replace("DESC", "ASC")
    sql = pgsql.SQL(sql_query).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit, sql)