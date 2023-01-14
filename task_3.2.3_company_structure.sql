
CREATE TABLE IF NOT EXISTS employees (
	employee_id sereal PRIMARY KEY,
	name varchar(60) NOT NULL,
	department varchar(120) NOT NULL,
	boss integer REFERENCES employees (employee_id)
);
