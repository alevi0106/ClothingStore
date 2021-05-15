select * from categorytype;
select * from Categories;
INSERT INTO Categories (name, categorytype)
VALUES ('Body', 7);
PRAGMA foreign_keys = 1;

select * from Categories WHERE categorytype = 7