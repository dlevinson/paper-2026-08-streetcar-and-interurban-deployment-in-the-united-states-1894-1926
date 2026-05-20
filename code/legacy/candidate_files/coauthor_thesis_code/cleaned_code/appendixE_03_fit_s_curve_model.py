import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import math
import statsmodels.api as sm
import statsmodels.formula.api as smf
import us
from fuzzywuzzy import fuzz

states = [str(i) for i in us.states.STATES] + ['D. C']
df = pd.read_csv('data.csv')
df['Year'] = df['Year'].astype(int)

xval = []
yval = []

years = [1894] + list(range(1898,1912)) + [1914] + list(range(1917, 1927))

place = [] #to record state
k_optimal = [] #to record best k value
params_intercept = [] #to record intercept
params_slope = [] #to record slope
params_rsquared_adj = [] #to record adj rsquared
params_pvalue = [] #to record pvalue
params_stderr_int = [] #to record intercept std error
params_stderr_slp = [] #to record slope std error
params_stderr_reg = [] #to record regression std error
time_inflex = [] #to record t0 
observes = [] #to record sample size
incdec = [] #to record if increase or decrease

for state in states:
    
        for year in years:

            #gathering data
            year_sum = 0

            for i in range(len(df)):
                if df['State'][i] == state and df['Year'][i] == year:
                    year_sum = year_sum + df['Miles'][i]

            yval.append(year_sum)
            xval.append(year)

        #finding s-curve
        k_loc = yval.index(max(yval)) #find the year with max track length

        if k_loc > len(yval) - 3: #it's very close to 1926, no need to make 2 separate s-curves
            k_start = int(max(yval)) + 1
            k_range = range(k_start + 1, round(k_start*1.5), 1) #generates a range of k-values to test, up to 150% of maximum

            reg_calc = []
            rsq_value = -1
            best_k = 0
            best_reg_calc = []

            for value in k_range:
                for i in range(len(yval)):
                    if yval[i] != 0: #if not a 0 mile year, use the equation ln(miles/k minus miles)
                        from_ln = np.log(yval[i]/(value - yval[i]))
                    else:
                        from_ln = -2 #low discouraging value for regression

                    reg_calc.append(from_ln) #save the value

                #once all reg_calc for that value found, find correlation coefficient, rsq
                correlation_matrix = np.corrcoef(xval, reg_calc)
                correlation_xy = correlation_matrix[0,1]
                r_squared = correlation_xy**2

                if r_squared > rsq_value: #if it's a better rsq than before, store it:
                    best_k = value
                    best_reg_calc = reg_calc

                    slope_value, slt0 = np.polyfit(xval, reg_calc, deg=1)
                    time_0 = -1 * slt0/slope_value

                reg_calc = [] #clear the reg_calc list so the loop can rerun for next k-value


            #once optimum k-value acquired:

            s_t = []
            for i in range(len(best_reg_calc)):
                power = xval[i] - time_0
                denom = 1 + math.exp(-1 * slope_value * power)
                total = best_k/denom
                s_t.append(total) #the k/1+e^-b(t-t0) equation

            plt.plot(xval, s_t, "tab:orange", label="S-curve")
            plt.plot(xval, yval, "tab:blue", label="McGraw Hill Data")
            plt.legend()
            plt.title(state)
            plt.xlim(1890, 1930)
            plt.xlabel('Year')
            plt.ylabel('Miles of track')
            plt.show()
            plt.clf()

            data2 = pd.DataFrame({'x':xval, 'y':best_reg_calc})
            model = smf.ols('y~x', data=data2).fit()

            #recording of stats
            place.append(state)
            observes.append(len(xval))
            time_inflex.append(time_0)
            k_optimal.append(best_k)
            params_intercept.append(model.params[0])
            params_slope.append(model.params[1])
            params_rsquared_adj.append(model.rsquared_adj) 
            params_pvalue.append(model.f_pvalue)
            params_stderr_int.append(model.bse[0])
            params_stderr_slp.append(model.bse[1])
            params_stderr_reg.append(model.scale**0.5)
            incdec.append('Inc')

            xval = []
            yval = []

        else: #if there does need to be two s-curves because the peak is in the middle
            inc_years = xval[:k_loc+1] #split into years with increasing values and years with decreasing values
            dec_years = xval[k_loc:] 

            inc_values = yval[:k_loc+1] #split into increasing values and decreasing values
            dec_values = yval[k_loc:]
            
            ##for regression with non-zero limits only: remove these two lines if regression with zero limit
            dec_years.append(1940)
            dec_values.append(max(yval)/3)

            #for INCREASING years
            k_start = int(max(yval)) + 1
            k_range = range(k_start + 1, k_start + 10, 1) #the range of k-values to test - max to max+10 (since known max)

            reg_calc = []
            rsq_value = -1
            best_k = 0
            best_reg_calc = []

            for value in k_range:
                for i in range(len(inc_values)):
                    if inc_values[i] != 0:
                        from_ln = np.log(inc_values[i]/(value-inc_values[i])) #the ln(miles/k minus miles) equation
                    else:
                        from_ln = -2
                    
                    reg_calc.append(from_ln)

                correlation_matrix = np.corrcoef(inc_years, reg_calc) #find the correlation coefficient and r squared value
                correlation_xy = correlation_matrix[0,1]
                r_squared = correlation_xy**2

                if r_squared > rsq_value: #if it's a better rsq than before, store it:
                    rsq_value = r_squared
                    best_k = value
                    best_reg_calc = reg_calc

                    slope_value, slt0 = np.polyfit(inc_years, reg_calc, deg=1)
                    time_0 = -1 * slt0/slope_value

                reg_calc = [] #clear the equation to run loop again

            inc_s_t = [] #once the best reg_calc has been found:

            for i in range(len(best_reg_calc)):
                power = inc_years[i] - time_0
                denom = 1 + math.exp(-1 * slope_value * power)
                total = best_k/denom
                inc_s_t.append(total)

            data2 = pd.DataFrame({'x':inc_years, 'y':best_reg_calc})
            model = smf.ols('y~x', data=data2).fit()

            place.append(state)
            observes.append(len(inc_years))
            time_inflex.append(time_0)
            k_optimal.append(best_k)
            params_intercept.append(model.params[0])
            params_slope.append(model.params[1])
            params_rsquared_adj.append(model.rsquared_adj) 
            params_pvalue.append(model.f_pvalue)
            params_stderr_int.append(model.bse[0])
            params_stderr_slp.append(model.bse[1])
            params_stderr_reg.append(model.scale**0.5)
            incdec.append('Inc')

            #for DECREASING years

            dec_reg_calc = []

            for i in range(len(dec_values)):
                from_ln = np.log(dec_values[i]/(best_k-dec_values[i])) #the ln(miles/k minus miles) equation
                dec_reg_calc.append(from_ln)

            correlation_matrix = np.corrcoef(dec_years, dec_reg_calc) #find the correlation coefficient and r squared value
            correlation_xy = correlation_matrix[0,1]
            r_squared = correlation_xy**2

            slope_value, slt0 = np.polyfit(dec_years, dec_reg_calc, deg=1)
            time_0 = -1 * slt0/slope_value

            dec_s_t = [] 

            for i in range(len(dec_reg_calc)):
                power = dec_years[i] - time_0
                denom = 1 + math.exp(-1 * slope_value * power)
                total = best_k/denom
                dec_s_t.append(total)

            data3 = pd.DataFrame({'x':dec_years, 'y':dec_reg_calc})
            model = smf.ols('y~x', data=data3).fit()

            place.append(state)
            observes.append(len(dec_years))
            time_inflex.append(time_0)
            k_optimal.append(best_k)
            params_intercept.append(model.params[0])
            params_slope.append(model.params[1])
            params_rsquared_adj.append(model.rsquared_adj) 
            params_pvalue.append(model.f_pvalue)
            params_stderr_int.append(model.bse[0])
            params_stderr_slp.append(model.bse[1])
            params_stderr_reg.append(model.scale**0.5)
            incdec.append('Dec')
            
            ##for non-zero regression ONLY
            dec_years = dec_years[:-1]
            dec_values = dec_values[:-1]

            plt.plot(xval, yval, "tab:blue", label="McGraw Hill Data")
            plt.plot(inc_years, inc_s_t, "tab:orange", label="Increasing S-Curve")
            plt.plot(dec_years, dec_s_t, "tab:pink", label="Decreasing S-Curve")
            plt.legend()
            plt.title(state)
            plt.xlabel('Year')
            plt.ylabel('Miles of track')
            plt.show()

            xval = []
            yval = []

result = pd.DataFrame({
        'State' : place,
        'Sample Size': observes,
        'K-value' : k_optimal,
        'Time Zero' : time_inflex,
        'Intercept' : params_intercept,
        'Slope' : params_slope,
        'RSQ-adj' : params_rsquared_adj,
        'Std error' : params_stderr_reg,
        'P-value' : params_pvalue,
        'Intercept error' : params_stderr_int,
        'Slope error' : params_stderr_slp,
        'IncDec' : incdec
    })

display(result)
