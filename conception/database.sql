CREATE TABLE `Factory` (
	`factory_id` INT NOT NULL AUTO_INCREMENT,
	`name` varchar(100) NOT NULL,
	`desc` TEXT NOT NULL,
	`logo` varchar(50) NOT NULL,
	`phone` varchar(15) NOT NULL,
	`employee_id` INT NOT NULL,
	`created_at` TIMESTAMP NULL,
	`updated_at` TIMESTAMP NULL,
	PRIMARY KEY (`factory_id`)
);

CREATE TABLE `Employee` (
	`employee_id` INT NOT NULL AUTO_INCREMENT,
	`manage_id` INT NOT NULL,
	`first_name` varchar(50) NOT NULL,
	`flast_name` varchar(50) NOT NULL,
	`email` varchar(50) NOT NULL,
	`password` varchar(100) NOT NULL,
	`gender` varchar(10) NOT NULL,
	`phone` varchar(15) NOT NULL,
	`city` varchar(20) NOT NULL,
	`address` TEXT NOT NULL,
	`picture` varchar(50) NOT NULL,
	`enable` BOOLEAN NOT NULL,
	`remember_token` varchar(100) NOT NULL,
	`trash` BOOLEAN NOT NULL,
	`created_at` TIMESTAMP NULL,
	`updated_at` TIMESTAMP NULL,
	PRIMARY KEY (`employee_id`)
);

CREATE TABLE `Point_of_sale` (
	`point_sale_id` INT NOT NULL,
	`name` varchar(50) NOT NULL,
	`address` varchar(50) NOT NULL,
	`created_at` TIMESTAMP NULL,
	`updated_at` TIMESTAMP NULL,
	`factory_id` INT NOT NULL,
	PRIMARY KEY (`point_sale_id`)
);

CREATE TABLE `Product` (
	`product_id` INT NOT NULL AUTO_INCREMENT,
	`name` varchar(150) NOT NULL,
	`desc` TEXT NOT NULL,
	`quantity_unit` INT NOT NULL,
	`unit_price` DECIMAL NOT NULL,
	`size` varchar(50) NOT NULL,
	`color` varchar(50) NOT NULL,
	`note` TEXT NOT NULL,
	`trash` BOOLEAN NOT NULL,
	`category_id` INT NOT NULL,
	`created_at` TIMESTAMP NULL,
	`updated_at` TIMESTAMP NULL,
	PRIMARY KEY (`product_id`)
);

CREATE TABLE `Customer` (
	`customer_id` INT NOT NULL,
	`first_name` varchar(50) NOT NULL,
	`last_name` varchar(50) NOT NULL,
	`email` varchar(50) NOT NULL,
	`password` varchar(50) NOT NULL,
	`age` INT NOT NULL,
	`phone` varchar(15) NOT NULL,
	`gender` varchar(10) NOT NULL,
	`city` varchar(50) NOT NULL,
	`address` varchar(100) NOT NULL,
	`picture` varchar(50) NOT NULL,
	`credit_card` varchar(100) NOT NULL,
	`credit_card_type` varchar(100) NOT NULL,
	`billin_address` varchar(100) NOT NULL,
	`billing_city` varchar(100) NOT NULL,
	`billing_region` varchar(100) NOT NULL,
	`billing_postal_code` varchar(100) NOT NULL,
	`black_list` BOOLEAN NOT NULL,
	`trash` BOOLEAN NOT NULL,
	`remember_token` varchar(100) NOT NULL,
	`active_token` varchar(100) NOT NULL,
	`online` BOOLEAN NOT NULL,
	`created_at` TIMESTAMP NULL,
	`updated_at` TIMESTAMP NULL,
	PRIMARY KEY (`customer_id`)
);

CREATE TABLE `Employee_point_of_sale` (
	`employee_id` INT NOT NULL,
	`point_sale_id` INT NOT NULL,
	`date` TIMESTAMP NOT NULL
);

