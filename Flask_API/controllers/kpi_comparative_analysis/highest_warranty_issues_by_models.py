from flask import Blueprint, request
from psycopg2 import sql as pgsql
from jwt_utils import jwt_required
from uitils.db_query_utils import DBQueryUtils
from controllers.query_controller import query_execution
from uitils.kpi_query_utils import get_kpi_query

DB_TABLE = DBQueryUtils.DB_NAME  

highest_warranty_issues_by_models = Blueprint("highest_warranty_issues_by_models", __name__, url_prefix="/kpi")

@highest_warranty_issues_by_models.route("/highest_warranty_issues_by_models", methods=["GET"])
@jwt_required
def get_highest_warranty_issues_by_models():
    """
    Retrieves the models with the highest number of warranty claims.
    """
    limit = DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS or  request.args.get("limit", default=5, type=int)
    sql = pgsql.SQL(get_kpi_query("highest_warranty_issues_by_models")).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit, sql)