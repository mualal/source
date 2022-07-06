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


CREATE TABLE trip(
	trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
	/*
	but in MySQL:
	trip_id INT PRIMARY KEY AUTO_INCREMENT,
	*/
	name VARCHAR(30),
	city VARCHAR(25),
	per_diem DECIMAL(8, 2),
	date_first DATE,
	date_last DATE
);


INSERT INTO trip(name, city, per_diem, date_first, date_last)
VALUES
	('Баранов П.Е.', 'Москва', 700, '2020-01-12', '2020-01-17'),
	('Абрамова К.А.', 'Владивосток', 450, '2020-01-14', '2020-01-27'),
	('Семенов И.В.', 'Москва', 700, '2020-01-23', '2020-01-31'),
	('Ильиных Г.Р.', 'Владивосток', 450, '2020-01-12', '2020-02-02'),
	('Колесов С.П.', 'Москва', 700, '2020-02-01', '2020-02-06'),
	('Баранов П.Е.', 'Москва', 700, '2020-02-14', '2020-02-22'),
	('Абрамова К.А.', 'Москва', 700, '2020-02-23', '2020-03-01'),
	('Лебедев Т.К.', 'Москва', 700, '2020-03-03', '2020-03-06'),
	('Колесов С.П.', 'Новосибирск', 450, '2020-02-27', '2020-03-12'),
	('Семенов И.В.', 'Санкт-Петербург', 700, '2020-03-29', '2020-04-05'),
	('Абрамова К.А.', 'Москва', 700, '2020-04-06', '2020-04-14'),
	('Баранов П.Е.', 'Новосибирск', 450, '2020-04-18', '2020-05-04'),
	('Лебедев Т.К.', 'Томск', 450, '2020-05-20', '2020-05-31'),
	('Семенов И.В.', 'Санкт-Петербург', 700, '2020-06-01', '2020-06-03'),
	('Абрамова К.А.', 'Санкт-Петербург', 700, '2020-05-28', '2020-06-04'),
	('Федорова А.Ю.', 'Новосибирск', 450, '2020-05-25', '2020-06-04'),
	('Колесов С.П.', 'Новосибирск', 450, '2020-06-03', '2020-06-12'),
	('Федорова А.Ю.', 'Томск', 450, '2020-06-20', '2020-06-26'),
	('Абрамова К.А.', 'Владивосток', 450, '2020-07-02', '2020-07-13'),
	('Баранов П.Е.', 'Воронеж', 450, '2020-07-19', '2020-07-25');

SELECT * FROM trip;


SELECT name, city, per_diem, date_first, date_last
FROM trip
WHERE name LIKE "%а _._."
ORDER BY date_last DESC;


SELECT DISTINCT name
FROM trip
WHERE city = "Москва"
ORDER BY name;


SELECT city, COUNT(city) as "Количество"
FROM trip
GROUP BY city
ORDER BY city;


SELECT city, COUNT(city) as "Количество"
FROM trip
GROUP BY city
ORDER BY 2 DESC
LIMIT 2;


SELECT name, city, JULIANDAY(date_last)-JULIANDAY(date_first)+1 AS "Длительность"
/*
but in MySQL:
SELECT name, city, DATEDIFF(date_last, date_first)+1 AS "Длительность"
*/
FROM trip
WHERE city <> "Москва" AND city <> "Санкт-Петербург"
ORDER BY 3 DESC, 2 DESC;


SELECT name, city, date_first, date_last
FROM trip
WHERE JULIANDAY(date_last)-JULIANDAY(date_first) = (SELECT MIN(JULIANDAY(date_last)-JULIANDAY(date_first)) FROM trip)
/*
but in MySQL:
WHERE DATEDIFF(date_last, date_first) = (SELECT MIN(DATEDIFF(date_last, date_first)) FROM trip)
*/


/* MySQL only
SELECT name, city, date_first, date_last
FROM trip
WHERE MONTH(date_first) = MONTH(date_last)
ORDER BY city, name;
*/


/* MySQL only
SELECT MONTHNAME(date_first) AS "Месяц", COUNT(MONTHNAME(date_first)) AS "Количество"
FROM trip
GROUP BY MONTHNAME(date_first)
ORDER BY 2 DESC, 1;
*/


/* MySQL only
SELECT name, city, date_first, (DATEDIFF(date_last, date_first)+1)*per_diem AS "Сумма"
FROM trip
WHERE (MONTH(date_first) = 2 OR MONTH(date_first) = 3) AND YEAR(date_first) = 2020
ORDER BY name, 4 DESC;
*/


