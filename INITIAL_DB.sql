--ADMIN
INSERT INTO users_user("password", last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, id, onboarding, "language")
VALUES('pbkdf2_sha256$870000$xSRDtkDhXStWjmMm5kBAON$3DgX08Lwy7pi46Z8CTaZ/gOQ0AFVTMwXP6oQVZv4l3M=', NULL, true, 'admin', '', '', '', true, true, '2024-10-14 22:03:14.210', '17b2c21f-37b1-4a0a-a738-c35900b9e1ae'::uuid, false, 'es');

-- DEPARTMENTS
INSERT INTO public.departments_department
(created, modified, is_removed, id, "name", description)
VALUES('2024-10-15 17:33:07.126', '2024-10-15 17:33:07.126', false, '016349e5-6f74-4caf-8f1b-6fe754ee800e'::uuid, 'Desarrollo', '');
INSERT INTO public.departments_department
(created, modified, is_removed, id, "name", description)
VALUES('2024-10-15 17:33:11.685', '2024-10-15 17:33:11.685', false, '5358be9b-a1c6-468c-9934-2985503af44f'::uuid, 'Gestión', '');

-- TECHNOLOGIES
INSERT INTO public.technologies_technology
(created, modified, is_removed, id, "name", description, "group")
VALUES('2024-10-15 17:34:19.496', '2024-10-15 17:34:19.496', false, '038d67b0-a3c4-4800-9ee2-519fbb572bca'::uuid, 'Django', '', 'Backend');
INSERT INTO public.technologies_technology
(created, modified, is_removed, id, "name", description, "group")
VALUES('2024-10-15 17:34:28.639', '2024-10-15 17:34:28.639', false, 'd569b10c-878c-4f4a-aa45-f34c8661490b'::uuid, 'React', '', 'Frontend');