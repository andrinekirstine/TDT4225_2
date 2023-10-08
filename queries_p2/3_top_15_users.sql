CREATE TEMPORARY TABLE totals AS
SELECT user_id, COUNT(*) AS total_trackpoints
FROM ( 
    SELECT Activity.user_id as user_id 
    FROM TrackPoint
    NATURAL JOIN Activity
) AS trackpoints
GROUP BY user_id;

SELECT * FROM totals
ORDER BY total_trackpoints DESC
LIMIT 15;