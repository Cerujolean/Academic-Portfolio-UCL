####task1
wind <- read.csv("wind_data.csv")
temp <- read.csv("temp_data.csv")
covid <- read.csv("covid_cases.csv")

#create function
compute_velocity <- function(U1,V1){
  velocity <- sqrt(U1^2+V1^2) #euclidean form
  print(velocity)
}

#store wind velocity in wind_velocity_table
wind_velocity_table <- matrix(nrow = 8294, ncol = 1)
for (i in 1:8294) {
  wind_velocity_table[i,] <- compute_velocity(wind[i,3],wind[i,4])
}

#add wind velocity to wind_data
wind$wind_velocity <- wind_velocity_table

#create first dataset(temp and wind velocity)
dataset_1 <- data.frame(temp[,1:3],wind[,5])
colnames(dataset_1) <- c("Date","Lads","Temperature","Wind_velocity")

#calculate cases per 100k
cases_per_100k <- 100000/covid[,5]*covid[,4]
covid$cases_per_100k <- cases_per_100k

#save csv files
write.csv(dataset_1,"uk_weather.csv")

#plots of dataset1
##scatterplot
pdf(file = "fig4.pdf")
par(mfrow = c(1,1))
plot(dataset_1$Temperature, dataset_1$Wind_velocity, 
     main = "scatterplot 3: Wind velocity versus Temperature", 
     xlab = "Temperature", ylab = "Wind velocity",
     pch = 19, cex = 0.3)
abline(lm(dataset_1$Wind_velocity~dataset_1$Temperature), 
       col = "red", lwd = 3)
corr_coeff_temp_vwind <- cor(dataset_1$Temperature, dataset_1$Wind_velocity)
dev.off()

##histogram
pdf(file = "fig1.pdf")
hist(dataset_1$Temperature, main = "Histogram 1:Temperature",
     xlab = "Temperature", cex.main = 1.5)
summ_temp <- summary(dataset_1$Temperature)
abline(v = summ_temp[2:5], col = c("red","blue","purple","orange"))
legend(x="topright", c("Q1","Median","Mean","Q3"),
       text.col = c("red","blue", "purple", "orange"), bg = "cornsilk",
       cex = 1, x.intersp = 0.5, y.intersp = 0.5, inset = 0.04)
skewness_temp <- mean(((dataset_1[,3]-mean(dataset_1[,3]))/sd(dataset_1[,3]))^3)
dev.off()

pdf(file = "fig2.pdf")
summ_wind <- summary(dataset_1$Wind_velocity)
hist(dataset_1$Wind_velocity, 
     main = "Histogram 2: Wind Velocity",
     xlab = "Wind Velocity", cex.main = 1.5)
abline(v = summ_wind[2:5], col = c("red","blue","purple","orange"))
legend(x="topright", c("Q1","Median","Mean","Q3"),
       text.col = c("red","blue", "purple", "orange"), bg = "cornsilk",
       x.intersp = 0.5, y.intersp = 0.5, cex = 1, inset = 0.04)
skewness_wind <- mean(((dataset_1[,4]-mean(dataset_1[,4]))/sd(dataset_1[,4]))^3)
dev.off()

#create dataset2 
lads_covid <- covid[,1]
lads_wind <- wind[,2]
lads_table <- matrix()
lads_covid_cases <- matrix()
temp_new_table <- matrix()
wind_new_table <- matrix()

##store lads(both in covid and temp) in table
for (i in 1:8294){
  ladsname_wind <- lads_wind[i]
  vwind <- wind$wind_velocity[i]
  temp_value <- temp$value[i]
  for (j in 1:6864){
    ladsname_covid <- lads_covid[j]
    covid_cases <- covid$cases_per_100k[j]
    if (ladsname_wind == ladsname_covid){
      lads_table <- rbind(lads_table, ladsname_wind)
      lads_covid_cases <- rbind(lads_covid_cases, covid_cases)
      temp_new_table <- rbind(temp_new_table, temp_value)
      wind_new_table <- rbind(wind_new_table, vwind)
      break
    }
  }
}

