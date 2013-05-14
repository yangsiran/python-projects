setup
-----

The code is this project use MySQL in xampp and the root user with a database
called `webapp`, modify them if you have other chioce.

In the database:

    create table files (
        name text,
        date timestamp default now(),
        user text,
        content longtext,
        lastest boolean default 1
    )
