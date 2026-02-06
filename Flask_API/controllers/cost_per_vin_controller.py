from flask import Blueprint, request, jsonify
from psycopg2 import  sql as pgsql
from psycopg2.extras import RealDictCursor
from jwt_utils import jwt_required
from db_utils import get_connection
import os
from dotenv import load_dotenv
from uitils.db_query_utils import DBQueryUtils
from .query_controller import query_execution


load_dotenv()
DB_TABLE = DBQueryUtils.DB_TABLE or os.getenv("DB_TABLE", "warranty_claims")
DB_QUERY_LIMIT = DBQueryUtils.DB_QUERY_LIMIT or os.getenv("DB_QUERY_LIMIT", 1000)

cost_per_vin = Blueprint("cost_per_vin", __name__, url_prefix="/kpi")

@cost_per_vin.route("/cost/vin", methods=["GET"])
# @jwt_required
def city():
    """ Query weather data for a specific city with an optional limit.
        http://localhost:5000/db_warranty_claims/cost/vin?limit=1000
    """
    print("DB_TABLE:", DB_TABLE)
    print("DB_QUERY_LIMIT:", DB_QUERY_LIMIT)
    limit = request.args.get("limit", type=int) or DB_QUERY_LIMIT 
    sql = pgsql.SQL("""
                    SELECT 
                    dealer_code, 
                    dealer_address,
                    DATE_TRUNC('month', TO_DATE(repair_date, 'DD-MM-YYYY')) AS month,
                    model_series,
                    service_type,
                    SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) AS total_cost_sum,
                    ROUND(SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) / NULLIF(COUNT(DISTINCT fin), 0), 2) AS cost_per_vin
                    FROM {}
                    GROUP BY dealer_code, dealer_address, month, model_series, service_type
                    ORDER BY dealer_code, month
                    LIMIT %s""").format(pgsql.Identifier(DB_TABLE))              
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
    print("DB_TABLE:", DB_TABLE)
    print("DB_QUERY_LIMIT:", DB_QUERY_LIMIT)
    limit = request.args.get("limit", type=int) or DB_QUERY_LIMIT 
    sql = pgsql.SQL("""
                        SELECT 
                        DATE_TRUNC('week', TO_DATE(repair_date, 'DD-MM-YYYY'))::DATE AS week_start,
                        DATE_TRUNC('week', TO_DATE(repair_date, 'DD-MM-YYYY'))::DATE + 6 AS week_end,
                        dealer_code, 
                        model_series,
                        service_type,
                        COUNT(DISTINCT fin) AS unique_vins,
                        SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) AS total_cost_sum,
                        ROUND(SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) / NULLIF(COUNT(DISTINCT fin), 0), 2) AS cost_per_vin
                        FROM {}
                        --WHERE dealer_code='81901'
                        GROUP BY week_start, week_end, dealer_code, model_series, service_type
                        ORDER BY week_start ASC, dealer_code
                        LIMIT %s""").format(pgsql.Identifier(DB_TABLE))              
    # sql = pgsql.SQL("""SELECT * 
    #                    FROM {} 
    #                    LIMIT %s""").format(pgsql.Identifier(DB_TABLE))
    result = query_execution(DB_TABLE,limit,sql)
    return result

    