LOAD DATA LOCAL INFILE 'E:/Dessertation/dash_app_skm/processed_data/output.csv'
INTO TABLE suicides
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(country, year, sex, age, suicides, population, sucid_in_hundredk, country_year, yearly_gdp, gdp_per_capita, generation, suicide_perc, internetusers, expenses, employeecompensation, unemployment, physician_price, laborforcetotal, lifeexpectancy, mobilesubscriptions, refugees, selfemployed, electricityacess, continent, country_code, mobilesubscription);

-- cd c:\xampp\mysql\bin

-- mysql.exe -u root --password

-- C:\xampp\mysql\bin\mysql.exe -u root -p



-- attempt 1 to upload file to dkit remote mysql db
LOAD DATA LOCAL INFILE '/root/dash/assets/processed_data/output.csv' 
INTO TABLE suicides 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES 
(country, year, sex, age, suicides, population, sucid_in_hundredk, country_year, yearly_gdp, gdp_per_capita, generation, suicide_perc, internetusers, expenses, employeecompensation, unemployment, physician_price, laborforcetotal, lifeexpectancy, mobilesubscriptions, refugees, selfemployed, electricityacess, continent, country_code, mobilesubscription);

-- attempt 2 succeeded to upload file to dkit remote mysql db
LOAD DATA LOCAL INFILE '/root/dash/assets/processed_data/output.csv' 
INTO TABLE suicides 
FIELDS TERMINATED BY ',' 
IGNORE 1 LINES 
(country, year, sex, age, suicides, population, sucid_in_hundredk, country_year, yearly_gdp, gdp_per_capita, generation, suicide_perc, internetusers, expenses, employeecompensation, unemployment, physician_price, laborforcetotal, lifeexpectancy, mobilesubscriptions, refugees, selfemployed, electricityacess, continent, country_code, mobilesubscription);



-- testing a small dataset loading to mysql table called test
LOAD DATA LOCAL INFILE '/root/dash/assets/processed_data/test.csv'
INTO TABLE test
FIELDS TERMINATED BY ','
IGNORE 1 ROWS;
