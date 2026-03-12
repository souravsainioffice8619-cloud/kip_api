monthly_kpi_query = """SELECT 
                    DATE_TRUNC('month', repair_date) AS month_start,

                    -- Month Name + Year (Example: December 2012)
                    TO_CHAR(DATE_TRUNC('month', repair_date), 'Month YYYY') AS month_name,

                    -- Base Metrics
                    COUNT(DISTINCT fin) AS unique_vehicles,
                    COUNT(DISTINCT ext_vega_claim_no) AS total_claims,
                    SUM(total_cost) AS total_cost,
                    SUM(op_time) AS total_hours,
                    COUNT(damage_code) AS total_damages,

                    -- KPI Calculations
                    ROUND(SUM(total_cost) / COUNT(DISTINCT fin), 2) AS cost_per_vehicle,
                    ROUND(SUM(total_cost) / COUNT(DISTINCT ext_vega_claim_no), 2) AS cost_per_visit,
                    ROUND(SUM(op_time) / COUNT(DISTINCT fin), 2) AS hours_per_vehicle,
                    ROUND(COUNT(damage_code)::numeric / COUNT(DISTINCT fin), 2) AS damages_per_vehicle,
                    ROUND(SUM(total_cost) / COUNT(DISTINCT fin), 2) AS damage_cost_per_vehicle

                FROM warranty_enriched
                WHERE repair_date BETWEEN DATE '2012-12-01' AND DATE '2013-07-31'
                GROUP BY month_start
                ORDER BY month_start
                LIMIT %s
"""

overall_kpi_query = """
                            WITH params AS (
                                SELECT
                                    'give_period_name'::text AS period,
                                    'give_region_name'::text AS region_filter
                            ),
                            filtered_data AS (
                                SELECT w.*
                                FROM warranty_enriched w
                                CROSS JOIN params p
                                WHERE
                                    -- Period Filter
                                    (
                                        p.period = 'all_time'
                                        OR (p.period = 'last_3_months' AND w.repair_date >= DATE '2013-07-31' - INTERVAL '3 months')
                                        OR (p.period = 'last_6_months' AND w.repair_date >= DATE '2013-07-31' - INTERVAL '6 months')
                                        OR (p.period = 'last_8_months' AND w.repair_date >= DATE '2013-07-31' - INTERVAL '8 months')
                                        OR (p.period = 'this_year'     AND EXTRACT(YEAR FROM w.repair_date) = 2013)
                                    )
                                    AND
                                    -- Region Filter
                                    (
                                        p.region_filter = 'all'
                                        OR LOWER(w.region) = LOWER(p.region_filter)
                                    )
                            )
                            SELECT
                                -- Base Metrics  (same names as old query)
                                COUNT(DISTINCT fin)                AS unique_vehicles,
                                COUNT(DISTINCT ext_vega_claim_no)  AS total_claims,
                                SUM(total_cost)                    AS total_cost,
                                SUM(op_time)                       AS total_hours,
                                COUNT(damage_code)                 AS total_damages,

                                -- KPIs
                                ROUND(SUM(total_cost)              / NULLIF(COUNT(DISTINCT fin), 0), 2)              AS cost_per_vehicle,
                                ROUND(SUM(total_cost)              / NULLIF(COUNT(DISTINCT ext_vega_claim_no), 0), 2) AS cost_per_visit,
                                ROUND(SUM(op_time)                 / NULLIF(COUNT(DISTINCT fin), 0), 2)              AS hours_per_vehicle,
                                ROUND(COUNT(damage_code)::numeric  / NULLIF(COUNT(DISTINCT fin), 0), 2)              AS damages_per_vehicle,
                                ROUND(SUM(parts_cost + labor_cost) / NULLIF(COUNT(DISTINCT fin), 0), 2)              AS damage_cost_per_vehicle

                            FROM filtered_data
"""
weekly_kpi_query = """WITH weekly_data AS (
                                                SELECT
                                                    FLOOR((repair_date - DATE '2012-12-01') / 7) + 1 AS week_number,

                                                    -- Week start and end dates
                                                    DATE '2012-12-01' + (FLOOR((repair_date - DATE '2012-12-01') / 7) * 7)::int AS week_start,
                                                    DATE '2012-12-01' + (FLOOR((repair_date - DATE '2012-12-01') / 7) * 7 + 6)::int AS week_end,

                                                    COUNT(DISTINCT fin)               AS unique_vehicles,
                                                    COUNT(DISTINCT ext_vega_claim_no) AS total_claims,
                                                    SUM(total_cost)                   AS total_cost,
                                                    SUM(op_time)                      AS total_hours,
                                                    COUNT(damage_code)                AS total_damages

                                                FROM warranty_enriched
                                                WHERE repair_date BETWEEN DATE '2012-12-01' AND DATE '2013-07-31'
                                                GROUP BY week_number, week_start, week_end
                                            )

                                            SELECT
                                                week_number,

                                                -- Format: "1 - 7 Dec 2012"
                                                TO_CHAR(week_start, 'DD')
                                                || ' - '
                                                || TO_CHAR(LEAST(week_end, DATE '2013-07-31'), 'DD Mon YYYY') AS week_label,

                                                week_start,
                                                week_end,

                                                unique_vehicles,
                                                total_claims,
                                                total_cost,
                                                total_hours,
                                                total_damages,

                                                -- KPI Calculations
                                                ROUND(total_cost / NULLIF(unique_vehicles, 0), 2)            AS cost_per_vehicle,
                                                ROUND(total_cost / NULLIF(total_claims, 0), 2)               AS cost_per_visit,
                                                ROUND(total_hours / NULLIF(unique_vehicles, 0), 2)           AS hours_per_vehicle,
                                                ROUND(total_damages::numeric / NULLIF(unique_vehicles, 0), 2) AS damages_per_vehicle,
                                                ROUND(total_cost / NULLIF(unique_vehicles, 0), 2)            AS damage_cost_per_vehicle

                                            FROM weekly_data
                                            ORDER BY week_number
                                            LIMIT %s"""
