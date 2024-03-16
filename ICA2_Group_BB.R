# Read data and store in VotingData
VotingData <- read.csv(file = "ReferendumResults.csv")

# Load all the packages we may use in further coding
library(ggplot2)

## Recoding
# Deal with Deal with missing value "-1" 
VotingData$Leave[VotingData$Leave == -1] <- NA

## Introduce new variables we need to use in later analysis
# Add the proportion of "leave" vote for each ward
VotingData$LeavingRate <- VotingData$Leave / VotingData$NVotes

# Introduce three age groups to the original dataset
# Children: under 18
# Young-voters: 18-29
# Working_age: 30-64
# Retirement: above 65
VotingData$Children <- VotingData$Age_0to4 + VotingData$Age_5to7+ VotingData$Age_8to9 +
  VotingData$Age_10to14 + VotingData$Age_15 + VotingData$Age_16to17

VotingData$Young_Voters <- VotingData$Age_18to19 + VotingData$Age_20to24+ VotingData$Age_25to29

VotingData$Working_Age <- VotingData$Age_30to44 + VotingData$Age_45to59+ VotingData$Age_60to64

VotingData$Retirement <- VotingData$Age_65to74 + VotingData$Age_75to84+ VotingData$Age_85to89+
  VotingData$Age_90plus

# Introduce a new variable white_maj
# Value 1 represents that the ward is white majority
# Value 0 represents that the ward is not white majority
VotingData$white_maj[VotingData$White>=50] <- 1
VotingData$white_maj[VotingData$White<50] <- 0

# Perform Hierachical clustering for RegionName
RegionMeans <- # Means of covariates for each region
  aggregate(VotingData[,-(1:8)], by = list(VotingData$RegionName), FUN = mean)
rownames(RegionMeans) <- RegionMeans[,1]
RegionMeans <- scale(RegionMeans[,-1]) # Standardise to mean 0 & SD 1
Distances <- dist(RegionMeans) # Pairwise distances
ClusTree <- hclust(Distances, method = "complete") # Do the clustering
par(mar=c(3,3,3,1), mgp = c(2,0.75,0)) # Set plot margins
plot(ClusTree, xlab = "Region name", ylab = "Separation", cex.main = 0.8)
abline(h=8, col="red", lty=2)

# Regroup into 4 groups of similar regions
GroupByCluster <- cutree(ClusTree, k = 4)

# Print out which regions are categorised in the same new group
print(GroupByCluster, width = 90)

# Add the new generated group number into the original dataset
VotingData <- merge(data.frame(RegionName = names(GroupByCluster), NewGroup = factor(GroupByCluster)),
                    VotingData)

# Create a new data frame with only NA values
# The new dataset VotingData_NA is what we are going to predict
VotingData_NA <- VotingData[is.na(VotingData$Leave),]

# Create a new data frame with NA values removed
# We will use this new dataset VotingData_noNA to analyse the Leave votes
VotingData_noNA <- na.omit(VotingData)

# As we need to utilise VotingData_noNA for later analysis, 
# we attach it here
attach(VotingData_noNA)

## Explanatory Analysis
# Figure 1: three scatterplots representing LeavingRate vs. Qualification
# Add smooth regression lines for each scatterplot
par(mfrow = c(1,3))
plot(NoQuals, LeavingRate)
lines(lowess(y = LeavingRate,x=NoQuals), col = "tomato3", lwd = 2)
plot(L1Quals, LeavingRate)
lines(lowess(y = LeavingRate,x = L1Quals), col = "tomato3", lwd = 2)
plot(L4Quals_plus, LeavingRate)
lines(lowess(y = LeavingRate,x = L4Quals_plus), col = "tomato3", lwd = 2)
# Add a main title for these three plots
title(main = "Figure1: Leaving Rate vs. Qualification Level", outer = TRUE,
      line = -2)

# Figure 2: two scatterplots representing the relationship 
# between LeavingRate and Deprivation 
# Add smooth regression lines for each plot
par(mfrow = c(1,2))
plot(Deprived, LeavingRate)
lines(lowess(y = LeavingRate,x = Deprived), col = "tomato3", lwd = 2)
plot(MultiDepriv, LeavingRate)
lines(lowess(y = LeavingRate,x = MultiDepriv), col = "tomato3", lwd = 2)
# Add a main title for the two scatterplots
title(main = "Figure2: Leaving Rate vs. Deprivation / MultiDeprivation", 
      outer = TRUE, line = -2)

# Figure 3: scatterplot representing the relationship between adult mean age
# and proportion of Leave votes
# Add a smooth regression line
par(mfrow = c(1,1))
plot(AdultMeanAge, LeavingRate, main = "Figure3: Leaving Rate vs. Adult Mean Age")
lines(lowess(y=LeavingRate,x=AdultMeanAge), col = "tomato3", lwd = 2)

# Figure 4: three scatterplots representing the relationship between
# Leave votes and occupation
# Add smooth regression lines
par(mfrow = c(1,3))
plot(RoutineOccupOrLTU, LeavingRate)
lines(lowess(y = LeavingRate,x = RoutineOccupOrLTU), col = "tomato3", lwd = 2)
plot(HigherOccup, LeavingRate)
lines(lowess(y = LeavingRate,x = HigherOccup), col = "tomato3", lwd = 2)
plot(Unemp, LeavingRate)
lines(lowess(y = LeavingRate,x=Unemp), col = "tomato3", lwd = 2)
# Add a title for these three plots
title(main = "Figure4: Leaving Rate vs. Occupation", 
      outer = TRUE, line = -2)

