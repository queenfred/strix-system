select * from strix.vvehicle where LTRIM(make) like '%TOYOTA%' and LTRIM(model) like '%COROLLA CROS%' and location_datetime is not null and  location_datetime > '2025-04-01 00:01:00.000 -0300' and created_datetime > '2025-01-01 00:01:00.000 -0300'


select * from strix.vvehicle where LTRIM(make) like '%CHEVROLET%' and LTRIM(model) like  ('%ONIX%') and location_datetime is not null and  location_datetime > '2025-04-01 00:01:00.000 -0300' and created_datetime > '2025-01-01 00:01:00.000 -0300'



SELECT *
FROM strix.vvehicle 
-- inner join public."domain" d on d.id_thing = strix.vvehicle.id
WHERE 
  (
    (LTRIM(make) ILIKE '%CHEVROLET%' AND (LTRIM(model) ILIKE '%ONIX%' ))
    OR
    (LTRIM(make) ILIKE '%TOYOTA%' AND LTRIM(model) ILIKE '%COROLLA CROS%')
  )
  AND location_datetime IS NOT NULL
  AND location_datetime > '2025-04-01 00:01:00.000 -03'
  AND strix.vvehicle.created_datetime > '2025-01-01 00:01:00.000 -03';