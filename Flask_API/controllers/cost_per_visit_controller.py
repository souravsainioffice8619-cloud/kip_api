from flask import Blueprint, request, jsonify
from psycopg2 import  sql as pgsql
from psycopg2.extras import RealDictCursor
from jwt_utils import jwt_required
from uitils.db_query_utils import DBQueryUtils
from .query_controller import query_execution

DB_TABLE = DBQueryUtils.DB_TABLE 
DB_QUERY_LIMIT = DBQueryUtils.DB_QUERY_LIMIT 

cost_per_visit = Blueprint("cost_per_visit", __name__, url_prefix="/kpi")

@cost_per_visit.route("/cost/visit", methods=["GET"])
# @jwt_required
def city():
    """ Query weather data for a specific city with an optional limit.
        http://localhost:5000/db_warranty_claims/cost/vist?limit=1000
    """
    print("DB_TABLE:", DB_TABLE)
    print("DB_QUERY_LIMIT:", DB_QUERY_LIMIT)
    # city = request.args.get("city")
    limit = request.args.get("limit", type=int) or DB_QUERY_LIMIT   
    # sql = pgsql.SQL("SELECT * FROM {} WHERE city = %s LIMIT %s").format(pgsql.Identifier(table))
    sql = pgsql.SQL("""
                     SELECT 
                    dealer_code, 
                    dealer_address,
                    DATE_TRUNC('month', TO_DATE(repair_date, 'DD-MM-YYYY')) AS month,
                    model_series,
                    service_type,
                    repair_date, -- Included to define the specific visit
                    SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) AS total_cost_sum,
                    ROUND(SUM(CAST(REPLACE(total_cost, ',', '') AS DECIMAL)) / NULLIF(COUNT(DISTINCT fin || repair_date), 0), 2) AS cost_per_visit
                    FROM {}
                    GROUP BY dealer_code, dealer_address, month, model_series, service_type, repair_date
                    ORDER BY dealer_code, month
                    LIMIT %s""").format(pgsql.Identifier(DB_TABLE))    # params = [city, limit]
    return query_execution(DB_TABLE,limit,sql)
         

