CREATE TABLE IF NOT EXISTS members (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    jwt_token TEXT NOT NULL
);

INSERT INTO members (username, password, jwt_token)
VALUES
    ('tryton_member1', '123456', 'tryton_preissued_jwt_member1'),
    ('tryton_member2', '123456', 'tryton_preissued_jwt_member2'),
    ('tryton_member3', '123456', 'tryton_preissued_jwt_member3')
ON CONFLICT (username) DO UPDATE SET
    password = EXCLUDED.password,
    jwt_token = EXCLUDED.jwt_token;
