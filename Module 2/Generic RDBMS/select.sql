USE TimesheetDB;
GO

---------------------------------------------------------
-- VIEW
---------------------------------------------------------
-- Acest view afiseaza pontajul complet al fiecarui angajat.
-- LEFT JOIN este folosit pentru a afisa inclusiv zilele
-- fara proiect (concedii).

CREATE OR ALTER VIEW v_employee_timesheet
AS
SELECT

    e.employee_id,

    e.name,

    tc.week_start,

    tc.week_end,

    te.work_date,

    p.project_name,

    te.hours,

    te.location,

    te.time_type

FROM employees e

JOIN time_cards tc
ON e.employee_id = tc.employee_id

JOIN time_entries te
ON tc.time_card_id = te.time_card_id

LEFT JOIN projects p
ON te.project_id = p.project_id;

GO

---------------------------------------------------------
-- VIEW
---------------------------------------------------------
-- Afiseaza continutul view-ului creat anterior.

SELECT *

FROM v_employee_timesheet

ORDER BY

employee_id,

work_date;

GO

---------------------------------------------------------
-- GROUP BY
---------------------------------------------------------
-- Afiseaza numarul total de ore lucrate
-- de fiecare angajat.

SELECT

    e.name,

    SUM(te.hours) AS total_hours

FROM employees e

JOIN time_cards tc
ON e.employee_id = tc.employee_id

JOIN time_entries te
ON tc.time_card_id = te.time_card_id

GROUP BY

e.name

ORDER BY

total_hours DESC;

GO

---------------------------------------------------------
-- GROUP BY
---------------------------------------------------------
-- Afiseaza totalul orelor lucrate
-- pentru fiecare proiect.

SELECT

    p.project_name,

    SUM(te.hours) AS total_hours

FROM projects p

JOIN time_entries te
ON p.project_id = te.project_id

GROUP BY

p.project_name

ORDER BY

total_hours DESC;

GO

---------------------------------------------------------
-- LEFT JOIN
---------------------------------------------------------
-- Afiseaza toti angajatii inclusiv
-- cei fara pontaj.

SELECT

    e.name,

    tc.time_card_id,

    te.work_date,

    te.hours

FROM employees e

LEFT JOIN time_cards tc

ON e.employee_id = tc.employee_id

LEFT JOIN time_entries te

ON tc.time_card_id = te.time_card_id

ORDER BY

e.name,

te.work_date;

GO

---------------------------------------------------------
-- ANALYTIC FUNCTION
---------------------------------------------------------
-- Calculeaza totalul cumulativ al orelor
-- folosind functia SUM OVER.

SELECT

    tc.employee_id,

    te.work_date,

    te.hours,

    SUM(te.hours)

    OVER
    (
        PARTITION BY tc.employee_id

        ORDER BY te.work_date
    )

    AS cumulative_hours

FROM time_entries te

JOIN time_cards tc

ON te.time_card_id = tc.time_card_id

ORDER BY

tc.employee_id,

te.work_date;

GO

---------------------------------------------------------
-- ANALYTIC FUNCTION
---------------------------------------------------------
-- Clasamentul angajatilor dupa totalul
-- orelor lucrate.

SELECT

    employee_name,

    total_hours,

    DENSE_RANK()

    OVER
    (
        ORDER BY total_hours DESC
    )

    AS ranking

FROM

(
    SELECT

        e.name AS employee_name,

        SUM(te.hours) AS total_hours

    FROM employees e

    JOIN time_cards tc
    ON e.employee_id = tc.employee_id

    JOIN time_entries te
    ON tc.time_card_id = te.time_card_id

    GROUP BY

    e.name

) t;

GO

---------------------------------------------------------
-- JSON
---------------------------------------------------------
-- Extrage campul "task"
-- din coloana JSON.

SELECT

    entry_id,

    work_date,

    JSON_VALUE(task_details,'$.task') AS task

FROM time_entries

WHERE task_details IS NOT NULL;

GO

---------------------------------------------------------
-- ABSENCES
---------------------------------------------------------
-- Afiseaza zilele de concediu
-- impreuna cu tipul concediului.

SELECT

    e.name,

    te.work_date,

    a.absence_name

FROM employees e

JOIN time_cards tc

ON e.employee_id = tc.employee_id

JOIN time_entries te

ON tc.time_card_id = te.time_card_id

JOIN time_entry_absence ta

ON te.entry_id = ta.entry_id

JOIN absences a

ON ta.absence_id = a.absence_id

ORDER BY

te.work_date;

GO

---------------------------------------------------------
-- HOURS BY LOCATION
---------------------------------------------------------
-- Afiseaza numarul total de ore
-- lucrate din HOME si OFFICE.

SELECT

    location,

    SUM(hours) AS total_hours

FROM time_entries

GROUP BY

location;

GO

---------------------------------------------------------
-- HOURS BY DAY
---------------------------------------------------------
-- Afiseaza totalul orelor lucrate
-- pentru fiecare zi.

SELECT

    work_date,

    SUM(hours) AS total_hours

FROM time_entries

GROUP BY

work_date

ORDER BY

work_date;

GO

---------------------------------------------------------
-- INDEXED VIEW (Materialized View equivalent)
---------------------------------------------------------
-- Acest view memoreaza totalul orelor lucrate
-- pentru fiecare angajat.
---------------------------------------------------------

CREATE VIEW dbo.v_employee_total_hours
WITH SCHEMABINDING
AS
SELECT

    tc.employee_id,

    COUNT_BIG(*) AS total_entries,

    SUM(CAST(te.hours AS DECIMAL(10,2))) AS total_hours

FROM dbo.time_cards tc

JOIN dbo.time_entries te

ON tc.time_card_id = te.time_card_id

GROUP BY

tc.employee_id;

GO

---------------------------------------------------------
-- UNIQUE CLUSTERED INDEX
---------------------------------------------------------
-- Acest index transforma view-ul
-- intr-un Indexed View.

CREATE UNIQUE CLUSTERED INDEX IX_v_employee_total_hours

ON dbo.v_employee_total_hours(employee_id);

GO

---------------------------------------------------------
-- Afiseaza continutul Indexed View-ului.
---------------------------------------------------------

SELECT *

FROM dbo.v_employee_total_hours

ORDER BY employee_id;

GO