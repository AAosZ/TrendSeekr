--
-- PostgreSQL database dump
--

\restrict pRVcGc6vtmluFqgXFreNVB6dBVyhdsRLfoU3NDOyn9dlbgtsFgD76j02Pwfz2SY

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

-- Started on 2026-07-04 01:01:01

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;
CREATE EXTENSION IF NOT EXISTS vector SCHEMA public;

--
-- TOC entry 225 (class 1259 OID 16685)
-- Name: articles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    date TIMESTAMPTZ NOT NULL,
    url TEXT UNIQUE NOT NULL,
    processed BOOLEAN NOT NULL DEFAULT FALSE
);


ALTER TABLE public.articles OWNER TO postgres;

--
-- TOC entry 5015 (class 0 OID 16685)
-- Dependencies: 225
-- Data for Name: articles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.articles VALUES (2669, 'Texas investigates Celsius over energy-drinks marketing', '2026-06-05 14:00:23-04', 'https://www.yahoo.com/news/us/articles/texas-investigates-celsius-over-energy-180023241.html', false);
INSERT INTO public.articles VALUES (5902, 'Zealand Pharma Shares Slide After Boehringer Study Shows Obesity ShotÔÇÖs Side Effects', '2026-06-08 07:23:00-04', 'https://www.wsj.com/health/pharma/zealand-pharma-shares-slide-after-boehringer-study-shows-obesity-shots-side-effects-a624e7b4', false);
INSERT INTO public.articles VALUES (6273, 'Mark Carney''s trade push collides with reality of US dependence - Reuters', '2026-06-09 01:01:00-04', 'https://news.google.com/rss/articles/CBMipwFBVV95cUxOLXBWS2JsM0VrQ25OZS1GMXFIOEs1RGhrdnhfaVNtQjZnc1JPT29KV1RSSmtGNXZlU0psNkNDVDI1VzRMV0Yzbm5ObzJVdlRXR2NtVVA0SjVzMVB5UURoRkdyamp5cFdzNEdOUjlqWUtMSmVMSFphaWpyNnNYeHZCVHdtcl85N0IwdlEzeFI3ZDRRZE1nWHNLRXNtN19wdU5xSjFIcDF0aw?oc=5', false);
INSERT INTO public.articles VALUES (8237, 'Starlink Dominates Internet From Space. Can It Disrupt AT&T and Verizon on the Ground?', '2026-07-02T12:00:00+00:00', 'https://www.wsj.com/business/telecom/starlink-internet-att-verizon-t-mobile-005cf4e3?mod=pls_whats_news_us_business_f', false);
INSERT INTO public.articles VALUES (7353, 'Can You Pass the Test That Strikes Fear Into China’s High-Schoolers?', '2026-06-22 12:07:00-04', 'https://www.wsj.com/world/china/chinese-gaokao-test-quiz-c38937db', false);
INSERT INTO public.articles VALUES (7892, 'Rare tick-borne virus turns deadly fast as US cases reach record high, experts warn - Fox News', '2026-06-29 16:40:04-04', 'https://news.google.com/rss/articles/CBMirwFBVV95cUxPUkpyb1d3SnNWMGE4bnJlQ2NHWk9jYUlncVFVdHZQTlNuQi1XOHFHWndXQkx5cUR1dXBpTVptbGtnWTJ4THh4eG45QldGYUt1THlSSkVBMmphaHg4X2Y1VU5rMVpEWnV3TGFvSktMRWVaaTBULVN6YUhRWFhvTldwbDNqY2pHQUgwa052RXo2eDJ2U3dRT3dNSnNPT18yQUwtNzBoTXdnUVhkd2FkczlJ?oc=5', false);
INSERT INTO public.articles VALUES (2653, 'Multiple stillbirths at troubled hospital trust', '2026-06-05 11:16:35-04', 'https://www.yahoo.com/news/us/articles/multiple-stillbirths-troubled-hospital-trust-051424360.html', false);
INSERT INTO public.articles VALUES (8583, '''Large and growing'' parasitic infection outbreak spreading in Michigan, health officials say - ABC News - Breaking News, Latest News and Videos', '2026-07-02T20:40:36+00:00', 'https://news.google.com/rss/articles/CBMitAFBVV95cUxNUjVOODVBT3NCZDZYOEx6cmpwNUE1RFdSOTZSaTJ6ZXlfV2FyeXpuVFVhYjV6N3FDZm1LdEJXNUFQZGVJT3dsUUdhcnNjNzRRYXpHNTZ3NWhmTUtCOEdzeGVOQ016MTl6U3lmZ3d0NVowQVhZaUsyWnZYT2hrb213ZUxqbklvRGpBS1hpVGFnTFU3VzY5STltY0F3enBnVkw3emd1ckRIMmQ1anpieVhMQkhUTjfSAboBQVVfeXFMT1ZGRllVZWdfelRmT0VJbzl3OE9udGNiODU5d0JDUzkzYlVuYTEyREN5OHhZc3NLOHdUNEcxaWZqRjNuZjJKQ2swbnVJSzBKdF9vcHNXcVc2YS1pTzhRLVBmV3g4MXBmZV8tT3ZqUHJzbGJfUzAxTVZfZkhhajJST1J5bzV4bkVfVHZnamtQdHF0UGR3c1lMRHNDdjVwdFdCLVVSWFNVSUY5MnoxYnRXanI0TWo4RktsbzFR?oc=5', false);
INSERT INTO public.articles VALUES (8478, 'Amazon to start initial Leo internet service this year as network nears 400 satellites - Reuters', '2026-07-02T19:08:34+00:00', 'https://news.google.com/rss/articles/CBMi2wFBVV95cUxQMXBabjNzR3lMMnlJcEhWbUpxNGtLMUVqcmJRcW1Ubno0elRZUXBtQ1gwblhoOFVzZEN6dUJGdmlJeEtWVFhnY3NpSmpXTGZ4MFRmS0hQTVVFTVJ6bGVJNFRoQjVtZWkzVklubVN2STZZZHhVUWp2amFjTjNMQjZqQVoxSEJ2bFpVdzVXWEN6ZTlkVjg5azlWbmVZYTgtUk5rTmZUX25KNndNZVFDb3R2VVBERTRER3lvOGRSTVFoZkVraU5kUlQ5cjJjRU5XWXROUmVIUXp0NmxlN2M?oc=5', false);
INSERT INTO public.articles VALUES (8630, '13 IKEA Finds That Will Upgrade Your Home Office - bgr.com', '2026-07-02T20:02:00+00:00', 'https://news.google.com/rss/articles/CBMia0FVX3lxTE1faFM2NW1SaFlUUUVpV19NbThQdTYxWmNVQXA0NXZRYzdsWFlEaHVBM1gxQ2RsS2FJbWNoZ1hoNDFwYS1PWDlqdDJjS2RsSkUtUlhJR2Rqck1iRTBNMkQ4QXBoTUdwYjd5T3Mw?oc=5', false);
INSERT INTO public.articles VALUES (2655, 'OpenAI Files for IPO', '2026-06-05 11:16:35-04', 'https://www.yahoo.com/news/us/artidcldhs-troubled-hospital-trust-051424360.html', false);
INSERT INTO public.articles VALUES (2656, 'Intesa Bids $35 Billion for Monte dei Paschi', '2026-06-05 11:16:35-04', 'h', false);
INSERT INTO public.articles VALUES (2533, 'How to buy SpaceX shares as its blockbuster IPO readies for liftoff', '2026-06-05 11:16:35-04', 'ht', false);
INSERT INTO public.articles VALUES (2657, 'Nvidia Strikes Deals With Korean Tech Titans for AI Infrastructure Buildout', '2026-06-05 11:16:35-04', 'https:/', false);
INSERT INTO public.articles VALUES (2658, '3 Space Stocks That Could Double When SpaceX Starts Trading', '2026-06-05 11:16:35-04', 'https://www.yahoo.com/news/us/art', false);
INSERT INTO public.articles VALUES (2659, 'German Factory Orders Fell Back in April as Iran War Damps Demand', '2026-06-05 11:16:35-04', 'https://www.yahoo.com/news/us/articles/multiple-stillbirths-trouble', false);
INSERT INTO public.articles VALUES (2610, 'Ukraine recaptures more than 600 square km of territory in 2026, military chief says - Reuters', '2026-06-05 11:16:35-04', 'https://www.yahoo.com/news/us/artist-051424360.html', false);
INSERT INTO public.articles VALUES (2611, 'Five ways Elon Musk's SpaceX upended Wall Streets IPO playbook - Reuters', '2026-06-05 11:16:35-04', 'https://www.yahoo.com/newsoubled-hospital-trust-051424360.html', false);



-- Completed on 2026-07-04 01:01:01

--
-- PostgreSQL database dump complete
--

\unrestrict pRVcGc6vtmluFqgXFreNVB6dBVyhdsRLfoU3NDOyn9dlbgtsFgD76j02Pwfz2SY

