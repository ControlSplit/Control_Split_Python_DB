﻿# Control_Split_Python_DB


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

