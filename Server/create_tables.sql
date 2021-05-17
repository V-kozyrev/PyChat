CREATE TABLE public.users
(
    id bigint NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    user_login character varying(50) COLLATE pg_catalog."default" NOT NULL,
    user_password character varying(50) COLLATE pg_catalog."default" NOT NULL,
    user_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    online boolean,
    CONSTRAINT users_pkey PRIMARY KEY (id)
);
CREATE TABLE public.message_history
(
    id bigint NOT NULL DEFAULT nextval('message_history_id_seq'::regclass),
    sender_id integer NOT NULL,
    recipient_id integer NOT NULL,
    message character varying(1000) COLLATE pg_catalog."default" NOT NULL,
    "time" timestamp without time zone,
    CONSTRAINT historu_message_pkey PRIMARY KEY (id)
);