-- 
-- addTestData
--
-- $Id: addTestData.sql 80 2013-01-29 17:08:48Z  $
--

delete from Graph_Sensor;
delete from Graph;
delete from User;
delete from Data;
delete from Sensor;
delete from Unit;
delete from Customer;
delete from Sensor_Type;

insert into Customer (Customer_ID, Name, Abbreviation, Contact_Name, Contact_Email) 
       values(101,'J-Squared Limited', 'J2', 'Jennifer Liddle', 'jennifer@jsquared.co.uk');
insert into Customer (Customer_ID, Name, Abbreviation, Contact_Name, Contact_Email) 
       values(102,"Jenny and Jennifer's Farm Fresh Produce",'JJ', 'Jenny and Jennifer', 'j2@jsquared.co.uk');
insert into Customer (Customer_ID, Name, Abbreviation, Contact_Name, Contact_Email) 
       values(103,"ACME Products Limited",'ACME', 'Wolf', 'wolf@acme.org.com.co.uk');
insert into Customer (Customer_ID, Name, Abbreviation, Contact_Name, Contact_Email) 
       values(104,"The Sanger Institute",'Sanger', 'Jennifer Liddle', 'js10@sanger.ac.uk');

insert into User (User_ID, Customer_ID, Forename, Surname, Email, Password, Administrator) 
       values(105,101,'Jennifer','Liddle','jennifer@jsquared.co.uk','1271ed5ef305aadabc605b1609e24c52',1);
insert into User (User_ID, Customer_ID, Forename, Surname, Email, Password, Administrator) 
       values(106,101,'Jenny','Bailey','jennyb@jsquared.co.uk','1271ed5ef305aadabc605b1609e24c52',1);
insert into User (User_ID, Customer_ID, Forename, Surname, Email, Password, Administrator) 
       values(107,101,'Tom','Winch','tomjon@metahusky.net','1271ed5ef305aadabc605b1609e24c52',1);
insert into User (User_ID, Customer_ID, Forename, Surname, Email, Password) 
       values(102,103,'Wiley','Coyote','wolf@jsquared.co.uk','1271ed5ef305aadabc605b1609e24c52');
insert into User (User_ID, Customer_ID, Forename, Surname, Email, Password, Administrator) 
       values(108,104,'Jénnifer','Liddle','js10@sanger.ac.uk','xyzzy',1);

insert into Unit (Unit_ID, Customer_ID, Name, SW_Version, HW_Version) values (201, 102, 'Unit One','1.0','1.1');
insert into Unit (Unit_ID, Customer_ID, Name, SW_Version, HW_Version) values (202, 103, 'Unit One','2.1','1.1');
insert into Unit (Unit_ID, Customer_ID, Name, SW_Version, HW_Version) values (203, 101, 'Raspberry Pi','1.0','1.0');
insert into Unit (Unit_ID, Customer_ID, Name, SW_Version, HW_Version) values (204, 101, 'Power Monitor','1.0','1.0');
insert into Unit (Unit_ID, Customer_ID, Name, SW_Version, HW_Version) values (205, 101, 'DMZ','1.0','1.0');
insert into Unit (Unit_ID, Customer_ID, Name, SW_Version, HW_Version) values (206, 101, 'Pi Two','1.0','1.0');
insert into Unit (Unit_ID, Customer_ID, Name, SW_Version, HW_Version) values (207, 101, 'Solar Sensor','1.0','1.0');
insert into Unit (Unit_ID, Customer_ID, Name, SW_Version, HW_Version) values (208, 104, 'Netbotz','1.0','1.0');

insert into Sensor_Type (Type_ID, Description, Units) values (301, 'Oregon Scientific Temperature Sensor', 'C');
insert into Sensor_Type (Type_ID, Description, Units) values (302, 'Acme Evilness Detector', 'milliBlairs');
insert into Sensor_Type (Type_ID, Description, Units) values (303, 'Acme Speed Detector', 'mph');
insert into Sensor_Type (Type_ID, Description, Units) values (304, 'Onewire Temperature Sensor', '&deg;C');
insert into Sensor_Type (Type_ID, Description, Units) values (305, 'Power Monitor', 'Watts');
insert into Sensor_Type (Type_ID, Description, Units) values (306, 'Netbotz Sensor', '˚C');

insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (401, 'Greenhouse', 201, 301, 'Greenhouse Temperature');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (402, 'Evil', 201, 302, 'Evil Detector');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (403, 'Radar', 202, 303, 'Radar Gun');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (404, 'Pi', 203, 304, 'Pi');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (405, 'Power', 204, 305, 'Mains Power');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (406, 'DMZ_0', 205, 304, 'DMZ_0');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (407, 'DMZ_1', 205, 304, 'DMZ_1');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (408, 'DMZ_2', 205, 304, 'DMZ_2');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (500, 'Pi_1', 206, 304, 'Pi_1');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (501, 'Pi_2', 206, 304, 'Pi_2');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (502, 'Pi_3', 206, 304, 'Pi_3');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (600, 'SPower', 207, 305, 'Solar Power');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (700, 'BC3A8BD_nbAlinkEnc_1_3_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (701, 'BC3A8BD_nbAlinkEnc_1_3_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (702, 'BC3A8BD_nbAlinkEnc_2_1_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (703, 'BC3A8BD_nbAlinkEnc_1_4_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (704, 'BC3A8BD_nbAlinkEnc_1_5_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (705, 'BC3A8BD_nbAlinkEnc_0_5_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (706, 'BC3A8BD_nbAlinkEnc_0_4_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (707, 'BC3A8BD_nbAlinkEnc_0_2_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (708, 'BC3A8BD_nbAlinkEnc_1_6_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (709, 'BC3A8BD_nbAlinkEnc_1_2_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (710, 'BC3A8BD_nbAlinkEnc_0_3_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (711, 'BC3A8BD_nbAlinkEnc_0_1_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (712, 'BC3A8BD_nbAlinkEnc_1_1_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (713, 'BC3A8BD_nbAlinkEnc_2_2_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (714, 'BC3A8BD_nbAlinkEnc_0_6_TEMP', 208, 306, 'West Pavilion');
insert into Sensor (Sensor_ID, User_ID, Unit_ID, Type_ID, Name) values (715, 'BC3A8BD_nbAlinkEnc_2_3_TEMP', 208, 306, 'West Pavilion');

insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (501, 401, '18-01-11 06:00', -5.1);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (502, 401, '18-01-11 06:10', -5.0);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (503, 401, '18-01-11 06:20', -5.0);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (504, 401, '18-01-11 06:30', -4.2);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (505, 401, '18-01-11 06:40', -3.9);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (506, 401, '18-01-11 06:50', -3.8);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (507, 401, '18-01-11 07:00', -3.1);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (508, 401, '18-01-11 07:10', -2.8);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (509, 401, '18-01-11 07:20', -2.0);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (510, 401, '18-01-11 07:30', -1.1);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (511, 401, '18-01-11 07:40', -0.2);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (512, 401, '18-01-11 07:50', -1.7);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (513, 401, '18-01-11 08:00', -3.1);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (514, 401, '18-01-11 08:10', -3.3);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (515, 401, '18-01-11 08:20', -3.3);
insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (516, 401, '18-01-11 08:30', -3.4);

insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (517, 402, '18-01-11 08:30', 120);

insert into Data (Data_ID, Sensor_ID, Reading_Date, Value) values (518, 403, '18-01-11 08:30', 110);

insert into Graph (Graph_ID, Customer_ID, Name, Title, TitleX, TitleY1, TitleY2) values(1,101,'Power','Mains Power','Date','Watts',NULL);
insert into Graph (Graph_ID, Customer_ID, Name, Title, TitleX, TitleY1, TitleY2) values(2,101,'Heating','Heating System','Date','&deg;C',NULL);
insert into Graph (Graph_ID, Customer_ID, Name, Title, TitleX, TitleY1, TitleY2) values(3,104,'Sequencing Lab','Sequencing Lab','Date','°C',NULL);

insert into Graph_Sensor (Graph_Sensor_ID, Graph_ID, Sensor_ID, Colour, Legend) values(1,1,405,NULL,'Mains');
insert into Graph_Sensor (Graph_Sensor_ID, Graph_ID, Sensor_ID, Colour, Legend) values(2,1,600,'#ff0000','Boiler Pump');
insert into Graph_Sensor (Graph_Sensor_ID, Graph_ID, Sensor_ID, Colour, Legend) values(3,2,500,'#00ff00','Top of tank');
insert into Graph_Sensor (Graph_Sensor_ID, Graph_ID, Sensor_ID, Colour, Legend) values(4,2,501,'#0000ff','Solar Water Feed');
insert into Graph_Sensor (Graph_Sensor_ID, Graph_ID, Sensor_ID, Colour, Legend) values(5,2,502,NULL,'Boiler');




