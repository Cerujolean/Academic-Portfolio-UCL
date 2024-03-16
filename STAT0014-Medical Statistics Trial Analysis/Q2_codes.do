 use dataset_q2_J.dta, clear
 note: import data
 
 
 
 note: not sure what to include in exploratory analysis to address the problem (confounder)

 * the data overall and the crude effect(ingore confounder)
tab died mode
* show the crude effect risk ratio:0.9758
cs died mode

* the data by severity 
bysort severity: tab died mode
* show the risk ratio in each stratum
cs died mode, by(severity)

* confounder test for criteria 1: is severity a risk factor for died, independently of smoking?
graph bar died, over(severity) by(mode)

* confounder test for criteria 2: is severity associated with mode of transportation?
graph bar, over(severity) by(mode)
tab severity mode, col

* exploratory of age
sum age,detail
qnorm age
* find that the age is normally distributed, the median of age is 45, and the mean of age is 44.8
gen age_inverval = age
replace age_inverval=1 if age <= 45
replace age_inverval=0 if age > 45

* confounder test for criteria 1: is age a risk factor for died, independently of smoking?
graph bar died, over(age_inverval) by(mode)

* confounder test for criteria 2: is age associated with mode of transportation?
graph bar, over(severity) by(age_inverval)
graph bar (mean) died, over(age_inverval) by(mode)
graph box age, by(mode)
tab age_inverval mode, col

logistic died mode
logistic died mode, coef
logistic died mode severity
logistic died mode severity age_inverval##severity

sum age died

cs died mode
cs died mode, by(age)

tab died severity
cs died mode, by(severity)
ttest died, by(severity)

gen age_inverval = age
replace age_inverval=1 if age <= 50
replace age_inverval=0 if age >= 50

tab age_inverval died, row


   
   
   