drop table if exists commander;
drop table if exists device;
drop table if exists customer;

create table if not exists customer (
    name varchar (16) primary key,
    password varchar (16) not null ,
    display_name varchar(255) not null
);

create table if not exists commander (
    id INT GENERATED ALWAYS AS IDENTITY,
    display_name varchar (255),
    customer varchar (16) not null,
    primary key (id),
    constraint fk_customer_commander
        foreign key (customer)
            references customer(name)
);

create table if not exists device (
    id INT GENERATED ALWAYS AS IDENTITY,
    display_name varchar (255) not null ,
    customer varchar (16) not null,
    primary key (id),
    constraint fk_customer_device
        foreign key (customer)
            references customer(name)
);

INSERT INTO public.customer (name, password, display_name) VALUES
('quangkhanh', '1234', 'khanhquang'),
('giangtruong', '1234', 'truonggiang'),
('hieutran', '1234', 'tranhieu');

INSERT INTO public.commander (display_name, customer) VALUES
('speaker1', 'quangkhanh'),
('speaker2', 'giangtruong'),
('speaker3', 'hieutran');

INSERT INTO public.device (display_name, customer) VALUES
('lamp', 'quangkhanh'),
('television', 'giangtruong'),
('fan', 'hieutran');

