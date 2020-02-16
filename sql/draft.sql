
--drop table mng.environment_queries;
--create table mng.environment_queries
--(
--query_id int,
--query_name varchar(150),
--granularity varchar(200),
--inserted_timestamp timestamp,
--query_str varchar(3500)
--
--)
--commit;

select * from mng.environment_queries;


delete from mng.environment_queries where query_id in (1,2);
insert into mng.environment_queries values
--(
--1,
--'3.5 percent last hour',
--'currency, hour',
--current_date,
--'
--insert into dwh.dim_track_3h_percentage_change 
--select  distinct
--		rd.currency_id,
--		rd.currency_name,
--		rd.symbol,
--		rd.percent_change_1h,
--		current_date,
--		current_date,
--		1 as is_active
--from 
--	mrr.hourly_raw_data rd 
--inner join -- Filter last execution
--		(
--			select  
--				currency_id,
--				max(last_updated_date) as last_updated_date
--			from
--				mrr.hourly_raw_data hrd
--			where
--			last_updated_date::date = current_date
--		group by
--		1
--		) le
--	on 
--		rd.currency_id = le.currency_id and 
--		rd.last_updated_date = le.last_updated_date
--inner join 
--	dwh.dim_tracked_crypto_projects  tcp 
--	on 
--		rd.currency_id = tcp.currency_id
--where rd.conversion_id = 2 and rd.currency_id != 1
--union all 
--(select
--		rd.currency_id,
--		rd.currency_name,
--		rd.symbol,
--		rd.percent_change_1h,
--		current_date,
--		current_date,
--		1 as is_active
--from
--	mrr.hourly_raw_data rd
--where
--	conversion_id = 1
--	and currency_id = 1
--	and last_updated_date = (select max(last_updated_date) from mrr.hourly_raw_data hrd2  where conversion_id =1 and currency_id = 1));
--commit;'
--),
--(
--2,
--'truncate hourly_percentage_table',
--'cmd',
--current_date,
--'truncate table dwh.dim_track_3h_percentage_change;'
--)
(
3,
'Check for value drop',
'currency, hour',
current_date,
'select
string_agg(concat(''The '' ,  currency_symbol,'' Is falling down   '', round(last_hour_change::decimal,2)::text ,''. ''),'' '')
from
	dwh.dim_track_3h_percentage_change tcp
where
	last_hour_change < -3.5
;'
)


commit;






select * from mrr.hourly_raw_data where conversion_id = 2 limit 100;
-- Dim Currencies 
-- Dim Daily Average7days 
-- Dim Daily Average 31 days 


--create user cryptoapi with password 'admin';



create schema dwh;

grant all privileges on table mrr.hourly_raw_data to cryptoapi;
grant all privileges on schema mng  to cryptoapi;
grant all privileges on schema dwh  to cryptoapi;


grant all privileges on table mrr.hourly_raw_data to cryptoapi;
grant all privileges on table mrr.hourly_raw_data to cryptoapi;
grant all privileges on table dwh.dim_tracked_crypto_projects  to cryptoapi;
grant all privileges on table  mng.environment_queries to cryptoapi;
grant all privileges on table dwh.dim_track_3h_percentage_change  to cryptoapi;
--truncate table mrr.hourly_raw_data; 

select count(1) from mrr.hourly_raw_data;


drop table if exists dwh.dim_tracked_crypto_projects;
create table if not exists dwh.dim_tracked_crypto_projects (
currency_id int,
currency_name varchar(100),
currency_symbol varchar(6),
inserted_date timestamp,
last_update_date timestamp,
is_active smallint
)

drop table if exists dwh.dim_track_3h_percentage_change;
create table if not exists dwh.dim_track_3h_percentage_change (
currency_id int,
currency_name varchar(100),
currency_symbol varchar(6),
last_hour_change float,
inserted_date timestamp,
last_update_date timestamp,
is_active smallint
)






select * from dwh.tracked_crypto_projects 


-- track list
truncate table  dwh.dim_track_3h_percentage_change;
--insert into dwh.dim_track_3h_percentage_change 
select  distinct
		rd.currency_id,
		rd.currency_name,
		rd.symbol,
		rd.percent_change_1h,
		current_date,
		current_date,
		1 as is_active
from 
	mrr.hourly_raw_data rd 
inner join -- Filter last execution
		(
			select  
				currency_id,
				max(last_updated_date) as last_updated_date
			from
				mrr.hourly_raw_data hrd
			where
			last_updated_date::date = current_date
		group by
		1
		) le
	on 
		rd.currency_id = le.currency_id and 
		rd.last_updated_date = le.last_updated_date
inner join 
	dwh.dim_tracked_crypto_projects  tcp 
	on 
		rd.currency_id = tcp.currency_id
where rd.conversion_id = 2 and currency_id != 1;
commit;

select * from mng.environment_queries eq ;
select * from dwh.dim_tracked_crypto_projects limit 100;
select * from mrr.hourly_raw_data ;
select * from mrr.hourly_raw_data rd limit 100;
select * from dwh.dim_track_3h_percentage_change ;


currency_id int,
currency_name varchar(100),
currency_symbol varchar(6),
inserted_date timestamp,
last_update_date timestamp,
is_active smallint

--insert into dwh.dim_tracked_crypto_projects
--select 
--	rd.currency_id ,
--	rd.currency_name ,
--	rd.symbol ,
--	current_timestamp,
--	current_timestamp,
--	1
--from 
--	mrr.hourly_raw_data rd
--inner join -- Filter last execution
--		(
--			select  
--				currency_id,
--				max(last_updated_date) as last_updated_date
--			from
--				mrr.hourly_raw_data hrd
--			where
--			last_updated_date::date = current_date
--		group by
--		1
--		) le
--	on 
--		rd.currency_id = le.currency_id and 
--		rd.last_updated_date = le.last_updated_date
--where symbol  in 
--('BTC', 'EOS', 'TRX', 'XMR', 'ICX','LSK', 'NEO', 'GNT')
--and conversion_id = 2





;

select
string_agg(concat('The ' ,  currency_symbol,' Is falling down   ', round(last_hour_change::decimal,2)::text ,'. '),' ')
from
	dwh.dim_track_3h_percentage_change tcp
where
	last_hour_change < -3.5
;




  



