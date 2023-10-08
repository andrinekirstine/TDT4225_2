CREATE TEMPORARY TABLE totals AS
SELECT user_id, COUNT(*) AS total
FROM ( 
    SELECT Activity.user_id as user_id 
    FROM TrackPoint
    NATURAL JOIN Activity
) AS trackpoints
GROUP BY user_id;

SELECT user_id, total AS minimum_trackpoints
FROM totals
ORDER BY total ASC
LIMIT 1;

SELECT user_id, total AS maximum_trackpoints
FROM totals
ORDER BY total DESC
LIMIT 1;

SELECT AVG(total) AS average_trackpoints_per_user
FROM totals;
DROP TABLE totals;