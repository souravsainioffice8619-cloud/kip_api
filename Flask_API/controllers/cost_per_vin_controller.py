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
    """ Get overall KPI data with configurable period and region filters.
        http://localhost:5000/kpi/cost/vin/overall?period=last_3_months&region=North&limit=1000
    """
    # Get parameters from request
    period = request.args.get("period", default="all_time").lower()
    region = request.args.get("region", default="all").lower()
    limit = request.args.get("limit", type=int) or DB_QUERY_LIMIT
    
    # Map period to query parameter names
    period_mapping = {
        "last_3_months": "last_3_months",
        "last_6_months": "last_6_months",
        "last_8_months": "last_8_months",
        "this_year": "this_year",
        "all_time": "all_time"
    }
    
    if period not in period_mapping:
        return {"error": "Invalid period. Please choose from last_3_months, last_6_months, last_8_months, this_year, or All Time."}, 400
    
    period_param = period_mapping[period]
    
    # Validate region
    valid_regions = ['north', 'south', 'east', 'west', 'all']
    if region not in valid_regions:
        return {"error": "Invalid region. Please choose from North, South, East, West, or all."}, 400
    
    # Capitalize region for SQL (except 'all')
    region_param = region.capitalize() if region != 'all' else 'all'
    
    # Get the overall_kpi_query
    sql = get_kpi_query("overall_kpi")
    
    # Replace placeholders with actual values
    sql = sql.replace("give_period_name", period_param)
    sql = sql.replace("give_region_name", region_param)
    
    # Create SQL object
    sql = pgsql.SQL(sql)
    
    result = query_execution(DB_TABLE, limit, sql)
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

    