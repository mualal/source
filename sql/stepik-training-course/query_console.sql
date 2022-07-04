/* -------------------- Отношение (таблица) -------------------- */

/* table creation */
CREATE TABLE book(
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    /*
    but in MySQL:
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    */
    title VARCHAR(50),
    author VARCHAR(30),
    price DECIMAL(8, 2),
    amount INT
);

/* insertion to table */
INSERT INTO book(title,author,price,amount)
VALUES ("Мастер и Маргарита","Булгаков М.А.", 670.99,3);

INSERT INTO book(title,author,price,amount)
VALUES ("Белая гвардия","Булгаков М.А.", 540.50,5);

INSERT INTO book(title,author,price,amount)
VALUES ("Идиот","Достоевский Ф.М.", 460.00,10);

INSERT INTO book(title,author,price,amount)
VALUES ("Братья Карамазовы","Достоевский Ф.М.", 799.01,2);

INSERT INTO book(title,author,price,amount)
VALUES ("Стихотворения и поэмы","Есенин С.А.", 650.00,15);

/* -------------------- Выборка данных -------------------- */

/* entire table selection */
SELECT * FROM book;

/* only certain columns selection */
SELECT author, title, price FROM book;

/* renaming during selection */
SELECT title as Название, author AS Автор
FROM book;

/* create computing column during selection */
SELECT title,amount,amount*1.65 AS pack
FROM book;

/* computing with ROUND function */
SELECT title,author,amount,ROUND(price*0.7,2) AS new_price
FROM book;

/* computing with condition */
SELECT author,title,
IIF(author = "Булгаков М.А.",ROUND(price*1.1,2),IIF(author = "Есенин С.А.", ROUND(price*1.05,2),price)) AS new_price
/* but in MySQL: change IIF with IF */
FROM book;

/* selection with condition */
SELECT author,title,price
FROM book
WHERE amount < 10;

/* more interesting selection with condition */
SELECT title,author,price,amount
FROM book
WHERE (price<500 OR price>600) and amount*price >= 5000;

/* selection with BETWEEN and IN conditions */
SELECT title,author
FROM book
WHERE (price BETWEEN 540.50 AND 800) AND amount IN (2,3,5,7);

/* selection with ordering */
SELECT author,title
FROM book
WHERE (amount BETWEEN 2 AND 14)
ORDER BY author DESC, title ASC;

/* selection with similarities finder */
SELECT title,author
FROM book
WHERE title LIKE "_% _%" and author LIKE "%С.%"
ORDER BY title ASC;

/* dummy query */
SELECT author as "Автор книги",title as "Название книги",price*1.2 as "Новая цена книги"
FROM book
ORDER BY author ASC;

/* -------------------- Запросы, групповые операции -------------------- */

/* select distinct */
SELECT amount
FROM book
GROUP BY amount;


SELECT author AS "Автор", COUNT(amount) AS Различных_книг, SUM(amount) AS Количество_экземпляров
FROM book
GROUP BY author;


SELECT author, MIN(price) AS Минимальная_цена, MAX(price) AS Максимальная_цена, AVG(price) AS Средняя_цена
FROM book
GROUP BY author;


SELECT author, SUM(price*amount) AS Стоимость, ROUND((SUM(price*amount)*0.18)/1.18,2) AS НДС, ROUND(SUM(price*amount)/1.18,2) AS Стоимость_без_НДС
FROM book
GROUP BY author;


SELECT MIN(price) AS Минимальная_цена, MAX(price) AS Максимальная_цена, ROUND(AVG(price),2) AS Средняя_цена
FROM book;


SELECT ROUND(AVG(price),2) AS Средняя_цена, SUM(price*amount) AS Стоимость
FROM book
WHERE amount BETWEEN 5 and 14;


SELECT author, SUM(price*amount) AS Стоимость
FROM book
WHERE title <> "Идиот" and title <> "Белая гвардия"
GROUP BY author
HAVING SUM(price*amount)>5000
ORDER BY Стоимость DESC;


SELECT author, SUM(price*amount) AS Стоимость
FROM book
WHERE title <> "Идиот" and title <> "Белая гвардия"
GROUP BY author
HAVING SUM(price*amount)>1000 and MIN(price)<900
ORDER BY Стоимость DESC;


