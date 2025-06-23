-- public."domain" definition

-- Drop table

-- DROP TABLE public."domain";

CREATE TABLE public."domain" (
	id serial4 NOT NULL,
	"domain" varchar(30) NOT NULL,
	id_thing varchar(100) NULL,
	id_account varchar(100) NULL,
	CONSTRAINT domain_pkey PRIMARY KEY (id)
);

CREATE TABLE public.error_log (
	id serial4 NOT NULL,
	"method" varchar(255) NOT NULL,
	error_type varchar(255) NOT NULL,
	message text NOT NULL,
	bucket varchar(255) NULL,
	s3_key text NULL,
	created_at timestamp DEFAULT now() NULL,
	CONSTRAINT error_log_pkey PRIMARY KEY (id)
);

CREATE TABLE public."event" (
	id bigserial NOT NULL,
	id_domain int4 NOT NULL,
	latitude float8 NOT NULL,
	speed float8 NOT NULL,
	"event" text NOT NULL,
	longitude float8 NOT NULL,
	"timestamp" int8 NOT NULL,
	odometer float8 NOT NULL,
	heading int4 NOT NULL,
	CONSTRAINT event_pkey PRIMARY KEY (id)
);

CREATE TABLE public.portfolio (
	id int4 DEFAULT nextval('wallet_id_seq'::regclass) NOT NULL,
	"name" varchar(30) NOT NULL,
	CONSTRAINT wallet_pkey PRIMARY KEY (id)
);



CREATE TABLE public.portfolio_domain (
	portfolio_id int4 NOT NULL,
	domain_id int4 NOT NULL,
	state bool NOT NULL,
	fecha_alta timestamp NOT NULL,
	fecha_baja timestamp NULL,
	CONSTRAINT wallet_domain_pkey PRIMARY KEY (portfolio_id, domain_id)
);


-- public.portfolio_domain foreign keys

ALTER TABLE public.portfolio_domain ADD CONSTRAINT wallet_domain_domain_id_fkey FOREIGN KEY (domain_id) REFERENCES public."domain"(id) ON DELETE CASCADE;
ALTER TABLE public.portfolio_domain ADD CONSTRAINT wallet_domain_wallet_id_fkey FOREIGN KEY (portfolio_id) REFERENCES public.portfolio(id) ON DELETE CASCADE;
