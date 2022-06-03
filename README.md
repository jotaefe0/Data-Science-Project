  # Used Car Market in Argentina

**Note:** This project is currently in development

MVP Model in https://carspredic.herokuapp.com/input
It doesn't filter unreal cars, so you need to manually input a coherent car (eg if you put a 8v engine gol you will get a really expensive car)
It still needs further improvement, but it did predict my car with high accuracy. (Peugeot 308 2.0 100KM year 2012 Black) --> 2M$

## Road map

 - [x] Create a web scrapper to gather data ✅
 - [x] Preprocess data and upload to SQL on AWS ✅
 - [x] Analyze Data ✅
 - [x] Create a ML model ✅
 - [x] Deploy model to production using Flask and Heroku ✅
 - [ ] Automate the process by scripting the scrapper to add new rows to the database and feed the ML model
 
 - Iterate over the process to improve the model!
 - Improve the front end

# Scope

This project is intended to be for learning purposes by attempting to solve a real life problem and to find answers to the questions:

 - How is the current state of the used car market? 
 - What is my used car worth in the current market?  
 - What will be the value (price) of a car with given features?

# Development

The data is scrapped from mercadolibre argentina. 33951 rows of data were scrapped. 
This includes:
['brand', 'model', 'colour', 'fuel', 'doors', 'engine', 'location','price', 'year', 'transmission', 'km', 'type', 'url']

### Note: Details and code can be found inside the Data Analysis notebook.

 As this is my first full stack DS project I will document my findings and thoughts. As I find out this is an iterative process and it can be always be improved, this is by gathering new data, make changes to the model, or data cleaning algorithms by understanding better the importance of each variable into the problem we are trying to solve. So with this said I can feel that this work is yet far from finished.
 
 ## Scraping Data
 The first part of the project consists on gathering the data. This is done by using the request python library. The code is not fancy at all and the idea is get the basic features of the used cars (Brand, model, color, year, etc). The website declared a total of 100000 used cars, but it would only show 42 pages at most. If you want to get more data you need to apply filters and keep searching. That's why I made 2 scrapes (First one consists on brands only) The second one was to filter each brand and get as much data as possible. This script took a couple of hours to complete since it had to enter each listing and scrape the data.
 Finally, this was uploaded to a AWS SQL server. this is an "over-kill" if we are working alone, but in the future this will be useful when we automate the data scraping so that the model can retrieve the last updated data while in production.
 
 ## Cleaning Data
 The major issues here were that not all the data is uniform. Many values' which are equal have a different input. We also have to deal with Spanish characters and another problem is that the price of cars can be in ARS or USD currency. So we have to deal with that as well.
 
 ## Data Analysis
 In this section we start to understand how the data is structured and what relationships exist between each feature and the price. Also, I understood that this part is crucial to produce a decent model and also sometimes to go back and re structure the data to get a cleaner view of the overall scenario.
 
 Before getting into the discrete features, the main variables to plot are year, km and price. In this way we can easily spot outlines (We also use the.describe() method)
 
 ![Price - Year Relationship](/img/priceyear.png "priceyear")
 
 As we can see, older cars do not follow a trend, this may be because they are on other market, we can find ancient cars and some collection cars. Which is out of this scope, this is why we can discard cars that are older than year 1990. A part there is a clear gap between cars in ARS and cars in USD dollars (1 USD = 200ARS as June 2022)
 
 If we unify prices in ARS, using the conversion we get a linear trend. Also we can see how different brands have different price tendencies
 
 ![Price - Year Relationship](/img/priceyear2.png "priceyear")
 
 
 The other continuous variable to plot is KM. Also we can add a variable which is engine type, to see if there is any influence.
 
 ![Price - Km Relationship](/img/pricekm.png "price km")
 
 As we can see there is a decay in price and KM. it looks like Petrol ("Nafta") cars price decays faster. Whereas Diesel cars have a longer life and maintain their value. this is and interesting point. (I must admit that this data set has "known" outcomes and conclusions, but as a practice dataset is interesting to validate the data with field knowledge)
 
 This influence is revealed in the heat map
 
 ![Heat map](/img/heatmap.png "heat map")
 
 Where a negative correlation is found between km and price and a positive correlation between price and year.
 
 
 If we go deeper into the other features such as color, brand and location we can see the following:
 
 ![Price - Color](/img/boxplot1.png "color")
 
 In average, we can see, for example that "red" cars are cheaper than black or gray cars.
 
 ![Price - Brands](/img/brands.png "Brands")
 
 Also the most expensive brands, in average on this market are "RAM" and "Porsche" whereas the cheapest one are "Suzuki" and "Mazda"
 
 So If you are looking for a cheap car, maybe looking for a Red Suzuki is a good starting point. (Not predicting the quality of the good here)
 
 
 Finnaly we plot a histogram of the data to understand this "mean values" and what they mean
 
 ![Price - Brands](/img/histplot.png "Hist plot")
 
 As we can see, "Ram" has a high avg price, because the segment is "pick up" only, and also we can see that brands like "Mazda" have very few units' which means that the average will not be representative.
 
 In this way we can get most commons brands as an input for the model, and try to predict those prices.
 
  
 ## Model
 
 As we have many categorical features (With no ordinal value) One hot encoding is a power tool we can use to categorize this data for a Random Forest regression.
 Is not as easy as applying the function. Fist it is important to understand the features we want to encode and to check if they are unique. For example the location column had 3 values inside (neighborhood-city-province) but sometimes it only had (neighborhood-city). So choosing only "city" seems like a good fit. 
 We also had many empty features, for example not all cars have "color" or "engine". We can try to remove this feature or to remove the rows with missing data. In the notebook we can see that the latter is a better choice since is brings a more accurate model. This obviously will depend on the feature importance.
 Finally, the deployed model returns a MAE of 400KARS aprox. For cars that range from 2M to 5M ARS this can mean from 20% to a 10% error. Which may not be acceptable but is not a bad starting point.
 
 Deploying the model is this case is easy. But it should implement a pipeline for continous develompent. As new data is scraped, cleaned and model re-trained.
 We chosoe Flask and Heorku for its simplicity and quick deploy.
 The font end should be improved for better user experience. By now is just a MVP.
 
 ## First conclusions
 What I understand is that more data is required to get a more accurate model and also keep on refining features. For example "engine" feature seems to be of high importance as you can try, a V8 engine vs a 1.6 engine can make a huge difference alone, but usually this comes along the car brand and model. 
 The next step would be to keep refining the features. It is obvious that we can reduce the engine list since there are many engines with different name but same value. Also more data needs to be scraped (we got 30K cars from 100K cars) So the data is available, more time is needed though.
 
 Overall this is a learning project and I can say that is incredible how much information we can get when data is clean and organized. But also to understand this is engineering when we say that there are many trade-offs here between time spent, computational power spent and the accuracy we want.
 
  
 
  
 


  


