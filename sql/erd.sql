
create schema mng;
create schema mrr;
create schema stg;
create schema dwh;

grant all privileges on schema mrr  to cryptoapi;
grant all privileges on schema stg  to cryptoapi;
grant all privileges on schema dwh  to cryptoapi;
grant all privileges on schema mng  to cryptoapi;
grant all privileges on table dwh.tracked_crypto_projects  to cryptoapi;
grant all privileges on table mrr.hourly_raw_data to cryptoapi;


drop table if exists dwh.tracked_crypto_projects;
create table if not exists dwh.tracked_crypto_projects (
currency_id int,
currency_name varchar(100),
currency_symbol varchar(6),
percent_change_1h float,
inserted_date timestamp,
last_update_date timestamp
)


create table mng.environment_queries
(
query_id int,
query_name varchar(150),
granularity varchar(200),
inserted_timestamp timestamp,
query_str varchar(3500)

)