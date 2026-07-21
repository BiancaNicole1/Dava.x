USE TimesheetDB;
GO

/*=========================================================
    PROJECT: TIMESHEET SYSTEM
    FILE: insert.sql
=========================================================*/

---------------------------------------------------------
-- EMPLOYEES
---------------------------------------------------------

INSERT INTO employees
(employee_id, name, email)
VALUES
(1,'Mazare Bianca Nicole','nicole@email.com');

INSERT INTO employees
(employee_id, name, email)
VALUES
(2,'Popescu Andrei','andrei@email.com');

INSERT INTO employees
(employee_id, name, email)
VALUES
(3,'Ionescu Maria','maria@email.com');

-- Angajat fara pontaj (pentru LEFT JOIN)

INSERT INTO employees
(employee_id, name, email)
VALUES
(4,'Georgescu Elena','elena@email.com');

---------------------------------------------------------
-- PROJECTS
---------------------------------------------------------

INSERT INTO projects
(project_id, project_code, project_name)
VALUES
(1,'BT','BT Banking App');

INSERT INTO projects
(project_id, project_code, project_name)
VALUES
(2,'INT','Internal Work');

INSERT INTO projects
(project_id, project_code, project_name)
VALUES
(3,'HR','HR Platform');

---------------------------------------------------------
-- ABSENCES
---------------------------------------------------------

INSERT INTO absences VALUES
(1,'Annual Leave');

INSERT INTO absences VALUES
(2,'Medical Leave');

INSERT INTO absences VALUES
(3,'Unpaid Leave');

INSERT INTO absences VALUES
(4,'Special Leave');

INSERT INTO absences VALUES
(5,'Childcare Leave');

---------------------------------------------------------
-- TIME CARDS
---------------------------------------------------------

INSERT INTO time_cards
(time_card_id,employee_id,week_start,week_end)
VALUES
(1,1,'2026-06-16','2026-06-22');

INSERT INTO time_cards
(time_card_id,employee_id,week_start,week_end)
VALUES
(2,2,'2026-06-16','2026-06-22');

INSERT INTO time_cards
(time_card_id,employee_id,week_start,week_end)
VALUES
(3,3,'2026-06-16','2026-06-22');

---------------------------------------------------------
-- TIME ENTRIES
-- BIANCA
---------------------------------------------------------

INSERT INTO time_entries
VALUES
(
1,
1,
'2026-06-16',
1,
'{"task":"Development","module":"Login"}',
'REGULAR',
'HOME',
NULL,
'2026-06-16 09:00',
'2026-06-16 17:00',
8
);

INSERT INTO time_entries
VALUES
(
2,
1,
'2026-06-17',
1,
'{"task":"Bug Fixing"}',
'REGULAR',
'OFFICE',
NULL,
'2026-06-17 09:00',
'2026-06-17 17:00',
8
);

-- Zi de concediu

INSERT INTO time_entries
VALUES
(
3,
1,
'2026-06-18',
NULL,
NULL,
'REGULAR',
'HOME',
NULL,
NULL,
NULL,
0
);

INSERT INTO time_entries
VALUES
(
4,
1,
'2026-06-19',
2,
'{"task":"Internal Training"}',
'REGULAR',
'HOME',
NULL,
'2026-06-19 09:00',
'2026-06-19 17:00',
8
);

-- Concediu medical

INSERT INTO time_entries
VALUES
(
5,
1,
'2026-06-20',
NULL,
NULL,
'REGULAR',
'HOME',
NULL,
NULL,
NULL,
0
);

---------------------------------------------------------
-- ANDREI
---------------------------------------------------------

INSERT INTO time_entries
VALUES
(
6,
2,
'2026-06-16',
1,
'{"task":"Testing"}',
'REGULAR',
'OFFICE',
NULL,
'2026-06-16 08:00',
'2026-06-16 16:00',
8
);

INSERT INTO time_entries
VALUES
(
7,
2,
'2026-06-17',
3,
'{"task":"Documentation"}',
'REGULAR',
'HOME',
NULL,
'2026-06-17 09:00',
'2026-06-17 15:00',
6
);
---------------------------------------------------------
-- ANDREI (continuare)
---------------------------------------------------------

INSERT INTO time_entries
VALUES
(
8,
2,
'2026-06-18',
3,
'{"task":"Client Meeting"}',
'REGULAR',
'OFFICE',
NULL,
'2026-06-18 10:00',
'2026-06-18 17:00',
7
);

INSERT INTO time_entries
VALUES
(
9,
2,
'2026-06-19',
1,
'{"task":"Regression Testing"}',
'OVERTIME',
'HOME',
NULL,
'2026-06-19 09:00',
'2026-06-19 19:00',
10
);

---------------------------------------------------------
-- MARIA
---------------------------------------------------------

INSERT INTO time_entries
VALUES
(
10,
3,
'2026-06-16',
2,
'{"task":"Planning"}',
'REGULAR',
'HOME',
NULL,
'2026-06-16 09:00',
'2026-06-16 17:00',
8
);

INSERT INTO time_entries
VALUES
(
11,
3,
'2026-06-17',
2,
'{"task":"Code Review"}',
'REGULAR',
'HOME',
NULL,
'2026-06-17 09:00',
'2026-06-17 17:00',
8
);

INSERT INTO time_entries
VALUES
(
12,
3,
'2026-06-18',
3,
'{"task":"Requirements Analysis"}',
'REGULAR',
'OFFICE',
NULL,
'2026-06-18 09:00',
'2026-06-18 17:00',
8
);

INSERT INTO time_entries
VALUES
(
13,
3,
'2026-06-19',
3,
'{"task":"Project Workshop"}',
'REGULAR',
'OFFICE',
NULL,
'2026-06-19 09:00',
'2026-06-19 16:00',
7
);

---------------------------------------------------------
-- ABSENCE LINKS
---------------------------------------------------------

-- Bianca - concediu de odihna

INSERT INTO time_entry_absence
(entry_id, absence_id)
VALUES
(
3,
1
);

-- Bianca - concediu medical

INSERT INTO time_entry_absence
(entry_id, absence_id)
VALUES
(
5,
2
);

---------------------------------------------------------
-- VERIFICARE
---------------------------------------------------------

SELECT *
FROM employees;

SELECT *
FROM projects;

SELECT *
FROM absences;

SELECT *
FROM time_cards;

SELECT *
FROM time_entries
ORDER BY work_date;

SELECT *
FROM time_entry_absence;

GO