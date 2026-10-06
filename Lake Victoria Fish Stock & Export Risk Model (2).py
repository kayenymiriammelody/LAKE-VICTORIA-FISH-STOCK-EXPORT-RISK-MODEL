#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries
import numpy as np
import statistics
import matplotlib.pyplot as plt


# In[2]:


"""As a baseline, generate 15 Fibonacci numbers as "stock" and explain in 3–5 
sentences why unbounded Fibonacci growth is biologically unrealistic."""
fibonacci = [0, 1]
while len(fibonacci) < 15:
    fibonacci.append(fibonacci[-1] + fibonacci[-2])

print("Fibonacci stock:")
print(fibonacci)


# In[3]:


"""Implement a FishStock class using the discrete logistic growth model with 
harvesting: N(t+1) = N(t) + r·N(t)·(1 − N(t)/K) − h·N(t). Use r = 0.4, K = 10,000 
tonnes, N(0) = 4,000 tonnes and simulate 52 weeks."""
import numpy as np
class FishStock:
    def __init__(self, r=0.4, K=10000, N0=4000, h=0.10):
        self.r = r
        self.K = K
        self.N0 = N0
        self.h = h

    def simulate(self, weeks=52):
        stock = [self.N0]
        harvest = []

        for week in range(weeks):
            N = stock[-1]
            H = self.h * N
            harvest.append(H)
            next_N = (N + self.r * N * (1 - N / self.K)- self.h * N)
            next_N = max(0, next_N)
            stock.append(next_N)

        return np.array(stock), np.array(harvest)


# In[4]:


#test the model
fish = FishStock(h=0.10)
stock, harvest = fish.simulate(weeks=52)
print("Initial stock:", stock[0], "tonnes")
print("Final stock:", stock[-1], "tonnes")
print("Total harvested:", harvest.sum(), "tonnes")


# In[5]:


"""Implement a PriceModel class that simulates the weekly price in UGX/kg as a 
seeded random walk starting at 12,000, with bounds (e.g. 9,000–16,000). Weekly 
revenue = harvest (kg) × price."""
class PriceModel:
    def __init__(self,start=12000,lower=9000,upper=16000,seed=42,step_sd=300):
        self.start = start
        self.lower = lower
        self.upper = upper
        self.seed = seed
        self.step_sd = step_sd

    def simulate(self, weeks=52):
        rng = np.random.default_rng(self.seed)
        prices = [self.start]
        for week in range(weeks - 1):
            change = rng.normal(0, self.step_sd)
            new_price = prices[-1] + change
            new_price = np.clip(new_price,self.lower,self.upper)
            prices.append(new_price)
        return np.array(prices)


# In[6]:


#generate the prices
price_model = PriceModel(seed=42)
prices = price_model.simulate(52)
print("First 10 weekly prices:")
print(prices[:10])


# In[7]:


#weekly revenue
#1 tonne = 1,000 kg
weekly_revenue = harvest * 1000 * prices
print(weekly_revenue)


# In[8]:


"""Compute the mean, median, variance, standard deviation and coefficient of 
variation (CV) of revenue with statistics. Explain why a raw variance threshold such 
as 50,000 is meaningless here."""
mean_revenue = statistics.mean(weekly_revenue)
median_revenue = statistics.median(weekly_revenue)
variance_revenue = statistics.variance(weekly_revenue)
std_revenue = statistics.stdev(weekly_revenue)
cv_revenue = std_revenue / mean_revenue
print("Mean revenue:", mean_revenue)
print("Median revenue:", median_revenue)
print("Variance:", variance_revenue)
print("Standard deviation:", std_revenue)
print("Coefficient of variation:", cv_revenue)


# In[9]:


"""Build a RiskAssessor class that classifies risk with a justified rule based on CV. Run 
a Monte Carlo simulation (≥1,000 price paths) and report the 5% Value-at-Risk of 
annual revenue."""
class RiskAssessor:
    def classify(self, cv):
        if cv < 0.10:
            return "Low"

        elif cv <= 0.20:
            return "Moderate"

        else:
            return "High"


# In[10]:


risk_assessor = RiskAssessor()
risk_class = risk_assessor.classify(cv_revenue)
print("Revenue CV:", cv_revenue)
print("Risk class:", risk_class)


# In[11]:


#monte carlo simulation
def monte_carlo_revenue(h=0.10,simulations=7000,weeks=52,seed=123):
    fish = FishStock(h=h)
    stock, harvest = fish.simulate(weeks)
    rng = np.random.default_rng(seed)
    changes = rng.normal(0,300,size=(simulations, weeks - 1))
    prices = np.zeros((simulations, weeks))
    prices[:, 0] = 12000
    prices[:, 1:] = (12000 + np.cumsum(changes, axis=1))
    prices = np.clip(prices, 9000, 16000)
    harvest_kg = harvest * 1000
    revenue = prices * harvest_kg
    annual_revenue = revenue.sum(axis=1)
    return annual_revenue


