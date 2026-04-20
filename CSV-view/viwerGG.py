import csv
import matplotlib.pyplot as plt
import os


def read_csv(fileName):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE = os.path.join(BASE_DIR,'CSVdata',fileName)

    fileNameJPG = fileName+'.jpg'
    PNG_save_location = os.path.join(BASE_DIR,'PNGPLOTS',fileNameJPG)

    masterList = list()


    with open(CSV_FILE, 'r',encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            #print(row) 
            masterList.append(row)

    xData = list()
    y1Data = list()
    y2Data = list()

    legend1 = masterList[0][2]
    legend2 = masterList[0][4]


    for row in masterList[1:]:
        xData.append(float(row[0]))

        y1Data.append(float(row[2]))
    
        y2Data.append(float(row[4]))

    plt.plot(xData,y1Data,'-o',label = legend1)
    plt.plot(xData,y2Data,'-o',label = legend2)

    plt.title(fileName)
    plt.legend()
    plt.xlabel('Phase / π')
    plt.ylabel('Normalized Output Power')
    
    plt.savefig(PNG_save_location)
    plt.cla()
    plt.clf()
    

if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    dataPath = os.path.join(BASE_DIR, 'CSVdata')

    CSVfiles = os.listdir(dataPath)

    for fileName in CSVfiles:
        read_csv(fileName)