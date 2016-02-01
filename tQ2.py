#Copyright (c) <2016> <MICHAEL HUNTER>

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
#to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
#and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#AUTHOR'S NOTES(NOT TO SUPERCEEDE THE ABOVE CONDITIONS)
#AS OF 1/31/16 THERE IS NO PROPRIETARY xmlff file extension THAT THE AUTHOR IS AWARE OF,
#YOU CAN MAKE UP ONE AT YOUR DISCRESSION,
#AUTHOR WOULD LIKE TO CONSIDER XMLFF extensions ASSOCIATED WITH THIS PRODUCT

import time
import re
import traceback
import os
import tQ

#layout val1|delim|val2|delim|(E-delim)['value'](A-delim)[['',['att']]]
#ATTRIBUTES ARE ALWAYS ARRAY BASED EVEN IF ONLY ONE ELEMENT



#possibly applicable to a future implementation on top of this code
uInit=[1,"ADMIN","michael","0","300",[]]   #[userok?,username,userid,usertz,misc arr]

#heapPath="C:/Users/Jennifer/Desktop/CS4/Database/DB_V2/Database/Users/INITAL/user_HEAP.xmlff"
#rlPath="C:/Users/Jennifer/Desktop/CS4/Database/DB_V2/Database/Users/INITAL/user_RL.xmlff"

heapPath="C:/Python34/sample_HEAP.xmlff"   #root in the xmlff file must match the file name w/o extesnion this is the split file
rlPath="C:/Python34/sample_RL.xmlff"       #root in the xmlff file must match the file name w/o extension this is the control file


callMode="RH"                       #CALL MODE
                                    #RH(READ FROM HEAP) 
                                    #WH(WRITE TO HEAP)---USE writeQueryCmdArr, each entry will always get a state/indx/id/dateime samp       
                                    #UH(UPDATE HEAP)-----UPDATES THE STATE in the heap file
                                    #XH(TRANSFER HEAP) #not built out yet
                                    
#QUERY COMMAND
queryCmdArr=[]                      #used for read commands
writeQueryCmdArr=[]                 #used for write commands
updateSeq=[]                        #used for updating state values

#RH EXAMPLE IF NULL THEN ALL IF VALUE THEN ONLY VALUE FROM COLUMN
#[[QUERY DIM],[RESPONSE-TYPE],[[PARAM,OPERAND,INTERVAL],[PARAM-N,OPERAND-N,INTERVAL-N]]]
#QUERY DIM
#####['ALL']
#####=ALL VALUES TO RETURN
#####['<ELE1 ','<ELE2 ','<ELE3 '] NOTE WILL ONLY WORK ON THE IMMEDATE CHILDREN OF <column>
#####=RETURN VALUES FOR THE LISTED ELEMENTS USE A SPACE IF AN ELMENT NAME HAS ATTRIBUTE AND CAN BE SUBEST OF ANOTHER <USER VS <USERSPACE, IF YOU WANT USER AND IT HAS ATTRIBUTE THEN '<USER ', IF YOU WANT USER AND IT DOESN'T HAVE ATTRIBUTE THEN '<USER>'

#RESPONSE TYPE loc=1 is a spare
#####['xml','']
#####=RETURN XML, YOU WILL NEED TO ENCASE THE XML WITH A PARENT IF NEEDED
#####['json','']
#####=RETURN JSON, YOU WILL NEED TO ENCASE THE OBJECT
#####['tableELE','']
#####=RETURNS VERTICALIZED ELEMENT VALUES WITH THERE RESPETIVE DEPTHS
#####['tableATT','']
#####=RETURNS VERTICALIZED ATTRIBUTE VALUES, HOLDING THE SAME DIMENSION AS the tableELE call, NOTE THAT ATTRIBUTES WILL ONLY RENDER FOR ELEMENTS WITH VALUE
#####['tableALL','']
#####=RETURNS VERTICALIZED ELEMENT AND ATTRIBUTE VALUES
#####['updateArr','']
#####=RETURNS UPDATE ELMENTS ARRAY (not built out yet)

