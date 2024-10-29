-- SQL script that creates a stored procedure 
-- ComputeAverageWeightedScoreForUsers that computes and store 
-- the average weighted score for all students.
DELIMITER $
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE student_id, total_projects_weight INT;
    DECLARE average_weight_score, total_projects_weighted_score FLOAT;
    DECLARE students_flag INT DEFAULT FALSE;
    DECLARE students_cursor CURSOR FOR SELECT id from users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET students_flag = TRUE;
    OPEN students_cursor;
    students_loop: LOOP
        FETCH students_cursor INTO student_id;
        IF students_flag THEN
            LEAVE students_loop;
        END IF;
        SELECT SUM(score * projects.weight) INTO total_projects_weighted_score
            FROM corrections JOIN projects ON project_id = projects.id
            WHERE user_id = student_id GROUP BY user_id;
        SELECT SUM(projects.weight) INTO total_projects_weight FROM projects;
        SET average_weight_score = total_projects_weighted_score / total_projects_weight;
        UPDATE users SET average_score = average_weight_score WHERE id = student_id;
    END LOOP students_loop;
    CLOSE students_cursor;
END$
DELIMITER ;
