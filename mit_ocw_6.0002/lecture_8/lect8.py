import random 
import pylab 
import numpy
import matplotlib.pyplot as plt

#set line width
plt.rcParams['lines.linewidth'] = 4
#set font size for titles 
plt.rcParams['axes.titlesize'] = 12
#set font size for labels on axes
plt.rcParams['axes.labelsize'] = 12
#set size of numbers on x-axis
plt.rcParams['xtick.labelsize'] = 8
#set size of numbers on y-axis
plt.rcParams['ytick.labelsize'] = 8
#set size of ticks on x-axis
plt.rcParams['xtick.major.size'] = 8
#set size of ticks on y-axis
plt.rcParams['ytick.major.size'] = 8
#set size of markers
plt.rcParams['lines.markersize'] = 8
#set number of examples shown in legends
plt.rcParams['legend.numpoints'] = 1


def makeHist(data, title, xlabel, ylabel, bins = 20, fig=None):
    plt.hist(data, bins = bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)



def getHighs():
    inFile = open('temperatures.csv')
    population = []
    for l in inFile:
        try:
            tempC = float(l.split(',')[1])
            population.append(tempC)
        except:
            continue
    return population

def getMeansAndSDs(population, sample, verbose = False, vline=False):

    popMean = sum(population)/len(population)
    sampleMean = sum(sample)/len(sample)
    if verbose:
        plt.figure(figsize=(12,4))
        plt.subplot(121)
        makeHist(population,
                 'Daily High 1961-2015, Population\n' +\
                 '(mean = '  + str(round(popMean, 2)) + ')'+\
                 '\n(std =' + str(round(numpy.std(population),2)) + ')',
                 'Degrees C', 'Number Days')
        if vline:
            pylab.axvline(x = popMean, color = 'r')

        #pylab.figure()
        plt.subplot(122)
        makeHist(sample, 'Daily High 1961-2015, Sample\n' +\
                 '(mean = ' + str(round(sampleMean, 2)) + ')'+\
                 '\n(std =' + str(round(numpy.std(sample),2)) + ')',
                 'Degrees C', 'Number Days')   
        if vline:
            pylab.axvline(x = popMean, color = 'r')

    #     print('Population mean:', round(popMean,2))
    #     print('Standard deviation of population:',
    #           round(numpy.std(population)),2)
    #     print('Sample mean:', round(sampleMean,2))
    #     print('Standard deviation of sample:',
    #           round(numpy.std(sample),2))
    return popMean, sampleMean,\
           numpy.std(population), numpy.std(sample)

#random.seed(0)         
#population = getHighs()
#sample = random.sample(population, 100)
#getMeansAndSDs(population, sample, True)

#random.seed(0) 
#population = getHighs()
#sampleSize = 100
#numSamples = 1000
#sampleMeans = []
#for i in range(numSamples):
#    sample = random.sample(population, sampleSize)
#    popMean, sampleMean, popSD, sampleSD =\
#       getMeansAndSDs(population, sample, verbose = False)
#    sampleMeans.append(sampleMean)
#print('Mean of sample Means =',
#      round(sum(sampleMeans)/len(sampleMeans), 3))
#print('Standard deviation of sample means =',
#      round(numpy.std(sampleMeans), 3))
#makeHist(sampleMeans, 'Means of Samples', 'Mean', 'Frequency')
#pylab.axvline(x = popMean, color = 'r')

def showErrorBars(population, sizes, numTrials):
    xVals = []
    sizeMeans, sizeSDs = [], []
    for sampleSize in sizes:
        xVals.append(sampleSize)
        trialMeans = []
        for t in range(numTrials):
            sample = random.sample(population, sampleSize)
            popMean, sampleMean, popSD, sampleSD =\
               getMeansAndSDs(population, sample)
            trialMeans.append(sampleMean)
        sizeMeans.append(sum(trialMeans)/len(trialMeans))
        sizeSDs.append(numpy.std(trialMeans))
    print(sizeSDs)
    pylab.errorbar(xVals, sizeMeans,
                   yerr = 1.96*pylab.array(sizeSDs), fmt = 'o',
                   label = '95% Confidence Interval')
    pylab.title('Mean Temperature ('
                + str(numTrials) + ' trials)')
    pylab.xlabel('Sample Size')
    pylab.ylabel('Mean')
    pylab.axhline(y = popMean, color ='r', label = 'Population Mean')
    pylab.xlim(0, sizes[-1] + 10)
    pylab.legend()

#random.seed(0)
#population = getHighs()   
#showErrorBars(population,
#              (50, 100, 200, 300, 400, 500, 600), 100)

def sem(popSD, sampleSize):
    return popSD/sampleSize**0.5

