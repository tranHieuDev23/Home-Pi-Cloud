drop table if exists iot_db.commander;
drop table if exists iot_db.device;
drop table if exists iot_db.customer;

create schema if not exists iot_db;

create table if not exists iot_db.customer (
    name varchar (16) primary key,
    password varchar (16) not null ,
    display_name varchar(255) not null
);

create table if not exists iot_db.commander (
    id INT GENERATED ALWAYS AS IDENTITY,
    display_name varchar (255),
    customer varchar (16) not null,
    primary key (id),
    constraint fk_customer_commander
        foreign key (customer)
            references iot_db.customer(name)
);

create table if not exists iot_db.device (
    id INT GENERATED ALWAYS AS IDENTITY,
    display_name varchar (255) not null ,
    type varchar (32) not null ,
    customer varchar (16) not null,
    status varchar (512) not null ,
    primary key (id),
    constraint fk_customer_device
        foreign key (customer)
            references iot_db.customer(name)
);

INSERT INTO iot_db.customer (name, password, display_name) VALUES
('quangkhanh', '1234', 'khanhquang'),
('giangtruong', '1234', 'truonggiang'),
('hieutran', '1234', 'tranhieu');

INSERT INTO iot_db.commander (display_name, customer) VALUES
('speaker1', 'quangkhanh'),
('speaker2', 'giangtruong'),
('speaker3', 'hieutran');

INSERT INTO iot_db.device (display_name, type, customer, status) VALUES
('lamp', 'SMART_LIGHT', 'quangkhanh', 'GOOD'),
('television', 'SMART_LIGHT', 'giangtruong', 'GOOD'),
('fan', 'THERMOSTAT', 'hieutran', 'BAD');