CREATE TABLE `Store` (
	`point_sale_id` INT NOT NULL,
	`product_id` INT NOT NULL,
	`quantity_store` INT NOT NULL,
	`quantity_sold` INT NOT NULL
);

CREATE TABLE `Customer_sales` (
	`customer_id` INT NOT NULL,
	`payment_id` INT NOT NULL,
	`point_sale_id` INT NOT NULL,
	`product_id` INT NOT NULL,
	`quantity` INT NOT NULL,
	`paid` BOOLEAN NOT NULL,
	`payment_date` DATETIME NOT NULL,
	`created_at` TIMESTAMP NULL
);

CREATE TABLE `Picture` (
	`picture_id` INT NOT NULL,
	`product_id` INT NOT NULL,
	`name` varchar(50) NOT NULL,
	`size` INT NOT NULL,
	`created_at` TIMESTAMP NULL
);

CREATE TABLE `Payment` (
	`payment_id` INT NOT NULL AUTO_INCREMENT,
	`payment_type` varchar(50) NOT NULL,
	`created_type` TIMESTAMP NULL,
	`updated_type` TIMESTAMP NULL,
	PRIMARY KEY (`payment_id`)
);

CREATE TABLE `Category` (
	`category_id` INT NOT NULL,
	`name` varchar(50) NOT NULL,
	`slug` varchar(100) NOT NULL,
	`description` TEXT NOT NULL,
	`created_at` TIMESTAMP NULL,
	`updated_at` TIMESTAMP NULL,
	PRIMARY KEY (`category_id`)
);

ALTER TABLE `Factory` ADD CONSTRAINT `Factory_fk0` FOREIGN KEY (`employee_id`) REFERENCES `Employee`(`employee_id`);

ALTER TABLE `Employee` ADD CONSTRAINT `Employee_fk0` FOREIGN KEY (`manage_id`) REFERENCES `Employee`(`employee_id`);

ALTER TABLE `Point_of_sale` ADD CONSTRAINT `Point_of_sale_fk0` FOREIGN KEY (`factory_id`) REFERENCES `Factory`(`factory_id`);

ALTER TABLE `Product` ADD CONSTRAINT `Product_fk0` FOREIGN KEY (`category_id`) REFERENCES `Category`(`category_id`);

ALTER TABLE `Employee_point_of_sale` ADD CONSTRAINT `Employee_point_of_sale_fk0` FOREIGN KEY (`employee_id`) REFERENCES `Employee`(`employee_id`);

ALTER TABLE `Employee_point_of_sale` ADD CONSTRAINT `Employee_point_of_sale_fk1` FOREIGN KEY (`point_sale_id`) REFERENCES `Point_of_sale`(`point_sale_id`);

ALTER TABLE `Store` ADD CONSTRAINT `Store_fk0` FOREIGN KEY (`point_sale_id`) REFERENCES `Point_of_sale`(`point_sale_id`);

ALTER TABLE `Store` ADD CONSTRAINT `Store_fk1` FOREIGN KEY (`product_id`) REFERENCES `Product`(`product_id`);

ALTER TABLE `Customer_sales` ADD CONSTRAINT `Customer_sales_fk0` FOREIGN KEY (`customer_id`) REFERENCES `Customer`(`customer_id`);

ALTER TABLE `Customer_sales` ADD CONSTRAINT `Customer_sales_fk1` FOREIGN KEY (`payment_id`) REFERENCES `Payment`(`payment_id`);

ALTER TABLE `Customer_sales` ADD CONSTRAINT `Customer_sales_fk2` FOREIGN KEY (`point_sale_id`) REFERENCES `Point_of_sale`(`point_sale_id`);

ALTER TABLE `Customer_sales` ADD CONSTRAINT `Customer_sales_fk3` FOREIGN KEY (`product_id`) REFERENCES `Product`(`product_id`);

ALTER TABLE `Picture` ADD CONSTRAINT `Picture_fk0` FOREIGN KEY (`product_id`) REFERENCES `Product`(`product_id`);

