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


UPDATE fine, (SELECT name, number_plate, violation
FROM fine
GROUP BY name, number_plate, violation
HAVING COUNT(fine.violation)>1) AS new_query
SET fine.sum_fine = fine.sum_fine*2
WHERE fine.date_payment IS NULL AND fine.name=new_query.name;


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

/* Вложенные запросы в операторах соединения */
SELECT book.title, name_author, name_genre, book.price, book.amount
FROM
    author
    INNER JOIN book ON author.author_id = book.author_id
    INNER JOIN genre ON  book.genre_id = genre.genre_id
GROUP BY book.title, name_author,name_genre, genre.genre_id, book.price, book.amount
HAVING genre.genre_id IN
         (/* выбираем автора, если он пишет книги в самых популярных жанрах*/
          SELECT query_in_1.genre_id
          FROM
              ( /* выбираем код жанра и количество произведений, относящихся к нему */
                SELECT genre_id, SUM(amount) AS sum_amount
                FROM book
                GROUP BY genre_id
               )query_in_1
          INNER JOIN
              ( /* выбираем запись, в которой указан код жанр с максимальным количеством книг */
                SELECT genre_id, SUM(amount) AS sum_amount
                FROM book
                GROUP BY genre_id
                ORDER BY sum_amount DESC
                LIMIT 1
               ) query_in_2
          ON query_in_1.sum_amount= query_in_2.sum_amount
         )
ORDER BY 1;


/* TODO: изменить данные в таблице supply перед последующим объединением */

/* Операция соединение, использование USING() */
SELECT book.title AS "Название", name_author AS "Автор", supply.amount+book.amount AS "Количество"
FROM author
    INNER JOIN book USING (author_id)
    INNER JOIN supply ON book.title = supply.title
                         and author.name_author = supply.author
                         and book.price = supply.price;

/* -------------------- Запросы корректировки, соединение таблиц -------------------- */

DROP TABLE IF EXISTS author;
CREATE TABLE author(
      author_id INTEGER PRIMARY KEY AUTOINCREMENT,
      name_author VARCHAR(50)
);

INSERT INTO author(name_author)
VALUES ('Булгаков М.А.'),
       ('Достоевский Ф.М.'),
       ('Есенин С.А.'),
       ('Пастернак Б.Л.'),
       ('Лермонтов М.Ю.');

DROP TABLE IF EXISTS genre;
CREATE TABLE genre (
      genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
      name_genre VARCHAR(50)
);

INSERT INTO genre(name_genre)
VALUES ('Роман'),
       ('Поэзия'),
       ('Приключения');

