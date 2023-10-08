CREATE VIEW spanning_activities AS
SELECT
    activity_id,
    user_id,
    transportation_mode,
    TIMEDIFF(end_date_time, start_date_time) AS duration
FROM
    Activity
WHERE
    DATE(end_date_time) >= DATE_ADD(DATE(start_date_time), INTERVAL 1 DAY);

SELECT COUNT(DISTINCT(user_id)) as number_of_multiday_travelers FROM spanning_activities;
SELECT * FROM spanning_activities;