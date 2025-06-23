SELECT  
  v.domain,
  date_trunc( 'month', ( substring(el.s3_key FROM '/signals/date=[0-9]{4}-[0-9]{2}/([0-9]{4}-[0-9]{2}-[0-9]{2})_' )::date ))::date AS month,
  v.created_datetime,
  array_agg( DISTINCT EXTRACT( 
      DAY FROM ( substring(el.s3_key FROM '/signals/date=[0-9]{4}-[0-9]{2}/([0-9]{4}-[0-9]{2}-[0-9]{2})_' )::date )
    )::int
    ORDER BY EXTRACT(
      DAY FROM ( substring(el.s3_key FROM '/signals/date=[0-9]{4}-[0-9]{2}/([0-9]{4}-[0-9]{2}-[0-9]{2})_' )::date )
    )::int 
  ) AS failed_days

FROM error_log AS el INNER JOIN public.domain AS v  ON substring(el.s3_key FROM '(mrn:thing:vehicle:[^/]+)') = v.id_thing
	WHERE  el.s3_key ~ 'mrn:thing:vehicle:'  AND el.s3_key ~ '/signals/date=[0-9]{4}-[0-9]{2}/[0-9]{4}-[0-9]{2}-[0-9]{2}_'

GROUP BY
  v.domain,
  date_trunc( 'month', ( substring(el.s3_key FROM '/signals/date=[0-9]{4}-[0-9]{2}/([0-9]{4}-[0-9]{2}-[0-9]{2})_' )::date ) )::date,
  v.created_datetime
ORDER by  v.domain,   month;