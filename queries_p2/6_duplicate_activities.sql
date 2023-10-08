SELECT Activity.* FROM Activity 
NATURAL JOIN
    (SELECT
        user_id,
        start_date_time,
        end_date_time
    FROM
        Activity
    GROUP BY
        start_date_time,
        end_date_time,
        user_id
    HAVING
        (COUNT(start_date_time) > 1) AND
        (COUNT(end_date_time) > 1) AND
        (COUNT(user_id) > 1)) AS Dupes;