new_table <- data.frame(lads_table,lads_covid_cases, temp_new_table, wind_new_table)
dataset_2 <- new_table[order(new_table$lads_table),]
colnames(dataset_2) <- c("lads","covid per 100k population","temp","wind velocity")

#save csv files
write.csv(dataset_2,"england_data.csv")

##scatterplot
pdf("fig3.pdf")
par(mfrow = c(1,2))
plot(dataset_2$temp, dataset_2$`covid per 100k population`, 
     main = "scatterplot 1: covid cases per 
  100k population versus Temperature", 
     xlab = "Temperature", ylab = "Covid per 100k population",
     pch = 19, cex = 0.3, cex.main=1)
abline(lm(dataset_2$`covid per 100k population`~dataset_2$temp), 
       col = "red", lwd = 3)
corr_coeff_temp_covid <- cor(dataset_2$`covid per 100k population`, dataset_2$temp, use = "complete.obs")

plot(dataset_2$`wind velocity`, dataset_2$`covid per 100k population`, 
     main = "scatterplot 2: covid cases per 
   100k population versus wind velocity", 
     xlab = "Wind velocity", ylab = "Covid per 100k population",
     pch = 19, cex = 0.3, cex.main=1)
abline(lm(dataset_2$`covid per 100k population`~dataset_2$`wind velocity`), 
       col = "red", lwd = 3)
corr_coeff_vwind_covid <- cor(dataset_2$`wind velocity`, dataset_2$`covid per 100k population`, use = "complete.obs")
dev.off()

######Task 2

###(a)

##(i) Measurements of England

#Average temperature per day
temp_eng <- temp [which (temp$lads %in% covid$lads), ]
ave_temp_eng<-aggregate (temp_eng$value, by = list (date = temp_eng$date), mean)
colnames (ave_temp_eng) <- c ("date", "temp mean")
ave_temp_eng

#Average wind velocity per day
wind_eng <- wind [which (wind$lads %in% covid$lads), ]
ave_vel_eng <- aggregate (wind_eng$wind_velocity, by = list (date = wind_eng$date), mean)
colnames (ave_vel_eng) <- c ("date", "average vel")
ave_vel_eng

##(ii) Measurements of the rest of UK excluding England

#Average temperature per day
temp_oth <- temp [-which (temp$lads %in% covid$lads), ]
ave_temp_oth<-aggregate (temp_oth$value, by = list (date = temp_oth$date), mean)
colnames (ave_temp_oth) <- c ("date", "temp mean")
ave_temp_oth

#Average wind velocity per day
wind_oth <- wind [-which (wind$lads %in% covid$lads), ]
ave_vel_oth <- aggregate (wind_oth$wind_velocity, by = list (date = wind_oth$date), mean)
colnames (ave_vel_oth) <- c ("date", "average vel")
ave_vel_oth

temp_wind <- data.frame(ave_temp_eng$`temp mean`, ave_temp_oth$`temp mean`,
                              ave_vel_eng$`average vel`, ave_vel_oth$`average vel`, row.names = ave_temp_eng$date)
temp_wind_table <- as.data.frame(t(temp_wind),   
                                 row.names = c( "avg temp England", "avg temp other", "avg v.wind England", "avg v.wind other"))

temp_date <- names(temp_wind_table)
rnames <- rownames(temp_wind_table)
temp_wind_names <- list()
temp_data <- list()
for(i in 1:4){
  rname <- rnames[i]
  for(j in 1:22){
    temp_data <- c(temp_data, temp_wind_table[i,j])
    temp_wind_names <- c(temp_wind_names, paste(temp_date[j],rname))
  }
}

###(b)


##Temperature

x <- ave_temp_eng$`temp mean`
y <- ave_temp_oth$`temp mean`

#Firstly the normality of the data is tested to decide which statistical test is used
shapiro.test(x-y)
#p-value is 0.5245 which is greater than 0.05, so x-y is normally distributed

#one-sample t-test is used and the sample is x-y, 
#difference in temperature of England and non-England area