worst_dealers_query = """WITH dealer_kpi AS (
                                                SELECT
                                                    dealer_code,
                                                    dealer_name,
                                                    region,
                                                    COUNT(DISTINCT fin) AS vehicles,
                                                    SUM(total_cost) AS total_cost,
                                                    SUM(total_cost) / COUNT(DISTINCT fin) AS cost_per_vehicle
                                                FROM warranty_enriched
                                                GROUP BY dealer_code, dealer_name, region
                                                HAVING COUNT(DISTINCT fin) > 20
                                            )

                                            SELECT *
                                            FROM dealer_kpi
                                            ORDER BY cost_per_vehicle DESC
                                            LIMIT %s"""
best_dealers_query = """WITH dealer_kpi AS (
                                            SELECT
                                                dealer_code,
                                                dealer_name,
                                                region,
                                                COUNT(DISTINCT fin) AS vehicles,
                                                SUM(total_cost) AS total_cost,
                                                SUM(total_cost) / COUNT(DISTINCT fin) AS cost_per_vehicle
                                            FROM warranty_enriched
                                            GROUP BY dealer_code, dealer_name, region
                                            HAVING COUNT(DISTINCT fin) > 20
                                        )

                                        SELECT *
                                        FROM dealer_kpi
                                        ORDER BY cost_per_vehicle ASC
                                        LIMIT %s"""

region_wise_dealers_query = """WITH dealer_kpi AS (
                                            SELECT
                                                dealer_code,
                                                dealer_name,
                                                region,
                                                COUNT(DISTINCT fin) AS vehicles,
                                                COUNT(fin) AS Claims,
                                                SUM(total_cost) AS total_cost,
                                                SUM(total_cost) / COUNT(DISTINCT fin) AS cost_per_vehicle
                                            FROM warranty_enriched
                                            GROUP BY dealer_code, dealer_name, region
                                            HAVING COUNT(DISTINCT fin) > 20
                                        )

                                        SELECT *
                                        FROM dealer_kpi
                                        WHERE region = given_region_name
                                        ORDER BY cost_per_vehicle ASC
                                        LIMIT %s"""
models_wise_query = """     SELECT model_series,
                                                COUNT(DISTINCT fin) AS vehicles,
                                                COUNT(fin) AS Claims,
                                                SUM(total_cost) AS total_cost,
                                                SUM(total_cost) / COUNT(DISTINCT fin) AS cost_per_vehicle
                                            FROM warranty_enriched
                                            GROUP BY model_series
                                            HAVING COUNT(DISTINCT fin) > 20
                                        ORDER BY cost_per_vehicle ASC
                                        LIMIT %s"""
high_cost_per_vin_query =  """SELECT *
                FROM issue_kpi
                ORDER BY cost_per_vehicle DESC
                LIMIT %s"""

most_frequent_repairs = """SELECT *
                                FROM issue_kpi
                                ORDER BY frequency DESC
                                LIMIT %s"""
least_frequent_repairs = """SELECT *
                                FROM issue_kpi
                                ORDER BY frequency ASC
                                LIMIT %s"""
most_problematic_models  = """SELECT *
                FROM model_kpi
                ORDER BY cost_per_vehicle DESC
                LIMIT %s"""
least_problematic_models  = """SELECT *
                FROM model_kpi
                ORDER BY cost_per_vehicle ASC
                LIMIT %s"""

model_vs_issue_analysis ="""
                        SELECT
                                model_series,
                                issue,

                                COUNT(*) AS frequency,
                                -- Number of times this issue occurred for this model

                                SUM(total_cost) AS total_cost
                                -- Total warranty cost caused by this issue for this model

                                FROM warranty_enriched

                                WHERE issue IS NOT NULL AND total_cost > 0

                                GROUP BY model_series, issue

                                ORDER BY total_cost DESC 

                                Limit %s              
"""
kpi_queries = {
    "cost_per_damage": "SELECT * FROM warranty_enriched LIMIT %s",
    "overall_kpi": overall_kpi_query,
    "region_wise_dealers": region_wise_dealers_query,
    "models_wise_query": models_wise_query,
    "cost_per_vin": {'M' or 'm':monthly_kpi_query,
                    'W' or 'w':weekly_kpi_query},                    ''
    "cost_per_visit": {'M' or 'm': monthly_kpi_query,
                     'W' or 'w': weekly_kpi_query},
    "damage_cost_per_vin": {'M' or 'm': monthly_kpi_query,
                        'W' or 'w': weekly_kpi_query},
    "damages_per_vin": {'M' or 'm': monthly_kpi_query,
                        'W' or 'w': weekly_kpi_query},
    "hours_per_vin": {'M' or 'm': monthly_kpi_query,
                      'W' or 'w': weekly_kpi_query},
    "hrs_per_visit": {'M' or 'm': monthly_kpi_query,
                        'W' or 'w': weekly_kpi_query},
    'best_performance': best_dealers_query ,
    'highest_warranty_issues_by_models': most_problematic_models,
    "least_frequent_repairs": least_frequent_repairs,
    "lowest_warranty_issues_by_models": least_problematic_models,
    "most_costly_repairs": high_cost_per_vin_query,
    "most_frequent_repairs": most_frequent_repairs,
    "worst_performance": worst_dealers_query,
    "model_vs_issue_analysis":model_vs_issue_analysis
                            # Add more KPI queries as needed
}


def get_kpi_query(kpi_name):
    return kpi_queries.get(kpi_name, "KPI query not found")
