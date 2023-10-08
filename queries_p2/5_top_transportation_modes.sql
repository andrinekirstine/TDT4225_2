SELECT user_id, COUNT(DISTINCT(transportation_mode)) AS number_of_transportation_modes
FROM Activity
WHERE transportation_mode IS NOT NULL
GROUP BY user_id
ORDER BY number_of_transportation_modes DESC
LIMIT 10;