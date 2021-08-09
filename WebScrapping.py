from selenium import webdriver
import time
import datetime
import pandas as pd

def loopCompetitors(driver, competitors, eventDetails, df_Results, startTime, event, heat):
    for l in competitors:
        competitionName= eventDetails[1]
        competitionDate= eventDetails[0]
        competitionVenue= eventDetails[2]
        competitionCategory= eventDetails[3]
        competitionDiscipline= eventDetails[4]
        competitionGroup= eventDetails[5]
        results= l.find_elements_by_tag_name("td")
        place= results[0].text
        name= results[1].text
        birthDate= results[2].text
        nationality= results[3].text
        mark= results[4].text
        df_Results= df_Results.append({"Competition Name":competitionName, "Competition Date":competitionDate,
                                        "Venue": competitionVenue,"Rankings Category": competitionCategory,
                                        "Discipline":competitionDiscipline, "Competition Group":competitionGroup,
                                        "Event": event,"Heat": heat,"Competitor Place": place,
                                        "Competitor Name": name,"Competitor Birth Date": birthDate, 
                                        "Competitor Nationality": nationality, "Competitor Mark": mark},ignore_index=True)
    return(df_Results)
    

def loopRaces(driver, races, eventDetails, df_Results, startTime, day):
    for k in races:
        event= k.find_element_by_tag_name("h2").text
        heat= k.find_element_by_class_name("EventResults_eventMeta__75ELD").text
        competitorsTable= k.find_element_by_tag_name("tbody")
        competitors= competitorsTable.find_elements_by_tag_name("tr")
        df_Results= loopCompetitors(driver, competitors, eventDetails, df_Results, startTime, event, heat)      
    print("----------------------------")
    print("Competition Name: "+ eventDetails[1])
    print("Days completed: " + str(day-1))
    print("Time Elapsed: " + str((datetime.datetime.now())-startTime))
    print("----------------------------")
    print(" ")
    return(df_Results)
    

def loopDays(driver,days, eventDetails, df_Results, startTime):
    for j in range(2,len(days)):
        day= days[j].click()
        time.sleep(3)
        races= driver.find_elements_by_class_name("EventResults_eventResult__3oyX4")  
        df_Results= loopRaces(driver, races, eventDetails, df_Results, startTime, j)
    
    print("****************************************************")
    print("Competition Name: "+ eventDetails[1])
    print("All days completed")
    print("Number of total results: " + str(len(df_Results)))
    print("Time Elapsed: " + str((datetime.datetime.now())-startTime))
    print("****************************************************")
    print(" ")
    
    driver.close() 
    driver.switch_to.window(driver.window_handles[0])
    return(df_Results)
    

def loopEvents(driver,events, df_Results, startTime):
    for i in range(1,len(events)):
        eventDetail= events[i].find_elements_by_tag_name("td")
        eventDetails=[]
        eventDetails.append(eventDetail[1].text)
        eventDetails.append(eventDetail[0].text)
        eventDetails.append(eventDetail[2].text)
        eventDetails.append(eventDetail[3].text)
        eventDetails.append(eventDetail[4].text)
        eventDetails.append(eventDetail[5].text)      
        competitionResults= eventDetail[6].find_element_by_tag_name("a").get_attribute('href')
        driver.execute_script("window.open('');") 
        driver.switch_to.window(driver.window_handles[1]) 
        time.sleep(1)
        driver.get(competitionResults)
        time.sleep(3)
        
        daysFilter= driver.find_element_by_name("day-select")
        days= daysFilter.find_elements_by_tag_name("option")
        df_Results= loopDays(driver,days, eventDetails, df_Results, startTime)
    return(df_Results)

def newPage(driver, nresults, startTime):
    try:
        resultsTable= driver.find_element_by_class_name("ResultsTable_resultsTable__JBH1Y")
        return(resultsTable)
    except:
        print("##############################################")
        print("Last Page Readed")
        print("Number of total results: " + str(nresults))
        print("Time Elapsed: " + str((datetime.datetime.now())-startTime))
        print("##############################################")
        return(0)

PATH= "C:\Program Files (x86)\chromedriver.exe"
driver= webdriver.Chrome(PATH)

competitionColumns= ["Competition Name", "Competition Date", "Venue","Rankings Category", 
                     "Discipline", "Competition Group"]
competitorColumns= ["Event","Heat","Competitor Place","Competitor Name","Competitor Birth Date", 
                    "Competitor Nationality", "Competitor Mark"]
df_Results= pd.DataFrame(columns=competitionColumns+competitorColumns)
resultsPage= "https://worldathletics.org/competition/calendar-results?hideCompetitionsWithNoResults=true"  
driver.get(resultsPage)
time.sleep(5)
startTime= datetime.datetime.now()
offset=0
while True:
    resultsTable= newPage(driver,len(df_Results),startTime)
    if(resultsTable==0):
        break
    events= resultsTable.find_elements_by_tag_name("tr")
    df_Results= loopEvents(driver,events, df_Results, startTime)    
    offset+=50
    nextPage= "https://worldathletics.org/competition/calendar-results?hideCompetitionsWithNoResults=true&offset=" + str(offset)
    driver.get(nextPage)
        
        