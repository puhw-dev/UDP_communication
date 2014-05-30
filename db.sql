
/* Drop Tables */

DROP TABLE METRIC;
DROP TABLE SENSOR;
DROP TABLE USERS;




/* Create Tables */

CREATE TABLE USERS
(
	login text NOT NULL UNIQUE,
	password text UNIQUE,
	PRIMARY KEY (login)
);


CREATE TABLE SENSOR
(
	id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	owner text NOT NULL,
	hostname text,
	hostip text,
	sensorname text,
	sensortype text,
	rpm integer,
	FOREIGN KEY (owner)
	REFERENCES USER (login)
);


CREATE TABLE METRIC
(
	id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	sensorid integer NOT NULL,
	metricname text,
	time text,
	value text,
	FOREIGN KEY (sensorid)
	REFERENCES SENSOR (id)
);



