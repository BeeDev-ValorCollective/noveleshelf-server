-- ─── Content Ratings ──────────────────────────────────────────────────────────
INSERT INTO booksApp_contentrating (code, name, description, is_active, created_at)
VALUES
    ('G',  'General',    'Suitable for all audiences. No violence, romance, or mature themes.', 1, NOW()),
    ('YA', 'Young Adult','Mild violence, mild romance. Suitable for teen readers and above.', 1, NOW()),
    ('M',  'Mature',     'Strong language, violence, open-door romance, strong profanity, darker psychological themes. Suitable for adults.', 1, NOW()),
    ('E',  'Explicit',   'Graphic sexual content or violent material. Adults only.', 1, NOW()),
    ('X',  'Extreme',    'Intensely graphic, disturbing, or highly niche adult material that exceeds explicit content. Adults only.', 1, NOW())
ON DUPLICATE KEY UPDATE code=code;

-- ─── Genres ───────────────────────────────────────────────────────────────────
INSERT INTO booksApp_genre (name, is_active, created_at)
VALUES
    ('Romance/Romantasy', 1, NOW()),
    ('Fantasy',           1, NOW()),
    ('Paranormal',        1, NOW()),
    ('Thriller/Mystery',  1, NOW()),
    ('Sci-Fi',            1, NOW()),
    ('Horror',            1, NOW()),
    ('Contemporary',      1, NOW())
ON DUPLICATE KEY UPDATE name=name;

-- ─── Relationship Tags ────────────────────────────────────────────────────────
INSERT INTO booksApp_relationshiptag (code, name, is_active, created_at)
VALUES
    ('FM',   'Female/Male',   1, NOW()),
    ('MM',   'Male/Male',     1, NOW()),
    ('FF',   'Female/Female', 1, NOW()),
    ('POLY', 'Polyamorous',   1, NOW())
ON DUPLICATE KEY UPDATE code=code;

-- ─── Keywords ─────────────────────────────────────────────────────────────────
INSERT INTO booksApp_keyword (name, is_active, created_at)
VALUES
    ('Dragon',                    1, NOW()),
    ('Werewolf',                  1, NOW()),
    ('Vampire',                   1, NOW()),
    ('Demon/Devil',               1, NOW()),
    ('Fae',                       1, NOW()),
    ('Fairy',                     1, NOW()),
    ('Adventure',                 1, NOW()),
    ('Crime',                     1, NOW()),
    ('Superpower',                1, NOW()),
    ('Apocalypse/Post-Apocalypse',1, NOW()),
    ('Hero Journey',              1, NOW()),
    ('Quest',                     1, NOW()),
    ('Pirate',                    1, NOW()),
    ('Sweet Romance',             1, NOW()),
    ('Steamy Romance',            1, NOW()),
    ('Spicy Romance',             1, NOW()),
    ('Supernatural',              1, NOW())
ON DUPLICATE KEY UPDATE name=name;