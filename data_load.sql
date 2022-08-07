LOAD DATA LOCAL INFILE 'E:/Dessertation/desertion_dkit_msc_2022_sep/processed_data/output.csv'
INTO TABLE suicides
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(country, year, sex, age, suicides, population, sucid_in_hundredk, country_year, yearly_gdp, gdp_per_capita, generation, suicide_perc, internetusers, expenses, employeecompensation, unemployment, physician_price, laborforcetotal, lifeexpectancy, mobilesubscriptions, refugees, selfemployed, electricityacess, continent, country_code, mobilesubscription);