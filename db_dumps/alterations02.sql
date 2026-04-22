-- feature flags
ALTER TABLE userApp_authorprofile ADD COLUMN is_featured TINYINT(1) NOT NULL DEFAULT 0;
ALTER TABLE userApp_freeauthorprofile ADD COLUMN is_featured TINYINT(1) NOT NULL DEFAULT 0;