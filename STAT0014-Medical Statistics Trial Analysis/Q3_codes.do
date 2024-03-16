 note: Q3 partA
 
 use dataset_q3_J.dta, clear
 note: introducing data
 
 
 tab group
 note: table
 

 ttest hs12, by(group)
 note: comparing the average headache severity scores at  months between the two groups (approach 1)

generate hs_diff = hs12 - hs0
note: difference

ttest hs_diff, by(group)
note: compare the average of differences between headache severity at the time of randomisation and at 12 months, between the two groups





  
  