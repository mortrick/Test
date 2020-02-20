insert into dwh.agg_track_percentage_change
select  distinct
		rd.currency_id,
		rd.currency_name,
		rd.symbol,
		rd.percent_change_1h,
		current_date,
		current_date,
		1 as is_active
from
	mrr.fact_30_min_raw_data rd
inner join -- Filter last execution
		(
			select
				currency_id,
				max(run_id) as max_run_id
			from
				mrr.fact_30_min_raw_data rd
			where
			 rd.conversion_id = 2 and rd.currency_id != 1
		group by
		1
		) le
	on
		rd.currency_id = le.currency_id and
		rd.run_id = le.max_run_id
inner join
	dwh.dim_user_preferance  tcp
	on
		rd.currency_id = tcp.coin_id and abs(rd.percent_change_1h) >= tcp.track_limit
where rd.conversion_id = 2 and rd.currency_id != 1
union all -- -------------------------------------------------------
select
		rd.currency_id,
		rd.currency_name,
		rd.symbol,
		rd.percent_change_1h,
		current_date,
		current_date,
		1 as is_active
from
	mrr.fact_30_min_raw_data rd
inner join -- Filter last execution
		(
			select
				currency_id,
				max(rd.run_id) as max_run_id
			from
				mrr.fact_30_min_raw_data rd
			where
				rd.conversion_id = 1 and rd.currency_id = 1
			group by
					1
		) le
	on
		rd.currency_id = le.currency_id and
		rd.run_id = le.max_run_id
inner join
	dwh_.dim_user_preferance  tcp
on
	rd.currency_id = tcp.coin_id and abs(rd.percent_change_1h) >= tcp.track_limit
where
	rd.conversion_id = 1
	and rd.currency_id = 1
;