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

def xmlRaw(leedroot,endroot,f):
    #BUILD STRCTURED ARRAY OF CONROL XML
    bytcnt=0
    xmlRaw=""
    b=os.path.getsize(f.name)          
    for i,line in enumerate(f):
        bytcnt+=len(line)+1       #+1 accounts for \n
        if endroot not in line:          ###caputures header until closing of the root
            xmlRaw+=line
        elif endroot in line:            ###captures root ending element
            xmlRaw+=line
            break
    if bytcnt>b:                   #eof consideration
        bytcnt-=1
    #print(xmlRaw)
    #print(bytcnt)
    return (xmlRaw,bytcnt)

def flattenXML(leedroot,endroot,xmlRaw,usrBaseDB):
#xml parser
#note this method requires structured and readable xml, meaning elements are properly delimited by crlf 
#method converts ele att names to lowercase
#there should be no xml comments in the document,control data should speak for itself
#none of this <root>Hi there<stuff><el></el><whereAmI>I think in circles</whereAmI></stuff></root> crap
#xml should be readable with lines delimited by '\n'
#<root>
#   <stuff>
#       <el></el>
#       <whereAmI>/root/stuff/whereAmI   now thats nice :) </whereAmI>
#   </stuff>
#<root>
    #roots are passed into the function, userdb is passed in for exception handling

    xmlRawList=xmlRaw.split('\n')   #turn xml into list
    xmlStructArr=[]                      #array to determine dirctory pos
    xmlPosArr=[]                        #position in root file, using as a hook for storage of formatting characters in control xml
    i=0
    if len(xmlRawList) < 5000:                                      #implies that this is control xml data not dabase xml data
        while i<len(xmlRawList):
            line=xmlRawList[i]
            if '<?xml version="1.0" encoding="utf-8" ?>' in line:   #declartion line, if doctype line in document add it to an elif under this if statment
                xmlStructArr.append(line)
                xmlPosArr.append(line+"|,|"+line[0:line.index('<')])
            elif leedroot in line:                                    #indicates start of xml parsing
                xmlStructArr.append(leedroot)
                xmlPosArr.append(line+"|,|"+line[0:line.index('<')])
            elif endroot in line:                                #indicates end of xml parsing
                xmlStructArr.append(endroot)
                xmlPosArr.append(line+"|,|"+line[0:line.index('<')])
            else:
                stval=""
                elval=""
                enval=""

                stval=re.search(r'<.*?>',line) #begining element

		#cleanup
                if stval is not None and '</' in stval.group():
                    stval=""

                #element data elval.strip() <---this strips leading and trailing tabs and whitespaces
                elval=re.sub(r"<.*?>","",line)
                elval=re.sub(r"</.*?>","",elval)

                #do this to keep the tab/spacing in the base data while elimiting whitespace and tab data only lines
		#if len(elval)==elval.count('\t') or len(elval)==elval.count(' '):
		#elval=""
		#SCRATCH THAT CRAP JUST STRIP
                elval=elval.strip()
                enval=re.search(r'</.*?>',line)
                if stval is not None and stval != "":
                    stval=stval.group()
                    #print(stval)                            #to see array structure uncomment
                    xmlStructArr.append(stval)
                    xmlPosArr.append(stval+"|,|"+line[0:line.index('<')])
                if elval is not None and elval !="":
                    #print(elval)                            #to see array structure uncomment
                    xmlStructArr.append(elval)
                    #xmlPosArr.append(str(i)+"|"+line[0:line.index('<')])
                if enval is not None and enval != "":
                    enval=enval.group()
                    xmlStructArr.append(enval)
                    
                    if stval=="":
                        xmlPosArr.append(enval+"|,|"+line[0:line.index('<')])
                    #print(enval)                           #to see array structure uncomment
            i+=1
    else:
        print("Please investiage uncontroled cs xml data expansion lines=("+str(len(xmlRawList))+") detected for :" +usrBaseDB)

    return (xmlStructArr,xmlPosArr)





