-- userApp_user changes
ALTER TABLE userApp_user ADD COLUMN is_verified TINYINT(1) NOT NULL DEFAULT 0;
ALTER TABLE userApp_user ADD COLUMN verification_grace_ends datetime(6) NULL;

-- Set existing users as verified before verification system goes live
UPDATE userApp_user SET is_verified = 1 WHERE is_verified = 0;

-- userApp_authorprofile changes
ALTER TABLE userApp_authorprofile ADD COLUMN is_active TINYINT(1) NOT NULL DEFAULT 1;