#PARAM,OPERAND,INTERVAL,CHASE,ROW INDEX

#PARAM
####=ARRAY OF ELMENTS TO wittleDown

#OPERAND[,]
####=OPERANDS ON THE INTERVAL [0]=operand
## E2   equals to
## NE2  not equal to
## GRT  greater than
## LST  less than
## GRE2 greater than or equal to
## LSE2 less than or equal to
## LKE  like             (uses find operand, possible to add regex logic in the future)

####=Postion of the attribute if applicable [1]=position of the attribute
####=This will place the operand logic on the attribute value in the array starts at 0, attributes hard coded in conrol are assumed global for all data

#INTERVAL
####=VALUE IN QUESTION
#### NOTE FOR DATA WITH ' YOU WILL NEED  to double quote esacpe them if one if more than "'"+"data"+"'"

#CHASE (BOOLEAN)
####=BREAK POINT ON SUSPECTED QUERY MALFUNCTION OR ISSUES WITH THE DATA @ THIS POINT BEINGS A LOGGING ARRAYS OF THE DATA
####=NOT BUILT OUT YET

#ROW INDEX
####=INDEX OF THE COLUMN VALUE FOR THE ROW IN QUESTITON (ASSIGNED DYNAMICLY)
####=NOT BUILT OUT YET



#queryCmdArr=[['ALL'],['tableATT',''],[]]
queryCmdArr=[['ALL'],['xml',''],[['2|<first ',['E2',''],'mike',0,'AssignInx']]]
#queryCmdArr=[['ALL'],['xml',''],[['2|<first ',['E2','0'],'ms',0,'AssignInx']]]
#queryCmdArr=[['<state ','<user '],['xml',''],[['2|<first ',['E2','0'],'ms',0,'AssignInx']]]
#queryCmdArr=[['ALL'],['xml',''],[['1|<work ',['E2','2'],'ne',0,'AssignInx']]]
#queryCmdArr=[['ALL'],['json',''],[['1|<home ',['LKE','0'],'23',0,'AssignInx']]]

#WH EXAMPLE    APP MUST ESCAPE ' CHARACTERS IN DATA AND VALIDATE DIMENSION
writeQueryCmdArr=[['R','',"(E-34*3)[[['michael','hunter'],'00000000000']](A-34*3)[[[['',['mr']],['',['esq']],['spanish','english']],['',['france']]],[]]","(E-34*3)[['','notes about work']](A-34*3)[[['',['123 fake st','foobar','il','00000']],['',['345 fake st','foobar','il','000000']]]]"]]


#UH EXAMPE
updateSeq=[['1','R'],['2','R'],['3','R']]   #order by id a must otherwise loop will fail


#important notes
#developed in IDLE on python 3.4.3 on 64 bit windows 8 and subsequtually on a Windows 10
#I am hoping that a move to Linux would not be overly burdonsome as I am using a limited number of libarary usage in tQ and tQ2
#rl file(control) and heap file(split) root element names must match filenames!!
#no comments allowed in the control/spit file xml
#in control file <column> must be an inmediate child of the root in order to associate with the split file
#in control file any other child's of the root are bypassed for mapping, you can alter the code to account for in tQ
#in the root of the <column> branch, the number of elements must match the number of delims in the split file (otherwise, reads error assuming data corruption)
#if having trouble with creating mutli value dim arrays in the split file uncomment #print(atExStr) and #print(elExStr) in tQ.Mapp, this is the array that is executed at the dictonary level to grab data or if you're surly execute texttual python functions
#there are no type restrctions, but I am not aware of complied type restrictions at Python's high level, I recommend pointing to a file rather than storing compiled data in the (split)
#an entire entry for <column> must be one line in the spit file, if a line delimiter is in your data you will have to escape.
#query operand arrays only work in AND cases not yet built for OR cases
#if ev=0 in control and data in element, data will not show
#if av=0 or <> # of attributes other than loc/ev/av then all of the att values will not show in results
#when using queryCmdArr, '#|<element ' the # is the depth level within <column> for example, you will need to know this for query
#cursor when opening the spilt file should always be on the next line, each entry always has a line delimiter in this case '\n'
#delim2/delim3 in control file not required, but available if delim in base data, no  check built yet for delim in base data going with the convention in split of |delim|
#xml parser requires some level's of distinctness in the control data, so your queries may come back odd, it's an array based parser
#see ADD OTHER OUTPUTS HERE to create other triggers for output data, bytstrings, table types etc,uncomment the for loop and it will become apparrent the need for the #|<element in the queryCmdArr
#attributes cannot have " in the data, you may want to alter tQ.Scrub for this


