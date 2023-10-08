WITH transportation_count AS (SELECT
    user_id,
    transportation_mode,
    COUNT(transportation_mode) as number_used
FROM
    Activity
WHERE
    transportation_mode IS NOT NULL
GROUP BY
    user_id,
    transportation_mode
)

SELECT
    user_id,
    transportation_mode
FROM transportation_count
JOIN (
    SELECT 
        user_id,
        MAX(number_used) AS count
    FROM
        transportation_count
    GROUP BY
        user_id
) maximums ON maximums.user_id = user_id AND maximums.count = transportation_count.number_used