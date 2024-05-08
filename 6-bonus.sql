-- Write a SQL script that creates a stored procedure AddBonus that adds a new correction for a student.
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE PROCEDURE AddBonus(user_id INT, project_name VARCHAR(255), score FLOAT)
BEGIN
	DECLARE project_id INT;
	IF (SELECT COUNT(*) FROM projects where name = project_name) = 0
	THEN
		INSERT INTO projects(name) values (project_name);
	END IF;
	SET project_id = (SELECT id FROM projects WHERE name = project_name LIMIT 1);
	INSERT INTO corrections (user_id, project_id, score) VALUES(user_id, project_id, score);
END
$$
DELIMITER ;