SELECT name, SUM((JULIANDAY(date_last)-JULIANDAY(date_first)+1)*per_diem) AS "Сумма"
/*
but in MySQL:
SELECT name, SUM((DATEDIFF(date_last, date_first)+1)*per_diem) AS "Сумма"
*/
FROM trip
GROUP BY name
HAVING COUNT(name)>3
ORDER BY 2 DESC;

/* -------------------- Таблица "Нарушения ПДД", запросы корректировки -------------------- */

CREATE TABLE fine(
    fine_id        INTEGER PRIMARY KEY AUTOINCREMENT,
/* but in MySQL:
    fine_id        INT PRIMARY KEY AUTO_INCREMENT,
*/
    name           VARCHAR(30),
    number_plate   VARCHAR(6),
    violation      VARCHAR(50),
    sum_fine       DECIMAL(8, 2),
    date_violation DATE,
    date_payment   DATE
);

CREATE TABLE traffic_violation(
    violation_id INTEGER PRIMARY KEY AUTOINCREMENT,
/* but in MySQL:
    violation_id INT PRIMARY KEY AUTO_INCREMENT,
*/
    violation    VARCHAR(50),
    sum_fine     DECIMAL(8, 2)
);

INSERT INTO fine(name, number_plate, violation, sum_fine, date_violation, date_payment)
values ('Баранов П.Е.', 'P523BT', 'Превышение скорости(от 40 до 60)', 500.00, '2020-01-12', '2020-01-17'),
       ('Абрамова К.А.', 'О111AB', 'Проезд на запрещающий сигнал', 1000.00, '2020-01-14', '2020-02-27'),
       ('Яковлев Г.Р.', 'T330TT', 'Превышение скорости(от 20 до 40)', 500.00, '2020-01-23', '2020-02-23'),
       ('Яковлев Г.Р.', 'M701AA', 'Превышение скорости(от 20 до 40)', NULL, '2020-01-12', NULL),
       ('Колесов С.П.', 'K892AX', 'Превышение скорости(от 20 до 40)', NULL, '2020-02-01', NULL),
       ('Баранов П.Е.', 'P523BT', 'Превышение скорости(от 40 до 60)', NULL, '2020-02-14', NULL),
       ('Абрамова К.А.', 'О111AB', 'Проезд на запрещающий сигнал', NULL, '2020-02-23', NULL),
       ('Яковлев Г.Р.', 'T330TT', 'Проезд на запрещающий сигнал', NULL, '2020-03-03', NULL);


INSERT INTO traffic_violation(violation, sum_fine)
VALUES ('Превышение скорости(от 20 до 40)', 500),
       ('Превышение скорости(от 40 до 60)', 1000),
       ('Проезд на запрещающий сигнал', 1000);

SELECT * FROM fine;

SELECT * FROM traffic_violation;

/* MySQL only
UPDATE fine, traffic_violation
SET fine.sum_fine = traffic_violation.sum_fine
WHERE fine.sum_fine IS NULL AND fine.violation = traffic_violation.violation;

SELECT * FROM fine;


SELECT name, number_plate, violation
FROM fine
GROUP BY name, number_plate, violation
HAVING COUNT(violation)>1


UPDATE fine, payment
SET fine.date_payment = payment.date_payment, fine.sum_fine = IF(DATEDIFF(payment.date_payment,fine.date_violation)<21,fine.sum_fine/2,fine.sum_fine)
WHERE fine.name = payment.name AND fine.number_plate = payment.number_plate AND fine.violation = payment.violation AND fine.date_payment IS NULL


CREATE TABLE back_payment AS
SELECT name, number_plate, violation, sum_fine, date_violation
FROM fine
WHERE date_payment is NULL


DELETE FROM fine
WHERE date_violation < "2020-02-01";
SELECT * FROM fine;
*/

/* -------------------- Связи между таблицами -------------------- */

/* Создание таблицы author с первичным ключом */
CREATE TABLE author(
/* but in MySQL:
    author_id INT PRIMARY KEY AUTO_INCREMENT,
*/
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_author VARCHAR(50)
);

/* Вставка значений в таблицу author */
INSERT INTO author(name_author)
VALUES ('Булгаков М.А.'),
       ('Достоевский Ф.М.'),
       ('Есенин С.А.'),
       ('Пастернак Б.Л.');

/* Создание таблицы genre с первичным ключом */
CREATE TABLE genre(
/* but in MySQL:
    genre_id INT PRIMARY KEY AUTO_INCREMENT,
*/
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_genre VARCHAR(30)
);

/* Вставка значений в таблицу genre */
INSERT INTO genre(name_genre)
VALUES ('Роман'),
       ('Поэзия'),
       ('Приключения');

