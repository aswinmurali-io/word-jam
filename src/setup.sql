create table saves
(
    coins int not null,
    level_number int not null,
    level_progress int(3) not null
);

create table level_history
(
    level int primary key,
    level_time varchar(8),
    accuracy int(2)
);
