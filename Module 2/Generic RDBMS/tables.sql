USE TimesheetDB;
GO

---------------------------------------------------------
-- TABLE: EMPLOYEES
---------------------------------------------------------

CREATE TABLE employees
(
    employee_id INT PRIMARY KEY,

    name NVARCHAR(100) NOT NULL,

    email NVARCHAR(100) NOT NULL UNIQUE,

    hire_date DATE NOT NULL
        CONSTRAINT DF_Employees_HireDate
        DEFAULT (GETDATE()),

    status NVARCHAR(20) NOT NULL
        CONSTRAINT DF_Employees_Status
        DEFAULT ('ACTIVE'),

    CONSTRAINT CK_Employees_Status
    CHECK (status IN ('ACTIVE','INACTIVE'))
);

GO

---------------------------------------------------------
-- TABLE: PROJECTS
---------------------------------------------------------

CREATE TABLE projects
(
    project_id INT PRIMARY KEY,

    project_code NVARCHAR(20) NOT NULL UNIQUE,

    project_name NVARCHAR(100) NOT NULL,

    status NVARCHAR(20) NOT NULL
        CONSTRAINT DF_Projects_Status
        DEFAULT ('ACTIVE'),

    CONSTRAINT CK_Projects_Status
    CHECK (status IN ('ACTIVE','FINISHED','ON_HOLD'))
);

GO

---------------------------------------------------------
-- TABLE: ABSENCES
---------------------------------------------------------

CREATE TABLE absences
(
    absence_id INT PRIMARY KEY,

    absence_name NVARCHAR(100) NOT NULL UNIQUE
);

GO

---------------------------------------------------------
-- TABLE: TIME_CARDS
---------------------------------------------------------

CREATE TABLE time_cards
(
    time_card_id INT PRIMARY KEY,

    employee_id INT NOT NULL,

    week_start DATE NOT NULL,

    week_end DATE NOT NULL,

    total_hours DECIMAL(5,2)
        NOT NULL
        CONSTRAINT DF_TimeCards_TotalHours
        DEFAULT (0),

    approved BIT
        NOT NULL
        CONSTRAINT DF_TimeCards_Approved
        DEFAULT (0),

    CONSTRAINT CK_TimeCards_TotalHours
        CHECK (total_hours >= 0),

    CONSTRAINT CK_TimeCards_Week
        CHECK (week_end >= week_start),

    CONSTRAINT UQ_TimeCards_EmployeeWeek
        UNIQUE(employee_id, week_start),

    CONSTRAINT FK_TimeCards_Employees
        FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)
);

GO

---------------------------------------------------------
-- TABLE: TIME_ENTRIES
---------------------------------------------------------

CREATE TABLE time_entries
(
    entry_id INT PRIMARY KEY,

    time_card_id INT NOT NULL,

    work_date DATE NOT NULL,

    project_id INT NULL,

    task_details NVARCHAR(MAX) NULL,

    time_type NVARCHAR(30)
        NOT NULL
        CONSTRAINT DF_TimeEntries_TimeType
        DEFAULT ('REGULAR'),

    location NVARCHAR(20)
        NOT NULL
        CONSTRAINT DF_TimeEntries_Location
        DEFAULT ('HOME'),

    relocated_country NVARCHAR(50) NULL,

    start_time DATETIME NULL,

    end_time DATETIME NULL,

    hours DECIMAL(4,2)
        NOT NULL
        CONSTRAINT DF_TimeEntries_Hours
        DEFAULT (0),

    CONSTRAINT CK_TimeEntries_JSON
        CHECK
        (
            task_details IS NULL
            OR ISJSON(task_details)=1
        ),

    CONSTRAINT CK_TimeEntries_TimeType
        CHECK
        (
            time_type IN
            (
                'REGULAR',
                'OVERTIME',
                'PUBLIC_HOLIDAY',
                'TRAVEL'
            )
        ),

    CONSTRAINT CK_TimeEntries_Location
        CHECK
        (
            location IN
            (
                'HOME',
                'OFFICE'
            )
        ),

    CONSTRAINT CK_TimeEntries_Hours
        CHECK
        (
            hours BETWEEN 0 AND 24
        ),

    CONSTRAINT CK_TimeEntries_TimeInterval
        CHECK
        (
            start_time IS NULL
            OR end_time IS NULL
            OR end_time>=start_time
        ),

    CONSTRAINT FK_TimeEntries_TimeCards
        FOREIGN KEY(time_card_id)
        REFERENCES time_cards(time_card_id),

    CONSTRAINT FK_TimeEntries_Projects
        FOREIGN KEY(project_id)
        REFERENCES projects(project_id)
);

GO

---------------------------------------------------------
-- TABLE: TIME_ENTRY_ABSENCE
---------------------------------------------------------

CREATE TABLE time_entry_absence
(
    entry_id INT NOT NULL,

    absence_id INT NOT NULL,

    CONSTRAINT PK_TimeEntryAbsence
        PRIMARY KEY(entry_id,absence_id),

    CONSTRAINT FK_TimeEntryAbsence_Entry
        FOREIGN KEY(entry_id)
        REFERENCES time_entries(entry_id),

    CONSTRAINT FK_TimeEntryAbsence_Absence
        FOREIGN KEY(absence_id)
        REFERENCES absences(absence_id)
);

GO

---------------------------------------------------------
-- INDEXES
---------------------------------------------------------

CREATE INDEX IX_TimeEntries_WorkDate
ON time_entries(work_date);

GO

CREATE INDEX IX_TimeEntries_Location
ON time_entries(location);

GO

CREATE INDEX IX_Employees_Email
ON employees(email);

GO

---------------------------------------------------------
-- TRIGGER
---------------------------------------------------------

CREATE OR ALTER TRIGGER TR_Update_TimeCard_TotalHours
ON time_entries
AFTER INSERT, UPDATE, DELETE
AS
BEGIN

    SET NOCOUNT ON;

    UPDATE tc
    SET total_hours =
    (
        SELECT ISNULL(SUM(te.hours),0)
        FROM time_entries te
        WHERE te.time_card_id = tc.time_card_id
    )
    FROM time_cards tc
    WHERE tc.time_card_id IN
    (
        SELECT time_card_id FROM inserted

        UNION

        SELECT time_card_id FROM deleted
    );

END;

GO