WITH increasing_altitudes AS (
    SELECT
        activity_id,
        date_time,
        altitude,
        LAG(altitude) OVER (PARTITION BY activity_id ORDER BY date_time ASC) AS prev_altitude
    FROM
        TrackPoint
    WHERE
        activity_id between 14000 and 14500
)
SELECT
    user_id,
    Activity.activity_id,
    SUM(altitude_gains) AS total_altitude_gain
FROM (
    SELECT
        activity_id,
        (altitude - prev_altitude) * 0.3048 AS altitude_gains
    FROM
        increasing_altitudes
    WHERE
        altitude > prev_altitude AND
        altitude <> -777 AND
        prev_altitude <> -777 AND
        prev_altitude IS NOT NULL
) gains
JOIN
    Activity
GROUP BY
    activity_id
ORDER BY
    total_altitude_gain DESC
LIMIT 15;
