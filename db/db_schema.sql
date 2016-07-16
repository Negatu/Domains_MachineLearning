
/* This is the main schema file for the database. 
This schema will be used for creating databases for both learning datasets and testcases.
*/

CREATE TABLE DOMAINS (
	'domain_id' int not null,
	'domain_name' varchar(10) not null,
	primary key ('domain_id')
);

CREATE TABLE RESPONSES (
	'response_id' int not null, 
	'response_code' int not null,
	primary key ('response_id')
);

CREATE TABLE PINGS (
	'ping_id' int not null,
	'_domain_id' int not null,
	'_response_id' int not null,
	primary key ('ping_id'),
	foreign key ('_domain_id') references 'DOMAINS'('domain_id'),
	foreign key ('_response_id') references 'RESPONSES'('response_id')
);
