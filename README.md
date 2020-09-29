# UK House of Commons Parser

## Description
A parser that transforms speeches from the [UK House of Commons](https://www.parliament.uk/business/commons/) to a list of JSONs. The raw XML data is retrieved from [ParlParse](http://parser.theyworkforyou.com/hansard.html). 

The speeches are saved in `./speeches.jsonl`. Every line consists of one speech dictionary. See [sample output](#sample-output) for more information. 

## How to use
Clone and enter this repo:
``` 
$ git clone https://github.com/pournaki/houseofcommons-parser
$ cd houseofcommons-parser
```

Install the necessary libraries: 

``` 
$ pip3 install -r requirements.txt
```

Note that this repo does not contain the raw data. You need to retrieve the XMLs by year to the speeches directory from [ParlParse](http://parser.theyworkforyou.com/hansard.html) using rsync:

```
$ cd data
$ mkdir speeches
$ cd speeches
$ rsync -az --progress --exclude '.svn' --exclude 'tmp/' "data.theyworkforyou.com::parldata/scrapedxml/debates/debatesYEAR-*" .
```

For example, if you want the XMLs for 2019, run this command from within `./data/speeches`:
```
$ rsync -az --progress --exclude '.svn' --exclude 'tmp/' "data.theyworkforyou.com::parldata/scrapedxml/debates/debatesYEAR-*" .
```

Once you have the XMLs, go back to the parent folder and run the parser:
```  
$ cd ../../
$ python3 run.py
```

## Sample output
```
{
  "id": "uk.org.publicwhip/debate/2018-07-02b.117.0",
  "speaker_id": "uk.org.publicwhip/person/10045",
  "date": "2018-07-02",
  "name": "Clive Betts",
  "party": "labour",
  "text": "I thank the hon. Gentleman for the part he played in the joint Select Committee report. He is absolutely right about that. Figures in the inquiry showed that for the same work, social care workers were paid about 29% less on average than workers in the NHS.",
  "discussion_title": "MINISTRY OF JUSTICE 2018-07-02"
 }
```
