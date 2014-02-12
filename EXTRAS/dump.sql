--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: leo
--

INSERT INTO auth_user VALUES (3, 'Antonio', 'Munno', 'munnoantonio@gmail.com', 'pbkdf2(1000,20,sha512)$9e9fd81b3ffa34c9$9e27372982cdf30b9aa7968f1a92402bd4874f3d', '', '', '', '', 'Masculino', '2014-01-23 10:03:32', '2014-01-23 10:04:46', '', 'T', 2, '2014-02-10 20:09:11', 1);
INSERT INTO auth_user VALUES (2, 'María', 'Najún', 'mnajun@pioix.edu.ar', 'pbkdf2(1000,20,sha512)$9fbd2737e8aa6d7e$c006dd05775e61428730d09b9f302a2848f6aa46', '', '', '', '', 'Femenino', '2014-01-22 16:04:26', '2014-02-10 21:10:45', '', 'T', 1, '2014-02-10 21:10:45', 2);
INSERT INTO auth_user VALUES (5, 'Antonio', 'Munno', 'amunno@pioix.edu.ar', 'pbkdf2(1000,20,sha512)$b68cee18e9631b19$3a65b32a6966a4b3b390a1857c7f67f84a5322b2', '', '', '', '', 'Masculino', '2014-02-10 21:11:29', NULL, NULL, 'T', 2, '2014-02-10 21:11:29', 2);
INSERT INTO auth_user VALUES (1, 'Leandro', 'Colombo Viña', 'colomboleandro@pioix.edu.ar', 'pbkdf2(1000,20,sha512)$9bd3fe1542fc57ab$1c72ff6215cd465176e2863b542ff8b5c5b27510', '', '', '', 'Enrique', 'Masculino', NULL, '2014-02-12 11:46:28', '', 'T', NULL, '2014-02-12 11:46:28', 1);


--
-- Data for Name: address; Type: TABLE DATA; Schema: public; Owner: leo
--



--
-- Name: address_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('address_id_seq', 1, false);


--
-- Data for Name: auth_cas; Type: TABLE DATA; Schema: public; Owner: leo
--



--
-- Name: auth_cas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('auth_cas_id_seq', 1, false);


--
-- Data for Name: auth_event; Type: TABLE DATA; Schema: public; Owner: leo
--

