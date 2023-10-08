WITH lagged_times AS (
    SELECT
        *,
        LAG(date_time) OVER (ORDER BY date_time ASC) AS prev_date_time
    FROM
        TrackPoint
)

SELECT
    DISTINCT(Activity.activity_id) AS activity_id
FROM
    lagged_times
NATURAL JOIN
    Activity
WHERE
    TIME_TO_SEC(TIMEDIFF(date_time, prev_date_time)) / 60 > 5 AND
    prev_date_time IS NOT NULL
GROUP BY
    activity_id