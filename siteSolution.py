# Main Python File

# Imported libraries
import csv 
import os
import time
import matplotlib.pyplot as plt

# In order to append Power_Difference and sorted Wind_Speed the values are stored in corresponding lists
powerDifference = ["Power_Difference"]
windSpeed = []

# Defining headers of the csv file inside fieldnames and default csv filename
fieldnames = ["Date/Time","Active_Power", "Wind_Speed", "Theoretical_Power" ,"Wind Direction", "Error", "Service", "FaultMsg", "Status Text"]
csvDefault = "TurbineData.csv"

# Storing updated rows in a list of dictionaries for command number 5
updatedRows = []

# Variables used for checking if a different command was executed or not
commandOneExecuted = 0
commandFourExecuted = 0

# FILE MANIPULATION

# This function is called upon when appending the columns of Power_Difference and Wind_Speed into TurbineData.csv
# Reference: https://thispointer.com/python-add-a-column-to-an-existing-csv-file/
def add_column_in_csv(input_file, output_file, transform_row):
    # Open the input_file in read mode and output_file in write mode
    with open(input_file, 'r') as read_obj, open(output_file, 'w', newline='') as write_obj:
                # Create a csv.reader object from the input file object
                csv_reader = csv.reader(read_obj, delimiter = ';')
                # Create a csv.writer object from the output file object
                csv_writer = csv.writer(write_obj, delimiter = ';')
                # Read each row of the input csv file as list
                for row in csv_reader:
                    # Pass the list / row in the transform function to add column text for this row
                    transform_row(row, csv_reader.line_num)
                    # Write the updated row / list to the output file
                    csv_writer.writerow(row)

# Function that loops through every row of the csv file and overwrites Status Text 
#  and Service when Error is bigger than 3 and FaultMsg equals to True
def updateStatus (inputFile, outputFile):
    with open(inputFile , 'r') as fileRead:
        csv_reader = csv.DictReader(fileRead, delimiter = ";")
        with open(outputFile , 'w', newline='') as fileWrite:
            csv_writer = csv.DictWriter(fileWrite, delimiter = ";", fieldnames = fieldnames)
            csv_writer.writeheader()
            for line in csv_reader:
                if int(line["Error"]) > 3 and line["FaultMsg"] == "TRUE":
                    line.update({"Status Text" : "Turbine not in operation"})
                    line.update({"Service" : "Required"})
                    updatedRows.append(line)
                    csv_writer.writerow(line)
                else:
                    csv_writer.writerow(line)

# Function that solves the problem of wiping the file after rewriting itself
# It takes inputFile that is created after executing a command that creates a new
#  csv file and rewriting it into the csv file provided to the script
def fileUpdater (inputFile, outputFile):
    with open(inputFile , 'r') as fileRead:
        csv_reader = csv.DictReader(fileRead, delimiter = ";")
        with open(outputFile , 'w', newline='') as fileWrite:
            csv_writer = csv.DictWriter(fileWrite, delimiter = ";", fieldnames = fieldnames)
            csv_writer.writeheader()
            for line in csv_reader:
                csv_writer.writerow(line)
    os.remove(inputFile)

# Function that removes every row from csv file 
#  that contains the value of an Error that is bigger than 50
def removeError (inputFile, outputFile):
    with open(inputFile , 'r') as fileRead:
        csv_reader = csv.DictReader(fileRead, delimiter = ";")
        with open(outputFile , 'w', newline='') as fileWrite:
            csv_writer = csv.DictWriter(fileWrite, delimiter = ";", fieldnames = fieldnames)
            csv_writer.writeheader()
            for line in csv_reader:
                if int(line["Error"]) < 50:
                    csv_writer.writerow(line)
                else:
                    pass
    fileRead.close()

# PLOTTING

# Function for plotting the Wind Speed and Active Power as a Dot Graph
def plotDotGraph (inputFile):
    fileRead = open(inputFile)
    reader = csv.reader(fileRead, delimiter=';')
    reader.__next__() # Skip the first line
    aPPlot = []
    wSPlot = []
    for x in reader:
        turbines = sorted(reader, key=lambda i: i[2], reverse=True) # The entire csv file sorted by column 3
    for x in turbines[:20]: # Taking the first 20 indexes of the list
        aPPlot.append(x[1].replace(',' , '.'))
        wSPlot.append(x[2].replace(',' , '.'))
    plt.plot(wSPlot, aPPlot, 'bo') # X axis is the Windspeed, Y axis is the Active Power
    plt.grid()
    plt.xlabel("Wind Speed")
    plt.ylabel("Active Power")
    plt.show()

