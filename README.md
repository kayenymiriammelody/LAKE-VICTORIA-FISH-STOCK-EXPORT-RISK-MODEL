# LAKE-VICTORIA-FISH-STOCK-EXPORT-RISK-MODEL
This project aims to find out whether: 
- A fish-export cooperative in Jinja’s harvesting rate is sustainable
- how risky its revenue is
- This code was edited with the aid of CODEX, an Artificial Intelligence powered tool.
### IMPLEMENTATION
- Generated 15 Fibonacci numbers as a baseline. 
- Created a FishStock class using object oriented programming for a discrete logistic growth model with harvesting for 52 weeks.
- Created a PriceModel class that simulates weekly price in UGX/kg.
- Created a RiskAssessor class that classifies risk with a justified rule based on coefficient of variation.
- Ran a Monte Carlo simulation
- Illustrated findings
### FINDINGS, LIMITATIONS AND RECOMMENDATIONS
- Unbounded Fibonacci growth is unrealistic because it assumes that fish stock will keep increasing with time. It doesn’t account for death of fish due to diseases, competition and variations in living conditions among others. It also doesn’t take into account the reduction in fish population after the fish has been sold.
- After implementing the  FishStock class with an initial stock of4000 tonnes, the final stock after 52 weeks was found to be 7499.999925392722 tonnes and the total amount of fish harvested was 37362.5084681044 tonnes.
- The Mean revenue was 8734599777.197384, the median revenue was 8909306991.350906, the variance was 1.215715840879019e+18, the standard deviation was  1102595048.4556963 and the Coefficient of variation (CV) of  0.12623303603837005. A raw variance threshold is useless here because in sales and revenue analysis, it is difficult to use a single absolute value as a universal marker of risk because the meaning of a value depends on the scale of the business, the average revenue, the market, and the period being considered. Using the coefficient of variation is more realistic because it expresses the standard deviation relative to the mean for example, that of this analysis was 12.6%.
- The risk was classified as Moderate and was  0.12623303603837005 as per the RiskAssessor class created. After 7000 simulations using Monte Carlo simulation, the annual revenue was estimated to be UGX 449,005,884,471.4973and the 5% Value-at-Risk of annual revenue was UGX 375,300,782,715.3971 
- With the theoretical maximum sustainable yield at 1000tonnes, the harvest rate of 0.20 offers better revenue at a low risk compared to other run harvest rates. It has a total revenue of UGX 618.2, CV of 7.7%, total harvest of 50,871.7 tonnes with final stock of 5000 tonnes.
- The 8 week closed season reduced the 5-year revenue by 12.6% without closed season in the simulations. The five year revenue without 8 week closed season was 2,111,603,866,268.3682, the five year revenue with 8 week closed season was 1,838,748,938,783.082.

