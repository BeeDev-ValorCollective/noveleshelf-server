-- ─── Founding Author Bonus Tiers ─────────────────────────────────────────────
INSERT INTO currencyApp_foundingauthorbonustier (percent)
VALUES
    (10.00),
    (5.00)
ON DUPLICATE KEY UPDATE percent=percent;

-- ─── Founding Author Durations ───────────────────────────────────────────────
INSERT INTO currencyApp_foundingauthorduration (label, book_count)
VALUES
    ('Lifetime - All Books', NULL),
    ('First 5 Books',        5),
    ('First 3 Books',        3)
ON DUPLICATE KEY UPDATE label=label;

-- ─── Founding Author Slots (1-40) ────────────────────────────────────────────
-- Slots 1-5:   10% bonus, Lifetime - All Books
-- Slots 6-10:  10% bonus, First 5 Books
-- Slots 11-20: 10% bonus, First 3 Books
-- Slots 21-30: 5%  bonus, First 5 Books
-- Slots 31-40: 5%  bonus, First 3 Books
--
-- bonus_tier_id / duration_id are looked up by value rather than hardcoded,
-- so this isn't dependent on auto-increment ID assignment order.

INSERT INTO currencyApp_foundingauthorslot (slot_number, bonus_tier_id, duration_id, created_at, updated_at)
SELECT r.slot_num,
       (SELECT id FROM currencyApp_foundingauthorbonustier WHERE percent = r.bonus_percent),
       (SELECT id FROM currencyApp_foundingauthorduration WHERE label = r.duration_label),
       NOW(),
       NOW()
FROM (
    SELECT 1  AS slot_num, 10.00 AS bonus_percent, 'Lifetime - All Books' AS duration_label UNION ALL
    SELECT 2,  10.00, 'Lifetime - All Books' UNION ALL
    SELECT 3,  10.00, 'Lifetime - All Books' UNION ALL
    SELECT 4,  10.00, 'Lifetime - All Books' UNION ALL
    SELECT 5,  10.00, 'Lifetime - All Books' UNION ALL
    SELECT 6,  10.00, 'First 5 Books' UNION ALL
    SELECT 7,  10.00, 'First 5 Books' UNION ALL
    SELECT 8,  10.00, 'First 5 Books' UNION ALL
    SELECT 9,  10.00, 'First 5 Books' UNION ALL
    SELECT 10, 10.00, 'First 5 Books' UNION ALL
    SELECT 11, 10.00, 'First 3 Books' UNION ALL
    SELECT 12, 10.00, 'First 3 Books' UNION ALL
    SELECT 13, 10.00, 'First 3 Books' UNION ALL
    SELECT 14, 10.00, 'First 3 Books' UNION ALL
    SELECT 15, 10.00, 'First 3 Books' UNION ALL
    SELECT 16, 10.00, 'First 3 Books' UNION ALL
    SELECT 17, 10.00, 'First 3 Books' UNION ALL
    SELECT 18, 10.00, 'First 3 Books' UNION ALL
    SELECT 19, 10.00, 'First 3 Books' UNION ALL
    SELECT 20, 10.00, 'First 3 Books' UNION ALL
    SELECT 21, 5.00,  'First 5 Books' UNION ALL
    SELECT 22, 5.00,  'First 5 Books' UNION ALL
    SELECT 23, 5.00,  'First 5 Books' UNION ALL
    SELECT 24, 5.00,  'First 5 Books' UNION ALL
    SELECT 25, 5.00,  'First 5 Books' UNION ALL
    SELECT 26, 5.00,  'First 5 Books' UNION ALL
    SELECT 27, 5.00,  'First 5 Books' UNION ALL
    SELECT 28, 5.00,  'First 5 Books' UNION ALL
    SELECT 29, 5.00,  'First 5 Books' UNION ALL
    SELECT 30, 5.00,  'First 5 Books' UNION ALL
    SELECT 31, 5.00,  'First 3 Books' UNION ALL
    SELECT 32, 5.00,  'First 3 Books' UNION ALL
    SELECT 33, 5.00,  'First 3 Books' UNION ALL
    SELECT 34, 5.00,  'First 3 Books' UNION ALL
    SELECT 35, 5.00,  'First 3 Books' UNION ALL
    SELECT 36, 5.00,  'First 3 Books' UNION ALL
    SELECT 37, 5.00,  'First 3 Books' UNION ALL
    SELECT 38, 5.00,  'First 3 Books' UNION ALL
    SELECT 39, 5.00,  'First 3 Books' UNION ALL
    SELECT 40, 5.00,  'First 3 Books'
) AS r
ON DUPLICATE KEY UPDATE slot_number=slot_number;