INSERT INTO auth_event VALUES (1, '2014-01-22 15:22:54', '127.0.0.1', 1, 'auth', 'User 1 Registered');
INSERT INTO auth_event VALUES (2, '2014-01-22 15:25:45', '127.0.0.1', 1, 'auth', 'User 1 Logged-out');
INSERT INTO auth_event VALUES (3, '2014-01-22 15:42:10', '127.0.0.1', 1, 'auth', 'User 1 Logged-in');
INSERT INTO auth_event VALUES (4, '2014-01-22 16:10:57', '127.0.0.1', 1, 'auth', 'User 1 Logged-out');
INSERT INTO auth_event VALUES (5, '2014-01-22 17:22:45', '127.0.0.1', 1, 'auth', 'User 1 Logged-in');
INSERT INTO auth_event VALUES (6, '2014-01-22 19:34:14', '127.0.0.1', 1, 'auth', 'User 1 Logged-in');
INSERT INTO auth_event VALUES (7, '2014-01-22 19:55:42', '127.0.0.1', 1, '127.0.0.1:8000', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (8, '2014-01-22 19:56:39', '127.0.0.1', 1, 'auth', 'User 1 Logged-out');
INSERT INTO auth_event VALUES (9, '2014-01-22 19:56:52', '127.0.0.1', 2, 'auth', 'User 2 Logged-in');
INSERT INTO auth_event VALUES (10, '2014-01-22 19:56:54', '127.0.0.1', 2, '127.0.0.1:8000', 'User 2 - Najún, María - logged in');
INSERT INTO auth_event VALUES (11, '2014-01-22 20:16:07', '127.0.0.1', 2, 'auth', 'User 2 Logged-out');
INSERT INTO auth_event VALUES (12, '2014-01-23 09:58:30', '127.0.0.1', 1, 'auth', 'User 1 Logged-in');
INSERT INTO auth_event VALUES (13, '2014-01-23 09:58:30', '127.0.0.1', 1, '127.0.0.1:8000', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (14, '2014-01-23 09:59:23', '127.0.0.1', 1, 'auth', 'User 1 Logged-out');
INSERT INTO auth_event VALUES (15, '2014-01-23 09:59:24', '127.0.0.1', 1, 'auth', 'User 1 Logged-out');
INSERT INTO auth_event VALUES (16, '2014-01-23 09:59:43', '127.0.0.1', 2, 'auth', 'User 2 Logged-in');
INSERT INTO auth_event VALUES (17, '2014-01-23 09:59:43', '127.0.0.1', 2, '127.0.0.1:8000', 'User 2 - Najún, María - logged in');
INSERT INTO auth_event VALUES (18, '2014-01-23 10:04:32', '127.0.0.1', 2, 'auth', 'User 2 Logged-out');
INSERT INTO auth_event VALUES (19, '2014-01-23 10:04:32', '127.0.0.1', 2, 'auth', 'User 2 Logged-out');
INSERT INTO auth_event VALUES (20, '2014-01-23 10:04:44', '127.0.0.1', 3, 'auth', 'User 3 Logged-in');
INSERT INTO auth_event VALUES (21, '2014-01-23 10:04:46', '127.0.0.1', 3, '127.0.0.1:8000', 'User 3 - Munno, Antonio - logged in');
INSERT INTO auth_event VALUES (22, '2014-01-23 10:05:07', '127.0.0.1', 3, 'auth', 'User 3 Logged-out');
INSERT INTO auth_event VALUES (23, '2014-01-23 10:05:07', '127.0.0.1', 3, 'auth', 'User 3 Logged-out');
INSERT INTO auth_event VALUES (24, '2014-01-23 10:05:15', '127.0.0.1', 1, 'auth', 'User 1 Logged-in');
INSERT INTO auth_event VALUES (25, '2014-01-23 10:05:17', '127.0.0.1', 1, '127.0.0.1:8000', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (26, '2014-01-23 15:10:45', '127.0.0.1', 1, 'auth', 'User 1 Logged-in');
INSERT INTO auth_event VALUES (27, '2014-01-23 15:10:47', '127.0.0.1', 1, '127.0.0.1:8000', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (28, '2014-01-23 15:12:33', '127.0.0.1', 1, 'auth', 'User 1 Logged-out');
INSERT INTO auth_event VALUES (29, '2014-01-23 15:12:33', '127.0.0.1', 1, 'auth', 'User 1 Logged-out');
INSERT INTO auth_event VALUES (30, '2014-01-23 20:40:11', '127.0.0.1', 1, 'auth', 'User 1 Logged-in');
INSERT INTO auth_event VALUES (31, '2014-01-23 20:40:44', '127.0.0.1', 1, '127.0.0.1:8000', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (32, '2014-01-23 20:44:57', '127.0.0.1', 1, 'auth', 'User 1 Logged-out');
INSERT INTO auth_event VALUES (33, '2014-01-24 13:40:27', '127.0.0.1', 2, 'auth', 'User 2 Logged-in');
INSERT INTO auth_event VALUES (34, '2014-01-24 13:40:33', '127.0.0.1', 2, 'auth', 'User 2 - Najún, María - logged in');
INSERT INTO auth_event VALUES (35, '2014-01-24 13:41:21', '127.0.0.1', 2, 'auth', 'User 2 Logged-out');
INSERT INTO auth_event VALUES (36, '2014-01-24 13:53:24', '127.0.0.1', 2, 'auth', 'User 2 - Najún, María - logged in');
INSERT INTO auth_event VALUES (37, '2014-01-24 13:56:28', '127.0.0.1', 2, 'auth', 'User 2 - Najún, María - logged out');
INSERT INTO auth_event VALUES (38, '2014-01-24 13:58:02', '127.0.0.1', 2, 'auth', 'User 2 - Najún, María - logged in');
INSERT INTO auth_event VALUES (39, '2014-01-24 13:58:15', '127.0.0.1', 2, 'auth', 'User 2 - Najún, María - logged out');
INSERT INTO auth_event VALUES (40, '2014-01-24 14:06:16', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (41, '2014-01-24 14:14:26', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged out');
INSERT INTO auth_event VALUES (42, '2014-01-24 11:44:05', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (43, '2014-01-24 15:05:18', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (44, '2014-01-26 10:28:17', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (45, '2014-01-26 11:58:35', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (46, '2014-02-06 12:34:21', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (47, '2014-02-06 13:32:59', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (48, '2014-02-06 18:12:53', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (49, '2014-02-06 18:28:01', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (50, '2014-02-07 12:03:54', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (51, '2014-02-07 14:32:25', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (52, '2014-02-08 18:45:19', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (53, '2014-02-10 14:19:29', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (54, '2014-02-10 15:34:06', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (55, '2014-02-10 19:22:26', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (56, '2014-02-10 20:02:55', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged out');
INSERT INTO auth_event VALUES (57, '2014-02-10 20:03:20', '127.0.0.1', 2, 'auth', 'User 2 - Najún, María - logged in');
INSERT INTO auth_event VALUES (58, '2014-02-10 20:03:54', '127.0.0.1', 2, 'auth', 'User 2 - Najún, María - logged out');
INSERT INTO auth_event VALUES (59, '2014-02-10 20:08:30', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (60, '2014-02-10 20:09:23', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged out');
INSERT INTO auth_event VALUES (61, '2014-02-10 20:09:50', '127.0.0.1', 3, 'auth', 'User 3 - Munno, Antonio - logged in');
INSERT INTO auth_event VALUES (62, '2014-02-10 20:47:39', '127.0.0.1', 3, 'auth', 'User 3 - Munno, Antonio - logged out');
INSERT INTO auth_event VALUES (63, '2014-02-10 20:49:09', '127.0.0.1', 2, 'auth', 'User 2 - Najún, María - logged in');
INSERT INTO auth_event VALUES (64, '2014-02-10 20:55:56', '127.0.0.1', 2, 'auth', 'User 2 - Najún, María - logged out');
INSERT INTO auth_event VALUES (65, '2014-02-10 21:10:36', '127.0.0.1', 2, 'auth', 'User 2 - Najún, María - logged in');
INSERT INTO auth_event VALUES (66, '2014-02-10 21:11:39', '127.0.0.1', 2, 'auth', 'User 2 - Najún, María - logged out');
INSERT INTO auth_event VALUES (67, '2014-02-10 21:11:57', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (68, '2014-02-11 20:00:35', '190.55.37.111', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (69, '2014-02-11 20:01:00', '190.55.37.111', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged out');
INSERT INTO auth_event VALUES (70, '2014-02-11 21:02:38', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');
INSERT INTO auth_event VALUES (71, '2014-02-12 11:46:19', '127.0.0.1', 1, 'auth', 'User 1 - Colombo Viña, Leandro - logged in');


--
-- Name: auth_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('auth_event_id_seq', 71, true);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: leo
--

INSERT INTO auth_group VALUES (1, 'root', 'Superadministrador', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (2, 'empleado', 'Empleado de la Casa', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (3, 'soporte', 'Soporte Técnico', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (4, 'directivo', 'Directivo', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (5, 'director', 'Director General', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (6, 'rector', 'Rector del Colegio', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (7, 'secretaria', 'Secretaría', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (8, 'secretario', 'Secretario', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (9, 'derivaciones', 'Oficina de Derivaciones', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (10, 'eoe', 'Equipo de Orientación Escolar', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (11, 'administracion', 'Administración', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (12, 'administrador', 'Administrador', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (13, 'caja', 'Caja', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (14, 'padre', 'Padre o Madre', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_group VALUES (15, 'candidato', 'Ingresante', 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('auth_group_id_seq', 15, true);


--
-- Data for Name: auth_membership; Type: TABLE DATA; Schema: public; Owner: leo
--

INSERT INTO auth_membership VALUES (1, 1, 1, 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_membership VALUES (2, 2, 9, 'T', '2014-01-22 16:04:26', 1, '2014-01-22 16:04:26', 1);
INSERT INTO auth_membership VALUES (3, 3, 14, 'T', '2014-01-23 10:03:32', 2, '2014-01-23 10:03:32', 2);
INSERT INTO auth_membership VALUES (5, 5, 14, 'T', '2014-02-10 21:11:29', 2, '2014-02-10 21:11:29', 2);


--
-- Name: auth_membership_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('auth_membership_id_seq', 5, true);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: leo
--

INSERT INTO auth_permission VALUES (1, 1, 'create', 'auth_user', 0, 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_permission VALUES (2, 1, 'read', 'auth_user', 0, 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_permission VALUES (3, 1, 'update', 'auth_user', 0, 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_permission VALUES (4, 1, 'delete', 'auth_user', 0, 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_permission VALUES (5, 9, 'create new father', 'auth_user', 0, 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_permission VALUES (6, 9, 'view fathers list', 'auth_user', 0, 'T', '2014-01-22 15:42:39', 1, '2014-01-22 15:42:39', 1);
INSERT INTO auth_permission VALUES (7, 1, 'create', 'date', 0, 'T', '2014-01-22 17:23:16', 1, '2014-01-22 17:23:16', 1);
INSERT INTO auth_permission VALUES (8, 1, 'read', 'date', 0, 'T', '2014-01-22 17:50:27', 1, '2014-01-22 17:55:06', 1);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('auth_permission_id_seq', 8, true);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('auth_user_id_seq', 5, true);


--
-- Data for Name: date; Type: TABLE DATA; Schema: public; Owner: leo
--

INSERT INTO date VALUES (3, 'vencimiento', '2014-08-29', NULL, NULL, 'Cierre del período de inscripciones.', 'T', '2014-01-22 18:06:57', 1, '2014-01-22 18:06:57', 1);
INSERT INTO date VALUES (5, 'turno', '2014-03-12', '10:00:00', '11:00:00', 'Charla Informativa', 'T', '2014-01-22 18:10:12', 1, '2014-01-22 18:10:12', 1);
INSERT INTO date VALUES (6, 'apertura', '2014-03-10', NULL, NULL, 'Comienzo del período de inscripciones.', 'T', '2014-01-24 11:45:12', 1, '2014-01-24 11:45:12', 1);


--
-- Name: date_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('date_id_seq', 6, true);


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: leo
--



--
-- Data for Name: father; Type: TABLE DATA; Schema: public; Owner: leo
--

INSERT INTO father VALUES (1, 5, 'T', 'Sofía Munno', 'T', 'San Francisco de Sales', 'T', NULL, NULL, NULL, 'Password Change', NULL, 'T', '2014-02-10 21:11:29', 2, '2014-02-10 21:11:29', 2);


--
-- Name: father_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('father_id_seq', 1, true);


--
-- Data for Name: general_date; Type: TABLE DATA; Schema: public; Owner: leo
--

INSERT INTO general_date VALUES (64, 'Cierre de Inscripciones', 2013, '2013-02-10', NULL, NULL, 'T', '2014-02-10 16:56:21', 1, '2014-02-10 17:31:40', 1);
INSERT INTO general_date VALUES (6, 'Examen de Matemática', 2013, '2013-10-26', '08:00:00', NULL, 'T', '2014-02-07 11:16:28', 1, '2014-02-10 17:31:40', 1);
INSERT INTO general_date VALUES (65, 'Apertura de Inscripciones', 2013, '2013-02-25', NULL, NULL, 'T', '2014-02-10 16:56:21', 1, '2014-02-10 17:31:40', 1);
INSERT INTO general_date VALUES (8, 'Examen de Lengua', 2013, '2013-10-19', '08:00:00', NULL, 'T', '2014-02-07 11:16:28', 1, '2014-02-10 17:31:40', 1);
INSERT INTO general_date VALUES (9, 'Primera Reunión de Padres (Segunda Fecha)', 2013, '2013-07-24', '20:00:00', '21:00:00', 'T', '2014-02-07 11:16:28', 1, '2014-02-10 17:31:40', 1);
INSERT INTO general_date VALUES (10, 'Publicación de la Lista de Preinscriptos', 2013, '2013-11-20', '10:00:00', NULL, 'T', '2014-02-07 11:16:28', 1, '2014-02-10 17:31:40', 1);
INSERT INTO general_date VALUES (13, 'Fecha Límite de entrega de Boletines', 2013, '2013-10-18', NULL, NULL, 'T', '2014-02-07 11:16:28', 1, '2014-02-10 17:31:40', 1);
INSERT INTO general_date VALUES (4, 'Cierre de Inscripciones', 2014, '2014-09-26', NULL, NULL, 'T', '2014-02-07 13:06:19', 1, '2014-02-10 17:30:38', 1);
INSERT INTO general_date VALUES (1, 'Apertura de Inscripciones', 2014, '2014-03-03', NULL, NULL, 'T', '2014-02-07 12:59:20', 1, '2014-02-10 17:30:38', 1);
INSERT INTO general_date VALUES (3, 'Primera Reunión de Padres (Primera Fecha)', 2014, '2014-06-10', '18:30:00', '20:00:00', 'T', '2014-02-07 12:59:20', 1, '2014-02-10 17:30:38', 1);
INSERT INTO general_date VALUES (2, 'Fecha Límite de Prioritarios', 2014, '2014-06-27', NULL, NULL, 'T', '2014-02-07 12:59:20', 1, '2014-02-10 17:30:38', 1);


--
-- Name: general_date_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('general_date_id_seq', 102, true);


--
-- Data for Name: image; Type: TABLE DATA; Schema: public; Owner: leo
--

INSERT INTO image VALUES (1, 'Logo Pío IX Nuevo 250x245', 'image.file.ae9a423a27e76721.4c6f676f50696f49582d4e7565766f2e706e67.png', 'T', '2014-01-24 14:09:47', 1, '2014-01-24 14:09:47', 1);


--
-- Name: image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('image_id_seq', 1, true);


--
-- Data for Name: personal_data; Type: TABLE DATA; Schema: public; Owner: leo
--



--
-- Name: personal_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('personal_data_id_seq', 1, false);


--
-- Data for Name: sectors; Type: TABLE DATA; Schema: public; Owner: leo
--



--
-- Name: sectors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('sectors_id_seq', 1, false);


--
-- Name: student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('student_id_seq', 1, false);


--
-- Data for Name: subsectors; Type: TABLE DATA; Schema: public; Owner: leo
--



--
-- Name: subsectors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leo
--

SELECT pg_catalog.setval('subsectors_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