def splitQueryXML(query,xmlArr,accquire,acqval,usrBaseDB):
   #QUERY xmlArr for data
    if len(query)==1:
        lastparent=query[0]             #to account for queries at the root level
    else:
        lastparent=query[-2].replace('<','</')            
    valinx=""
    pathind=[]                          #this should not exceed the dimension of the xmlArr
    trigInxPts=[]                       #index points for query elements which reference the xml array
    retdataRAW=""                       #RAW DATA FROM THE ARRAY PARSE
    retdata=""                    
    attVALUE=""                         #parsed attribute value if requested
    currInx=0                          #stop index where the last element was found in the tree
    uquery=[]                           #assgin query list to this decrementing array to keep query available for subsequent parsing
    for i,itm in enumerate(query):
        uquery.append(itm)       
   
    for i,val in enumerate(xmlArr):
        foundit='0'                     #indicates if data was found
        if uquery[0] in val:
            trigInxPts.append(i)        #for index troubleshooting
            foundit='1'
            del uquery[0]
        pathind.append(foundit)

        #utilize indicator array and uquery list to verify statement and return results
        if len(uquery)==0:
            valinx=''.join(pathind).rfind('1')
            retdataRAW=xmlArr[valinx]
            currInx=i
            break
        elif lastparent in val:               
            retdataRAW='><'
            currInx=i
            break

    #ELEMENT VALUES
    if accquire=="ELEV":
        for val in xmlArr[currInx+1:]:
            if query[-1].replace('<','</') not in val:
                retdata+=val+'\n'
            else:
                #remove extra carraiage return from append method
                retdata=retdata[:-1]
                break

    
    #ATTRIBUTE VALUES either all attributes or a single attribute value
    if accquire=="ATTS" and retdataRAW !='><' and retdataRAW !="":
        B=retdataRAW.replace(query[-1],'').replace('>','').strip()
        #for attribute values
        if acqval !="":
            attval=acqval+'='
            if attval in B:
                B=B[B.find(attval):len(B)]
                if B[len(attval)]=="'":
                    B=B.split("'")
                elif B[len(attval)]=='"':
                    B=B.split('"')
                attVALUE=B[1]
                retdata=attVALUE
        else:
            retdata=B

    #META DATA DISALLOWCATION HARD CODED (if file contains user data do NOT ALLOW RESULTS) #lowest level of blocking
    xusrBaseDB=[]
    xusrBaseDB.append(usrBaseDB)
    xusrBaseDB[0]=xusrBaseDB[0].lower()
    if 'meta' in xusrBaseDB[0]:
        retdata="LINE RESULTS ON THIS LEVEL NOT ALLOWED"

    #print(retdata)

    
    return retdata


