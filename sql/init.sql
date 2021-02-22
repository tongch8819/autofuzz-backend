set time zone "Asia/Shanghai";
show time zone;


-- user table
CREATE TABLE "user" (
	"uid" integer not null,
	"username" varchar(256) not null,
	"password" varchar(50) not null,
	"create_t" timestamp,
	primary key ("uid")
);

insert into "user" values 
(1, 'Auto Fuzzer', '123456', current_timestamp),
(2, 'Zhang San', '123456', current_timestamp),
(3, 'Li Si', '123456', current_timestamp);


-- fuzzer table
CREATE TABLE "fuzzer" (
	"fid" integer not null,
	"fname" varchar(256) not null default 'Unknown',
	"description" text,
	"upload_t" timestamp,
	primary key ("fid")
);

insert into "fuzzer" values 
(1, 'AFL', 'A light and faster fuzzing tool.', current_timestamp),
(2, 'MemLock',  'A fuzzing tool customized for memory corruption bug.', current_timestamp),
(3, 'MOpt',  'A fuzzing tool with more efficient mutation operator scheduling algorithm.', current_timestamp),
(4, 'Triforce',  'This is a patched version of AFL that supports full-system fuzzing using QEMU.', current_timestamp),
(5, 'AFLPlusPlus', 
 'afl++ is a superior fork to Google''s afl - more speed, more and better mutations, more and better instrumentation, 
 custom module support, etc.', current_timestamp);


 -- project 
CREATE TABLE "project" (
	"pid" integer not null,
	"pname" varchar(256) not null default 'Unknown',
	"size" varchar(10) ,
	"uid" integer not null ,
	"fuzzer_id" integer not null,
	"description" text,
	"upload_t" timestamp,
	primary key ("pid"),
	constraint fk1 foreign key ("uid") references "user"("uid"),
	constraint fk2 foreign key ("fuzzer_id") references "fuzzer"("fid")
);


-- table crash
CREATE TABLE "crash" (
	"cid" integer not null,
	"seed_name" varchar(256),
	"src_posi_desc" text,
	"project_id" integer,
	"fuzzer_id" integer,
	"trigger_t" timestamp,
	primary key ("cid"),
	constraint fk foreign key ("project_id") references "project"("pid")
);
