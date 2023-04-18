create database bankDemo;

use bankDemo;

create table shop_transactions(
trans_id int auto_increment primary key,
initial_bal float,
shop_name varchar(60),
total_amount float,
current_bal float,
date_time datetime
);
drop table shop_transactions;
select * from shop_transactions;
create table owner_credits(
id int auto_increment primary key,
credit_amount float,
actual_balance float,
date_time datetime
);
select * from owner_credits;
create table account_master(
id int auto_increment primary key,
initial_balance float,
credit_amount float,
shop_name varchar(60),
shop_amount float,
receiver varchar(60),
sent_amount float,
send_ref varchar(60),
current_balance float default 0,
date_time datetime
);
insert into account_master (current_balance) values (0);
select * from account_master;
drop table account_master;
create table remittances(
id int auto_increment primary key,
initial_balance float,
receiver_name varchar(60),
sent_amount float,
send_ref varchar(60),
current_balance float,
date_time datetime
);
select * from remittances;

