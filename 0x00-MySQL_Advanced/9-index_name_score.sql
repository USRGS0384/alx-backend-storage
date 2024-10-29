-- Creates index on the table names using 
-- first letter of name column and score column
CREATE INDEX idx_name_first_score ON names (name(1), score);
