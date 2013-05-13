setup
-----

In the database:

    create table files (
        name text,
        date timestamp default now(),
        user text,
        content longtext,
        lastest boolean default 1
    )
