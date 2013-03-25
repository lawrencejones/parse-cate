import os, urllib2, sys, datetime, getpass
from bs4 import BeautifulSoup

def displayHelp():  #-----HELP INFORMATION------------------------------------
    print('\n----------------------------------------------------------------\n'
         +'CATE Scraper, a python script that can peel CATE like an orange!\n'
         +'----------------------------------------------------------------\n\n')
    print('To print out all the exercises in the selected term, just call\n'
         +'the script with no arguments.\n\n'
         +'To have the script produce information on a single module, call\n'
         +'it with the argument of the module id, ie 141 for Reasoning.\n\n'
         +'To download all the CATE files locally from the current term,\n'
         +'call the script like so...\n\n'
         +'      python LocalParser.py kickass\n\n'
         +'...which will proceed to take login details, then download the\n'
         +'exercises from the currently selected term (spec sheet and model\n'
         +'answers if available).\n\n'
         +'  NB- kickass specific, to download just one of the modules, call\n'
         +'      the script like so...\n\n'
         +'          python LocalParser.py 141 kickass\n\n'
         +'      ...which would download only a single module into the current\n'
         +'      path. Note that rm **/TickList is recommended before laying\n'
         +'      downloads (ie, downloading 1st term, then 2nd for all content)\n'
         +'      in order to avoid duplicating folder titles.\n\n')
    exit()

#------------------------------------------
if len(sys.argv) == 2:
    optionalSelection = sys.argv[1]
    if optionalSelection == 'help':
        displayHelp()
if len(sys.argv) == 3:
    moduleID = sys.argv[1]

login = raw_input('Enter your CATE login... ')
password = getpass.getpass('Enter password... ')
userClass = raw_input('Enter your class code (ie, c1)... ')
period = raw_input('Enter the term to download, where \n'+
                   '  Autumn = 1 \n  Spring = 3 \n  Summer = 5... ')

cateTopLvl = "https://cate.doc.ic.ac.uk/"
#------------------------------------------
months = ["JANUARY","FEBRUARY","MARCH","APRIL"
         ,"MAY","JUNE","JULY","AUGUST","SEPTEMBER"
         ,"OCTOBER","NOVEMBER","DECEMBER"]

#Exercise dict = {id, moduleId, name, set, due, spec, givenLink, email, handinLink}
#Module dict = {id, name, notesURL, notes}


def generateProjLink(login, period, userClass):
    return (cateTopLvl+'timetable.cgi?keyt=20'+login[len(login)-2:] +
            ':'+period+':'+userClass+':'+login)

def exerciseToString(e):
    return ("\n[ Exercise ID : " + e['id'] + ' {'+e['moduleId']+'}' + "\n  Exercise name : " + 
            e['name'] + "\n  Set : " + e['set'].strftime('%d/%m/%y') + "  Due : " + e['due'].strftime("%d/%m/%y") +
            "\n  Spec link : " + e['spec'] + "\n  Given link : " + e['givenLink'] + 
            "\n  Email link : " + e['email'] + "\n  Hand in link : " + e['handinLink'] +  " ]\n")


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
    return ({'id':exerciseId,'moduleId':moduleId,'name':exerciseName,
             'set':setDate,'due':dueDate,'spec':specLink,'givenLink':givenLink,
             'email':emailLink,'handinLink':handinLink})

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

def processExerciseCells(cells,moduleId,exercises):
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
            e = processExerciseCell(exerciseCell,startDay,count,months,2012,moduleId)
            exercises.append(e)
            if len(sys.argv) == 1:
                print exerciseToString(e)
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

def extractModelURL(url):
    if url != "NA":
        s = opener.open(cateTopLvl + str(url))
        givenSoup = BeautifulSoup(s.read())
        for a in givenSoup('a'):
            if 'MODEL' in a.encode('utf-8'):
                return a['href'].encode('utf-8')
    return False