#sampleSizes = (25, 50, 100, 200, 300, 400, 500, 600)
#numTrials = 50
#population = getHighs()
#popSD = numpy.std(population)
#sems = []
#sampleSDs = []
#for size in sampleSizes:
#    sems.append(sem(popSD, size))
#    means = []
#    for t in range(numTrials):
#        sample = random.sample(population, size)
#        means.append(sum(sample)/len(sample))
#    sampleSDs.append(numpy.std(means))
#pylab.plot(sampleSizes, sampleSDs,
#           label = 'Std of ' + str(numTrials) + ' means')
#pylab.plot(sampleSizes, sems, 'r--', label = 'SEM')
#pylab.xlabel('Sample Size')
#pylab.ylabel('Std and SEM')
#pylab.title('SD for ' + str(numTrials) + ' Means and SEM')
#pylab.legend()

def plotDistributions():
    uniform, normal, exp = [], [], []
    for i in range(100000):
        uniform.append(random.random())
        normal.append(random.gauss(0, 1))
        exp.append(random.expovariate(0.5))
    makeHist(uniform, 'Uniform', 'Value', 'Frequency')
    pylab.figure()
    makeHist(normal, 'Gaussian', 'Value', 'Frequency')
    pylab.figure()
    makeHist(exp, 'Exponential', 'Value', 'Frequency')

#plotDistributions()

def getDiffs(population, sampleSizes):
    popStd = numpy.std(population)
    diffsFracs = []
    for sampleSize in sampleSizes:
        diffs = []
        for t in range(100):
            sample = random.sample(population, sampleSize)
            diffs.append(abs(popStd - numpy.std(sample)))
        diffMean = sum(diffs)/len(diffs)
        diffsFracs.append(diffMean/popStd)
    return pylab.array(diffsFracs)*100
    
def plotDiffs(sampleSizes, diffs, title, label, color = 'b'):
    pylab.plot(sampleSizes, diffs, label = label,
               color = color)
    pylab.xlabel('Sample Size')
    pylab.ylabel('% Difference in SD')
    pylab.title(title)
    pylab.legend()

#sampleSizes = range(20, 600, 1)
#diffs = getDiffs(getHighs(), sampleSizes)
#plotDiffs(sampleSizes, diffs,
#          'Sample SD vs Population SD, Temperatures',
#          label = 'High temps')


def compareDists():
    uniform, normal, exp = [], [], []
    for i in range(100000):
        uniform.append(random.random())
        normal.append(random.gauss(0, 1))
        exp.append(random.expovariate(0.5))
    sampleSizes = range(20, 600, 1)
    udiffs = getDiffs(uniform, sampleSizes)
    ndiffs = getDiffs(normal, sampleSizes)
    ediffs = getDiffs(exp, sampleSizes)
    plotDiffs(sampleSizes, udiffs,
              'Sample SD vs Population SD',
              'Uniform population', 'm')
    plotDiffs(sampleSizes, ndiffs,
              'Sample SD vs Population SD',
              'Normal population', 'b')
    plotDiffs(sampleSizes, ediffs,
              'Sample SD vs Population SD',
              'Exponential population', 'r')

#compareDists()  
#
#popSizes = (10000, 100000, 1000000)
#sampleSizes = range(20, 600, 1)
#for size in popSizes:
#    population = []
#    for i in range(size):
#        population.append(random.expovariate(0.5))
#    ediffs = getDiffs(population, sampleSizes)
#    plotDiffs(sampleSizes, ediffs,
#              'Sample SD vs Population SD, Uniform',
#              'Population size = ' + str(size))

#temps = getHighs()
#popMean = sum(temps)/len(temps)
#sampleSize = 200
#numTrials = 10000
#
#random.seed(0)
#numBad = 0
#for t in range(numTrials):
#    posStartingPts = range(0, len(temps) - sampleSize)
#    start = random.choice(posStartingPts)
#    sample = temps[start:start+sampleSize]
#    sampleMean = sum(sample)/sampleSize
#    se = numpy.std(sample)/sampleSize**0.5
#    if abs(popMean - sampleMean) > 1.96*se:
#        numBad += 1
#print('Fraction outside 95% confidence interval =',
#      numBad/numTrials)
#
#random.seed(0)      
#numBad = 0
#for t in range(numTrials):
#    sample = random.sample(temps, sampleSize)
#    sampleMean = sum(sample)/sampleSize
#    se = numpy.std(sample)/sampleSize**0.5
#    if abs(popMean - sampleMean) > 1.96*se:
#        numBad += 1
#print('Fraction outside 95% confidence interval =',
#      numBad/numTrials)