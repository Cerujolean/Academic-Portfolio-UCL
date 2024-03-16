* import dataset
use dataset_q1_J.dta, clear

* Q1 

* A. 

* 1)
* count for missing data to be used in consort diagram
count if missing(appointment)

* 2). tables for baseline characteristics
* 2-way contigency tables for categorical variables
tab randgrp
tab withdrawn randgrp, col
tab compliance randgrp, col
tab appointment randgrp, col
tab site randgrp, col
tab gender randgrp, col
tab ethngrp randgrp, col
tab specgrp randgrp, col
* summary tables for continuous variables
bysort randgrp: sum age
bysort randgrp: sum dusoi
bysort randgrp: sum sf12phy0




* 3) an unadjusted, complete case ITT analysis
* a student's t-test between randgrp
ttest appointment, by(randgrp)
* an unadjusted logistic regression 
logistic appointment randgrp
* table providing risk difference and risk ratio
cs randgrp appointment


* 4) adjusted analysis (logistic regression model)
logistic appointment randgrp site gender age specgrp


* 5) investigation of the variable site
* logistic regression for London
logistic appointment randgrp if site == 0
* logistic regression for Shrewsbury
logistic appointment randgrp if site == 1
* logistic regression with interaction term
logistic appointment site##randgrp


