INSERT INTO roles (role_name, allowed_actions)
VALUES
('OWNER',   '["ALL"]'),
('MANAGER', '["VIEW_REPORTS","INVENTORY_EDIT","ALERTS_VIEW"]'),
('CASHIER', '["SALES_ONLY"]');


INSERT INTO users (username, password_hash, role_id)
VALUES
(
  'owner',
  '$2b$12$rLQ1Yb9YJUkiGals.NE5u.ICcxdQsvScBBO4vrB.mhhyNaB4kBCvS',
  (SELECT role_id FROM roles WHERE role_name='OWNER')
),
(
  'cashier',
  '$2b$12$J7ivPoHi2cuq5h66FG6huO8nV.uj0bxao3sMGfXWQ2ESvscEbPa/.',
  (SELECT role_id FROM roles WHERE role_name='CASHIER')
),
(
  'manager',
  '$2b$12$aNJa5633GSTM.iN2OtlF6u.J5.KcXZ2L0m7ZSNh1FbxTyDga.AFMO',
  (SELECT role_id FROM roles WHERE role_name='MANAGER')
);