def plotBarGraphTP(inputFile):
    # List of numbers displayed on X axis
    xAxis = []

    # List of labels for X axis
    tick_label = [] 

    numOfParams = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25] 
    with open(inputFile , 'r') as fileRead:
        reader = csv.DictReader(fileRead, delimiter = ";")
        # This for loop checks for the right Date and time and
        #  appends relevant data to the lists above
        for line in reader:
            if "05 01 2018 04:" in line["Date/Time"]:
                tP = float(line["Theoretical_Power"].replace(',' , '.'))
                date = line["Date/Time"][11: ]
                tick_label.append(date)
                xAxis.append(tP)
            elif "05 01 2018 05:" in line["Date/Time"]:
                tP = float(line["Theoretical_Power"].replace(',' , '.'))
                date = line["Date/Time"][11: ]
                tick_label.append(date)
                xAxis.append(tP)
            elif "05 01 2018 06:" in line["Date/Time"]:
                tP = float(line["Theoretical_Power"].replace(',' , '.'))
                date = line["Date/Time"][11: ]
                tick_label.append(date)
                xAxis.append(tP)
            elif "05 01 2018 07:" in line["Date/Time"]:
                tP = float(line["Theoretical_Power"].replace(',' , '.'))
                date = line["Date/Time"][11: ]
                tick_label.append(date)
                xAxis.append(tP)
            elif "05 01 2018 08:00" in line["Date/Time"]:
                tP = float(line["Theoretical_Power"].replace(',' , '.'))
                date = line["Date/Time"][11: ]
                tick_label.append(date)
                xAxis.append(tP)
            else: pass
    fileRead.close()

    # Bar Chart attributes
    plt.rcParams.update({'font.size': 10}) # Font Size
    plt.xticks(rotation='vertical') # Rotation for labels on x axis in order for them to fit the frame
    plt.bar(numOfParams, xAxis, tick_label = tick_label, width = 0.8, color = ['red']) # Plotting a bar chart 
    plt.xlabel('Time of the day (05 01 2018)') # Setting the name for the x-axis 
    plt.ylabel('Theoretical Power') # Setting the name for the y-axis 
    plt.title('Bar chart of Theoretical Power in a specific Date/Time') # Setting the title of the chart 
  
    # Function to plot the chart 
    plt.show() 

def plotBarGraphAP(inputFile):
    # List of numbers displayed on the X axis
    xAxis = []
    # List of labels for X axis 
    tick_label = [] 

    numOfParams = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25] 
    with open(inputFile , 'r') as fileRead:
        reader = csv.DictReader(fileRead, delimiter = ";")
        for line in reader:
            if "05 01 2018 04:" in line["Date/Time"]:
                aP = float(line["Active_Power"].replace(',' , '.'))
                date = line["Date/Time"][11: ]
                tick_label.append(date)
                xAxis.append(aP)
            elif "05 01 2018 05:" in line["Date/Time"]:
                aP = float(line["Active_Power"].replace(',' , '.'))
                date = line["Date/Time"][11: ]
                tick_label.append(date)
                xAxis.append(aP)
            elif "05 01 2018 06:" in line["Date/Time"]:
                aP = float(line["Active_Power"].replace(',' , '.'))
                date = line["Date/Time"][11: ]
                tick_label.append(date)
                xAxis.append(aP)
            elif "05 01 2018 07:" in line["Date/Time"]:
                aP = float(line["Active_Power"].replace(',' , '.'))
                date = line["Date/Time"][11: ]
                tick_label.append(date)
                xAxis.append(aP)
            elif "05 01 2018 08:00" in line["Date/Time"]:
                aP = float(line["Active_Power"].replace(',' , '.'))
                date = line["Date/Time"][11: ]
                tick_label.append(date)
                xAxis.append(aP)
            else: pass
    fileRead.close()
    
    # Bar Chart attributes
    plt.rcParams.update({'font.size': 10}) # Font Size
    plt.xticks(rotation='vertical') # Rotation for labels on x axis in order for them to fit the frame
    plt.bar(numOfParams, xAxis, tick_label = tick_label, width = 0.8, color = ['red']) # Plotting a bar chart 
    plt.xlabel('Time of the day (05 01 2018)') # Setting the name for the x-axis 
    plt.ylabel('Active Power') # Setting the name for the y-axis 
    plt.title('Bar chart of Active Power in a specific Date/Time') # Setting the title of the chart 
  
    # Function to plot the chart 
    plt.show()

# After executing any command this fuction is called upon and prompts the user with 
# an option to choose and execute a different command or exit the script
def continueOrNot ():
    print("*********************************************")
    print("Would you like to execute a different command?")
    executeAgain = input("(Y for yes / N for no) > ")
    if executeAgain.upper() == "N":
        print("Closing the script")
        time.sleep(1.5)
        quit()
    elif executeAgain.upper() == "Y":
        pass
    else:
        print("Please type in only 'Y' or 'N'")
        continueOrNot()