# In[12]:


annual_revenue = monte_carlo_revenue(h=0.10,simulations=7000)
var_5 = np.percentile(annual_revenue, 5)
print("Mean annual revenue:",np.mean(annual_revenue))
print("5% VaR:",var_5)


# In[13]:


"""Scenario analysis: run harvest rates h = 0.05, 0.10, 0.20 and 0.30. For each one, 
report the final stock, total revenue and risk class. Compare your results with the 
theoretical maximum sustainable yield, MSY = rK/4."""
harvest_rates = [0.05, 0.10, 0.20, 0.30]

scenario_results = []
price_model = PriceModel(seed=42)
prices = price_model.simulate(52)
for h in harvest_rates:
    fish = FishStock(h=h)
    stock, harvest = fish.simulate(52)
    revenue = harvest * 1000 * prices
    mean_rev = statistics.mean(revenue)
    median_rev = statistics.median(revenue)
    variance_rev = statistics.variance(revenue)
    sd_rev = statistics.stdev(revenue)
    cv = sd_rev / mean_rev
    risk = RiskAssessor().classify(cv)
    scenario_results.append({"Harvest rate": h,"Final stock (tonnes)": stock[-1],"Total harvest (tonnes)": harvest.sum(),
        "Total revenue (UGX)": revenue.sum(),"Mean weekly revenue (UGX)": mean_rev,"CV": cv,"Risk class": risk})
for result in scenario_results:
    print(result)


# In[14]:


#compared with maximum sustainable yield
r = 0.4
K = 10000
MSY = r * K / 4
print("Theoretical MSY:", MSY, "tonnes per week")


# In[15]:


"""Produce (a) stock trajectories for each harvest rate on one chart, and (b) a 
histogram of simulated annual revenue with the VaR marked."""
plt.figure(figsize=(10, 6))
for h in harvest_rates:
    fish = FishStock(h=h)
    stock, harvest = fish.simulate(52)
    plt.plot(range(53),stock,label=f"h = {h:.2f}")
plt.axhline(5000,linestyle="--",label="MSY stock = K/2 = 5,000 tonnes")
plt.title("Fish Stock Trajectories Under Different Harvest Rates")
plt.xlabel("Week")
plt.ylabel("Fish stock (tonnes)")
plt.legend()
plt.grid(True)
plt.show()


# In[16]:


plt.figure(figsize=(10, 6))
plt.hist(annual_revenue,bins=40)
plt.axvline(var_5,linestyle="--",linewidth=2,label=f"5% VaR = UGX {var_5/1e9:.1f} billion")
plt.title("Monte Carlo Simulation of Annual Fish Revenue")
plt.xlabel("Annual Revenue (UGX)")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True)
plt.show()


# In[17]:


""" Add a closed season (no harvesting for 8 weeks per year) and quantify its effect on 
long-run revenue over 5 years."""
harvest = 0
def simulate_closed_season(h=0.10,years=5,closed_weeks=8,seed=42):
    total_weeks = years * 52
    price_model = PriceModel(seed=seed)
    prices = price_model.simulate(total_weeks)
    N = 4000
    stock = [N]
    harvest = []
    for week in range(total_weeks):
        week_of_year = week % 52
        if week_of_year < closed_weeks:
            H = 0
        else:
            H = h * N
        harvest.append(H)
        N_next = (N + 0.4 * N * (1 - N / 10000)- H)
        N_next = max(0, N_next)
        stock.append(N_next)
        N = N_next

    stock = np.array(stock)
    harvest = np.array(harvest)
    revenue = harvest * 1000 * prices
    return stock, harvest, prices, revenue


# In[17]:


# No closed season
stock_normal, harvest_normal, prices_normal, revenue_normal = (
    simulate_closed_season(h=0.10,years=5,closed_weeks=0,seed=42))
# 8-week closed season
stock_closed, harvest_closed, prices_closed, revenue_closed = (
    simulate_closed_season(h=0.10,years=5,closed_weeks=8,seed=42))

normal_total = revenue_normal.sum()
closed_total = revenue_closed.sum()
difference = closed_total - normal_total
percentage_change = (difference / normal_total) * 100
print("5-year revenue without closed season:",
      normal_total)
print("5-year revenue with 8-week closed season:",
      closed_total)
print("Difference:",
      difference)
print("Percentage change:",
      percentage_change)

