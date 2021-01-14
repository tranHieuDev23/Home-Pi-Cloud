drop table if exists iot_db.status_logs;
drop table if exists iot_db.commanders;
drop table if exists iot_db.devices;
drop table if exists iot_db.users;
drop table if exists iot_db.blacklisted_jwts;

create schema if not exists iot_db;

create table if not exists iot_db.users (
    username text primary key,
    password text not null,
    display_name text not null,
    command_topic text not null,
    status_topic text not null
);

create table if not exists iot_db.commanders (
    id text primary key,
    display_name varchar (255),
    of_user text,
    constraint fk_customer_commander
        foreign key (of_user)
            references iot_db.users(username)
);

create table if not exists iot_db.devices (
    id text primary key,
    display_name varchar (255) not null,
    type varchar (32) not null,
    of_user text,
    constraint fk_customer_device
        foreign key (of_user)
            references iot_db.users(username)
);

create table if not exists iot_db.status_logs (
    id text primary key,
    of_device text,
    timestamp bigint,
    field_name varchar (32) not null,
    field_value text,
    constraint fk_log_device
        foreign key (of_device)
            references iot_db.devices(id)
);

create table if not exists iot_db.blacklisted_jwts (
    jti text primary key,
    exp bigint
);

INSERT INTO iot_db.commanders(id, display_name, of_user) VALUES
    ('speaker:1', 'Home Pi Speaker', null),
    ('speaker:2', 'Home Pi Speaker', null),
    ('speaker:3', 'Home Pi Speaker', null),
    ('speaker:4', 'Home Pi Speaker', null),
    ('speaker:5', 'Home Pi Speaker', null),
    ('speaker:6', 'Home Pi Speaker', null),
    ('speaker:7', 'Home Pi Speaker', null),
    ('speaker:8', 'Home Pi Speaker', null),
    ('speaker:9', 'Home Pi Speaker', null),
    ('speaker:10', 'Home Pi Speaker', null);

INSERT INTO iot_db.devices(id, display_name, type, of_user) VALUES
    ('light:1', 'Home Pi Light', 'LIGHT', null),
    ('light:2', 'Home Pi Light', 'LIGHT', null),
    ('light:3', 'Home Pi Light', 'LIGHT', null),
    ('light:4', 'Home Pi Light', 'LIGHT', null),
    ('light:5', 'Home Pi Light', 'LIGHT', null),
    ('thermostat:1', 'Home Pi Thermostat', 'THERMOSTAT', null),
    ('thermostat:2', 'Home Pi Thermostat', 'THERMOSTAT', null),
    ('thermostat:3', 'Home Pi Thermostat', 'THERMOSTAT', null),
    ('thermostat:4', 'Home Pi Thermostat', 'THERMOSTAT', null),
    ('thermostat:5', 'Home Pi Thermostat', 'THERMOSTAT', null);