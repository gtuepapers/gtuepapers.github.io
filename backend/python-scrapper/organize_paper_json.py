"""
    departments.json
    BE.json
    BEsem1.json
    and so onn..
"""


import json
import re
import time


departments = dict()

ExamDateRegex = re.compile('[WS][0-9]+', re.IGNORECASE)

papersProcessed = []


class paper:
    def __init__(self):
        self.code = "code"  # Subject Code.
        self.link = "link"  # Link to .zip or .pdf
        self.year = "year"  # year of the paper
        self.branch = "branch"  # Mechanical etc.
        self.dept = "dept"  # BE , DE , etc.
        self.sem = "sem"  # sem.

    def setCode(self, code):
        self.code = code

    def setLink(self, link):
        self.link = link

    def setYear(self, year):
        self.year = year

    def setBranch(self, branch):
        # TODO replace the branch shortform(BE) to full form (Bachelors Of Engineering) 
        self.branch = branch

    def setDept(self, dept):
        self.dept = dept

    def setSem(self, sem):
        self.sem = "Sem " + sem

    def getCode(self):
        return self.code.upper()

    def getLink(self):
        return self.link

    def getYear(self):
        return self.year

    def getBranch(self):
        return self.branch.upper()

    def getDept(self):
        return self.dept.upper()

    def getSem(self):
        return self.sem.lower()

    def toJson(self):
        return "\n\t\t{\n\
                     \"code\" : \"%s\", \n\
                     \"link\" : \"%s\", \n\
                     \"year\" : \"%s\", \n\
                     \"branch\": \"%s\", \n\
                     \"dept\": \"%s\", \n\
                     \"sem\" :  \"%s\" \n\
                }" % (self.code, self.link, self.year, self.branch, self.dept, self.sem)


def jsonToListOfPaper():
    # Load JSON into papersJson.
    papersJson = json.load(open("./json/papers.json", "r"))
    # Go Through Each Paper.
    for paperjson in papersJson:

        curPaper = paper()

        # Split Paper link with '/' to get Department and Year.. And also remove prefix *http://old.gtu.ac.in/GTU_Papers/*
        curPaperLinkSplitted = ""
        if(paperjson[1].startswith("http://old.gtu.ac.in/GTU_Papers/")):
            curPaperLinkSplitted = paperjson[1].split(
                "http://old.gtu.ac.in/GTU_Papers/")[1].split("/")
        else:
            curPaperLinkSplitted = paperjson[1].split(
                "http://files.gtu.ac.in/GTU_Papers/")[1].split("/")
        # make Year in Proper Format
        # {Summer/Winter} Exam {Year}
        curPaperLinkSplitted[1] = curPaperLinkSplitted[1].replace("_", " ")
        if ExamDateRegex.match(curPaperLinkSplitted[1].replace(" ", "")):
            curPaperLinkSplitted[1] = curPaperLinkSplitted[1].replace(
                "W", "Winter Exam ")
            curPaperLinkSplitted[1] = curPaperLinkSplitted[1].replace(
                "S", "Summer Exam ")

        # Remove .pdf or .zip from subject code
        curPaperLinkSplitted[curPaperLinkSplitted.__len__(
        ) - 1] = curPaperLinkSplitted[curPaperLinkSplitted.__len__() - 1].replace(".pdf", "")
        curPaperLinkSplitted[curPaperLinkSplitted.__len__(
        ) - 1] = curPaperLinkSplitted[curPaperLinkSplitted.__len__() - 1].replace(".zip", "")

        #  curPaperLinkSplitted Format...
        #    {Department} / {Year} / {code}
        #      0            1           2

        # setting Paper Code.
        curPaper.setCode(paperjson[0])

        # Setting Paper link
        curPaper.setLink(paperjson[1])

        # setting paper year..
        curPaper.setYear(curPaperLinkSplitted[1])

        # setting up paper department
        curPaper.setDept(curPaperLinkSplitted[0])

        # TODO Sem and branch...
        if curPaperLinkSplitted[2][3:5] == "00":
            curPaper.setBranch("General")
        # setting up branch.
        else:
            curPaper.setBranch(curPaper.getCode()[
                               (curPaper.getCode().__len__()-4):(curPaper.getCode().__len__()-2)])
        # setting up sem
        if curPaperLinkSplitted[2][2] == "0":
            curPaper.setSem(curPaperLinkSplitted[2][1])
        else:
            curPaper.setSem(curPaperLinkSplitted[2][2])
        papersProcessed.append(curPaper)

        # print(curPaper.toJson())

    print(papersProcessed.__len__(), papersJson.__len__())


if __name__ == "__main__":
    jsonToListOfPaper()
    f = open("./json/papers-categorized.json", "w+")
    for paper in papersProcessed:
        if not departments.__contains__(paper.getDept()):
            departments[paper.getDept()] = dict()

        if not departments[paper.getDept()].__contains__(paper.getBranch()):
            departments[paper.getDept()][paper.getBranch()] = dict()
        
        if not departments[paper.getDept()][paper.getBranch()].__contains__(paper.getSem()):
            departments[paper.getDept()][paper.getBranch()][paper.getSem()] = dict()

        if not departments[paper.getDept()][paper.getBranch()][paper.getSem()].__contains__(paper.getCode()):
            departments[paper.getDept()][paper.getBranch()][paper.getSem()][paper.getCode()] = list()

        departments[paper.getDept()][paper.getBranch()][paper.getSem()][paper.getCode()].append(paper.getLink())

    f.write(json.dumps(departments))
    f.close()

    departments = json.load(open("./json/papers-categorized.json", "r"))
    # The Main File has been writtern.
    # Now writing file clients need to get.
    # like first one.
    # departments.json //be,me etc
    # be.json //sem1 etc..
    # be_sem1.jsson

    deptJson = []
    for dept in departments:# BE
        deptJson.append(dept) # BE
        branchJson = [] # COMPUTER
        for branch in departments[dept]: #COMPUTER 
            branchJson.append(branch) #COMPUTER
            deptSem = [] # SEM 1
            for sem in departments[dept][branch]: # SEM 1
                deptSem.append(sem) # SEM 1 
                semPaper = [] # PAPER 1
                for papers in departments[dept][branch][sem]: # PAPER1
                    semPaper.append([papers, departments[dept][branch][sem][papers]]) # PAPER 1
                f = open("./json/"+dept+"-"+branch+"-"+sem+".json", "w+")# BE-1.json
                f.write(json.dumps(semPaper))
                f.close()
            f = open("./json/"+dept+"-"+branch+ ".json", "w+")#BE.json
            f.write(json.dumps(deptSem))
            f.close()
        f = open("./json/"+dept+".json", "w+")#BE.json
        f.write(json.dumps(branchJson))
        f.close()
    f = open("./json/departments.json", "w+")
    f.write(json.dumps(deptJson))
    f.close()