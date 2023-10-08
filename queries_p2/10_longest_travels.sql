WITH lagged_point AS (
    SELECT
        *,
        LAG(lat) OVER (ORDER BY date_time ASC) AS prev_lat,
        LAG(lon) OVER (ORDER BY date_time ASC) AS prev_lon
    FROM
        TrackPoint
)

SELECT
    Activity.user_id AS user_id,
    Activity.transportation_mode AS transportation_mode,
    Activity.activity_id AS activity_id,
    SUM(ST_Distance_Sphere(point(lon, lat), point(prev_lon, prev_lat))) as distance_traveled
FROM
    lagged_point
NATURAL JOIN
    Activity
GROUP BY activity_id


-- user_id activity_id     total_altitude_gain
-- 128     24259   48962746
-- 144     27017   29688079
-- 144     26999   17431103
-- 128     24051   16047570
-- 144     27077   14038170
-- 144     27011   13287188
-- 041     16688   10406046
-- 144     27018   8648833
-- 128     24247   8561424
-- 034     16133   8158600
-- 163     29593   7744370
-- 128     24185   7206752
-- 128     23941   7007988
-- 128     24245   5563561
-- 144     26973   5061053