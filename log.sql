CREATE TABLE IF NOT EXISTS deed_20151030_clean_buyercount
  SELECT
    mail_address,
    mail_city,
    mail_state,
    owner_1_label_name,
    Count(*) N
  FROM
    deed_20151030_clean
  GROUP BY
    1, 2, 3;
