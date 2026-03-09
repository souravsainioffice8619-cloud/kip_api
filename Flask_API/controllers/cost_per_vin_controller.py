from flask import Blueprint, request, jsonify
from psycopg2 import  sql as pgsql
from psycopg2.extras import RealDictCursor
from jwt_utils import jwt_required
from db_utils import get_connection
import os
from dotenv import load_dotenv
from uitils.db_query_utils import DBQueryUtils
from .query_controller import query_execution
from uitils.kpi_query_utils import get_kpi_query


load_dotenv()
DB_TABLE = DBQueryUtils.DB_TABLE or os.getenv("DB_TABLE", "warranty_claims")
DB_QUERY_LIMIT = DBQueryUtils.DB_QUERY_LIMIT or os.getenv("DB_QUERY_LIMIT", 1000)

cost_per_vin = Blueprint("cost_per_vin", __name__, url_prefix="/kpi")

@cost_per_vin.route("/cost/vin/overall", methods=["GET"])
# @jwt_required
def city_overall():
    """ Query weather data for a specific city with an optional limit.
        http://localhost:5000/db_warranty_claims/cost/vin?limit=1000
    """
    # print("DB_TABLE:", DB_TABLE)
    # print("DB_QUERY_LIMIT:", DB_QUERY_LIMIT)
    limit = request.args.get("limit", type=int) or DB_QUERY_LIMIT 
    sql = pgsql.SQL(get_kpi_query("overall_kpi")).format(pgsql.Identifier(DB_TABLE))              
    # sql = pgsql.SQL("""SELECT * 
    #                    FROM {} 
    #                    LIMIT %s""").format(pgsql.Identifier(DB_TABLE))
    result = query_execution(DB_TABLE,limit,sql)
    return result

@cost_per_vin.route("/cost/vin", methods=["GET"])
# @jwt_required
def city():
    """ Query weather data for a specific city with an optional limit.
        http://localhost:5000/db_warranty_claims/cost/vin?limit=1000
    """
    # print("DB_TABLE:", DB_TABLE)
    # print("DB_QUERY_LIMIT:", DB_QUERY_LIMIT)
    limit = request.args.get("limit", type=int) or DB_QUERY_LIMIT 
    sql = pgsql.SQL(get_kpi_query("cost_per_vin")['M']).format(pgsql.Identifier(DB_TABLE))              
    # sql = pgsql.SQL("""SELECT * 
    #                    FROM {} 
    #                    LIMIT %s""").format(pgsql.Identifier(DB_TABLE))
    result = query_execution(DB_TABLE,limit,sql)
    return result

@cost_per_vin.route("/cost/vin/weekly", methods=["GET"])
# @jwt_required
def weekly():
    """ Query weather data for a specific city with an optional limit.
        http://localhost:5000/db_warranty_claims/cost/vin/weekly?limit=1000
    """
    # print("DB_TABLE:", DB_TABLE)
    # print("DB_QUERY_LIMIT:", DB_QUERY_LIMIT)
    limit = request.args.get("limit", type=int) or DB_QUERY_LIMIT 
    sql = pgsql.SQL(get_kpi_query("cost_per_vin")['W']).format(pgsql.Identifier(DB_TABLE))              
    # sql = pgsql.SQL("""SELECT * 
    #                    FROM {} 
    #                    LIMIT %s""").format(pgsql.Identifier(DB_TABLE))
    result = query_execution(DB_TABLE,limit,sql) 
    return result

    