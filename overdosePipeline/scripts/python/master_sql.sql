WITH base AS (
    SELECT
        Year,
        `State Name`,
        Indicator,
        `Total Deaths` AS deaths
    FROM cleaned_vsrr_data
    WHERE `Total Deaths` IS NOT NULL
),


/* national totals */

national_totals AS (
    SELECT
        Year,
        MAX(CASE WHEN `State Name` = 'United States' THEN deaths END)
            AS national_all_drug_total
    FROM base
    GROUP BY Year
),


national_by_drug AS (
    SELECT
        Year,
        Indicator,
        MAX(CASE WHEN `State Name` = 'United States' THEN deaths END)
            AS national_drug_total
    FROM base
    GROUP BY Year, Indicator
),


national_yoy AS (
    SELECT
        Year,
        national_all_drug_total,
        LAG(national_all_drug_total)
            OVER (ORDER BY Year) AS prev_total,
        (national_all_drug_total - LAG(national_all_drug_total)
            OVER (ORDER BY Year)) AS yoy_change,
        CASE
            WHEN LAG(national_all_drug_total) OVER (ORDER BY Year) IS NULL THEN NULL
            ELSE ROUND(
                (national_all_drug_total - LAG(national_all_drug_total)
                    OVER (ORDER BY Year)) * 100.0
                / LAG(national_all_drug_total) OVER (ORDER BY Year),
            2)
        END AS yoy_pct
    FROM national_totals
),

national_ma AS (
    SELECT
        Year,
        national_all_drug_total,
        AVG(national_all_drug_total)
            OVER (ORDER BY Year ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
            AS ma_3yr,
        AVG(national_all_drug_total)
            OVER (ORDER BY Year ROWS BETWEEN 4 PRECEDING AND CURRENT ROW)
            AS ma_5yr
    FROM national_totals
),


/* state totals */

state_totals AS (
    SELECT
        Year,
        `State Name`,
        Indicator,
        SUM(deaths) AS total_deaths
    FROM base
    WHERE `State Name` <> 'United States'
    GROUP BY Year, `State Name`, Indicator
),

state_rank AS (
    SELECT
        Year,
        `State Name`,
        Indicator,
        total_deaths,
        ROW_NUMBER() OVER (
            PARTITION BY Year, Indicator
            ORDER BY total_deaths DESC
        ) AS rank_within_drug
    FROM state_totals
),


state_rank_flagged AS (
    SELECT
        *,
        CASE WHEN rank_within_drug <= 10 THEN 1 ELSE 0 END AS top10_flag
    FROM state_rank
),


/* final table totals */

final AS (
    SELECT
        st.Year,
        st.`State Name`,
        st.Indicator,

        st.total_deaths,
        sr.rank_within_drug,
        sr.top10_flag,

        n.national_all_drug_total,
        n.prev_total AS national_prev_year,
        n.yoy_change AS national_yoy_change,
        n.yoy_pct AS national_yoy_pct,

        nd.national_drug_total,

        ma.ma_3yr,
        ma.ma_5yr
    FROM state_totals st
    LEFT JOIN state_rank_flagged sr
        ON st.Year = sr.Year
        AND st.`State Name` = sr.`State Name`
        AND st.Indicator = sr.Indicator
    LEFT JOIN national_yoy n
        ON st.Year = n.Year
    LEFT JOIN national_by_drug nd
        ON st.Year = nd.Year
        AND st.Indicator = nd.Indicator
    LEFT JOIN national_ma ma
        ON st.Year = ma.Year
)


SELECT *
FROM final
ORDER BY Indicator, `State Name`, Year;
