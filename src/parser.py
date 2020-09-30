#!/usr/bin/env python

"""Parser for UK House of Commons Data

Transforms HoC speeches from XML 
to json list file.
"""

__author__ = "Armin Pournaki"
__copyright__ = "Copyright 2020, Armin Pournaki"
__license__ = "GPLv3"
__version__ = "1.0"
__email__ = "pournaki@mis.mpg.de"


def parser():

    def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        # Print New Line on Complete
        if iteration == total: 
            print()

    # load libraries
    from lxml import etree
    import nested_lookup as nl
    import os
    import json

    
    DATADIR = "./data/speeches/"
    # get all the filenames in the directory
    filenamelist = []
    def absoluteFilePaths(DATADIR):
        for dirpath,_,filenames in os.walk(DATADIR):
            for f in filenames:
                filenamelist.append(os.path.join(dirpath, f))
        return filenamelist
    filenamelist = sorted(absoluteFilePaths(DATADIR))

    with open("./data/people.json") as json_file:
        memberdata = json.load(json_file)
    
    jsondict     = {}

    l = len(filenamelist)
    
    # Initial call to print 0% progress
    printProgressBar(0, l, prefix = 'Parsing...', suffix = 'Complete', length = 50)
    
    for progresso, filename in enumerate(filenamelist):

        parser = etree.XMLParser(dtd_validation=False)
        tree = etree.parse(filename, parser)
        root = tree.getroot()

        printProgressBar(progresso + 1, l, prefix = 'Parsing...', suffix = 'Complete', length = 50)

        context = root.findall('./')

        for element in context:
    
            if element.tag == 'major-heading':
                headingtext = element.text
                headingtext = headingtext.replace("\n","").replace("\t","")
                date = filename[23:33]
                jsondict[f"{headingtext} {date}"] = {}
                jsondict[f"{headingtext} {date}"]["speeches"] = []
            
            if "headingtext" in locals():

                if element.tag == 'speech':    
                    speakername = element.attrib.get("speakername")
                    speakerid   = element.attrib.get("person_id")
                    speechid    = element.attrib.get("id")

                    speechtext = str()
                    
                    for t in element.getchildren():
                        if t.getchildren() == []:
                            try:
                                speechtext += t.text
                            except TypeError:
                                pass
                        else:
                            for p in t.getchildren():
                                try:
                                    speechtext += t.text
                                    speechtext += p.text
                                    speechtext += p.tail
                                    speechtext += " "
                                except TypeError:
                                    pass


                    speechdict = {}

                    try:
                        speechdict["id"] = speechid
                    except KeyError:
                        pass
                    try:
                        speechdict["speaker_id"] = speakerid
                    except KeyError:
                        speechdict["speaker_id"] = "None"
                    try:
                        speechdict["date"] = date
                    except KeyError:
                        speechdict["date"] = "None"  
                    try:
                        speechdict["name"] = speakername
                    except KeyError:
                        speechdict["name"] = "None"
                    try:
                        speechdict["party"]  = memberdata[speakerid]
                    except KeyError:
                        speechdict["party"] = "None"
                    try:
                        speechdict["text"]           = speechtext
                    except KeyError:
                        pass
                    try:
                        jsondict[f"{headingtext} {date}"]["speeches"].append(speechdict)
                    except KeyError:
                        pass

                    if speechdict["name"] == None:
                        speechdict["name"] = "None"
                    if speechdict["speaker_id"] == None:
                        speechdict["speaker_id"] = "None"
                    if speechdict["party"] == None:
                        speechdict["party"] = "None"
                    
    
    parsed_speeches = jsondict

    for element in parsed_speeches:
        for speech in parsed_speeches[element]["speeches"]:
            speech["discussion_title"] = element

    flatdict = []
    for element in parsed_speeches:
        for speech in parsed_speeches[element]["speeches"]:
            flatdict.append(speech)

    for speeches in flatdict:
        speeches["text"] = speeches["text"].replace('"', '``').replace("'",'`')

        try:
            speeches["name"] = speeches["name"].replace('"', '``').replace("'",'`')
        except AttributeError:
            pass
    
    with open ("./speeches.jsonl", "w", encoding = "utf-8") as f:
        for line in flatdict:
            json.dump(line, f, ensure_ascii=False)
            f.write("\n")

    print("Success! Saved parsed speeches to './speeches.jsonl'.")

    return flatdict


    # with open(f"./speeches_nested.json","w", encoding='utf-8') as f:
    #     json.dump(jsondict,f,ensure_ascii=False,indent = 0)
     
    # return jsondict
