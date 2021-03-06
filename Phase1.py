#Phase 1 - Preparing data files
#Uses python2
#Issues: not ordered from t to o to a

import sys

if len(sys.argv) > 1: # Text file name is given
    temp_file = open(sys.argv[1], 'r')
else: # Else read from standard input
    print("Needs text file name as first argument")
    exit()

temp_file.readline() #First line is garbage in XML file
line_input = "example"

terms = open("terms.txt", 'w')
years = open("years.txt", 'w')
recs = open("recs.txt", 'w')

while line_input != "</dblp>": # Stops the program from looping infinitely
    
    line_input = temp_file.readline()
    
    #print(line_input)
    #Base case: end of file reached
    if (line_input == "</dblp>\n" or line_input == "</dblp>" or len(line_input)==0):
        break
        
    #Segment line into different pieces according to the tags
    xml_split = line_input.split("<")[1:]
    
    #Get key by parsing for "
    start = False
    for i in range(len(xml_split[0])):
        if (xml_split[0][i] == "\""):
            if (not start):
                #Found first "
                start = True
                keyStart = i+1
            else:
                #Found last "
                keyEnd = i
                break
    key = xml_split[0][keyStart:keyEnd]
    #print(key)
    
    #Record in recs.txt
    recs.write(key+":"+line_input.replace("\\", "&#92;"))#+"\n"
    
    #Get terms and record them(make sure to lowercase!)
    for i in range(1, len(xml_split)-1, 2):
        #Term is author
        if xml_split[i][0:6] == "author":
            tags_split = xml_split[i][7:].lower().split() #split title terms
            for tag in tags_split:
                if len(tag) > 2: #make sure term length > 2
                    terms.write("a-"+filter(str.isalnum, tag)+":"+key+"\n")
        #Term is title
        elif xml_split[i][0:5] == "title":
            tags_split = xml_split[i][6:].lower().split() #split title terms
            for tag in tags_split:
                if len(tag) > 2: #make sure term length > 2
                    terms.write("t-"+filter(str.isalnum, tag)+":"+key+"\n")
        #Term is year
        elif xml_split[i][0:4] == "year":
            years.write(xml_split[i][5:]+":"+key+"\n")
        #Term is something random that is a text field
        else:
            if xml_split[i][0:5] == "pages": #must be text field
                continue
            tags_split = xml_split[i].split(">")[1] #e.g. xml_split = pages>607-619
            tags_split = tags_split.lower().split() #split title terms
            for tag in tags_split:
                if len(tag) > 2: #make sure term length > 2
                    terms.write("o-"+tag+":"+key+"\n")
    
# End of program
terms.close()
years.close()
recs.close()
temp_file.close()
print("Done!")
