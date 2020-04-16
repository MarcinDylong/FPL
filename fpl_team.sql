--
-- PostgreSQL database dump
--

-- Dumped from database version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: fantasy_pl_team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fantasy_pl_team (
    id smallint NOT NULL,
    name character varying(32) NOT NULL,
    short_name character varying(4) NOT NULL,
    "position" smallint NOT NULL,
    played smallint NOT NULL,
    win smallint NOT NULL,
    draw smallint NOT NULL,
    loss smallint NOT NULL,
    points smallint NOT NULL,
    form text,
    strength smallint NOT NULL,
    strength_overall_home smallint NOT NULL,
    strength_overall_away smallint NOT NULL,
    strength_attack_home smallint NOT NULL,
    strength_attack_away smallint NOT NULL,
    strength_defence_home smallint NOT NULL,
    strength_defence_away smallint NOT NULL
);


ALTER TABLE public.fantasy_pl_team OWNER TO postgres;

--
-- Data for Name: fantasy_pl_team; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fantasy_pl_team (id, name, short_name, "position", played, win, draw, loss, points, form, strength, strength_overall_home, strength_overall_away, strength_attack_home, strength_attack_away, strength_defence_home, strength_defence_away) FROM stdin;
17	Spurs	TOT	8	29	11	8	10	41	DLLWW	4	1180	1240	1100	1130	1200	1140
14	Norwich	NOR	20	29	5	6	18	21	LWLLD	2	980	1020	1030	1040	990	990
2	Aston Villa	AVL	19	28	7	4	17	25	LLLLW	2	1020	1050	970	980	1000	1040
3	Bournemouth	BOU	18	29	7	6	16	27	LDLLW	2	1020	1020	990	1030	1000	1050
18	Watford	WAT	17	29	6	9	14	27	LWLDL	3	1030	1140	1120	1120	1020	1150
19	West Ham	WHU	16	29	7	6	16	27	LWLLD	2	1040	1030	1000	1030	1030	1150
4	Brighton	BHA	15	29	6	11	12	29	DLDDD	2	1050	1010	1100	1100	1040	1030
16	Southampton	SOU	14	29	10	4	15	34	LLWLL	3	1150	1040	1080	1050	1110	1080
13	Newcastle	NEW	13	29	9	8	12	35	WDLLD	3	1090	1100	1030	1040	980	990
8	Everton	EVE	12	29	10	7	12	37	LDLWW	3	1100	1240	1100	1210	1170	1180
7	Crystal Palace	CRY	11	29	10	9	10	39	WWWLL	3	1130	1120	1080	1180	1040	1040
5	Burnley	BUR	10	29	11	6	12	39	DDWWD	3	1110	1180	1130	1070	970	1110
1	Arsenal	ARS	9	28	9	13	6	40	WWWDD	4	1180	1240	1170	1170	1150	1200
15	Sheffield Utd	SHU	7	28	11	10	7	43	WDWWL	3	1180	1200	1170	1180	1050	1110
20	Wolves	WOL	6	29	10	13	6	43	DWWDD	4	1230	1190	1180	1230	1200	1200
12	Man Utd	MUN	5	29	12	9	8	45	WDWWD	4	1220	1300	1260	1330	1180	1260
6	Chelsea	CHE	4	29	14	6	9	48	WDWLD	4	1220	1230	1240	1240	1220	1250
9	Leicester	LEI	3	29	16	5	8	53	WLLDD	3	1210	1160	1150	1080	1210	1100
11	Man City	MCI	2	28	18	3	7	57	LWWLW	5	1330	1340	1260	1270	1320	1320
10	Liverpool	LIV	1	29	27	1	1	82	WLWWW	5	1340	1350	1310	1320	1310	1330
\.


--
-- Name: fantasy_pl_team fantasy_pl_team_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fantasy_pl_team
    ADD CONSTRAINT fantasy_pl_team_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