/* Создание таблицы book с внешними ключами */
CREATE TABLE book(
/* but in MySQL:
    book_id INT PRIMARY KEY AUTO_INCREMENT,
*/
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(50),
    author_id INT NOT NULL,
    genre_id INT,
    price DECIMAL(8,2),
    amount INT,
    FOREIGN KEY (author_id) REFERENCES author (author_id),
    FOREIGN KEY (genre_id) REFERENCES genre (genre_id)
);

/* Создание таблицы book с внешними ключами и действиями при удалении записи главной таблицы */
CREATE TABLE book(
/* but in MySQL:
    book_id INT PRIMARY KEY AUTO_INCREMENT,
*/
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(50),
    author_id INT NOT NULL,
    genre_id INT,
    price DECIMAL(8,2),
    amount INT,
    FOREIGN KEY (author_id) REFERENCES author (author_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre (genre_id) ON DELETE SET NULL
);

/* Вставка значений в таблицу book */
INSERT INTO book(title, author_id, genre_id, price, amount)
VALUES ('Стихотворения и поэмы', 1, 1, 670.99, 3),
       ('Белая гвардия', 1, 1, 540.50, 5),
       ('Идиот', 2, 1, 460.00, 10),
       ('Братья Карамазовы', 2, 1, 799.01, 3),
       ('Игрок', 2, 1, 480.50, 10),
       ('Стихотворения и поэмы', 3, 2, 650.00, 15),
       ('Черный человек', 3, 2, 570.20, 6),
       ('Лирика', 4, 2, 518.99, 2);

/* -------------------- Запросы на выборку, соединение таблиц -------------------- */

/* Соединение INNER JOIN */
SELECT title, name_genre, price
FROM
    genre INNER JOIN book
    ON genre.genre_id = book.genre_id
WHERE amount > 8
ORDER BY price DESC;

/* Внешнее соединение LEFT и RIGHT OUTER JOIN */
SELECT name_genre
FROM genre LEFT JOIN book
     ON genre.genre_id = book.genre_id
WHERE title is NULL;

/* Перекрёстное соединение CROSS JOIN */
/* MySQL only
SELECT name_city, name_author, DATE_ADD('2020-01-01', INTERVAL FLOOR(RAND() * 365) DAY) AS "Дата"
FROM city CROSS JOIN author
ORDER BY name_city, 3 DESC;
*/

/* Запросы на выборку из нескольких таблиц */
SELECT name_genre, title, name_author
FROM genre
     INNER JOIN book ON genre.genre_id = book.genre_id
     INNER JOIN author ON book.author_id = author.author_id
WHERE name_genre LIKE "Роман"
ORDER BY title;

/* Запросы для нескольких таблиц с группировкой */
SELECT name_author, SUM(amount) AS "Количество"
FROM
    author LEFT JOIN book
    on author.author_id = book.author_id
GROUP BY name_author
HAVING SUM(amount)<10 OR SUM(amount) is NULL
ORDER BY 2;
/* TODO: здесь посмотреть подробнее вроде в SQLite и MySQL разные результаты - в MySQL появляется Лермонтов с NULL */

/* Запросы для нескольких таблиц со вложенными запросами */
SELECT name_author
FROM
    author INNER JOIN book
    on author.author_id = book.author_id
GROUP BY name_author
HAVING COUNT(DISTINCT genre_id)=1
ORDER BY name_author;

/* TODO: изменить данные в таблице supply перед последующим объединением */

/* Операция соединение, использование USING() */
SELECT book.title AS "Название", name_author AS "Автор", supply.amount+book.amount AS "Количество"
FROM author
    INNER JOIN book USING (author_id)
    INNER JOIN supply ON book.title = supply.title
                         and author.name_author = supply.author
                         and book.price = supply.price;

/* -------------------- Запросы корректировки, соединение таблиц -------------------- */


/* -------------------- База данных "Интернет-магазин книг", запросы на выборку -------------------- */


/* -------------------- База данных "Интернет-магазин книг", запросы корректировки -------------------- */


/* -------------------- База данных "Тестирование", запросы на выборку -------------------- */


/* -------------------- База данных "Тестирование", запросы корректировки -------------------- */


/* -------------------- База данных "Абитуриент", запросы на выборку -------------------- */


/* -------------------- База данных "Абитуриент", запросы корректировки -------------------- */


/* -------------------- База данных "Учебная аналитика по курсу", -------------------- */


/* -------------------- База данных "Интернет-магазин книг", часть 1 -------------------- */


/* -------------------- База данных "Интернет-магазин книг", часть 2 -------------------- */


/* -------------------- База данных "Интернет-магазин книг", часть 3 -------------------- */


/* -------------------- База данных "Тестирование" -------------------- */