def columnBuild(query,queryDat,xmlArr,usrBaseDB):
    accquire="ELEV"                                #RETURNS A COLUMN ORDINAL FOR THE SPLIT FILE IN QUESTION
    acqval=""
    columnRaw=splitQueryXML(query,xmlArr,accquire,acqval,usrBaseDB)
    columnRaw=list(columnRaw.split('\n'))
    columnList=[]
    
    #print(columnRaw)                   #get to the top level for column by removing sub elements

    xcolumnRaw=[]
    xcolumnAttRaw=[]
    #peel out element values just creating start and end tags
    for j,jval in enumerate(columnRaw):
        if '<' in jval:
            tag=jval[0:jval.find(' ')]
            xcolumnRaw.append(tag)
            xcolumnAttRaw.append(jval[jval.find(' '):])

    alldone=0           #all done
    itr=0               #number of interations in the while loop
    lenXCR=len(xcolumnRaw)-1   #intrateive length of xcolumnRaw
    while alldone==0:
        
        #scan logic interates repeditively for each level/depth of elements
        j=0
        ordpnt=itr*1
        itr+=1
        while j<lenXCR:
            xval=xcolumnRaw[j]
            nested=0
            if '</' not in xval and '|<' not in xval:
                stval=''+xval
                enval=xval.replace('<','</')
                
                if enval in xcolumnRaw[j+1]:
                    nested=0
                else:
                    nested=1
                k=j*1
                if nested==0:
                    xcolumnRaw[j]=str(ordpnt)+'|'+xval
                else:
                    topoint=k*1
                    while k<lenXCR:
                        nestval=xcolumnRaw[k+1]
                        if enval in nestval:
                            xcolumnRaw[topoint]=str(ordpnt)+'|'+xval
                            break
                        else:
                            k+=1
                            j+=1
                        
                    
            j+=1

        #determine if we should break meaning the entire xml has been scanned    
        i=0
        while i<lenXCR:
            ival=xcolumnRaw[i]
            if ival.index('<')==0 and '</' not in ival:
                alldone=0
                break
            elif i==lenXCR-1:
                alldone=1
            i+=1

    #build the column_Array
    Col_Arr=[]
    i=0
    while i<lenXCR:
        ival=xcolumnRaw[i]
        if '</' not in ival:
            Col_Arr.append(ival+xcolumnAttRaw[i])
        
        i+=1
        
    #Look for column ordinal in query
    columnOrdinal=[]
    for i,ival in enumerate(queryDat):
        colord=-1
        for j,jval in enumerate(Col_Arr):
            if jval[0]=='0':
                colord+=1
                if ival in jval:
                    columnOrdinal.append(colord)
                    break

    #If querying all then just assign the ordinals
    if queryDat[0]=="ALL":
        colord=-1
        for j,jval in enumerate(Col_Arr):
            if jval[0]=='0':
                colord+=1
                columnOrdinal.append(colord)
    

    #print(columnOrdinal)
    return (columnOrdinal,Col_Arr)

def writeHEAP(inboundData,delim,usrBaseDB,f,leedroot,endroot):
    #BUILD STRCTURED ARRAY OF CONROL XML
    xmlRaw_WL,bytcnt=xmlRaw(leedroot,endroot,f)
    xmlArr,xmlPos=flattenXML(leedroot,endroot,xmlRaw_WL,usrBaseDB)        ##flatten xml for read queries and db file position of xml
    query=[leedroot,'<id']
    accquire="ELEV"
    acqval=""
    entryID=splitQueryXML(query,xmlArr,accquire,acqval,usrBaseDB)
    
    entryID_inc=int(entryID)    #convert for incremental counter
    b=os.path.getsize(usrBaseDB)
    f.seek(b)                    #this may be redundant as from testing I have seen it write at the end of the file even if data present, may be able to distribute writes further within this logic base

    #write data to the file
    #first values for this design of control split
    #'<state accept="R,U,D">', '<inx>', '<id>', '<date>'
    if len(inboundData)>0:
        #check dim and other handles here
        for i,ival in enumerate(inboundData):
            entryID_inc+=1
            writeLine=""
            if ival[0]=='R':
                writeLine='R'+delim+ival[1]+delim+str(entryID_inc)+delim+time.strftime("%Y-%m-%d %H:%M:%S")
                del ival[0]
                del ival[0]
            elif ival[0]=='U':
                writeLine='R'+delim+ival[1]+delim+str(entryID_inc)+delim+time.strftime("%Y-%m-%d %H:%M:%S")
                del ival[0]
                del ival[0]
            else:
                break
            
            for j,jval in enumerate(ival):
                writeLine+=delim+jval

            #add a crlf to list
            writeLine+='\n'
            f.write(writeLine)                            #write to file

        entryID=str(entryID_inc).zfill(12)
    
    
    return(xmlPos,xmlArr,entryID)

def updateHEAP(line,delim,updateSeq,f,bytcnt,lnbytcnt):
    #first values for this design of control split
    #'<state accept="D,U,R,T">', '<inx>', '<id>', '<date>' 
    line=line.split(delim)
    currId=line[2]
    for up,upval in enumerate(updateSeq):
        upId=updateSeq[0][0]
        if currId==upId:
            upState=updateSeq[0][1]
            if len(upState)==1 and upState in 'DURT':
                f.seek(bytcnt-lnbytcnt)
                f.write(upState)
                f.seek(bytcnt)
            del updateSeq[0]
            break
    return

