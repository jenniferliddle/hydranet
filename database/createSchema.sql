-- 
-- Create the Hydranet Database Schema
--
-- $Id: createSchema.sql 91 2013-12-23 11:39:26Z  $
--

--
-- First, drop all of the existing tables and indexes...
--
drop table User;
drop table Graph_Sensor;
drop table Graph;
drop table Data;
drop table Sensor;
drop table Unit;
drop table Customer;
drop table Sensor_Type;
drop table Alert;

-- 
-- Create the Customer table
-- 
select 'Creating Customer table';
create table Customer (
	Customer_ID serial,
	Abbreviation varchar(10) not null unique,
	Name varchar(80) not null,
	IsCurrent boolean not null default 1,
	Contact_Name varchar(80) not null,
	Contact_Email varchar(80) not null,
	Address1 varchar(80),
	Address2 varchar(80),
	Address3 varchar(80),
	Address4 varchar(80),
	Postcode varchar(10),
	Primary Key (Customer_ID)
)
engine = InnoDB;

-- 
-- Create the User table
-- 
select 'Creating User table';
create table User (
	User_ID serial,
	Customer_ID bigint(20) unsigned,
	Forename varchar(50) not null,
	Surname varchar(50) not null,
	Email varchar(50) not null unique,
	Password varchar(128),
	Administrator boolean not null default 0,
	IsCurrent boolean not null default 1,
	Primary Key (User_ID)
)
engine = InnoDB;

create index user_username_ind on User(Email);
alter table User add constraint foreign key (Customer_ID) references Customer (Customer_ID);

-- 
-- Create Sensor_Type table
--
select 'Creating Sensor_Type table';
create table Sensor_Type (
	Type_ID serial,
	Description varchar(60) not null,
	Units varchar(30) not null,
	Primary Key (Type_ID)
)
engine = InnoDB;

-- 
-- Create the Unit table
-- 
select 'Creating Unit table';
create table Unit (
	Unit_ID serial,
	Customer_ID bigint(20) unsigned not null,
	Name varchar(30) not null,
	SW_Version varchar(10),
	HW_version varchar(10),
	Primary Key (Unit_ID)
)
engine = InnoDB;

create index unit_customer_ind on Unit(Customer_ID);
alter table Unit add constraint foreign key (Customer_ID) references Customer (Customer_ID);

-- 
-- Create Sensor Table
-- 
select 'Creating Sensor table';
create table Sensor (
	Sensor_ID serial,
	User_ID varchar(30) not null,
	Unit_ID bigint(20) unsigned not null,
	Name varchar(30) not null,
	Type_ID bigint(20) unsigned not null,
	Primary Key (Sensor_ID)
)
engine = InnoDB;
create index sensor_unit_ind on Sensor(Unit_ID);
alter table Sensor add constraint foreign key (Unit_ID) references Unit (Unit_ID);
create index sensor_type_ind on Sensor(Type_ID);
alter table Sensor add constraint foreign key (Type_ID) references Sensor_Type(Type_ID);

-- 
-- create Data table
-- 
select 'Creating Data table';
create table Data (
	Data_ID serial,
	Sensor_ID bigint(20) unsigned not null,
	Reading_Date timestamp not null,
	Value double not null,
	Primary Key (Data_ID)
)
engine = InnoDB;
create index data_sensor_ind on Data(Sensor_ID);
create index data_date_ind on Data(Reading_Date);
alter table Data add constraint foreign key (Sensor_ID) references Sensor(Sensor_ID);

--
-- create Graph table
--
select 'Creating Graph table';
create table Graph (
	Graph_ID serial,
	Customer_ID bigint(20) unsigned not null,
	Name varchar(20) not null,
	Title varchar(40) not null,
	TitleX varchar(40) not null,
	TitleY1 varchar(40) not null,
	TitleY2 varchar(40),
	Visible boolean default 1,
	Primary Key (Graph_ID)
)
engine = InnoDB;
alter table Graph add constraint foreign key (Customer_ID) references Customer(Customer_ID);

--
-- create Graph_Sensor table
--
select 'Creating Graph_Sensor table';
create table Graph_Sensor (
	Graph_Sensor_ID serial,
	Graph_ID bigint(20) unsigned not null,
	Sensor_ID bigint(20) unsigned not null,
	Colour varchar(10),
	Legend varchar(30),
	YLeft boolean default 1,
	Visible boolean default 1,
	Primary Key (Graph_Sensor_ID)
)
engine = InnoDB;
alter table Graph_Sensor add constraint foreign key (Sensor_ID) references Sensor(Sensor_ID);
alter table Graph_Sensor add constraint foreign key (Graph_ID) references Graph(Graph_ID);

-- 
-- create Alert table
--
select 'Creating Alert table';
create table Alert (
    Alert_ID serial,
    Sensor_ID bigint(20) unsigned not null,
    User_ID bigint(20) unsigned not null,
    Minmax varchar(3) not null,
    Value double not null,
    Text varchar(1024),
    Period int default 0,
    Primary Key (Alert_ID)
)
engine = InnoDB;
alter table Alert add constraint foreign key (Sensor_ID) references Sensor(Sensor_ID);
alter table Alert add constraint foreign key (User_ID) references User(User_ID);

