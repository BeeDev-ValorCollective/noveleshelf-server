DELETE FROM notificationApp_notificationtype;
ALTER TABLE notificationApp_notificationtype AUTO_INCREMENT = 1;
INSERT INTO notificationApp_notificationtype 
    (code, label, description, recipient_type, sends_to_user, sends_to_admins, is_active, created_at) 
VALUES
    ('new_user_registered', 'New User Registered', 'Triggered when a new user registers on the platform', 'admin', 0, 1, 1, NOW()),
    ('free_author_upgrade', 'Free Author Upgrade', 'Triggered when a reader upgrades to free author', 'admin', 0, 1, 1, NOW()),
    ('new_author_request', 'New Author Request', 'Triggered when a user submits a paid author request', 'admin', 0, 1, 1, NOW()),
    ('author_request_approved', 'Author Request Approved', 'Triggered when an author request is approved', 'both', 1, 1, 1, NOW()),
    ('author_request_status_change', 'Author Request Status Change', 'Triggered when an author request status is updated', 'user', 1, 0, 1, NOW()),
    ('book_submitted_for_approval', 'Book Submitted for Approval', 'Triggered when a paid author submits a book for approval', 'admin', 0, 1, 1, NOW()),
    ('book_status_change', 'Book Status Change', 'Triggered when a book status changes eg approved or changes requested', 'user', 1, 0, 1, NOW()),
    ('flagged_content', 'Flagged Content', 'Triggered when a review or comment is flagged', 'admin', 0, 1, 1, NOW()),
    ('author_deactivated', 'Author Deactivated', 'Triggered when an author profile is deactivated', 'both', 1, 1, 1, NOW()),
    ('author_reactivated', 'Author Reactivated', 'Triggered when an author profile is reactivated', 'both', 1, 1, 1, NOW());