select * from categorytype;
select * from Categories;
INSERT INTO Categories (name, categorytype)
VALUES ('Body', 7);
PRAGMA foreign_keys = 1;

select * from Categories WHERE categorytype = 7
select * from products where id = 4
select * from CategoryProductLink where product = 4