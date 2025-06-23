UPDATE public."domain" AS d
SET created_datetime = v.created_datetime
FROM strix.vvehicle AS v
WHERE d.id_thing = v.id
  AND d.created_datetime IS NULL
  AND v.created_datetime IS NOT NULL;