def splitQueryXML_Update(upquery,update,uval,xmlArr,xmlPos,leedroot,endroot):
    #WARNING THIS UPDATE STATEMENT IS OPEN
    #THIS MEANS THAT THERE CAN BE ADVERSE EFFECTS FOR MISFORMED UPDATE STATEMENTS
    #PLEASE VALIDATE STATEMENTS BEFORE ANY DEPLOYS TO PRODUCTION
    query=upquery
    if '</' in ''.join(query):                     #CHECK FOR END TAGS IN UPDATE STATEMENT
        print('['+','.join(query)+'] Cannot have end tags in the query example <abc not </abc')
        xmlReturn=""
    else:
        x_xmlpos=[]
        for i,itm in enumerate(xmlPos):         #doing this to keep xmlPos consistant
            x_xmlpos.append(itm)
        #QUERY xmlArr for data  COPIED FROM splitQueryXML
        if len(query)==1:
            lastparent=query[0]             #to account for queries at the root level
        else:
            lastparent=query[-2].replace('<','</')            
        valinx=""
        pathind=[]                          #this should not exceed the dimension of the xmlArr
        trigInxPts=[]                       #index points for query elements which reference the xml array
        retdataRAW=""                       #RAW DATA FROM THE ARRAY PARSE
        retdata=""                    
        attVALUE=""                         #parsed attribute value if requested
        currInx=0                          #stop index where the last element was found in the tree
        uquery=[]                           #assgin query list to this decrementing array to keep query available for subsequent parsing
        for i,itm in enumerate(query):
            uquery.append(itm)       
       
        for i,val in enumerate(xmlArr):
            foundit='0'                     #indicates if data was found
            if uquery[0] in val:
                trigInxPts.append(i)        #for index troubleshooting
                foundit='1'
                del uquery[0]
            pathind.append(foundit)

            #utilize indicator array and uquery list to verify statement and return results
            if len(uquery)==0:
                valinx=''.join(pathind).rfind('1')
                #retdataRAW=xmlArr[valinx]
                currInx=i
                break
            elif lastparent in val:               
                #retdataRAW='><'
                currInx=i
                break
            
        #get element name start and finish tags
        currtag=xmlArr[currInx]
        currtag=currtag.replace('>','')
        currtag=currtag[0:currtag.find(' ')]
        endtag=currtag.replace('<','</')
        endtag=endtag[0:endtag.find(' ')]

        #update xmlarr in here using the update value  as a trigger
        if update=="ELEV":
            #update element value
            if endtag in xmlArr[currInx+1] and uval!="":                #implies that is it is an empty element
                xmlArr.insert(currInx+1,uval)
            elif uval=="" and endtag not in xmlArr[currInx+1]:
                del xmlArr[currInx+1]                   #delete if data present and update value is none, if you want to delete all children, you will need to add to the code here possibly a loop
            elif uval!="":
                xmlArr[currInx+1]=uval                  #update the value if data present "</" not in implies that the element value exists
        if "ATTS" in update:
            attBox=xmlArr[currInx]
            attArr=attBox.split('"')
            atts=update.split('^')
            del atts[0] #remove the ATTS TRIGGER
            uval=uval.split('^')
            if len(atts)!=len(uval):
                print('attribute update dimension does not match please review your statement n in update must equal n-1 uval')
            else:
                for i,ival in enumerate(attArr):
                    if len(atts)==0:    #break to avoid dimension issues with respect to the number of atts vs the data in attArr
                        break
                    for j,jval in enumerate(atts):
                        if jval+"=" in ival:
                            attArr[i+1]=uval[j]
                            del atts[j]
                            del uval[j]
                            break
                #assign new attributes to xmlArr
                xmlArr[currInx]='"'.join(attArr)
            
        xmlReturn=""
        endmark=0
        for i,ival in enumerate(xmlArr):
            stval=""
            stval=re.search(r'<.*?>',ival)
            enval=""
            enval=re.search(r'</.*?>',ival)
            
            if stval is not None:
                stval=stval.group()
            if enval is not None:
                enval=enval.group()
            
                
            #add formatting back from xmlPos
            for j,jval in enumerate(x_xmlpos):
                xval=ival[0:ival.find(' ')]
                if xval in jval:
                    fmtstr=jval[jval.index('|,|')+3:]
                    del x_xmlpos[j]
                    break
            
            #build output string
            if "<?xml" in ival:                             #may need to add doctype to the process
                xmlReturn+=ival
            elif stval is not None and enval is None:       #this means the value is a lead element    
                xmlReturn+='\n'+fmtstr+ival
                endmark=1
            elif stval is None and enval is None:
                xmlReturn+=ival
            elif endmark==1:
                endmark=0
                xmlReturn+=ival
            else:
                xmlReturn+='\n'+fmtstr+ival
        
        #add a final carriage return to the control xml
        xmlReturn+='\n'
    return (xmlReturn,xmlArr)

