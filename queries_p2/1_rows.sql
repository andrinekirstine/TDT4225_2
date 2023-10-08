SELECT 
    (SELECT COUNT(*) FROM User) AS rows_in_user,
    (SELECT COUNT(*) FROM Activity) AS rows_in_activity,
    (SELECT COUNT(*) FROM TrackPoint) AS rows_in_track_point;