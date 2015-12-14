CREATE TABLE IF NOT EXISTS [BUYER_COUNT_TABLE]
  SELECT
    mail_address,
    mail_city,
    mail_state,
    owner_1_label_name,
    Count(*) N
  FROM
    [DEED_CLEAN_TABLE]
  GROUP BY
    1, 2, 3;
