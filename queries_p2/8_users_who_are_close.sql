CREATE TEMPORARY TABLE close_activities AS
SELECT 
    A.activity_id AS activity_id_1,
    B.activity_id AS activity_id_2,
    ST_Distance_Sphere(point(A.lon, A.lat), point(B.lon, B.lat)) AS distance,
    TIMESTAMPDIFF(SECOND, A.date_time, B.date_time) as timediff
FROM TrackPoint AS A
JOIN TrackPoint AS B
ON
    ST_Distance_Sphere(point(A.lon, A.lat), point(B.lon, B.lat)) < 50 AND
    A.activity_id <> B.activity_id AND
    TIMESTAMPDIFF(SECOND, A.date_time, B.date_time) < 30
;

SELECT A.user_id, B.user_id, distance, timediff
FROM close_activities
JOIN Activity AS A ON A.activity_id = activity_id_1
JOIN Activity AS A ON B.activity_id = activity_id_2;