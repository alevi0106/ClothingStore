CREATE TYPE "paymentmode" AS ENUM (
  'cod',
  'card',
  'upi'
);

CREATE TABLE "users" (
  "id" integer,
  "name" varchar,
  "password" varchar,
  "email" varchar,
  "phone" integer
);

CREATE TABLE "useraddress" (
  "id" integer,
  "userid" integer,
  "address" varchar,
  "city" varchar,
  "pincode" integer
);

CREATE TABLE "admin" (
  "email" varchar,
  "password" varchar
);

CREATE TABLE "products" (
  "id" integer,
  "name" varchar,
  "description" varchar,
  "price" real,
  "availblequantity" integer,
  "thumbnailpath" varchar
);

CREATE TABLE "productimages" (
  "id" integer,
  "productid" integer,
  "imagepath" varchar,
  "sequence" integer,
  "imagecontext" varchar
);

CREATE TABLE "discount" (
  "id" integer,
  "percentage" real,
  "reason" varchar
);

CREATE TABLE "sale" (
  "id" integer,
  "endDate" datetime,
  "discountid" integer,
  "productid" integer
);

CREATE TABLE "cart" (
  "id" integer,
  "userid" integer,
  "productid" integer,
  "quantity" integer
);

CREATE TABLE "orders" (
  "id" integer,
  "productid" integer,
  "userid" integer,
  "price" real,
  "quantity" integer,
  "orderdate" datetime,
  "status" varchar
);

CREATE TABLE "payments" (
  "id" integer,
  "userid" integer,
  "time" datetime,
  "amountpaid" real,
  "paymentmode" paymentmode
);

CREATE TABLE "category" (
  "id" integer,
  "name" varchar,
  "type" varchar
);

CREATE TABLE "categoryproductlink" (
  "id" integer,
  "productid" integer,
  "categoryid" integer
);

ALTER TABLE "useraddress" ADD FOREIGN KEY ("userid") REFERENCES "users" ("id");

ALTER TABLE "productimages" ADD FOREIGN KEY ("productid") REFERENCES "products" ("id");

ALTER TABLE "sale" ADD FOREIGN KEY ("discountid") REFERENCES "discount" ("id");

ALTER TABLE "sale" ADD FOREIGN KEY ("productid") REFERENCES "products" ("id");

ALTER TABLE "cart" ADD FOREIGN KEY ("userid") REFERENCES "users" ("id");

ALTER TABLE "cart" ADD FOREIGN KEY ("productid") REFERENCES "products" ("id");

ALTER TABLE "orders" ADD FOREIGN KEY ("productid") REFERENCES "products" ("id");

ALTER TABLE "orders" ADD FOREIGN KEY ("userid") REFERENCES "users" ("id");

ALTER TABLE "payments" ADD FOREIGN KEY ("userid") REFERENCES "users" ("id");

ALTER TABLE "categoryproductlink" ADD FOREIGN KEY ("productid") REFERENCES "products" ("id");

ALTER TABLE "categoryproductlink" ADD FOREIGN KEY ("categoryid") REFERENCES "category" ("id");

COMMENT ON COLUMN "productimages"."imagecontext" IS 'Front or back';
