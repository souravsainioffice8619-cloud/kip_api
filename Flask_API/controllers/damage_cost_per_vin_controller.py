from flask import Blueprint, request, jsonify
from psycopg2 import  sql as pgsql
from psycopg2.extras import RealDictCursor
from jwt_utils import jwt_required
from uitils.db_query_utils import DBQueryUtils
from .query_controller import query_execution
from uitils.kpi_query_utils import get_kpi_query

DB_TABLE = DBQueryUtils.DB_TABLE 
DB_QUERY_LIMIT = DBQueryUtils.DB_QUERY_LIMIT 

damage_cost_per_vin = Blueprint("damage_cost_per_vin", __name__, url_prefix="/kpi")

@damage_cost_per_vin.route("/damage_cost/vin", methods=["GET"])
# @jwt_required
def city():
    """ Query weather data for a specific city with an optional limit.
        http://localhost:5000/db_warranty_claims/cost/vist?limit=1000
    """
    # print("DB_TABLE:", DB_TABLE)
    # print("DB_QUERY_LIMIT:", DB_QUERY_LIMIT)
    # city = request.args.get("city")
    limit = request.args.get("limit", type=int) or DB_QUERY_LIMIT   
    # sql = pgsql.SQL("SELECT * FROM {} WHERE city = %s LIMIT %s").format(pgsql.Identifier(table))
    sql = pgsql.SQL(get_kpi_query("damage_cost_per_vin")['M']).format(pgsql.Identifier(DB_TABLE))    # params = [city, limit]
    return query_execution(DB_TABLE,limit,sql)
         
@damage_cost_per_vin.route("/damage_cost/vin/weekly", methods=["GET"])
# @jwt_required
def weekly():
    """ Query weather data for a specific city with an optional limit.
        http://localhost:5000/db_warranty_claims/cost/vist?limit=1000
    """
    # print("DB_TABLE:", DB_TABLE)
    # print("DB_QUERY_LIMIT:", DB_QUERY_LIMIT)
    # city = request.args.get("city")
    limit = request.args.get("limit", type=int) or DB_QUERY_LIMIT   
    # sql = pgsql.SQL("SELECT * FROM {} WHERE city = %s LIMIT %s").format(pgsql.Identifier(table))
    sql = pgsql.SQL(get_kpi_query("damage_cost_per_vin")['W']).format(pgsql.Identifier(DB_TABLE))    # params = [city, limit]
    return query_execution(DB_TABLE,limit,sql)
