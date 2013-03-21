import urllib2, sys, datetime, getpass
from bs4 import BeautifulSoup

#------------------------------------------
login = 'lmj112'
password = getpass.getpass('Enter password... ')
userClass = 'c1'
period = '3'
cateTopLvl = "https://cate.doc.ic.ac.uk/"
#------------------------------------------
months = ["JANUARY","FEBRUARY","MARCH","APRIL"
         ,"MAY","JUNE","JULY","AUGUST","SEPTEMBER"
         ,"OCTOBER","NOVEMEBER","DECEMBER"]

def generateProjLink(login, period, userClass):
    return (cateTopLvl+'timetable.cgi?keyt=20'+login[len(login)-2:] +
            ':'+period+':'+userClass+':'+login)
    

def processExerciseCell(cell,startDay,count,months,year,moduleId):
    exerciseId = (cell.find('b')).text.encode('utf-8')
    exerciseName = (cell.text.encode('utf-8'))[len(exerciseId)+1:]
    specLink   = "NA"
    givenLink  = "NA"
    handinLink = "NA"
    emailLink  = "NA"
    for a in cell('a'):
        if ("SPECS" in str(a)):
            specLink = a['href']
        elif ("given.cgi" in str(a)):
            givenLink = a['href']
        elif ('handins.cgi' in str(a)):
            handinLink = a['href']
        elif ('mailto' in str(a)):
            emailLink = a['href']
    setDate = startDay + datetime.timedelta(days=int(count))
    dueDate = setDate + datetime.timedelta(days=int(cell['colspan']) -1)
    return ("\n[ Exercise ID : " + exerciseId + ' {'+moduleId+'}' + "\n  Exercise name : " + 
            exerciseName + "\n  Set : " + setDate.strftime('%d/%m/%y') + "  Due : " + dueDate.strftime("%d/%m/%y") +
            "\n  Spec link : " + specLink + "\n  Given link : " + givenLink + 
            "\n  Email link : " + emailLink + "\n  Hand in link : " + handinLink +  " ]\n")

def getFirstDay(row):
    day = 0
    for td in row.findAll('th'):
        s = td.text.strip()
        if (s != ''):
            return int(s)

def extractMonthNames(row):
    monthNames = []
    for cell in rows[0]('th'):
        if ('white' in str(cell)) and int(cell['colspan']) > 2:
            monthNames.append(cell.text.upper().strip())
    return monthNames 

def stripOutHeaders(rows,monthNamesRow):
    newTable = []
    count = 0
    for row in rows:
        if (count > 0):
            count = count -1
        else:
            if (row == monthNamesRow):
                count = count + 6
            else:
                newTable.append(row)
    return newTable

def processExerciseCells(cells,moduleId):
    count = -2
    for exerciseCell in cells:
    #print exerciseCell
        if (len(exerciseCell('b')) == 0):
            if (not 'colspan' in str(exerciseCell)):
                #print "incrm 1"
                count = count + 1
            else:
                count = count + int(exerciseCell['colspan'])
                #print "increment by " + str(exerciseCell['colspan'])
        elif ('href' in str(exerciseCell)):
            print processExerciseCell(exerciseCell,startDay,count,months,2012,moduleId)
            count = count + int(exerciseCell['colspan'])

def extractNoteURLS(url):
    s = opener.open(cateTopLvl + str(url))
    noteSoup = BeautifulSoup(s.read())
    s.close()
    noteInfos = []
    for row in (noteSoup('table')[2])('tr')[1:]:
        cells = row('td')
        if len(cells) >1:
            title = (cells[1].text)
            link = 'NA'
            if 'href' in row.encode('utf-8'):
                link = (row('a')[0])['href']
            noteInfos.append((title,link))
    return noteInfos


passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
#establish password manager
passmgr.add_password(None, cateTopLvl, login, password)
#add user/pass combo to the mgr
authhandler = urllib2.HTTPBasicAuthHandler(passmgr)
#establist a authentication handler to sign in
opener = urllib2.build_opener(authhandler)
#delegate an opener to open the url with the authhandler
cateWelcome = "https://cate.doc.ic.ac.uk/personal.cgi?keyp=20"+login[-2:]+":"+login
#print cateWelcome   #testing
s = opener.open(generateProjLink(login,period,userClass))
#dwld html src
html = s.read()
s.close()
#finish all html dwlds
soup = BeautifulSoup(html)
#use beautifulsoup to parse html text
rows = soup.findAll('table', {'border':0})[0].findAll('tr')   
#picks up the project table - read, project table only one with border 0
monthNamesRow = rows[0]
#construct a row of month names #weeksRow = rows[1] #construct a row of week names
monthNames = extractMonthNames(monthNamesRow)
daysRow = rows[2]
#construct a row of days
startDay = datetime.date(2012,months.index(monthNames[0]) +1,getFirstDay(daysRow))
headerRows = rows[0:7]
#construct a list of header rows
rows = stripOutHeaders(rows,monthNamesRow)
#strip headers from the entire table
modules = []
exercises = []
for i in range(len(rows)):
    for cell in rows[i]('td'):   #for each cell in each row
        #print cell.text.encode('utf-8')
        exIds = cell.findAll('b')
        moduleIds = cell.findAll(attrs={'color':'blue'})  #if the cell has a blue marker
        if len(moduleIds) != 0:
            moduleId = moduleIds[0].text   #then this is the module id
            moduleName =  (cell.text).encode('utf-8','ignore').strip()[len(moduleId) + 3:]
            noteURLs = 'NA'
            notesURL = 'NA'
            for a in cell('a'):
                if 'notes.cgi' in str(a):
                    notesURL = a['href']
            if notesURL != 'NA':
                noteURLs = extractNoteURLS(notesURL)
            rowCount = int(cell['rowspan']) -1
            print "******************************************"
            print moduleId + " - " + moduleName
            print 'Module Notes link : ' + notesURL
            if noteURLs != 'NA':
                for (t,l) in noteURLs:
                    print '  --'+t+ '  :  ' + l
            print "******************************************"
            modules.append((moduleId,moduleName))
            processExerciseCells((rows[i]('td'))[rows[i]('td').index(cell)+3:],moduleId)
            while rowCount != 0:
                processExerciseCells((rows[i+rowCount]('td')[1:]),moduleId)
                rowCount -= 1

