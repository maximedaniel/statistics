
import numpy as np
import pandas as pd
from scipy import stats
import time
import statsmodels.api as sm
import math
from plotter.StackedBarPlotter import StackedBarPlotter 
from plotter.BoxPlotter import BoxPlotter 
from plotter.ScatterPlotter import ScatterPlotter 
import os

dataFile = 'data.xlsx'
imgDir = 'img'

if not os.path.exists(imgDir):
    os.makedirs(imgDir)


class Statistic:

    @staticmethod
    def qualNominalPaired(sheetName, sheetDf):
        print("######################################## ",sheetName," ########################################")
        meltedSheetDf = sheetDf.melt(var_name='columns', value_name='index')
        contingencySheetTable = pd.crosstab(index=meltedSheetDf['index'], columns=meltedSheetDf['columns'])
        #if len(splittedSheetName) > 1:
        #     orderedColumns = splittedSheetName[1].split('>')
        #     contingencySheetTable = contingencySheetTable.reindex(orderedColumns)
        contingencySheetTable.loc['COUNT'] = contingencySheetTable.sum().values
        contingencySheetTable = contingencySheetTable.drop(index='COUNT')
        
        if len(sheetDf.columns) > 2:
            print(contingencySheetTable)
            chi2, pvalue, dof, ex = stats.chi2_contingency(contingencySheetTable.T)
            print( sheetDf.columns.str.cat(sep=' | '), " -> CHI² (statistic: ", chi2, ", p-value: ", pvalue,")")
        for i in range(len(sheetDf.columns.values)):
            for j in range(i+1, len(sheetDf.columns.values)):
                try:
                    ctab = contingencySheetTable[[sheetDf.columns.values[i], sheetDf.columns.values[j]]]
                    print(ctab)
                    chi2, pvalue, dof, ex = stats.chi2_contingency(ctab)
                    print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j],  " -> CHI² (statistic: ", chi2, ", p-value: ", pvalue,")")
                except ValueError as ChiError:
                    print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j],  " -> CHI² (",ChiError,")")
                    try:
                        ctab = contingencySheetTable[[sheetDf.columns.values[i], sheetDf.columns.values[j]]]
                        oddsratio, pvalue = stats.fisher_exact(ctab)
                        print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j], " -> Fisher (statistic: ", oddsratio, ", p-value: ", pvalue,")")
                    except ValueError as FisherError:
                        print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j], " -> Fisher (", FisherError,")")
    
    @staticmethod
    def qualNominalUnpaired(sheetName, sheetDf):
        print("######################################## ",sheetName," ########################################")
        meltedSheetDf = sheetDf.melt(var_name='columns', value_name='index')
        contingencySheetTable = pd.crosstab(index=meltedSheetDf['index'], columns=meltedSheetDf['columns'])
        #if len(splittedSheetName) > 1:
        #    orderedColumns = splittedSheetName[1].split('>')
        #    contingencySheetTable = contingencySheetTable.reindex(orderedColumns)
        contingencySheetTable.loc['COUNT'] = contingencySheetTable.sum().values
        
        if len(sheetDf.columns) > 2:
            print(contingencySheetTable)
            contingencySheetTable = contingencySheetTable.drop(index='COUNT')
            chi2, pvalue, dof, ex = stats.chi2_contingency(contingencySheetTable.T)
            print( sheetDf.columns.str.cat(sep=' | '), " -> CHI² (statistic: ", chi2, ", p-value: ", pvalue,")")
        
        for i in range(len(sheetDf.columns.values)):
            for j in range(i+1, len(sheetDf.columns.values)):
                try:
                    ctab = contingencySheetTable[[sheetDf.columns.values[i], sheetDf.columns.values[j]]]
                    print(ctab)
                    chi2, pvalue, dof, ex = stats.chi2_contingency(ctab)
                    print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j],  " -> CHI² (statistic: ", chi2, ", p-value: ", pvalue,")")
                except ValueError as ChiError:
                    print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j],  " -> CHI² (",ChiError,")")
                    try:
                        ctab = contingencySheetTable[[sheetDf.columns.values[i], sheetDf.columns.values[j]]]
                        oddsratio, pvalue = stats.fisher_exact(ctab)
                        print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j], " -> Fisher (statistic: ", oddsratio, ", p-value: ", pvalue,")")
                    except ValueError as FisherError:
                        print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j], " -> Fisher (", FisherError,")")
        StackedBarPlotter(
         filename =  imgDir + '/' + sheetName + '.png', 
         title = sheetName,
         sheetDf = contingencySheetTable)

    @staticmethod
    def qualOrdinalPaired(sheetName, sheetDf):
        print("######################################## ",sheetName," ########################################")
        meltedSheetDf = sheetDf.melt(var_name='columns', value_name='index')
        contingencySheetTable = pd.crosstab(index=meltedSheetDf['index'], columns=meltedSheetDf['columns'])
        contingencySheetTable.loc['COUNT'] = contingencySheetTable.sum().values
        contingencySheetTable = contingencySheetTable.drop(index='COUNT')
        
        if len(sheetDf.columns) > 2:
            print(sheetDf)
            statistic, pvalue = stats.friedmanchisquare( *[content.values for label, content in sheetDf.iteritems()])
            print( sheetDf.columns.str.cat(sep=' | '), " -> Friedman (statistic:", statistic, " p-value: ", pvalue, ")")

        for i in range(len(sheetDf.columns.values)):
            for j in range(i+1, len(sheetDf.columns.values)):
                try:
                    ctab = contingencySheetTable[[sheetDf.columns.values[i], sheetDf.columns.values[j]]]
                    print(ctab)
                    statistic, pvalue = stats.wilcoxon(sheetDf[sheetDf.columns.values[i]], sheetDf[sheetDf.columns.values[j]])
                    print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j],  " -> Wilcoxon (statistic: ", statistic, ", p-value: ", pvalue,")")
                except ValueError as WilcoxonError:
                    print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j],  " -> Wilcoxon (",WilcoxonError,")")
        StackedBarPlotter(
         filename =  imgDir + '/' + sheetName + '.png', 
         title = sheetName,
         sheetDf = contingencySheetTable)

    @staticmethod
    def qualOrdinalUnpaired(sheetName, sheetDf):
        print("######################################## ",sheetName," ########################################")
        meltedSheetDf = sheetDf.melt(var_name='columns', value_name='index')
        contingencySheetTable = pd.crosstab(index=meltedSheetDf['index'], columns=meltedSheetDf['columns'])
        contingencySheetTable.loc['COUNT'] = contingencySheetTable.sum().values
        contingencySheetTable = contingencySheetTable.drop(index='COUNT')
        if len(sheetDf.columns) > 2:
            print(sheetDf)
            statistic, pvalue = stats.kruskal( *[content.values for label, content in sheetDf.iteritems()])
            print( sheetDf.columns.str.cat(sep=' | '), " -> Kruskal-Wallis (statistic:", statistic, " p-value: ", pvalue, ")")
        for i in range(len(sheetDf.columns.values)):
            for j in range(i+1, len(sheetDf.columns.values)):
                try:
                    ctab = contingencySheetTable[[sheetDf.columns.values[i], sheetDf.columns.values[j]]]
                    print(ctab)
                    ans = sm.stats.Table(ctab).test_ordinal_association()
                    print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j],  " -> Cochran-Armitage (statistic: ", ans.statistic, ", p-value: ", ans.pvalue,")")
                except ValueError as CochranArmitageError:
                    print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j],  " -> Cochran-Armitage (",CochranArmitageError,")")
        StackedBarPlotter(
         filename =  imgDir + '/' + sheetName + '.png', 
         title = sheetName,
         sheetDf = contingencySheetTable)
    
    @staticmethod
    def quantPaired(sheetName, sheetDf):
        print("######################################## ",sheetName," ########################################")
        if len(sheetDf.columns) > 2:
            print(sheetDf)
            statistic, pvalue = stats.friedmanchisquare( *[content.values for label, content in sheetDf.iteritems()])
            print( sheetDf.columns.str.cat(sep=' | '), " -> Friedman (statistic:", statistic, " p-value: ", pvalue, ")")

        for i in range(len(sheetDf.columns.values)):
            for j in range(i+1, len(sheetDf.columns.values)):
                try:
                    df = sheetDf[[sheetDf.columns.values[i], sheetDf.columns.values[j]]]
                    print(df)
                    statistic, pvalue = stats.ttest_rel(*[content.values for label, content in df.iteritems()])
                    print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j],  " -> Student (statistic: ", statistic, ", p-value: ", pvalue,")")
                except ValueError as StudentError:
                    print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j],  " -> Student (",StudentError,")")
        BoxPlotter(
         filename =  imgDir + '/' + sheetName + '.png', 
         title = sheetName,
         sheetDf = sheetDf)

    @staticmethod
    def quantUnpaired(sheetName, sheetDf):
        print("######################################## ",sheetName," ########################################")
        if len(sheetDf.columns) > 2:
            print(sheetDf)
            statistic, pvalue = stats.f_oneway(*[content.values for label, content in sheetDf.iteritems()])
            print( sheetDf.columns.str.cat(sep=' | '), " -> ANOVA (statistic:", statistic, " p-value: ", pvalue, ")")
        for i in range(len(sheetDf.columns.values)):
            for j in range(i+1, len(sheetDf.columns.values)):
                try:
                    df = sheetDf[[sheetDf.columns.values[i], sheetDf.columns.values[j]]]
                    print(df)
                    statistic, pvalue = stats.ttest_ind(*[content.values for label, content in df.iteritems()])
                    print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j],  " -> Student (statistic: ", statistic, ", p-value: ", pvalue,")")
                except ValueError as StudentError:
                    print(sheetDf.columns.values[i],'|', sheetDf.columns.values[j],  " -> Student (",StudentError,")")
        BoxPlotter(
         filename =  imgDir + '/' + sheetName + '.png', 
         title = sheetName,
         sheetDf = sheetDf)
         
    @staticmethod
    def biQuantUnpaired(sheetName, sheetDf):
        print("######################################## ",sheetName," ########################################")
        try:
            print(sheetDf)
            coefficient, pvalue = stats.pearsonr(sheetDf.iloc[:,0], sheetDf.iloc[:,1])
            print(sheetDf.columns.values[0],'|', sheetDf.columns.values[1], " -> Pearson Correlation (coefficient: ", coefficient,", pvalue: ", pvalue, ")")
            try:
                slope, intercept, r_value, p_value, std_err = stats.linregress(sheetDf.iloc[:,0], sheetDf.iloc[:,1])
                print(sheetDf.columns.values[0],'|', sheetDf.columns.values[1], " -> Linear Regression (slope: ",slope, ", intercept: ", intercept, ", r_value: ", r_value, ", p_value: ", p_value, ", std_err: ", std_err, ")")
            except ValueError as LinearRegressError:
                print(sheetDf.columns.values[0],'|', sheetDf.columns.values[1], " -> Linear Regression (",LinearRegressError,")")
        except ValueError as PearsonError:
            print(sheetDf.columns.values[0],'|', sheetDf.columns.values[1], " -> Pearson Correlation (",PearsonError,")")
       
        ScatterPlotter(
         filename =  imgDir + '/' + sheetName + '.png', 
         title = sheetName,
         sheetDf = sheetDf,
         slope= slope,
         intercept= intercept)

         
# Parse .xlsx file
dictDf = pd.read_excel(dataFile, sheet_name=None)
# Iterating key, value over Excel dictionary
for sheetName, sheetDf in dictDf.items():
    splittedSheetName = sheetName.split('|')
    statType = splittedSheetName[1]
    switcher = {
        'QNP': Statistic.qualNominalPaired,
        'QNU': Statistic.qualNominalUnpaired,
        'QOP': Statistic.qualOrdinalPaired,
        'QOU': Statistic.qualOrdinalUnpaired,
        'QP': Statistic.quantPaired,
        'QU': Statistic.quantUnpaired,
        '2QU': Statistic.biQuantUnpaired,
    }
    statFunc = switcher.get(statType, lambda: "Bad statType")
    statFunc(splittedSheetName[0], sheetDf)