def printModuleLinks(modules):
    for module in modules:
        if module['id'] == optionalSelection:
            print "\n******************************************"
            print module['id'] + " - " + module['name']
            print 'Module Notes link : ' + module['notesURL']
            if module['notesURL'] != 'NA':
                for link in module['notes']:
                    print(cateTopLvl+link)
            print "******************************************"

def getSubIndexForExercise(e):
    return int(e['id'].split(':')[0])

def downloadModuleNotes(m,notesDir):
    if m['notes'] != 'NA':
        for note in m['notes']:
            wget = 'wget -A pdf --http-user="'+login+'" --http-password="'+password+'" --content-disposition --no-check-certificate '
            os.system(wget+'-P '+notesDir+' '+cateTopLvl+note)

def createFoldersForExercises(moduleId,exercises,pathExtension):
    wget = 'wget -A pdf --http-user="'+login+'" --http-password="'+password+'" --content-disposition --no-check-certificate '
    moduleExs = []
    for e in exercises:
        if e['moduleId'] == moduleId:
            moduleExs.append(e)
    moduleExs = sorted(moduleExs, key=getSubIndexForExercise)
    cmds = []
    for i in range(0,len(moduleExs)-1):
        e = moduleExs[i]
        prefix = str(i+1)
        if len(prefix) == 1:
            prefix = '0'+prefix
        folderName = pathExtension + prefix + '-' + (e['name'][:].replace(' ','')).replace('-','')
        cmds.append('mkdir ' + folderName +';')
        if e['spec'] != 'NA':
            cmds.append(wget+'-P '+folderName+'/ '+cateTopLvl+e['spec']+';')
        modelLink = extractModelURL(e['givenLink'])
        if modelLink != False:
            cmds.append(wget+'-P '+folderName+'/ '+cateTopLvl+modelLink)
    for cmd in cmds:
        os.system(cmd)

def createAllFileDirectorys(modules,exercises):
    for m in modules:
        moduleFolderName = (m['name'][:]).replace(' ','_');
        os.system('mkdir '+moduleFolderName)
        os.system('mkdir '+moduleFolderName+'/00-Notes')
        if m['notesURL'] != 'NA':
            downloadModuleNotes(m,moduleFolderName + '/00-Notes')
        createFoldersForExercises(m['id'],exercises,moduleFolderName+'/')
    os.system('for big_folder in `ls`; do ' +
                 'for folder in `ls $big_folder | grep -iv "00"`; do ' +
                 'echo "$folder" >> $big_folder/TickList; ' +
                 'echo "--Nothing as of yet" >> $big_folder/TickList; ' + 
                 'echo >> $big_folder/TickList; ' +
                 'done; ' +
                 'done')


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
startDay = datetime.date(2013,months.index(monthNames[0]) +1,getFirstDay(daysRow))
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
            urls = []
            if noteURLs != 'NA':
                for (t,l) in noteURLs:
                    if l != '':
                        urls.append(l)
            if len(sys.argv) == 1:
                print "******************************************"
                print moduleId + " - " + moduleName
                print 'Module Notes link : ' + notesURL
                if noteURLs != 'NA':
                    for (t,l) in noteURLs:
                        print '  --'+t+ '  :  ' + l
                print "******************************************"
            modules.append({'id':moduleId,'name':moduleName,'notesURL':notesURL,'notes':urls})
            processExerciseCells((rows[i]('td'))[rows[i]('td').index(cell)+3:],moduleId,exercises)
            while rowCount != 0:
                processExerciseCells((rows[i+rowCount]('td')[1:]),moduleId,exercises)
                rowCount -= 1

if len(sys.argv) == 2:
    if sys.argv[1] == 'kickass':
        createAllFileDirectorys(modules,exercises)
    else:
        printModuleLinks(modules)

if len(sys.argv) == 3:
    if sys.argv[2] == 'kickass':
        createFoldersForExercises(sys.argv[1],exercises,'')
