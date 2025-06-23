1) Script para reiniciar el conteo de las tablas autoincrementales

SELECT pg_get_serial_sequence('public.portfolio', 'id');
ALTER SEQUENCE public.wallet_id_seq RESTART WITH 1;