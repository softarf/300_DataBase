
CREATE TABLE IF NOT EXISTS employees (
	employee_id SERIAL PRIMARY KEY,
	name VARCHAR(60) NOT NULL,
	department VARCHAR(120) NOT NULL,
	boss INTEGER REFERENCES employees (employee_id)
);