def Mapp(line,delim1,d,columnOrdinal,Col_Arr,stateMode):
    #clean column array for each interation
    #note xml requires at least one attribute for this method to work 
    xCol_Arr=[]
    for i,ival in enumerate(Col_Arr):
        xCol_Arr.append(ival)
        #print(ival)
    j=0
    #print('----------top level-------')
    parentCounter=-1
    while j<len(xCol_Arr):
        jval=xCol_Arr[j]
        if jval[0]=='0':
            #print(jval+' top parent')
            parentCounter+=1
            try:
                fnd=columnOrdinal.index(parentCounter)
                pos=columnOrdinal[fnd]
                leedtag=jval[0:jval.index('>')+1]
                #notes
                #attributes in xml for mv "order of attributes important!!!!! and must remain consistant"
                #(loc)loc must be the first attribtue and must exist for all mv related tags
                #(loc)loc's value must be of a list location type [0],[0][0][1],etc
                #(ev)ev attribute must be the second attribute and must exist for all mv related tags
                #(ev)ev=1 implies that data is present for the element in the list via the loc tag position
                #(at)at attribtue must be the third attribute and must exist for all mv related tags
                #(at)at>0 this implies that there are  > 3 attributes in the tag other than (loc,ev,at)
                #(at)this tells the program the dimension of the attribute listing
                #(at) also there must be encasement of a ['',['','']] in the attribute array
                if "loc="+'"[0]"' in leedtag:
                    ElnAtt=line[pos]
                    eldelim='(E-'+delim1.replace('|','')+')'
                    atdelim='(A-'+delim1.replace('|','')+')'
                    elinx=ElnAtt.index(eldelim)+len(eldelim)
                    atinx=ElnAtt.index(atdelim)+len(atdelim)
                    elArr=ElnAtt[elinx:atinx-len(atdelim)]
                    atArr=ElnAtt[atinx:]
                    
                    #strip crlf if present in the end of the string
                    if elArr[-1]=='\n':
                        elArr=elArr[0:-1]
                    if atArr[-1]=='\n':
                        atArr=atArr[0:-1]
                    
                    #add other code here to avoid malicous data causing an issue with the executed variable listing after ok is solid
                    ok=1
                    #determine if outline is ok
                    if elArr[0]!='[' or elArr[-1]!=']':
                        ok=0
                    if atArr[0]!='[' or atArr[-1]!=']':
                        ok=0
                    #determine if dimension is ok list dimensions must be the same all the way within element or attribute
                    if elArr.count('[')!=elArr.count(']') or atArr.count('[')!=atArr.count(']'):
                        ok=0
                    #print(ok)
                    

                    #traverse the dom here point of no return to stop malicious
                    #!!!!!!!!Notice!!!!!!!!!!!!!!!call MAL here !!!!!!!!!! also check for escape mechanisims exec at dict item will execute python functions!!!!!!!!!!!!!!
                    if ok==1:
                        elExStr=""
                        atExStr=""
                        k=j*1
                        
                        itr=0
                        while k<len(xCol_Arr):
                            kval=xCol_Arr[k]
                            if itr>0 and kval[0]=='0':
                                k=len(xCol_Arr)
                                #print('breakpoint')
                            else:
                                
                                kvalSplit=kval.split('"')
                                depthMatrix=""
                                #print(kvalSplit)
                                x=""
                                y=""
                                elVal=""
                                atVal=""
                                elExStr=""
                                atExStr=""
                                evBit=0
                                atBit=0
                                #print('start----->'+xCol_Arr[k])
                                if 'loc=' in kvalSplit[0]:
                                    depthMatrix=kvalSplit[1]
                                    evBit=int(kvalSplit[3])
                                    atBit=int(kvalSplit[5])
                                    #print(depthMatrix + ' ' +evBit+' '+atBit)
                                if evBit==1:
                                    elExStr='x='+elArr+depthMatrix
                                    #print(elExStr)
                                    exec(elExStr,d)
                                    elVal=d['x']
                                    #print(elVal)
                                    kvalSplit[-1]=kvalSplit[-1]+str(elVal)       #add element value to tag
                                if atBit>=1:
                                    atExStr='y='+atArr+depthMatrix+"[-1]" #depthMatrix[0:depthMatrix.rfind('[')]+"[-1]"           
                                    #print(atExStr)
                                    exec(atExStr,d)
                                    atVal=d['y']
                                    #print(kvalSplit)
                                    #print(atVal)
                                    #print(atBit)
                                    atLoc=[]
                                    if atBit==len(atVal):                       #this blocks mv control atts from being altered if numerical value for attbit does not jive with the lenghth of the attribute listing, if you are altering dimensions dnynamicly via data you will need to alter av but note this requires a dimensional change for the base data arrays, if you update the loc att and make it work then clearly you are mathematicly full of awsomeness
                                        for l,lval in enumerate(kvalSplit):
                                            if '>' in lval:                 #I am making the assumption that the last in this array is '>' or '> with some element value'
                                                break
                                            if '=' not in lval:
                                                atLoc.append(l)
                                        #print(kval)
                                        while len(atVal)>0:
                                            Lval=atVal[-1]
                                            attInx=atLoc[-1]
                                            if Lval!="":
                                                kvalSplit[attInx]=Lval
                                            del atVal[-1]
                                            del atLoc[-1]
                                        #print(kvalSplit)
                                            
                                #update xCol_Arr
                                xCol_Arr[k]='"'.join(kvalSplit)
                                #print('finish----->'+xCol_Arr[k]) 
                                k+=1
                                itr+=1

                        #print(len(currList))
                        #print(currList[0])      
                else:
                    xCol_Arr[j]=jval+line[pos]
            except ValueError:
                pass
            
        
        j+=1

    
    #end tag reassign
    #assign entags back to xCol_arr for non mv elements and most granular elements
    for r,rval in enumerate(xCol_Arr):
        depth=int(rval[0:rval.index('|')])
        depthNxt=""
        leedtag=rval[rval.index('|')+1:rval.index(' ')]
        endtag=leedtag.replace('<','</')+'>'
        #print(leedtag)
        #print(endtag)
        
        arrEnd=len(xCol_Arr)-1
        if r!=arrEnd:
            depthNxt=int(xCol_Arr[r+1][0])
        else:
            depthNxt=depth
            
        if depthNxt<=depth:
            xCol_Arr[r]=xCol_Arr[r].replace('\n','')+endtag


        

    #assign endtags back to xCol_arr for mv elements not covered by most granular
    for r,rval in enumerate(xCol_Arr):
        if '</' not in rval:
            depth=int(rval[0:rval.index('|')])
            leedtag=rval[rval.index('|')+1:rval.index(' ')]
            endtag=leedtag.replace('<','</')+'>'
            #print(leedtag)
            #print(endtag)
            
            arrEnd=len(xCol_Arr)-1
            s=r*1
            while s<=arrEnd:
                s+=1
                sval=""
                sdepth=0
                if s<=arrEnd:
                    sval=xCol_Arr[s]
                    sdepth=int(sval[0:sval.index('|')])
            
                if sdepth<=depth:
                    #print(sval)
                    xCol_Arr.insert(s,str(depth)+'|'+endtag)
                    break

    
    #return xml
    retXML=""
    if stateMode[0]=="xml":
        for r,rval in enumerate(xCol_Arr):
            depth=int(rval[0:rval.index('|')])
            rval=rval[rval.index('|')+1:]
            retXML+='\t'*depth+rval+'\n'


    #return array table structure data for element values
    retTable=[]
    mvCarry=[]
    if stateMode[0]=="tableELE" or stateMode[0]=="tableALL":
        for r,rval in enumerate(xCol_Arr):
            depth=int(rval[0:rval.index('|')])
            rval=rval[rval.index('|')+1:]
            leedtag=rval[0:rval.index('>')+1]
            elVal=""
            if '</' not in leedtag:
                elVal=rval[rval.index('>')+1:rval.rindex('<')]
                if depth==0 and 'loc=' not in leedtag:
                    tag=leedtag.strip()
                    tag=tag[tag.index('<')+1:tag.index(' ')]
                    tag+='->'
                    retTable.append(tag+elVal)
                elif depth==0 and 'loc=' in leedtag:
                    mvCarry=[]
                    tag=leedtag.strip()
                    tag=tag[tag.index('<')+1:tag.index(' ')]
                    tag+='>'
                    mvCarry.append(tag)
                elif depth>0 and 'loc=' in leedtag and 'ev='+'"0"' in leedtag:
                    tag=leedtag.strip()
                    tag=tag[tag.index('<')+1:tag.index(' ')]
                    tag+='>'
                    mvCarry.append(tag)
                elif depth>0 and 'loc=' in leedtag and 'ev='+'"1"' in leedtag:
                    if depth==len(mvCarry)-1:
                        del mvCarry[depth:]
                    tag=leedtag.strip()
                    tag=tag[tag.index('<')+1:tag.index(' ')]
                    tag+='->'
                    retTable.append("".join(mvCarry)+tag+elVal)
                    #print(mvCarry)
                    del mvCarry[depth:]


    #return array table structure data for attribute values
    attTable=[]
    mvCarry=[]
    if stateMode[0]=="tableATT" or stateMode[0]=="tableALL":
        for r,rval in enumerate(xCol_Arr):
            depth=int(rval[0:rval.index('|')])
            rval=rval[rval.index('|')+1:]
            leedtag=rval[0:rval.index('>')+1]
            elVal=""
            if '</' not in leedtag:
                #must have element retrun value in order to qualify the att return
                elVal=rval[rval.index(' ')+1:rval.index('>')] 
                
                    
                if depth==0 and 'loc=' not in leedtag:
                    tag=leedtag.strip()
                    tag=tag[tag.index('<')+1:tag.index(' ')]
                    tag+='->(A)->'
                    attTable.append(tag+elVal)
                elif depth==0 and 'loc=' in leedtag:
                    mvCarry=[]
                    tag=leedtag.strip()
                    tag=tag[tag.index('<')+1:tag.index(' ')]
                    tag+='>'
                    mvCarry.append(tag)
                elif depth>0 and 'loc=' in leedtag and 'ev='+'"0"' in leedtag:
                    tag=leedtag.strip()
                    tag=tag[tag.index('<')+1:tag.index(' ')]
                    tag+='>'
                    mvCarry.append(tag)
                elif depth>0 and 'loc=' in leedtag and 'ev='+'"1"' in leedtag:
                    if depth==len(mvCarry)-1:
                        del mvCarry[depth:]
                    tag=leedtag.strip()
                    tag=tag[tag.index('<')+1:tag.index(' ')]
                    tag+='->(A)->'
                    attTable.append("".join(mvCarry)+tag+elVal)
                    #print(mvCarry)
                    del mvCarry[depth:]
                    
    #json return
    jsonRet=[]
    mvCarry=[]
    if stateMode[0]=="json":
        for r,rval in enumerate(xCol_Arr):
            #print(rval)
            depth=int(rval[0:rval.index('|')])
            rval=rval[rval.index('|')+1:]
            leedtag=rval[0:rval.index('>')+1]
            elVal=""
            atVal=""
            elName=""
            if '</' not in leedtag:
                elName=leedtag[1:rval.index(' ')]
                elVal=rval[rval.index('>')+1:rval.rindex('<')]
                atVal=rval[rval.index(' ')+1:rval.index('>')] 
                
                    
                
                atValArr=atVal.split('"')
                #consequence of the split delete last list item array should always have an even value
                del atValArr[-1]
                
                if 'loc=' in atValArr:   #mvcases
                    #print(depth)
                    #print(atValArr)
                    attLineItm=""
                    depthMult=depth+1
                    
                    
                    if '</' in rval:
                        jsonRet[-1]=jsonRet[-1]+','
                        jsonRet.append(depth*'\t'+'"'+elName+'":{')
                    else:
                        
                        jsonRet.append(depth*'\t'+'"'+elName+'":{')
                    
                    for s,sval in enumerate(atValArr):
                        sval=sval.strip()
                        if s % 2 ==0:
                            attLineItm+='"_'+sval.replace('=','')+'":'
                        else:
                            attLineItm+='"'+sval+'",'
                            jsonRet.append(depthMult*'\t'+attLineItm)
                            attLineItm=""
                    #att element value if present
                    jsonRet.append(depthMult*'\t'+'"__text":"'+elVal+'"')
                    if '</' in rval:
                        jsonRet.append(depthMult*'\t'+'}')
                    
                else:         #non mv cases
                    jsonRet.append('"'+elName+'":{')
                    attLineItm=""
                    for s,sval in enumerate(atValArr):
                        sval=sval.strip()
                        if s % 2 ==0:
                            attLineItm+='"_'+sval.replace('=','')+'":'
                        else:
                            attLineItm+='"'+sval+'",'
                            jsonRet.append('\t'+attLineItm)
                            attLineItm=""
                    #att element value if present
                    jsonRet.append('\t'+'"__text":"'+elVal+'"')
                    jsonRet.append('}')
            else:
                jsonRet.append(depth*'\t'+'}')
        #add comma's to 0 level elements
        for r,rval in enumerate(jsonRet):
            if rval=='}' and r<len(jsonRet)-1:
                jsonRet[r]=jsonRet[r]+','

    #concate jsonRetArr
    jsonRet='\n'.join(jsonRet)


    #ADD OTHER OUTPUTS HERE BASED ON A PARSE OF xCol_Arr
    #for i,ival in enumerate(xCol_Arr):
        #print(ival)
        

                
    return(retXML,retTable,attTable,jsonRet)