/* -------------------- Вложенные запросы -------------------- */


SELECT author, title, price
FROM book
WHERE price <= (
		SELECT AVG(price)
        FROM book
	)
ORDER BY price DESC;


SELECT author, title, price
FROM book
WHERE price - (SELECT MIN(price) from book) <= 150
ORDER BY price ASC;


SELECT author, title, amount
FROM book
WHERE amount IN (
		SELECT amount
        FROM book
        GROUP BY amount
        HAVING COUNT(amount) = 1
		);

/* ANY keyword only for MySQL queries
SELECT author, title, price
FROM book
WHERE price < ANY (
		SELECT MIN(price)
        FROM book
        GROUP BY author
	);
*/

SELECT title, author, amount, (SELECT MAX(amount) FROM book) - amount as Заказ
FROM book
WHERE amount <> (SELECT MAX(amount) FROM book);


SELECT title, author, amount, (SELECT MAX(amount)+1 FROM book) - amount as Заказ
FROM book;


/* -------------------- Запросы корректировки данных -------------------- */

/* table creation */
CREATE TABLE supply(
	supply_id INTEGER PRIMARY KEY AUTOINCREMENT,
	/*
	but in MySQL:
	supply_id INT PRIMARY KEY AUTO_INCREMENT,
	*/
    title VARCHAR(50),
    author VARCHAR(30),
    price DECIMAL(8, 2),
    amount INT
);

/* insertion to table */
INSERT INTO supply(title,author,price,amount)
VALUES
	('Лирика','Пастернак Б.Л.', 518.99,2),
    ('Черный человек','Есенин С.А.',570.20,6),
    ('Белая гвардия','Булгаков М.А.',540.50,7),
    ('Идиот','Достоевский Ф.М.',360.80,3);
SELECT * FROM supply;

/* insertion to table from another table */
INSERT INTO book(title,author,price,amount)
SELECT title,author,price,amount
FROM supply
WHERE author != 'Булгаков М.А.' AND author != 'Достоевский Ф.М.';
SELECT * FROM book;

/* insertion to table from another table */
INSERT INTO book(title,author,price,amount)
SELECT title,author,price,amount
FROM supply
WHERE author NOT IN (
		SELECT author
        FROM book
        );
SELECT * FROM book;

/* update query */
UPDATE book
SET price=0.9*price
WHERE amount BETWEEN 5 AND 10;
SELECT * FROM book;

/* create new column in table */
ALTER TABLE book
ADD buy INT;
SELECT * FROM book;

/* update values in newly created column */
UPDATE book
SET buy=0
WHERE title="Мастер и Маргарита";
UPDATE book
SET buy=3
WHERE title="Белая гвардия";
UPDATE book
SET buy=8
WHERE title="Идиот";
UPDATE book
SET buy=0
WHERE title="Братья Карамазовы";
UPDATE book
SET buy=18
WHERE title="Стихотворения и поэмы";
UPDATE book
SET buy=0
WHERE title="Лирика";
UPDATE book
SET buy=0
WHERE title="Чёрный человек";
SELECT * FROM book;

/* update values in column with condition */
UPDATE book
SET buy = IIF(buy>amount,amount,buy);
/*
but in MySQL:
supply_id INT PRIMARY KEY AUTO_INCREMENT,
*/
UPDATE book
SET price=0.9*price
WHERE buy=0;
SELECT * FROM book;

SELECT * FROM supply;

/* MySQL only
UPDATE book, supply
SET book.amount = book.amount + supply.amount
WHERE book.title = supply.title AND book.author = supply.author;

UPDATE book, supply
SET book.price = (book.price + supply.price) / 2
WHERE book.title = supply.title AND book.author = supply.author;
SELECT * FROM book;
*/

DELETE FROM supply
WHERE author in (SELECT author FROM book GROUP BY author HAVING SUM(amount)>10);
SELECT * FROM supply;


CREATE TABLE ordering AS
SELECT author, title,
   (
    SELECT ROUND(AVG(amount))
    FROM book
   ) AS amount
FROM book
WHERE amount < (SELECT ROUND(AVG(amount)) FROM book);

SELECT * FROM ordering;

/* -------------------- Таблица "Командировки", запросы на выборку -------------------- */

/* -------------------- Таблица "Нарушения ПДД", запросы корректировки -------------------- */


