
create schema mng;
create schema mrr;
create schema stg;
create schema dwh;
create schema mrr_test;
create schema stg_test;
create schema dwh_test;



drop table if exists dwh.dim_tracked_crypto_projects;
create table if not exists dwh.dim_tracked_crypto_projects (
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


delete from mng.environment_queries where query_id in (1,2,3);



INSERT INTO dwh_test.dim_tracked_crypto_projects (currency_id,currency_name,currency_symbol,allowed_change_percentage, inserted_date,last_update_date) VALUES
(1,'Bitcoin','BTC',3.5,'2020-02-15 00:00:00.000','2020-02-15 00:00:00.000')
,(328,'Monero','XMR',4,'2020-02-15 00:00:00.000','2020-02-15 00:00:00.000')
,(1214,'Lisk','LSK',5,'2020-02-15 00:00:00.000','2020-02-15 00:00:00.000')
,(1376,'Neo','NEO',6,'2020-02-15 00:00:00.000','2020-02-15 00:00:00.000')
,(1455,'Golem','GNT',16,'2020-02-15 00:00:00.000','2020-02-15 00:00:00.000')
,(1765,'EOS','EOS',10,'2020-02-15 00:00:00.000','2020-02-15 00:00:00.000')
,(1958,'TRON','TRX',6,'2020-02-15 00:00:00.000','2020-02-15 00:00:00.000')
,(2099,'ICON','ICX',7,'2020-02-15 00:00:00.000','2020-02-15 00:00:00.000')