#future dev notes
#for multi threading I recommend adding elements to the writeQueryArr array variable and single thread writes through a mirrored split file in memory.
#I also would recommend adding logic to distribute the split files on the index
#SQL can be put on top of the conrol and split flies, given its row like nature, I haven't yet build out.
#Given the nature of the control xmlff, you can also take a query listing and automate the re-classclassification of the control struture.
#In effect creating a self learning DB. I recommend not doing this given humanity's nature for self destruction. :)
#Given the nature of the split xmlff, you can build an interface between spreadsheet software and have a user do math functions on the data,
#if the speadsreadsheet code blocks dimension changes and keeps types if appplicable. I haven't yet built out
#Also it is possible to put Python functions in the base data as when textual arrays are assigned to dictonary variables for logic they are executed,
#it is imperative that you are careful with the split data comming in.
#Or you may just want to put a bunch of def's \t\n stuff in there and execute within said line in the split data
#MAL would just be a function created for the sole purpose of parsing data for malicious executable I haven't yet built out



def main(uInit,callMode,heapPath,rlPath,queryCmdArr,writeQueryCmdArr,updateSeq):
    
    print (time.strftime("%H:%M:%S")) ##for latency considerations uncomment out time statements

    
    #EXECUATBLE DISALLOW add as needed
    heapPCk=heapPath.lower()
    rlPCk=rlPath.lower()
    if '.exe' in heapPCk or '.sh' in heapPCk:
        print(heapPath)
        print('no executables allowed')
        return
    if '.exe' in rlPCk or '.sh' in rlPCk:
        print(rlPath)
        print('no executables allowed')
        return

    nameHEAP=heapPath[heapPath.rindex('/')+1:heapPath.rindex('.')]
    nameRL=rlPath[rlPath.rindex('/')+1:rlPath.rindex('.')]
    lrHEAP="<"+nameHEAP+">"                         #LEED ROOT FOR THE HEAP FILE
    erHEAP="</"+nameHEAP+">"                        #END ROOT FOR THE HEAP FILE
    lrRL="<"+nameRL+">"                             #LEED ROOT FOR THE RL FILE
    erRL="</"+nameRL+">"                            #END ROOT FOR THE RL FILE

    #ALWAYS GET THE DELIMINATOR AND SPLIT DATA STRUCTURE columns>child1,child2,child(n) FROM THE RL FILE
    
    if os.path.isfile(rlPath):
        with open(rlPath,'r') as f:
            xmlRaw,bytcnt=tQ.xmlRaw(lrRL,erRL,f)
            xmlArr,xmlPos=tQ.flattenXML(lrRL,erRL,xmlRaw,rlPath)        ##flatten xml for read queries and db file position of xml

            
            
            #CONTROL QUERY POINT
            #GET DELIM1
            query=[lrRL,'<delim1'] #path of dom
            accquire="ATTS"        #if ELEV nd query path has children this data will be exposed
            acqval="accept"              #if left blank when accquire="ATTS" will return all atts in a name value type list if populated with the attribute name will return the value
            delim=tQ.splitQueryXML(query,xmlArr,accquire,acqval,rlPath)
            #print(delim)
            

            #GET COLUMNS for call modes (RH) and RH parameterization
            if callMode=="RH":
                query=[lrRL,'<column']
                queryDat=queryCmdArr[0]      #ALL GETS ALL THE ORIDNALS, OR YOU CAN USE A LIST <VAL1 <VAL2,<VAL..n
                columnOrdinal,Col_Arr=tQ.columnBuild(query,queryDat,xmlArr,rlPath)
                #print(Col_Arr)
                #print(columnOrdinal)
                
                #if stateMode[0]='xml'  then xml return will have value
                #if statemode[0]='tableELE' then tableRet will have value of Elements
                #if statemode[0]='tableATT' then tableAttRet will have value of Attributes
                #if statemode[0]='tableALL' then tableRet will have value of Elements AND tableAttRet will have value of Attributes
                #if statemode[0]='updateArr' then updateRet will have a listing of all qualfying line elements
                stateMode=[queryCmdArr[1][0],queryCmdArr[1][1]]

                #wittle down USED TO RESTICT RESULTS POST GET LINE AND PRE MAP
                wittleDown=queryCmdArr[2]
                

                #wittleDown Error handling then assign index
                for i,ival in enumerate(wittleDown):
                    #ERROR-indexing
                    if ival[0][-1] not in [' ','>']:
                        print("ERROR IN !!!!!>PARAM<!!!!!,OPERAND,INTERVAL,CHASE,ROW INDEX : PARAM MUST HAVE AN ATTRIBUTE OR MUST BE ENDED IN '>' IN ORDER TO INDEX CORRECTLY")
                        return
                    #ERROR-operand listing
                    if ival[1][0] not in ['E2','NE2','GRT','LST','GRE2','LSE2','LKE']:
                        print("ERROR IN PARAM,!!!!!!>OPERAND<!!!!!!,INTERVAL,CHASE,ROW INDEX : OPERAND MUST BE LISTING OF ACCEPTABLE TYPES")
                        return
                    #INDEX ASSIGN
                    rootCnt=-1
                    for j,jval in enumerate(Col_Arr):
                        if "0|" in jval:
                            rootCnt+=1
                        if ival[0] in jval and "loc=" not in jval:
                            ival[4]=str(rootCnt)+":::"
                            break

                        if ival[0] in jval and "loc=" in jval:
                            jvalSplit=jval.split('"')
                            jvalLoc=jvalSplit[1]
                            jvalEv=jvalSplit[3]
                            jvalAt=jvalSplit[5]
                            #assign location based on presesence of ev or av
                            if int(jvalEv)>0 and int(jvalAt)>0:
                                ival[4]=str(rootCnt)+":"+jvalLoc+":"+jvalLoc+"[-1]:"+jvalAt
                            if int(jvalEv)>0 and int(jvalAt)==0:
                                ival[4]=str(rootCnt)+":"+jvalLoc+"::"+""
                            if int(jvalEv)==0 and int(jvalAt)>0:
                                ival[4]=str(rootCnt)+"::"+jvalLoc+"[-1]:"+jvalAt
                            if int(jvalEv)==0 and int(jvalAt)==0:
                                ival[4]=str(rootCnt)+":::"

                            break
                        
                    

                #GLOBAL ROOT COUNT FOR CHECKING READ IN OF END LINE WHILE WRIGHT, IF DIM DOES NOT MATCH THEN THE FILE READ WILL BAIL
                rootCnt=0
                for i,ival in enumerate(Col_Arr):
                    if "0|" in ival:
                        rootCnt+=1
                    
    
                
                #optimize order here of operands here if needed
                #recomend on this order
                ## E2   equals to
                ## NE2  not equal to
                ## GRT  greater than
                ## LST  less than
                ## GRE2 greater than or equal to
                ## LSE2 less than or equal to
                ## LKE  like
                


                #chase used to break query at point
    
        f.close()
                    
    #####CALL MODE READ FROM HEAP
    if callMode=="RH":                              #READ FROM HEAP
        if os.path.isfile(heapPath):
            print("RH")
            with open(heapPath,'r') as f:
                xmlRaw,bytcnt=tQ.xmlRaw(lrHEAP,erHEAP,f)
                xmlArr,xmlPos=tQ.flattenXML(lrHEAP,erHEAP,xmlRaw,heapPath)        ##flatten xml for read queries and db file position of xml
                #print(xmlArr)
                #!!!!CREATE  A DICTIONARY ITEM TO GENERATE THE LIST VARIABLE
                x=""
                y=""
                z=""
                d={'x': x,'y':y,'z':z}
                #print(Col_Arr)
                #print(columnOrdinal)
                
                b=os.path.getsize(heapPath)
                eldelim='(E-'+delim.replace('|','')+')'
                atdelim='(A-'+delim.replace('|','')+')'
                updateRet=[]                 #update array which matches the dimension for the heap file and can be used to update data
                for i,ival in enumerate(f):
                    lnbytcnt=len(ival)+1
                    bytcnt+=len(ival)+1
                    
                    if bytcnt>b:             #eof consideration
                        bytcnt-=1
                        lnbytcnt-=1
                        
                    if ival!='\n':                                  #bypass the leed 7
                        #ival=tQ.scrub(ival,"python","ob")          #scrub if applicable
                        line=ival.split(delim)
                        lineLen=len(line)
                        #bail file read (dimesnion issue in data that needs to be resolved.
                        #if delta > 0 then it is not a write/read issue, it is an issue with the base data!!!! base data issues caught after next write
                        if lineLen!=rootCnt:
                            print("FILE READ BAILED FOR LINE STARTING AT BYTE="+str(bytcnt-lnbytcnt)+" SIZE="+str(b)+" DELTA="+str(b-int(bytcnt)))
                            break
                        
                        #apply restriction clause here!!!
                        ok=[]
                        #print(wittleDown)
                        for j,jval in enumerate(wittleDown):
                            #print(jval)
                            operand=jval[1][0]
                            attOperand=jval[1][1]                    #this should be the index of the attribute in question in the array
                            fndVal=jval[2]
                            chse=jval[3]
                            lineLocArr=jval[4].split(":")
                            linePos=int(lineLocArr[0])
                            evPos=lineLocArr[1]
                            atPos=lineLocArr[2]
                            atCnt=lineLocArr[3]
                            fileVal=line[linePos]

                            #for end of line cases where crlf comes accross when indexed, doing this instead on on each fileval
                            if linePos==lineLen-1:
                                fileVal=fileVal.replace("\n","")
                            
                            if eldelim in fileVal:
                                ElnAtt=fileVal
                                elinx=ElnAtt.index(eldelim)+len(eldelim)
                                atinx=ElnAtt.index(atdelim)+len(atdelim)
                                elArr=ElnAtt[elinx:atinx-len(atdelim)]
                                atArr=ElnAtt[atinx:]
                            else:
                                ElnAtt=""
                                eldelim=""
                                atdelim=""
                                elinx=""
                                atinx=""
                                elArr=""
                                atArr=""
                            
                            if lineLocArr[1]=="" and lineLocArr[2]=="" and lineLocArr[3]=="":
                                ExStr='z='+'"'+fileVal+'"'
                            elif attOperand!="":
                                ExStr='z='+atArr+atPos+'['+attOperand+']'
                            else:
                                ExStr='z='+elArr+evPos   
                            #print(ExStr)

                            #or logic should be added or the below code should be redesigned for other boolean type logic
                            #!!!!!!!!Notice!!!!!!!!!!!!!!!call MAL here !!!!!!!!!! also check for escape mechanisims exec at dict item will execute python functions!!!!!!!!!!!!!!
                            ## E2   equals to
                            ## NE2  not equal to
                            ## GRT  greater than
                            ## LST  less than
                            ## GRE2 greater than or equal to
                            ## LSE2 less than or equal to
                            ## LKE  like
                            if operand=="E2":
                                #print("E2 OPERAND")
                                exec(ExStr,d)
                                if d['z']!=fndVal:
                                    ok.append(0)   
                                #print(d['z'])
                            elif operand=="NE2":
                                #print("NE2 OPERAND")
                                exec(ExStr,d)
                                if d['z']==fndVal:
                                    ok.append(0)
                            elif operand=="GRT":
                                #print("GRT OPERAND")
                                exec(ExStr,d)
                                #isNum=d['z'].isnumeric()
                                if d['z']<=fndVal:
                                    ok.append(0)
                            elif operand=="LST":
                                #print("LST OPERAND")
                                exec(ExStr,d)
                                #isNum=d['z'].isnumeric()
                                if d['z']>=fndVal:
                                    ok.append(0)
                            elif operand=="GRE2":
                                #print("GRE2 OPERAND")
                                exec(ExStr,d)
                                #isNum=d['z'].isnumeric()
                                if d['z']<fndVal:
                                    ok.append(0)

                            elif operand=="LSE2":
                                #print("LSE2 OPERAND")
                                exec(ExStr,d)
                                #isNum=d['z'].isnumeric()
                                if d['z']>fndVal:
                                    ok.append(0)

                            elif operand=="LKE":
                                #print("LKE OPERAND")
                                exec(ExStr,d)
                                fndTrig=d['z'].find(fndVal)
                                #lkeTrig=re.search('fndVal',d['z']) #maybe for regex searches in the future
                                if fndTrig<0:
                                    ok.append(0)       
                            else:
                                print("Should never be here :)")
                                
                            

                        if 0 not in ok and stateMode[0] not in ('updateArr'):     
                            xmlRet,tableRet,tableAttRet,jsonRet=tQ.Mapp(line,delim,d,columnOrdinal,Col_Arr,stateMode)

                            
                            if len(xmlRet)>1:
                                print(xmlRet)
                            if len(tableRet)>1:
                                for j,jval in enumerate(tableRet):
                                    print(jval)
                            if len(tableAttRet)>1:
                                for j,jval in enumerate(tableAttRet):
                                    print(jval)
                            if len(jsonRet)>1:
                                print(jsonRet)
                    
                        elif 0 not in ok and stateMode[0]==('updateArr'):
                            updateRet.append(line)
    
                        
            f.close()


    #####CALL MODE WRITE TO HEAP
    if callMode=="WH":                               #WRITE TO HEAP(NEED TO ADD LOCKING PIVOT OR APPEND TO queryCmdArr GLOBALLY VIA AN ALG)
        if os.path.isfile(heapPath):
            print("WH")
            with open(heapPath, 'r+') as f:
                if len(writeQueryCmdArr)>0:
                    xmlPos,xmlArr,entryID=tQ.writeHEAP(writeQueryCmdArr,delim,heapPath,f,lrHEAP,erHEAP)
                    upquery=[lrHEAP,'<id']
                    update="ELEV"
                    uval=entryID
                    xmlReturn,xmlArr=tQ.splitQueryXML_Update(upquery,update,uval,xmlArr,xmlPos,lrHEAP,erHEAP)
                    f.seek(0,0)        #return to start of file and update control
                    f.write(xmlReturn) #write out updated control   #this is ok as the character/byte dimension for the split id counter is fixed
            f.close()



    #####CALL MODE TO UPDATE HEAP
    if callMode=="UH":
        if os.path.isfile(heapPath):
            print("UH")
            with open(heapPath, 'r+') as f:
                xmlRaw,bytcnt=tQ.xmlRaw(lrHEAP,erHEAP,f)
                xmlArr,xmlPos=tQ.flattenXML(lrHEAP,erHEAP,xmlRaw,heapPath)        ##flatten xml for read queries and db file position of xml
                #print(xmlArr)
                b=os.path.getsize(heapPath)
                if len(updateSeq)>0:
                    for i,ival in enumerate(f):
                        lnbytcnt=len(ival)+1
                        bytcnt+=len(ival)+1
                        
                        if bytcnt>b:             #eof consideration
                            bytcnt-=1
                            lnbytcnt-=1
                            
                        if ival!='\n':
                            updateHeap=tQ.updateHEAP(ival,delim,updateSeq,f,bytcnt,lnbytcnt)

                                
                                


                
    print (time.strftime("%H:%M:%S")) ##for latency considerations uncomment out time statements

if __name__=="__main__":
    if uInit[0]==1:
        main(uInit,callMode,heapPath,rlPath,queryCmdArr,writeQueryCmdArr,updateSeq)
