from flask import Blueprint, request
from psycopg2 import sql as pgsql
from jwt_utils import jwt_required
from uitils.db_query_utils import DBQueryUtils
from controllers.query_controller import query_execution

DB_TABLE = DBQueryUtils.DB_NAME 

lowest_warranty_issues_by_models = Blueprint("lowest_warranty_issues_by_models", __name__, url_prefix="/kpi")

@lowest_warranty_issues_by_models.route("/lowest_warranty_issues_by_models", methods=["GET"])
@jwt_required
def get_lowest_warranty_issues_by_models():
    """
    Retrieves the models with the lowest number of warranty claims.
    """
    limit =DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS or request.args.get("limit", default=5, type=int)
    sql = pgsql.SQL("""
        SELECT 
            model_series,
            COUNT(*) AS total_claims,
            COUNT(DISTINCT fin) AS unique_vins,
            SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) AS total_cost,
            ROUND(SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) / NULLIF(COUNT(DISTINCT fin), 0), 2) AS cost_per_vin
        FROM {}
        GROUP BY 1
        ORDER BY total_claims ASC
        LIMIT %s
    """).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit, sql)