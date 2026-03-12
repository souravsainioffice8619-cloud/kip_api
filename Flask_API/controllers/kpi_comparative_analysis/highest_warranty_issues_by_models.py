from flask import Blueprint, request
from psycopg2 import sql as pgsql
from jwt_utils import jwt_required
from uitils.db_query_utils import DBQueryUtils
from controllers.query_controller import query_execution
from uitils.kpi_query_utils import get_kpi_query

DB_TABLE = DBQueryUtils.DB_NAME  

highest_warranty_issues_by_models = Blueprint("highest_warranty_issues_by_models", __name__, url_prefix="/kpi")

@highest_warranty_issues_by_models.route("/highest_warranty_issues_by_models", methods=["GET"])
# @jwt_required
def get_highest_warranty_issues_by_models():
    """
    Retrieves the models with the highest number of warranty claims.
    """
    limit = DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS or  request.args.get("limit", default=25, type=int)
    sql = pgsql.SQL(get_kpi_query("highest_warranty_issues_by_models")).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit, sql)

@highest_warranty_issues_by_models.route("/region_wise_dealers", methods=["GET"])
# @jwt_required
def get_region_wise_dealers():
    """
    Retrieves dealers in a specific region.
    """
    region = request.args.get("region", default=None, type=str)
    if region is None:
        return {"error": "Region parameter is required."}, 400
    if region not in ['North', 'South', 'East', 'West', 'all']:
        return {"error": "Invalid region. Please choose from North, South, East, or West."}, 400
    region_wise_dealers_query = get_kpi_query("region_wise_dealers")
    match region:
        case 'North':
            region_wise_dealers_query = region_wise_dealers_query.replace("given_region_name", "'North'")
        case 'South':
            region_wise_dealers_query = region_wise_dealers_query.replace("given_region_name", "'South'")
        case 'East':
            region_wise_dealers_query = region_wise_dealers_query.replace("given_region_name", "'East'")
        case 'West':
            region_wise_dealers_query = region_wise_dealers_query.replace("given_region_name", "'West'")
        case  'all' :
            region_wise_dealers_query = region_wise_dealers_query.replace("WHERE region = given_region_name", " ")
    if request.args.get("limit") in ('All', 'all', 'ALL'):
        region_wise_dealers_query = region_wise_dealers_query.replace("LIMIT %s", " ")
        limit = 5
    else:
        limit = request.args.get("limit", default=5, type=int) or DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS

    sql = pgsql.SQL(region_wise_dealers_query)
    return query_execution(region, limit, sql)

@highest_warranty_issues_by_models.route("/models_wise_query", methods=["GET"])
# @jwt_required
def get_models_wise_query():
    """
    Retrieves the models with the highest number of warranty claims.
    """
    limit = request.args.get("limit", default=25, type=int) or DBQueryUtils.DB_QUERY_LIMIT_FOR_COMPARATIVE_ANALYSIS  
    sql = pgsql.SQL(get_kpi_query("models_wise_query")).format(pgsql.Identifier(DB_TABLE))
    return query_execution(DB_TABLE, limit, sql)