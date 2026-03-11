CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    jwt_token TEXT NOT NULL
);

INSERT INTO members (username, password, jwt_token)
VALUES
    ('erpnext_member1', '123456', 'erpnext_preissued_jwt_member1'),
    ('erpnext_member2', '123456', 'erpnext_preissued_jwt_member2'),
    ('erpnext_member3', '123456', 'erpnext_preissued_jwt_member3')
ON DUPLICATE KEY UPDATE
    password = VALUES(password),
    jwt_token = VALUES(jwt_token);