def scrub(val,lang,mode):
    #crlf=""                                     #carriage return line feed base data stored as /x0D/x0A #commented out to throw error as variable will only be defined if lang answered correctly
    #tab=""                                      #tab  base data stored as /x09

    if lang=="python":
        crlf="\n"
        tab="\t"
    if lang=="javascript":
        crlf="\r\n"
        tab="\t"

    if mode=="ob":
        val=val.replace('/x0D/x0A',crlf)          #crlf
        val=val.replace('/x09',tab)              #tab

    return(val)
    

    
def createTemp(tmp,trgt,data,trig):
    ftemp=open(tmp,'w')
    ftemp.write(data)                                #write out the control
    switch=""
    delim=""
    if trig!=0:                                      #trigger data set to filter data for temp to file process
        switch=trig[0]
        delim=trig[1]
    #print(switch)
    #print(delim)
        
    for line in trgt:                                #file pointer for f at this point should be on the split data which is awsomeness
        if trig!=0 and delim in line:                                  #deletion/updates via omission of write to temp file and subsequent write to RL also omits added crlf
            lineArr=line.split(delim)
            lnType=lineArr[1]
            lnID=lineArr[2]
            if lnType=='R':                         #assumes initial line seen is a R line
                lnState=lineArr[4]
                if lnState not in switch and delim in line:
                    ftemp.write(line)
            else:
                if lnState not in switch and delim in line:                    #assumes lnState is only defined on the R line (this should error out of R line is undefined for the call)
                    ftemp.write(line)
        else:                                       #no filtering case
            if delim in line:
                ftemp.write(line)
    ftemp.close()

    return

def switchAroo(deleteF,tempF):
    os.remove(deleteF)
    os.rename(tempF,deleteF)

    return
    
    
