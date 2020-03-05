import numpy as np
import pandas as pd
from scipy import stats
import time
import matplotlib.pyplot as pyplot
from colour import Color
import seaborn as sns

class StackedBarPlotter:
     def __init__(self, filename, title, sheetDf):
        df = sheetDf/sheetDf.sum() * 100
        height=0.75
        fig = pyplot.figure(1, figsize=(len(df.columns.values)+1, 1))
        ax = fig.add_subplot(1,1,1) #, aspect=1
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        pyplot.title(r"$\bf{" + str(title) + "}$", size=14, y=1.15)
        
        columnIndexes = np.arange(len(df.columns.values))    # the x locations for the groups
        rowIndexes = np.arange(len(df.index.values))
        colorRange = sns.color_palette("RdYlGn", len(df.index.values))

        # getting middle position
        xMidPos = 0
        data = {}
        for index in df.index.values:
          data[index] = {'x':[], 'y':[],  'label':[], 'count':[], 'width':[], 'height':[], 'left':[], 'color':[], 'edgecolor':[]}
        
        for i in columnIndexes:
          columnName = df.columns.values[i]
          dfColumn = df.loc[:,columnName]
          dfRawColumn = sheetDf.loc[:,columnName]
          nbIndexes = len(dfColumn.index.values)
          if nbIndexes % 2: # unpaired
            midIndex = int(nbIndexes/2)
            leftMidPos = xMidPos - dfColumn[midIndex]/2
            data[midIndex]['label'].append(columnName)
            data[midIndex]['width'].append(dfColumn[midIndex])
            data[midIndex]['count'].append(dfRawColumn[midIndex])
            data[midIndex]['left'].append(leftMidPos)
            data[midIndex]['color'].append(colorRange[midIndex])
            data[midIndex]['y'].append(i)
            data[midIndex]['x'].append(leftMidPos + dfColumn[midIndex]/2)

            for j in range(midIndex-1, -1, -1):
              leftLeftPos = leftMidPos - dfColumn[j:midIndex].sum()
              data[j]['label'].append(columnName)
              data[j]['width'].append(dfColumn[j])
              data[j]['count'].append(dfRawColumn[j])
              data[j]['left'].append(leftLeftPos)
              data[j]['color'].append(colorRange[j])
              data[j]['y'].append(i)
              data[j]['x'].append(leftLeftPos + dfColumn[j]/2)

            for j in range(midIndex+1, len(dfColumn.index.values), +1):
              leftRightPos = leftMidPos + dfColumn[midIndex:j].sum()
              data[j]['label'].append(columnName)
              data[j]['width'].append(dfColumn[j])
              data[j]['count'].append(dfRawColumn[j])
              data[j]['left'].append(leftRightPos)
              data[j]['color'].append(colorRange[j])
              data[j]['y'].append(i)
              data[j]['x'].append(leftRightPos + dfColumn[j]/2)


          else: # paired
            midIndex = int(nbIndexes/2)
            for j in range(midIndex-1, -1, -1):
              leftLeftPos = xMidPos - dfColumn[j:midIndex].sum()
              data[j]['label'].append(columnName)
              data[j]['width'].append(dfColumn[j])
              data[j]['count'].append(dfRawColumn[j])
              data[j]['left'].append(leftLeftPos)
              data[j]['color'].append(colorRange[j])
              data[j]['y'].append(i)
              data[j]['x'].append(leftLeftPos + dfColumn[j]/2)

            for j in range(midIndex, len(dfColumn.index.values), +1):
              leftRightPos = xMidPos + dfColumn[midIndex:j].sum()
              data[j]['label'].append(columnName)
              data[j]['width'].append(dfColumn[j])
              data[j]['count'].append(dfRawColumn[j])
              data[j]['left'].append(leftRightPos)
              data[j]['color'].append(colorRange[j])
              data[j]['y'].append(i)
              data[j]['x'].append(leftRightPos + dfColumn[j]/2)
        print(data)
        for key, value in data.items():
          pyplot.barh(y=value['label'], width=value['width'], height=height, left=value['left'], color=value['color'])
          for x, y, v, c in zip(value['x'], value['y'], value['count'], value['color']):
            if int(v):
              pyplot.text(x, y, int(v), ha='center', va='center',  size=6, color='black')
        
        # plots = []
        # prevColumnValues = np.zeros(len(columnIndexes))
        # for i in rowIndexes:
        #     rowName = df.index.values[i]
        #     columnValues = df.loc[rowName,:]
        #     fillColorValues = [colorRange[i].rgb for j in range(len(columnIndexes))]
        #     edgeColorValues = [Color('black').rgb for j in range(len(columnIndexes))]
        #     textColorValues = [textColorRange[i].rgb for j in range(len(columnIndexes))]
        #     plots.append(pyplot.barh(columnIndexes, columnValues.values, width, left=prevColumnValues, color=fillColorValues, edgecolor=edgeColorValues))

        #     for x, py, cy, t, c in zip(columnIndexes, prevColumnValues, columnValues.values, columnValues.values, textColorValues):
        #         if t:
        #             pyplot.text(x, py + cy/2, "{:.1f}%".format(t/maxValue*100), ha='center', va='center',  size=10, color=c)
        #     prevColumnValues += columnValues.values

        pyplot.legend( labels=[key for key in data], loc='upper center', frameon=False, bbox_to_anchor=(0.5, 1.35),fancybox=False, shadow=False, ncol=len(data))
        pyplot.xlabel('FREQUENCY', size=9)
        ax.tick_params(axis='both', which='major', labelsize=9)
        pyplot.yticks(columnIndexes, df.columns.values)
        ax.set_xlim([-100, 100])
        vals = ax.get_xticks()
        ax.set_xticklabels([ str(int(abs(x))) + '%' for x in vals])
        fig.savefig(filename, bbox_inches='tight', dpi = 300)
        pyplot.close("all")
