create database bank;
use bank;
drop table users;
drop table admins;
create table users(
ACCNO varchar(100) primary key,
NAME varchar(50),
PHNO char(10),
AMOUNT integer(20),
PIN integer(4));
create table admins(USERNAME varchar(20) primary key,
NAME varchar(50),
PASSWORD varchar(12));

select * from users;
select * from admins;
-- select NAME from users where NAME="%s";
insert into admins(USERNAME,NAME,PASS) values('DS','imdr',2022);
insert into users(ACCNO,NAME,PHNO,AMOUNT,PIN) values(10000,'mahesh',999999999,1000,14);