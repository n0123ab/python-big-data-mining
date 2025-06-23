-- 整合20024年到2024年之间的用户行为数据的总和
SELECT 
    SUM(CASE WHEN behavior_type = 'buy' THEN 1 ELSE 0 END) AS buy_count,
    SUM(CASE WHEN behavior_type = 'pv' THEN 1 ELSE 0 END) AS click_count,
    SUM(CASE WHEN behavior_type = 'cart' THEN 1 ELSE 0 END) AS cart_count
FROM userbehavior 
WHERE datestamp BETWEEN '2004-01-01' AND '2024-12-30';