# Figure 5: Create two box plots showing the difference between 
# white majority and other ethnic groups as majority
par(mfrow = c(1,1))
boxplot(LeavingRate~white_maj,
        main = "Figure5: Boxplots of LeavingRates on different ethnic groups")
points(c(mean(LeavingRate[white_maj==0]), mean(LeavingRate[white_maj==1]))
       ,col = "red", pch = 19)

# Table 1: create a correlation matrix for ethnicity and LeavingRate
print(cor(VotingData_noNA[,c(28:32,51)]))


# Figure 6: create box plots showing the difference between regions
par(mfrow = c(1,1))
boxplot(LeavingRate~RegionName, main = "Figure6: Boxplots of 
        LeavingRates on different regions")

# Figure 7: scatterplots representing relationship between proportion of Leave votes
# and population density, different region groups represented by colors
ggplot(VotingData_noNA, aes(x = Density, y = LeavingRate, 
                            color = as.factor(NewGroup))) + 
  geom_point(alpha = 0.8) + scale_color_manual(values = c("darkblue", "tomato", "green", "yellow")) + 
  ggtitle("       Figure7: Scatterplot between \n LeavingRate and population density") + 
  theme(plot.title = element_text(face = "bold")) +
  labs(color = "Region Group")

## Model Building
# Simple glm with all untransformed variables included
Model_0 <- glm(LeavingRate ~ MeanAge + AdultMeanAge + White + Black + Asian
               + Indian + Pakistani+ Owned + OwnedOutright + SocialRent +
                 PrivateRent + NoQuals + L1Quals + L4Quals_plus + Students 
               + Unemp + UnempRate_EA + HigherOccup + RoutineOccupOrLTU + Density
               + Deprived + MultiDepriv + C1C2DE + C2DE + DE + Children + Young_Voters
               + Working_Age + Retirement, 
               family = binomial, weights = NVotes)
summary(Model_0)
# Print out the dispersion parameter
cat("The dispersion parameter is", Model_0$deviance/Model_0$df.residual)

# The dispersion parameter in model_0 is too large
# Therefore, use Quasi-binomial distribution with all covariates
Model_1 <- glm(LeavingRate ~ MeanAge + AdultMeanAge + White + Black + Asian
               + Indian + Pakistani+ Owned + OwnedOutright + SocialRent +
                 PrivateRent + NoQuals + L1Quals + L4Quals_plus + Students 
               + Unemp + UnempRate_EA + HigherOccup + RoutineOccupOrLTU + Density
               + Deprived + MultiDepriv + C1C2DE + C2DE + DE + Children + Young_Voters
               + Working_Age + Retirement, 
               family = quasibinomial(link = "logit"), weights = NVotes)
summary(Model_1)

# To avoid collinearity, remove some covariates that sum up to 1
# We chose the covariates by previous analysis
# Then we got Model_2
Model_2 <- glm(LeavingRate ~ Asian + White + Black +
                 Owned + AdultMeanAge +
                 L4Quals_plus + Students 
               + RoutineOccupOrLTU + Density
               + Deprived + MultiDepriv + DE +  Young_Voters, 
               family = quasibinomial(link = "logit"), weights = NVotes)
summary(Model_2)
cat("proportion deviance explained is",1-(Model_2$deviance/Model_2$null.deviance))
# Consider cross effect after building Model_2
# Introduce interaction terms in Model_3
Model_3 <- glm(LeavingRate ~ NewGroup:White+NewGroup:Black+NewGroup:Asian
               +RoutineOccupOrLTU  + Density:NewGroup + AdultMeanAge:L4Quals_plus +  Owned + 
                 NewGroup:Young_Voters + MultiDepriv
               + DE + Deprived + L4Quals_plus:Deprived + Students,  
               family = quasibinomial(link = "logit"), 
               weights = NVotes)
summary(Model_3)
par(mfrow = c(2,2))
plot(Model_3)
title(main = "Figure8: various plots of Model_3", outer = TRUE,
      line = -1)

# Applied Chi-squared and F test to test the goodness of fit of two nested models
anova(Model_2, Model_3, test = "Chi")
anova(Model_2, Model_3, test = "F")  
# Print out the proportion of deviance explained
cat("proportion deviance explained is",1-(Model_3$deviance/Model_3$null.deviance))


## Create text file of our prediction on the missing values
# First, we should detach the dataset with existing values
detach(VotingData_noNA)

# Predict the missing value in VotingData_NA
predict_NA <- predict(Model_3, newdata=VotingData_NA, type = "response",
                      se.fit = TRUE)
# Extract prediction values from the generated dataset
predict_NA_fit <- predict_NA$fit

# Calculation of standard deviations of prediction errors
# Get variance of p_i
var_NA <- predict_NA$se.fit^2
# Get variance of Yi with the formula p_i*(1-p_1)/n
var_yi_NA <- predict_NA_fit*(1-predict_NA_fit)/VotingData_NA$NVotes
# Calculate standard deviation of prediction error
sd_error_NA <- sqrt(var_NA+var_yi_NA)

# Combine the calculations above with ward ID and prediction values
pred_table <- cbind(VotingData_NA$ID, predict_NA_fit, sd_error_NA)

# Generate the data into a table
write.table(pred_table, "ICA2_Group_BB_pred.dat", 
            sep = " ", row.names = FALSE, col.names = FALSE)

# Check whether the generated table is as required
pred_data <- read.csv("ICA2_Group_BB_pred.dat")


