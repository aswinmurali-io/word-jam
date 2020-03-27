create table saves
(
    coins int not null,
    level_number int not null,
    level_progress int(3) not null,
    level_time varchar(8)
);

create table level_history
(
    level int primary key,
    level_time varchar(8),
    accuracy float
);