#H0:The rest of UK is warmer than England
#H1:England is warmer than other areas

t.test (x-y, alternative = "greater")
p_value_temp <- t.test (x-y, alternative = "greater")$p.value

#p-value is 0.003871, less than 0.05
#accept alternative, so accept H1


##Velocity
a <- ave_vel_eng$`average vel`
b <- ave_vel_oth$`average vel`

#Firstly the normality of the data is tested to decide which statistical test is used
shapiro.test(a-b)
#p-value is 0.5691 which is greater than 0.05, so a-b is normally distributed

#H0:The rest of UK is more windy than England
#H1:England is more windy than the rest of UK

t.test (a-b, alternative = "greater")
#p-value is 0.06575, greater than 0.05
#there is no clear evidence to reject H0
#therefore, The rest of UK is more windy than England
p_value_wind <- t.test (a-b, alternative = "greater")$p.value

######Task 3

#Covid cases per 100k people
covid_cases_per_100k_people <- c()
sum_of_covid_cases<-aggregate (covid$cases, by = list (date = covid$date), sum)
sum_of_population<-aggregate (covid$population, by = list (date = covid$date), sum)
population <- sum_of_population$x[1]
for(i in sum_of_covid_cases$x)
{
  covid_cases_per_100k_people <- c(covid_cases_per_100k_people,(i/population)*100000)
}

#Covid cases per wind speed
WindSpeed <- c()
for(i in ave_vel_eng$`average vel`)
{
  WindSpeed <- c(WindSpeed,i)
}
plot(WindSpeed,covid_cases_per_100k_people,main = "Covid cases/Wind speed",
     abline(lm(covid_cases_per_100k_people~WindSpeed),col = "red"),cex = 0.5,xlab = "Wind speed",
     ylab = "Covid cases per 100k people")

#Covid Case Per Temperature in K
Temperature <- c()
for(i in ave_temp_eng$`temp mean`)
{
  Temperature <- c(Temperature,i)
}
plot(Temperature,covid_cases_per_100k_people,main = "Covid cases/Temperature in K",
     abline(lm(covid_cases_per_100k_people~Temperature),col = "red"),cex = 0.5,xlab = "Temperature in K",
     ylab = "Covid cases per 100k people")


#Covid infections and wind velocity
#H0:there is not a monotonic linear relationship between daily covid infections and wind velocity, p=0
#H1:there is a monotonic linear relationship between daily covid infections and wind velocity,p>0

model=lm(covid_cases_per_100k_people~WindSpeed)
summary(model)
p_value_covid_wind <- summary(model)$coefficients[2,4]

#p-value is less than 0.01, reject H0

#Covid infections and temperature
#H0:there is not a monotonic relationship between daily covid infections and temperature, p=0
#H1:there is a monotonic relationship between daily covid infections and temperature, p>0

model=lm(covid_cases_per_100k_people~Temperature)
summary(model)
p_value_covid_temp <- summary(model)$coefficients[2,4]

#Sufficient evidence to accept H0

#all data used in report
value_temp <- matrix(summ_temp)
value_wind <- matrix(summ_wind)

value <- c(skewness_temp, skewness_wind,
                         corr_coeff_temp_covid, corr_coeff_temp_vwind,
                         corr_coeff_vwind_covid, value_temp,
                         value_wind, temp_data, p_value_wind, p_value_temp,
                         p_value_covid_temp, p_value_covid_wind)

summ_temp_names <- names(summ_temp)
new_temp_names <- paste(summ_temp_names, "(temp)", sep = "")
summ_wind_names <- names(summ_wind)
new_wind_names <- paste(summ_wind_names, "(wind)", sep = "")

names <- c("skewness of temp", "skewness of wind", 
           "corr coeff of temp and covid", "corr coeff of temp and vwind",
           "corr coeff of vwind and covid", new_temp_names,
           new_wind_names, temp_wind_names, "p value of wind data",
           "p value of temperature", "p value of covid and temperature",
           "p value of covid and wind")

data_mat <- cbind(names, value)

#export statistics to txt file
write.table(data_mat, file = "output.txt")
