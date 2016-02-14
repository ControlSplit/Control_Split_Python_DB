# Control_Split_Python_DB

Please read in Raw Form, thanks. 

If you would like to take a look, please copy and paste the xmlff files onto your machine. 
Please have at least python 3.4.3 installed. 
Copy the tQ2.py and tQ.py files onto your machine. 

tQ2.py=Current Main point of entry for Control Split Database design (query level) Fopen qualifers etc
tQ.py=Core XML parser/Mapping/etc


Open up the tQ2.py file and alter the following variables for your path
heapPath="C:/Python34/sample_HEAP.xmlff"   #root in the xmlff file must match the file name w/o extesnion this is the split file
rlPath="C:/Python34/sample_RL.xmlff"       #root in the xmlff file must match the file name w/o extension this is the control file


Read comments in code, I am presently working on building this out for more funtionality in the future. I just wanted to get the code out there to get some feedback. 


Thanks
Michael

---Top level of how it works
In a nutshell, what this software does is takes a shell of xml (as long as it follows some certain parameters for the xml parser) and maps it to a entry type/row type data set via  array based structures.
This to allow for more of a granular level approach to a response document or data structure from a server.
Data types concerns would need to be addressed by an application that writes to the the split/heap file.

For example
Line based Data (future application would need to escape line delimiters and parser error like data in the arrays)
R|34*3||34*3|1|34*3|2015-10-31 12:33:48|34*3|(E-34*3)[[['<xml><NAME>JOE</NAME></xml>','hunter'],'00000000000']](A-34*3)[[[['',['mr']],['',['esq']],['spanish','english']],['',['france']]],[]]|34*3|(E-34*3)[['','notes about work']](A-34*3)[[['',['123 fake st','foobar','il','00000']],['',['345 fake st','foobar','il','000000']]]]
R|34*3||34*3|2|34*3|2016-01-31 11:15:38|34*3|(E-34*3)[[['mike','hunter'],'00000000000']](A-34*3)[[[['',['mr']],['',['esq']],['spanish','english']],['',['france']]],[]]|34*3|(E-34*3)[['','notes about work']](A-34*3)[[['',['23 fake st','foobar','il','00000']],['',['345 fake st','foobar','il','000000']]]]
R|34*3||34*3|3|34*3|2016-01-31 11:15:55|34*3|(E-34*3)[[['michelle','hunter'],'00000000000']](A-34*3)[[[['',['ms']],['',['esq']],['spanish','english']],['',['france']]],[]]|34*3|(E-34*3)[['','notes about work']](A-34*3)[[['',['13 fake st','foobar','il','00000']],['',['345 fake st','foobar','ne','000000']]]]

Shell:
        <column>
                 <state accept="D,U,R,X"></state>
                 <inx accept="AN"></inx>
                 <id accept="N"></id>
                 <date accept="D"></date>
                 <user loc="[0]" ev="0" av="0" >
                         <name loc="[0][0]" ev="0" av="2" primLang="" secLang="">
                                  <first loc="[0][0][0]" ev="1" av="1" srnme=""></first>
                                 <last loc="[0][0][1]" ev="1" av="1" srnme=""></last>
                        </name>
                         <phone loc="[0][1]" ev="1" av="1" type=""></phone>
                 </user>
                 <address loc="[0]" ev="0" av="0">
                         <home loc="[0][0]" ev="0" av="4" street="" city="" state="" zip=""></home>
                         <work loc="[0][1]" ev="1" av="4" street="" city="" state="" zip=""></work>
                </address>
        </column>

Query 1:
queryCmdArr=[['ALL'],['xml',''],[['2|<first ',['LKE',''],'<xml>',0,'AssignInx']]]
Explained: Get all elements, return xml, where the 2nd depth <first> element like the text value <xml>