DROP TABLE IF EXISTS book;
CREATE TABLE book(
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(50),
    author_id INT,
    genre_id INT,
    price DECIMAL(8, 2),
    amount INT,
    FOREIGN KEY (author_id) REFERENCES author (author_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre (genre_id) ON DELETE SET NULL
);

INSERT INTO book(title,author_id,genre_id,price,amount)
VALUES ("Мастер и Маргарита",1,1,670.99,3),
       ("Белая гвардия",1,1,540.50,5),
       ("Идиот",2,1,460.00,10),
       ("Братья Карамазовы",2,1,799.01,3),
       ("Игрок",2,1,480.50,10),
       ("Стихотворения и поэмы",3,2,650.00,15),
       ("Черный человек",3,2,570.20,6),
       ("Лирика",4,2,518.99,2);

DROP TABLE IF EXISTS supply;
CREATE TABLE IF NOT EXISTS supply(
  supply_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  title VARCHAR(50),
  author VARCHAR(30),
  price DECIMAL(8, 2),
  amount INT
);

INSERT INTO supply(title, author, price, amount)
VALUES
    ("Доктор Живаго","Пастернак Б.Л.",380.80,4),
    ("Черный человек","Есенин С.А.",570.20,6),
    ("Белая гвардия", "Булгаков М.А.",540.50,7),
    ("Идиот", "Достоевский Ф.М.",360.80,3),
    ("Стихотворения и поэмы","Лермонтов М.Ю.",255.90,4),
    ("Остров сокровищ","Стивенсон Р.Л.",599.99,5);


/* запросы на обновление, связанные таблицы */
/* MySQL only*/
UPDATE book
     INNER JOIN author ON author.author_id = book.author_id
     INNER JOIN supply ON book.title = supply.title
                         and supply.author = author.name_author
SET book.amount = book.amount + supply.amount,
    supply.amount = 0,
    book.price = (book.price*book.amount+supply.price*supply.amount)/(book.amount+supply.amount)
WHERE book.price <> supply.price;
SELECT * FROM book;

/* запросы на добавление связанные таблицы */
/* MySQL only */
INSERT INTO author(name_author)
SELECT supply.author
FROM
    author
    RIGHT JOIN supply on author.name_author = supply.author
WHERE name_author IS NULL;

/* запрос на добавление связанные таблицы */
INSERT INTO book(title, author_id, price, amount)
SELECT title, author_id, price, amount
FROM
    author
    INNER JOIN supply ON author.name_author = supply.author
WHERE amount <> 0;
SELECT * FROM book;

/* запрос на обновление, вложенные запросы */
UPDATE book
SET genre_id =
      (
       SELECT genre_id
       FROM genre
       WHERE name_genre = 'Поэзия'
      )
WHERE title = "Стихотворения и поэмы" AND author_id = (SELECT author_id FROM author WHERE name_author = "Лермонтов М.Ю.");
UPDATE book
SET genre_id =
      (
       SELECT genre_id
       FROM genre
       WHERE name_genre = 'Приключения'
      )
WHERE title = "Остров сокровищ" AND author_id = (SELECT author_id FROM author WHERE name_author = "Стивенсон Р.Л.");
SELECT * FROM book;

/* каскадное удаление записей связанных таблиц */
DELETE FROM author
WHERE author_id IN (SELECT author_id
                      FROM book
                      GROUP BY author_id
                      HAVING SUM(amount) < 20
                     );
SELECT * FROM book;

/* удаление записей главной таблицы с сохранением записей в зависимой */
DELETE FROM genre
WHERE genre_id IN (SELECT genre_id
                      FROM book
                      GROUP BY genre_id
                      HAVING COUNT(title) < 4
                     );

/* удаление записей, использование связанных таблиц */
DELETE FROM author
USING book
      INNER JOIN author ON author.author_id = book.author_id
WHERE book.genre_id=(SELECT genre_id FROM genre WHERE name_genre="Поэзия");


/* -------------------- База данных "Интернет-магазин книг", запросы на выборку -------------------- */

/* запросы на основе трёх и более связанных таблиц */
SELECT buy.buy_id, book.title, book.price, buy_book.amount
FROM
    client
    INNER JOIN buy ON client.client_id = buy.client_id
    INNER JOIN buy_book ON buy_book.buy_id = buy.buy_id
    INNER JOIN book ON buy_book.book_id=book.book_id
WHERE client.name_client = "Баранов Павел"
ORDER BY buy.buy_id, book.title;


SELECT author.name_author, book.title, COUNT(buy_book.buy_id) AS "Количество"
FROM
    buy_book
    RIGHT JOIN book ON book.book_id = buy_book.book_id
    INNER JOIN author ON book.author_id = author.author_id
GROUP BY book.title, author.name_author
ORDER BY author.name_author, book.title;


SELECT city.name_city, COUNT(buy.buy_id) AS "Количество"
FROM buy
      INNER JOIN client ON buy.client_id = client.client_id
      INNER JOIN city ON client.city_id = city.city_id
GROUP BY city.name_city
ORDER BY 2 DESC, 1;


SELECT buy_step.buy_id, buy_step.date_step_end
FROM buy_step
      INNER JOIN step ON step.step_id = buy_step.step_id
WHERE step.step_id = 1 AND buy_step.date_step_end IS NOT NULL;


SELECT buy.buy_id, client.name_client, SUM(buy_book.amount*book.price) AS "Стоимость"
FROM buy_book
      INNER JOIN book ON buy_book.book_id = book.book_id
      INNER JOIN buy ON buy_book.buy_id = buy.buy_id
      INNER JOIN client ON buy.client_id = client.client_id
GROUP BY buy_book.buy_id
ORDER BY 1;


SELECT buy_step.buy_id, step.name_step
FROM buy_step
      INNER JOIN step ON buy_step.step_id = step.step_id
WHERE buy_step.date_step_beg IS NOT NULL AND buy_step.date_step_end IS NULL
ORDER BY 1;


SELECT buy.buy_id, DATEDIFF(buy_step.date_step_end, buy_step.date_step_beg) AS "Количество_дней", IF(DATEDIFF(buy_step.date_step_end, buy_step.date_step_beg)>city.days_delivery,DATEDIFF(buy_step.date_step_end, buy_step.date_step_beg)-city.days_delivery,0) AS "Опоздание"
FROM buy_step
     INNER JOIN buy ON buy_step.buy_id=buy.buy_id
     INNER JOIN client ON buy.client_id=client.client_id
     INNER JOIN city ON client.city_id=city.city_id
     INNER JOIN step ON buy_step.step_id=step.step_id
WHERE step.name_step = "Транспортировка" AND buy_step.date_step_end IS NOT NULL;


SELECT DISTINCT client.name_client
FROM buy_book
     INNER JOIN book ON buy_book.book_id=book.book_id
     INNER JOIN author ON book.author_id=author.author_id
     INNER JOIN buy ON buy_book.buy_id=buy.buy_id
     INNER JOIN client ON buy.client_id=client.client_id
WHERE author.name_author = "Достоевский Ф.М."
ORDER BY 1;


SELECT genre.name_genre, SUM(buy_book.amount) AS "Количество"
FROM buy_book
     INNER JOIN book ON buy_book.book_id=book.book_id
     INNER JOIN genre ON book.genre_id=genre.genre_id
GROUP BY genre.name_genre
HAVING SUM(buy_book.amount) = (SELECT MAX(sum_amount)
                               FROM (SELECT SUM(buy_book.amount) AS sum_amount
                                     FROM buy_book
                                          INNER JOIN book ON buy_book.book_id=book.book_id
                                          INNER JOIN genre ON book.genre_id=genre.genre_id
                                     GROUP BY genre.name_genre) query_in);


SELECT YEAR(buy_archive.date_payment) AS "Год", MONTHNAME(buy_archive.date_payment) AS "Месяц", SUM(buy_archive.price*buy_archive.amount) AS "Сумма"
FROM
    buy_archive
GROUP BY YEAR(buy_archive.date_payment), MONTHNAME(buy_archive.date_payment)
UNION ALL
SELECT YEAR(buy_step.date_step_end), MONTHNAME(buy_step.date_step_end), SUM(book.price*buy_book.amount)
FROM
    book
    INNER JOIN buy_book USING(book_id)
    INNER JOIN buy USING(buy_id)
    INNER JOIN buy_step USING(buy_id)
    INNER JOIN step USING(step_id)
WHERE buy_step.date_step_end IS NOT Null and step.name_step = "Оплата"
GROUP BY YEAR(buy_step.date_step_end), MONTHNAME(buy_step.date_step_end)
ORDER BY 2,1;


SELECT Название AS title, SUM(Количество) AS "Количество", SUM(Количество*Цена) AS "Сумма" FROM
(SELECT book.title AS "Название", buy_archive.amount AS "Количество", buy_archive.price AS "Цена"
FROM buy_archive
     INNER JOIN book ON buy_archive.book_id=book.book_id
UNION ALL
SELECT book.title, buy_book.amount, book.price
FROM
    book
    INNER JOIN buy_book USING(book_id)
    INNER JOIN buy USING(buy_id)
    INNER JOIN buy_step USING(buy_id)
    INNER JOIN step USING(step_id)
WHERE buy_step.date_step_end IS NOT Null and step.name_step = "Оплата") query_in
GROUP BY Название
ORDER BY 3 DESC;


/* -------------------- База данных "Интернет-магазин книг", запросы корректировки -------------------- */

INSERT INTO client(name_client, city_id, email)
SELECT "Попов Илья", city_id, "popov@test"
FROM city
WHERE name_city LIKE "Москва";


INSERT INTO buy(buy_description, client_id)
SELECT "Связаться со мной по вопросу доставки", client_id
FROM client
WHERE name_client = "Попов Илья";


INSERT INTO buy_book(buy_id, book_id, amount)
SELECT 5, book_id, 2
FROM book
WHERE author_id = (SELECT author_id FROM author WHERE name_author = "Пастернак Б.Л.") AND title="Лирика";
INSERT INTO buy_book(buy_id, book_id, amount)
SELECT 5, book_id, 1
FROM book
WHERE author_id = (SELECT author_id FROM author WHERE name_author = "Булгаков М.А.") AND title="Белая гвардия";


UPDATE book, buy_book
SET book.amount = book.amount - buy_book.amount
WHERE buy_book.buy_id = 5 AND book.book_id = buy_book.book_id;
SELECT * FROM book;


CREATE TABLE buy_pay AS
SELECT book.title, author.name_author, book.price, buy_book.amount, buy_book.amount*book.price AS Стоимость
FROM buy_book
     INNER JOIN book ON buy_book.book_id=book.book_id
     INNER JOIN author ON book.author_id=author.author_id
WHERE buy_book.buy_id=5
ORDER BY book.title;
SELECT * FROM buy_pay;


CREATE TABLE buy_pay AS
SELECT buy_book.buy_id, SUM(buy_book.amount) AS Количество, SUM(buy_book.amount*book.price) AS Итого
FROM buy_book
     INNER JOIN book ON buy_book.book_id=book.book_id
GROUP BY buy_book.buy_id
HAVING buy_book.buy_id=5;
SELECT * FROM buy_pay;


INSERT INTO buy_step(buy_id, step_id, date_step_beg, date_step_end)
SELECT buy.buy_id, step.step_id, NULL, NULL
FROM step CROSS JOIN buy
WHERE buy.buy_id=5;
SELECT * FROM buy_step;


UPDATE buy_step
SET date_step_beg="2020-04-12"
WHERE buy_id=5 AND step_id=1;
SELECT * FROM buy_step
WHERE buy_id=5;


UPDATE buy_step
SET date_step_end="2020-04-13"
WHERE buy_id=5 AND step_id=(SELECT step_id
                            FROM step
                            WHERE name_step = 'Оплата');
UPDATE buy_step
SET date_step_beg="2020-04-13"
WHERE buy_id=5 AND step_id=(SELECT step_id + 1
                            FROM step
                            WHERE name_step = 'Оплата');
SELECT * FROM buy_step
WHERE buy_id=5;


/* -------------------- База данных "Тестирование", запросы на выборку -------------------- */

SELECT student.name_student, attempt.date_attempt, attempt.result
FROM attempt
     INNER JOIN student ON attempt.student_id=student.student_id
     INNER JOIN subject ON attempt.subject_id=subject.subject_id
WHERE subject.name_subject="Основы баз данных"
ORDER BY 3 DESC;


SELECT subject.name_subject, COUNT(attempt.attempt_id) AS "Количество", ROUND(AVG(attempt.result),2) AS "Среднее"
FROM attempt
     RIGHT JOIN subject ON attempt.subject_id=subject.subject_id
GROUP BY subject.name_subject
ORDER BY 3 DESC;


SELECT DISTINCT student.name_student, attempt.result
FROM attempt
     INNER JOIN student ON attempt.student_id=student.student_id
WHERE attempt.result = (SELECT MAX(result)
                        FROM attempt)
ORDER BY 1;


SELECT student.name_student, subject.name_subject, DATEDIFF(MAX(attempt.date_attempt),MIN(attempt.date_attempt)) AS "Интервал"
FROM attempt
     INNER JOIN student ON attempt.student_id=student.student_id
     INNER JOIN subject ON attempt.subject_id=subject.subject_id
GROUP BY student.name_student, subject.name_subject
HAVING Интервал > 0
ORDER BY 3;


SELECT subject.name_subject, COUNT(DISTINCT attempt.student_id) AS "Количество"
FROM attempt
     RIGHT JOIN subject ON attempt.subject_id=subject.subject_id
GROUP BY subject.name_subject
ORDER BY 2 DESC, 1;


SELECT question.question_id, question.name_question
FROM question
     INNER JOIN subject ON question.subject_id=subject.subject_id
WHERE subject.name_subject="Основы баз данных"
ORDER BY RAND()
LIMIT 3;


SELECT question.name_question, answer.name_answer, IF(answer.is_correct, "Верно", "Неверно") AS "Результат"
FROM testing
     INNER JOIN question ON testing.question_id=question.question_id
     INNER JOIN answer ON testing.answer_id=answer.answer_id
WHERE testing.attempt_id=7;


SELECT student.name_student, subject.name_subject, attempt.date_attempt, ROUND(SUM(answer.is_correct)/3*100,2) AS "Результат"
FROM testing
     INNER JOIN attempt ON testing.attempt_id=attempt.attempt_id
     INNER JOIN student ON attempt.student_id=student.student_id
     INNER JOIN subject ON attempt.subject_id=subject.subject_id
     INNER JOIN answer ON testing.answer_id=answer.answer_id
GROUP BY student.name_student, subject.name_subject, attempt.date_attempt
ORDER BY 1, 3 DESC;


SELECT subject.name_subject, CONCAT(LEFT(question.name_question,30),"...") AS "Вопрос", COUNT(answer.is_correct) AS "Всего_ответов", ROUND(SUM(answer.is_correct)/COUNT(answer.is_correct)*100,2) AS "Успешность"
FROM answer
     INNER JOIN question ON answer.question_id=question.question_id
     RIGHT JOIN subject ON question.subject_id=subject.subject_id
     INNER JOIN testing ON answer.answer_id=testing.answer_id
GROUP BY subject.name_subject, question.name_question
ORDER BY 1, 4 DESC, 2;

/* -------------------- База данных "Тестирование", запросы корректировки -------------------- */

INSERT INTO attempt(student_id, subject_id, date_attempt)
SELECT (SELECT student_id FROM student WHERE student.name_student="Баранов Павел"),
        (SELECT subject_id FROM subject WHERE subject.name_subject="Основы баз данных"),
        NOW();
SELECT * FROM attempt;


INSERT INTO testing(attempt_id, question_id)
SELECT attempt.attempt_id, question.question_id
FROM attempt
     INNER JOIN question ON attempt.subject_id=question.subject_id
WHERE attempt.attempt_id = (SELECT MAX(attempt_id)
                           FROM attempt)
ORDER BY RAND()
LIMIT 3;
SELECT * FROM testing;


UPDATE attempt
SET attempt.result=(SELECT ROUND(SUM(answer.is_correct)/COUNT(answer.answer_id)*100,0)
                   FROM testing
                        INNER JOIN answer ON testing.answer_id=answer.answer_id
                   WHERE testing.attempt_id=8)
WHERE attempt.attempt_id=8;
SELECT * FROM attempt;

DELETE FROM attempt
WHERE DATEDIFF(attempt.date_attempt, "2020-05-01") < 0;
SELECT * FROM attempt;
SELECT * FROM testing;

/* -------------------- База данных "Абитуриент", запросы на выборку -------------------- */

SELECT enrollee.name_enrollee
FROM program_enrollee
     INNER JOIN program ON program_enrollee.program_id=program.program_id
     INNER JOIN enrollee ON program_enrollee.enrollee_id=enrollee.enrollee_id
WHERE program.name_program="Мехатроника и робототехника"
ORDER BY 1;


SELECT program.name_program
FROM program_subject
     INNER JOIN program ON program_subject.program_id=program.program_id
     INNER JOIN subject ON program_subject.subject_id=subject.subject_id
WHERE subject.name_subject="Информатика"
ORDER BY 1 DESC;


SELECT subject.name_subject, COUNT(enrollee_subject.enrollee_id) AS "Количество", MAX(enrollee_subject.result) AS "Максимум", MIN(enrollee_subject.result) AS "Минимум", ROUND(AVG(enrollee_subject.result), 1) AS "Среднее"
FROM enrollee_subject
     INNER JOIN subject ON enrollee_subject.subject_id=subject.subject_id
GROUP BY 1
ORDER BY 1;


SELECT program.name_program
FROM program_subject
     INNER JOIN program ON program_subject.program_id=program.program_id
GROUP BY program.name_program
HAVING MIN(program_subject.min_result) >= 40
ORDER BY 1;


SELECT program.name_program, program.plan
FROM program
WHERE program.plan = (SELECT MAX(program.plan)
                     FROM program);


SELECT enrollee.name_enrollee, IF(SUM(achievement.bonus) IS NULL, 0, SUM(achievement.bonus)) AS "Бонус"
FROM enrollee_achievement
     RIGHT JOIN enrollee ON enrollee_achievement.enrollee_id=enrollee.enrollee_id
     LEFT JOIN achievement ON enrollee_achievement.achievement_id=achievement.achievement_id
GROUP BY enrollee.name_enrollee
ORDER BY 1;


SELECT department.name_department, program.name_program, program.plan, COUNT(program_enrollee.program_enrollee_id) AS "Количество", ROUND(COUNT(program_enrollee.program_enrollee_id)/program.plan,2) AS "Конкурс"
FROM program_enrollee
     INNER JOIN program ON program_enrollee.program_id=program.program_id
     INNER JOIN department ON program.department_id=department.department_id
GROUP BY department.name_department, program.name_program, program.plan
ORDER BY 5 DESC;


SELECT DISTINCT program.name_program
FROM program_subject
     INNER JOIN subject ON program_subject.subject_id=subject.subject_id
     INNER JOIN program ON program_subject.program_id=program.program_id
WHERE subject.name_subject IN ("Информатика", "Математика")
GROUP BY program.name_program
HAVING COUNT(subject.name_subject)=2
ORDER BY 1;


SELECT program.name_program, enrollee.name_enrollee, SUM(enrollee_subject.result) AS "itog"
FROM enrollee
     INNER JOIN program_enrollee ON enrollee.enrollee_id=program_enrollee.enrollee_id
     INNER JOIN program ON program_enrollee.program_id=program.program_id
     INNER JOIN program_subject ON program.program_id=program_subject.program_id
     INNER JOIN subject ON program_subject.subject_id=subject.subject_id
     INNER JOIN enrollee_subject ON subject.subject_id=enrollee_subject.subject_id AND enrollee_subject.enrollee_id=enrollee.enrollee_id
GROUP BY program.name_program, enrollee.name_enrollee
ORDER BY 1, 3 DESC;


SELECT program.name_program, enrollee.name_enrollee
FROM enrollee
     INNER JOIN program_enrollee ON enrollee.enrollee_id=program_enrollee.enrollee_id
     INNER JOIN program ON program_enrollee.program_id=program.program_id
     INNER JOIN program_subject ON program.program_id=program_subject.program_id
     INNER JOIN subject ON program_subject.subject_id=subject.subject_id
     INNER JOIN enrollee_subject ON subject.subject_id=enrollee_subject.subject_id AND enrollee_subject.enrollee_id=enrollee.enrollee_id
WHERE enrollee_subject.result<program_subject.min_result
GROUP BY 1,2
ORDER BY 1,2;

/* -------------------- База данных "Абитуриент", запросы корректировки -------------------- */

CREATE TABLE applicant AS
SELECT program.program_id, enrollee.enrollee_id, SUM(enrollee_subject.result) AS "itog"
FROM enrollee
     INNER JOIN program_enrollee ON enrollee.enrollee_id=program_enrollee.enrollee_id
     INNER JOIN program ON program_enrollee.program_id=program.program_id
     INNER JOIN program_subject ON program.program_id=program_subject.program_id
     INNER JOIN subject ON program_subject.subject_id=subject.subject_id
     INNER JOIN enrollee_subject ON subject.subject_id=enrollee_subject.subject_id AND enrollee_subject.enrollee_id=enrollee.enrollee_id
GROUP BY program.program_id, enrollee.enrollee_id
ORDER BY 1, 3 DESC;
SELECT * FROM applicant;


DELETE FROM applicant
USING applicant
      INNER JOIN program_subject ON applicant.program_id=program_subject.program_id
      INNER JOIN enrollee_subject ON applicant.enrollee_id=enrollee_subject.enrollee_id AND enrollee_subject.subject_id=program_subject.subject_id
WHERE enrollee_subject.result<program_subject.min_result;
SELECT * FROM applicant;


UPDATE applicant
       INNER JOIN (SELECT enrollee.enrollee_id, IF(SUM(achievement.bonus) IS NULL, 0, SUM(achievement.bonus)) AS "Бонус"
FROM enrollee_achievement
     RIGHT JOIN enrollee ON enrollee_achievement.enrollee_id=enrollee.enrollee_id
     LEFT JOIN achievement ON enrollee_achievement.achievement_id=achievement.achievement_id
GROUP BY enrollee.enrollee_id
ORDER BY 1) query_in ON applicant.enrollee_id = query_in.enrollee_id
SET applicant.itog=applicant.itog+query_in.Бонус;
SELECT * FROM applicant;


CREATE TABLE applicant_order AS
SELECT program_id, enrollee_id, itog
FROM applicant
ORDER BY 1, 3 DESC;
DROP TABLE applicant;
SELECT * FROM applicant_order;


ALTER TABLE applicant_order ADD str_id INTEGER FIRST;


SET @num_pr := 1;
SET @row_num := 0;
UPDATE applicant_order
SET str_id = IF(program_id = @num_pr, @row_num := @row_num + 1, @row_num := 1 AND @num_pr := program_id);
SELECT * FROM applicant_order;


CREATE TABLE student AS
SELECT program.name_program, enrollee.name_enrollee, applicant_order.itog
FROM applicant_order
     INNER JOIN enrollee ON applicant_order.enrollee_id=enrollee.enrollee_id
     INNER JOIN program ON applicant_order.program_id=program.program_id
WHERE applicant_order.str_id<=program.plan
ORDER BY 1, 3 DESC;
SELECT * FROM student;


/* -------------------- База данных "Учебная аналитика по курсу", -------------------- */


/* -------------------- База данных "Интернет-магазин книг", часть 1 -------------------- */


/* -------------------- База данных "Интернет-магазин книг", часть 2 -------------------- */


/* -------------------- База данных "Интернет-магазин книг", часть 3 -------------------- */


/* -------------------- База данных "Тестирование" -------------------- */
