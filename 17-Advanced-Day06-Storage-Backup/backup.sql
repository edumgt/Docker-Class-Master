--
-- PostgreSQL database cluster dump
--

\restrict dn4kgLDeWfHwf1uc7ayg3FNnofFzAmJLANu10oVJYaMwwtd0WEpvj2jsZSCM1sY

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Drop databases (except postgres and template1)
--





--
-- Drop roles
--

DROP ROLE postgres;


--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:jHkxAw1bCp3GdqjYPi6/PA==$soHIQdl9IEgDWI6YAfpvg0eedBu6KQ42J+Ep5Og96Kw=:TCFBbkT5EsbNoy4D+ugdx+LnSh+WNxlWaU3HMmcU62U=';

--
-- User Configurations
--








\unrestrict dn4kgLDeWfHwf1uc7ayg3FNnofFzAmJLANu10oVJYaMwwtd0WEpvj2jsZSCM1sY

--
-- Databases
--

--
-- Database "template1" dump
--

--
-- PostgreSQL database dump
--

\restrict Mk34zTxoHcF1b6POWgmgTHOIcCItWerlJgAY4XuyESLTSgLSQhAiQLQY3v2tCCv

-- Dumped from database version 16.13
-- Dumped by pg_dump version 16.13

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

UPDATE pg_catalog.pg_database SET datistemplate = false WHERE datname = 'template1';
DROP DATABASE template1;
--
-- Name: template1; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE template1 OWNER TO postgres;

\unrestrict Mk34zTxoHcF1b6POWgmgTHOIcCItWerlJgAY4XuyESLTSgLSQhAiQLQY3v2tCCv
\connect template1
\restrict Mk34zTxoHcF1b6POWgmgTHOIcCItWerlJgAY4XuyESLTSgLSQhAiQLQY3v2tCCv

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

--
-- Name: DATABASE template1; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: template1; Type: DATABASE PROPERTIES; Schema: -; Owner: postgres
--

ALTER DATABASE template1 IS_TEMPLATE = true;


\unrestrict Mk34zTxoHcF1b6POWgmgTHOIcCItWerlJgAY4XuyESLTSgLSQhAiQLQY3v2tCCv
\connect template1
\restrict Mk34zTxoHcF1b6POWgmgTHOIcCItWerlJgAY4XuyESLTSgLSQhAiQLQY3v2tCCv

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

--
-- Name: DATABASE template1; Type: ACL; Schema: -; Owner: postgres
--

REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\unrestrict Mk34zTxoHcF1b6POWgmgTHOIcCItWerlJgAY4XuyESLTSgLSQhAiQLQY3v2tCCv

--
-- Database "postgres" dump
--

--
-- PostgreSQL database dump
--

\restrict gbmyveyDhld2Scnc49Mhc5nXfNdCVZc4nCnoMN23KidCVsuNKSw34X4PFuZ0Uj8

-- Dumped from database version 16.13
-- Dumped by pg_dump version 16.13

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

DROP DATABASE postgres;
--
-- Name: postgres; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE postgres OWNER TO postgres;

\unrestrict gbmyveyDhld2Scnc49Mhc5nXfNdCVZc4nCnoMN23KidCVsuNKSw34X4PFuZ0Uj8
\connect postgres
\restrict gbmyveyDhld2Scnc49Mhc5nXfNdCVZc4nCnoMN23KidCVsuNKSw34X4PFuZ0Uj8

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

--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- PostgreSQL database dump complete
--

\unrestrict gbmyveyDhld2Scnc49Mhc5nXfNdCVZc4nCnoMN23KidCVsuNKSw34X4PFuZ0Uj8

--
-- PostgreSQL database cluster dump complete
--

