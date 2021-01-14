drop table if exists iot_db.status_logs;
drop table if exists iot_db.commanders;
drop table if exists iot_db.devices;
drop table if exists iot_db.users;

create schema if not exists iot_db;

create table if not exists iot_db.users (
    username varchar (16) primary key,
    password text not null,
    display_name varchar(255) not null
);

create table if not exists iot_db.commanders (
    id int generated always as identity,
    display_name varchar (255),
    of_user varchar (16) not null,
    primary key (id),
    constraint fk_customer_commander
        foreign key (of_user)
            references iot_db.users(username)
);

create table if not exists iot_db.devices (
    id int generated always as identity,
    display_name varchar (255) not null,
    type varchar (32) not null,
    of_user varchar (16) not null,
    primary key (id),
    constraint fk_customer_device
        foreign key (of_user)
            references iot_db.users(username)
);

create table if not exists iot_db.status_logs (
    id int generated always as identity,
    of_device int,
    timestamp bigint,
    field_name varchar (32) not null,
    field_value text,
    primary key(id),
    constraint fk_log_device
        foreign key (of_device)
            references iot_db.devices(id)
);

INSERT INTO iot_db.users (username, password, display_name) VALUES
('quangkhanh', '1234', 'khanhquang'),
('giangtruong', '1234', 'truonggiang'),
('hieutran', '1234', 'tranhieu');

INSERT INTO iot_db.commanders (display_name, of_user) VALUES
('speaker1', 'quangkhanh'),
('speaker2', 'giangtruong'),
('speaker3', 'hieutran');

INSERT INTO iot_db.devices (display_name, type, of_user) VALUES
('lamp', 'SMART_LIGHT', 'quangkhanh'),
('television', 'SMART_LIGHT', 'giangtruong'),
('fan', 'THERMOSTAT', 'hieutran');