Query 1 xml response:
<state accept="D,U,R,X">R</state>
<inx accept="AN"></inx>
<id accept="N">1</id>
<date accept="D">2015-10-31 12:33:48</date>
<user loc="[0]" ev="0" av="0" >
        <name loc="[0][0]" ev="0" av="2" primLang="spanish" secLang="english">
                <first loc="[0][0][0]" ev="1" av="1" srnme="mr"><xml><NAME>JOE</NAME></xml></first>
                <last loc="[0][0][1]" ev="1" av="1" srnme="esq">hunter</last>
        </name>
        <phone loc="[0][1]" ev="1" av="1" type="france">00000000000</phone>
</user>
<address loc="[0]" ev="0" av="0">
        <home loc="[0][0]" ev="0" av="4" street="123 fake st" city="foobar" state="il" zip="00000"></home>
        <work loc="[0][1]" ev="1" av="4" street="345 fake st" city="foobar" state="il" zip="000000">notes about work</work>
</address>


Query 2:
queryCmdArr=[['<state ','<user '],['json',''],[['2|<first ',['E2','0'],'ms',0,'AssignInx']]]
Explained: Get the data soley for the <state> and <user> elements, return json, where the 2nd depth <first> element, 1st attribute is equal to 'ms'

Query 2 json response:
"state":{
        "_accept":"D,U,R,X",
        "__text":"R"
},
"inx":{
        "_accept":"AN",
        "__text":""
},
"id":{
        "_accept":"N",
        "__text":""
},
"date":{
        "_accept":"D",
        "__text":""
},
"user":{
        "_loc":"[0]",
        "_ev":"0",
        "_av":"0",
        "__text":""
        "name":{
                "_loc":"[0][0]",
                "_ev":"0",
                "_av":"2",
                "_primLang":"spanish",
                "_secLang":"english",
                "__text":"",
                "first":{
                        "_loc":"[0][0][0]",
                        "_ev":"1",
                        "_av":"1",
                        "_srnme":"ms",
                        "__text":"michelle"
                        },
                "last":{
                        "_loc":"[0][0][1]",
                        "_ev":"1",
                        "_av":"1",
                        "_srnme":"esq",
                        "__text":"hunter"
                        }
        },
        "phone":{
                "_loc":"[0][1]",
                "_ev":"1",
                "_av":"1",
                "_type":"france",
                "__text":"00000000000"
                }
},
"address":{
        "_loc":"[0]",
        "_ev":"0",
        "_av":"0",
        "__text":"",
        "home":{
                "_loc":"[0][0]",
                "_ev":"0",
                "_av":"4",
                "_street":"",
                "_city":"",
                "_state":"",
                "_zip":"",
                "__text":""
                },
        "work":{
                "_loc":"[0][1]",
                "_ev":"1",
                "_av":"4",
                "_street":"",
                "_city":"",
                "_state":"",
                "_zip":"",
                "__text":""
                }
}

Query 3:
queryCmdArr=[['ALL'],['tableALL',''],[['1|<work ',['E2','2'],'ne',0,'AssignInx']]]
Explained: Get all data, return in a verticalized from all element and attribute values, where depth 1 <work> element 3rd attrubute equal to ne

Query3 response:
state->R
inx->
id->3
date->2016-01-31 11:15:55
user>name>first->michelle
user>name>last->hunter
user>phone->00000000000
address>work->notes about work
state->(A)->accept="D,U,R,X"
inx->(A)->accept="AN"
id->(A)->accept="N"
date->(A)->accept="D"
user>name>first->(A)->loc="[0][0][0]" ev="1" av="1" srnme="ms"
user>name>last->(A)->loc="[0][0][1]" ev="1" av="1" srnme="esq"
user>phone->(A)->loc="[0][1]" ev="1" av="1" type="france"
address>work->(A)->loc="[0][1]" ev="1" av="4" street="345 fake st" city="foobar" state="ne" zip="000000"





Licensed under MIT standard

#Copyright (c) <2016> <MICHAEL HUNTER>

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
#to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
#and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

