-- Creates a function SafeDiv that divides and 
-- returns the first number by the second number
-- by the second number or returns 0 if the seond number is 0
DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
BEGIN
    DECLARE result FLOAT DEFAULT 0;
    IF b != 0 THEN
        SET result = a / b;
    END IF;
    RETURN result;
END$$
DELIMITER ;
