/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
SELECT
    category.name,
    COUNT(film_category.film_id) AS film_count
FROM
    category
INNER JOIN film_category ON category.category_id = film_category.category_id
GROUP BY
    category.name
ORDER BY
    film_count DESC;


/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
SELECT
    COUNT(rental.rental_id) AS rental_count,
    CONCAT(actor.first_name, ', ', actor.last_name) AS actor_full_name
FROM actor
INNER JOIN
    film_actor ON actor.actor_id = film_actor.actor_id
INNER JOIN
    film ON film.film_id = film_actor.film_id
INNER JOIN
    inventory ON film.film_id = inventory.film_id
INNER JOIN
    rental ON inventory.inventory_id = rental.inventory_id
GROUP BY
    actor.actor_id,
    actor_full_name
ORDER BY
    rental_count DESC
LIMIT 10;

SELECT actor.actor_id, actor.first_name, actor.last_name, COUNT(film_actor.film_id) AS film_count
FROM actor
JOIN film_actor ON actor.actor_id = film_actor.actor_id
GROUP BY actor.actor_id, actor.first_name, actor.last_name
ORDER BY film_count DESC
LIMIT 10;


/*
3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
-- SQL code goes here...



/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
-- SQL code goes here...


/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
-- SQL code goes here...
