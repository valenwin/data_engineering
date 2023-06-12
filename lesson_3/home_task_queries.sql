/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
SELECT
    category.name AS category_name,
    COUNT(film_category.film_id) AS film_count
FROM
    category
INNER JOIN
        film_category
            ON category.category_id = film_category.category_id
GROUP BY
    category_name
ORDER BY
    film_count DESC;


/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
SELECT
    CONCAT(actor.first_name, ', ', actor.last_name) AS actor_full_name,
    COUNT(rental.rental_id) AS rental_count
FROM
    actor
INNER JOIN
        film_actor
            ON actor.actor_id = film_actor.actor_id
INNER JOIN
        film
            ON film.film_id = film_actor.film_id
INNER JOIN
        inventory
            ON film.film_id = inventory.film_id
INNER JOIN
        rental
            ON inventory.inventory_id = rental.inventory_id
GROUP BY
    actor.actor_id,
    actor_full_name
ORDER BY
    rental_count DESC
LIMIT 10;


/*
3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
SELECT
    category.name AS category_name,
    SUM(payment.amount) AS total_amount
FROM category
INNER JOIN
    film_category
        ON category.category_id = film_category.category_id
INNER JOIN
    film
        ON film_category.film_id = film.film_id
INNER JOIN
    inventory
        ON film.film_id = inventory.film_id
INNER JOIN
    rental
        ON inventory.inventory_id = rental.inventory_id
INNER JOIN
    payment
        ON rental.rental_id = payment.rental_id
GROUP BY
    category_name
ORDER BY total_amount DESC
LIMIT 1;


/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
SELECT
    film.title AS film_name
FROM
    film
LEFT JOIN
        inventory
            ON inventory.film_id = film.film_id
WHERE inventory.inventory_id is NULL;


/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
SELECT
    CONCAT(actor.first_name, ', ', actor.last_name) AS actor_full_name,
    COUNT(film_actor.film_id) AS film_count
FROM actor
INNER JOIN
    film_actor
        ON actor.actor_id = film_actor.actor_id
INNER JOIN
    film
        ON film_actor.film_id = film.film_id
INNER JOIN
    film_category
        ON film.film_id = film_category.film_id
INNER JOIN
    category
        ON film_category.category_id = category.category_id
WHERE category.name = 'Children'
GROUP BY
    actor_full_name
ORDER BY film_count DESC
LIMIT 3;
