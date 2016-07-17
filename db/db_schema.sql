
/* This is the main schema file for the database. 
This schema will be used for creating databases for both learning datasets and testcases.
*/

CREATE TABLE DOMAINS (
	'domain_id' integer primary key AUTOINCREMENT,
	'domain_name' varchar(10) not null
);

CREATE TABLE RESPONSES (
	'response_id' integer primary key AUTOINCREMENT, 
	'response_code' int not null
);

CREATE TABLE PINGS (
	'ping_id' integer primary key AUTOINCREMENT,
	'_domain_id' int not null,
	'_response_id' int not null,
	foreign key ('_domain_id') references 'DOMAINS'('domain_id'),
	foreign key ('_response_id') references 'RESPONSES'('response_id')
);
