CREATE TABLE "user" (
  "uid" varchar PRIMARY KEY,
  "name" varchar,
  "username" varchar UNIQUE,
  "email" varchar UNIQUE,
  "password" varchar,
  "user_type" varchar,
  "agency" varchar
);

CREATE TABLE "user_type" (
  "code" varchar PRIMARY KEY,
  "committe" varchar,
  "description" varchar
);

CREATE TABLE "agency" (
  "code" varchar PRIMARY KEY,
  "name" varchar,
  "type" varchar,
  "description" varchar
);

CREATE TABLE "project" (
  "project_id" varchar PRIMARY KEY,
  "proposal_id" varchar UNIQUE,
  "start_date" date,
  "completion" float,
  "actual_cost" float
);

CREATE TABLE "proposal" (
  "project_id" varchar PRIMARY KEY,
  "name" varchar,
  "location" varchar,
  "latitude" float,
  "longitude" float,
  "exec" varchar,
  "cost" float,
  "timespan" float,
  "goal" varchar,
  "propsal_date" date
);

CREATE TABLE "constraint" (
  "code" varchar PRIMARY KEY,
  "max_limit" int,
  "constraint_type" varchar
);

CREATE TABLE "component" (
  "component_id" varchar PRIMARY KEY,
  "project_id" varchar,
  "excecuting_agency" varchar,
  "component_type" varchar,
  "depends_on" varchar,
  "budget_ratio" float
);

CREATE TABLE "issue" (
  "uid" varchar,
  "project_id" varchar,
  "description" varchar,
  "status" varchar
);

ALTER TABLE "user" ADD FOREIGN KEY ("user_type") REFERENCES "user_type" ("code");

ALTER TABLE "user" ADD FOREIGN KEY ("agency") REFERENCES "agency" ("code");

ALTER TABLE "project" ADD FOREIGN KEY ("proposal_id") REFERENCES "proposal" ("project_id");

ALTER TABLE "proposal" ADD FOREIGN KEY ("exec") REFERENCES "agency" ("code");

ALTER TABLE "component" ADD FOREIGN KEY ("project_id") REFERENCES "project" ("project_id");

ALTER TABLE "component" ADD FOREIGN KEY ("depends_on") REFERENCES "component" ("component_id");

ALTER TABLE "component" ADD FOREIGN KEY ("excecuting_agency") REFERENCES "agency" ("code");

ALTER TABLE "issue" ADD FOREIGN KEY ("uid") REFERENCES "user" ("uid");

ALTER TABLE "issue" ADD FOREIGN KEY ("project_id") REFERENCES "project" ("project_id");