# Defining the header and reader in order for Python to loop through the csv file
with open(csvDefault , 'r') as fileRead:
    reader = csv.DictReader(fileRead, delimiter = ";")
    # In this for loop Python is looping through every row of the csv file
    # calculating the difference between Theoretical_Power and Active_Power
    # and also reading the Wind_Speed values and storing all of them into corresponding lists
    for line in reader:
        tP = float(line["Theoretical_Power"].replace(',' , '.'))
        aP = float(line["Active_Power"].replace(',' , '.'))
        calculatePD = round(aP - tP, 2)
        powerDifference.append(calculatePD)
    
        wS = float(line["Wind_Speed"].replace(',', '.'))
        windSpeed.append(wS)
fileRead.close()
# Two commands that are responsible for sorting the Wind_Speed
# and appending the header to the first index
windSpeedSorted = sorted(windSpeed, key = lambda x:float(x) , reverse = True)
windSpeedSorted.insert(0, "Wind_Speed descending")

# While loop that ensures that the script is running until the user decides to exit
print("                *Csv file was succesfully parsed*")
while True:
    # Printing the menu
    print("                                                            "       )
    print("                         ---- MENU ----                     "       )   
    print("   Please type in the number of the command you wish to perform"    )
    print("                                                            "       )
    print("       1. Add the Power_Difference and add sorted Wind_Speed"       )
    print("       2. Plot the bar graph of Theoretical and Active Power"       )
    print("       3. Plot a graph of Wind Speed and Active Power"              )
    print("       4. Update Status Test and Service requirement"               )
    print("       5. Print the updated rows with Error > 3 and FaultMsg True"  )
    print("       6. Delete data from Turbines with Error > 50"                )
    print("                           7. Quit                          "       )

    # Prompting the user for the input to know which command to execute
    userChoice = input("> ")

    # Executing the first command
    if(userChoice) == "1":
        if(commandOneExecuted) == 0:
            # Append the calculated power difference into the csv file
            add_column_in_csv(csvDefault, 'TurbineData2.csv', lambda row, line_num: row.append(powerDifference[line_num - 1]))
            fieldnames.append("Power_Difference")
            print("Power difference column added")

            # Append the sorted wind speed into the csv file
            add_column_in_csv('TurbineData2.csv', csvDefault, lambda row, line_num: row.append(windSpeedSorted[line_num - 1]))
            os.remove("TurbineData2.csv")
            fieldnames.append("Wind_Speed descending")
            print("Wind speed sorted column added")

            commandOneExecuted += 1
            continueOrNot()
        else:
            print("This command was already executed")
            print("If you would like to append the csv file again run the script again and provide new unedited csv file")
            continueOrNot()

    # Executing the second command
    elif(userChoice) == "2":
        print("            Choose which Bar Graph to plot")
        print("       ****************************************")
        print("       1. Plot Theoretical Power (4:00 - 8:00)")
        print("         2. Plot Active Power (4:00 - 8:00)")
        print("                      3. Back")
        selectPlot = input("> ")
        if(selectPlot) == "1":
            pass
            plotBarGraphTP(csvDefault)
            continueOrNot()
        elif(selectPlot) == "2":
            plotBarGraphAP(csvDefault)
            continueOrNot()
        elif(selectPlot) == "3":
            print("Returning to menu")
            time.sleep(1.5)
        else:
            print("Please choose a number between 1 and 3")
            time.sleep(2)     

    # Executing the third command
    elif(userChoice) == "3":
        plotDotGraph(csvDefault)
        print("Dot graph (Wind Speed/Active Power) successfuly ploted")
        continueOrNot()

    # Executing the fourth command
    elif(userChoice) == "4":
        if(commandFourExecuted) == 1:
            print("Status Test and Service Requirement already updated")
            continueOrNot()
        else:
            updateStatus(csvDefault, "TurbineData2.csv")
            fileUpdater("TurbineData2.csv", csvDefault)
            print("Status Test and Service Requirement updated")
            commandFourExecuted += 1
            continueOrNot()
    
    # Executing the fifth command
    elif(userChoice) == "5":
        if(commandFourExecuted) == 1:
            print(updatedRows)
            print("Updated rows printed")
            continueOrNot()
        else:
            print("Please execute command number 4 first")
            continueOrNot()
    # Executing the sixth command    
    elif(userChoice) == "6":
        removeError(csvDefault, "TurbineData2.csv")
        fileUpdater("TurbineData2.csv", csvDefault)
        print("Data from turbines with Error > 50 deleted")
        continueOrNot()

    # Executing the seventh command
    elif(userChoice) == "7":
        print("Closing the script")
        time.sleep(1.5)
        quit()

    # Ensuring that the user only chooses a relevant option
    else:
        print("Please choose a number between 1 and 7")
        time.sleep(2)

fileRead.close()