#!/usr/bin/python
#title           :bt_csvTobt_json.py
#description     :This will create a header for a python script.
#author          :bgw
#date            :20110930
#version         :0.4
#usage           :bt_csvTobt_json.py
#notes           :
#python_version  :3.6.6  
#==============================================================================
import os
import json
import requests
import time
import argparse

def extractTojson():
    x = 0
    y = 0
    err = 0
    csv_file = open("../data/bt_tool.txt",'r')
    for tool in csv_file.readlines():
        if len(tool.split('\t')) >= 10 :
            tool_name = tool.split('\t')[2]
            json = tool.split('\t')[10]
            if json != "":
                try :
                    json_tool = json.replace('""','"').replace('"{','{').replace('}"','}')
                    if y == 100:
                        y = 0
                        x = x + 100
                    directory = "../results/json/"+str(x)

                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    json_file = open("../results/json/"+str(x)+"/"+tool_name+'.json','w')
                    json_file.write(json_tool)
                    json_file.close

                    y += 1
                except:
                    print(tool_name)
                    err +=1
    print(err)
            
def jsonToPMIDcsv():
    path = "../results/json/"
    file_out = open("../results/20181123_format_bttools.txt","a")
    err = 0
    for subdir in os.listdir(path):
        for json_file in os.listdir(os.path.join(path,subdir)):
            try :
                #print(os.path.join(path,subdir,json_file))
                with open(os.path.join(path,subdir,json_file)) as f:
                    d_json = json.load(f)            
                tool_name = json_file.replace(".json","")
                topics = []
                inputs = []
                inputs_f = []
                operations = []
                outputs = []
                outputs_f = []
                publication_pmid = []
                publication_doi = []
                publications =  d_json["publication"]
                for topic in d_json["topic"]:
                    if topic["term"] != "" and topic["term"] not in topics and topic["term"] != None:
                        topics.append(topic["term"])
                for function in d_json["function"]:
                    if "input" in function :
                        if function["input"] != "" and function["input"] != None:
                            for ip in function["input"] :
                                if "data" in ip :
                                    inputs.append(ip["data"]["term"])
                                if "format" in ip :
                                    if "format" in ip :
                                        for form in ip["format"] :
                                            inputs_f.append(form["term"])

                    if "operation" in function :
                        if function["operation"] != "" and function["operation"] != None:
                            for ip in function["operation"] :
                                operations.append(ip["term"])
                    if "output" in function :
                        if function["output"] != "" and function["output"] != None:
                            for out in function["output"] :
                                if "data" in out :
                                    outputs.append(out["data"]["term"])
                                if "format" in out :
                                    for form in out["format"] :
                                        outputs_f.append(form["term"])
                for pub in publications :
                    if pub["pmid"] != "" and pub["pmid"] not in publication_pmid and pub["pmid"] != None:
                        publication_pmid.append(pub["pmid"])
                    if pub["doi"] != "" and pub["doi"] not in publication_doi and pub["doi"] != None:
                        publication_doi.append(pub["doi"])
                if len(publication_pmid) != 0:
                    str_publication_pmid = '|'.join(publication_pmid)
                else :
                    str_publication_pmid = "NA"
                if len(publication_doi) != 0:
                    str_publication_doi = '|'.join(publication_doi)
                else :
                    str_publication_doi = "NA"
                if len(topics) != 0:
                    str_topics = '|'.join(topics)
                if len(inputs) != 0:
                    str_inputs = '|'.join(inputs)
                if len(operations) != 0:
                    str_operations = '|'.join(operations)
                if len(outputs) != 0:
                    str_outputs = '|'.join(outputs)
                if len(inputs_f) != 0:
                    str_inputs_f = '|'.join(inputs_f)
                if len(outputs_f) != 0:
                    str_outputs_f = '|'.join(outputs_f)
                else :
                    str_topics = "NA"
                    str_outputs = "NA"
                    str_outputs = "NA"
                    str_inputs = "NA"
                    str_inputs_f = "NA"
                    str_outputs_f = "NA"

                file_out.write(tool_name+"\t"+str_publication_pmid+"\t"+str_publication_doi+"\t"+str_topics+"\t"+str_inputs+"\t"+str_inputs_f+"\t"+str_operations+"\t"+str_outputs+"\t"+str_outputs_f+"\t"+d_json["homepage"]+"\n")
            except:
                print(os.path.join(path,subdir,json_file))
                err += 1
    print(err)

def getPmid(doi):
    resp = requests.get('https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=dardethomas@gmail.com&ids='+doi+'&format=json')
    if resp.status_code != 200:
        print("This means something went wrong.")
        print(doi)
        return ['NA']
    response = resp.json()
    l_pmid = []
    for i in response['records']:
        if 'pmid' in i :
            if i['pmid'] not in l_pmid :
                l_pmid.append(i['pmid'])
        else :
            l_pmid.append('NA')
    return l_pmid

def getPmidSCOPUS(doi):
    l_pmid = []
    resp = requests.get('https://api.elsevier.com/content/search/scopus?query=DOI('+doi+')&field=pubmed-id&apiKey=6d11611f1e707149a907c3dd01e00f33&httpAccept=application/json')
    if resp.status_code != 200:
        print("This means something went wrong.")
        print(doi)
        if 'NA' not in l_pmid :
            l_pmid.append('NA')
    else :
        response = resp.json()
        entry = response["search-results"]['entry']
        for i in entry :
            if 'pubmed-id' in i :
                if i['pubmed-id'] not in l_pmid :
                    l_pmid.append(i['pubmed-id'])    
    resp = requests.get('https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=dardethomas@gmail.com&ids='+doi+'&format=json')
    if resp.status_code != 200:
        print("This means something went wrong.")
        print(doi)
        if 'NA' not in l_pmid :
            l_pmid.append('NA')
    else :
        response = resp.json()
        for i in response['records']:
            if 'pmid' in i :
                if i['pmid'] not in l_pmid :
                    l_pmid.append(i['pmid'])
    return l_pmid


def getCitation():
    file_id = open('../results/20181123_format_bttools.txt','r')
    format_out = open('../results/20181126_bttools_citations.txt','a')
    i = 0
    max_tool = 11686
    for tool in file_id.readlines():
        i += 1
        print(str(i)+'/'+str(max_tool))
        tool_info = tool.split('\t')
        if tool_info[2] != "NA" and tool_info[2] != "none":
            doi_to_pmid = []
            if '|' in tool_info[2] :
                list_doi = tool_info[2].split('|')
                for doi in list_doi :
                    l_pmid = getPmidSCOPUS(doi)
                    doi_to_pmid.extend(l_pmid)
            else :
                l_pmid = getPmidSCOPUS(tool_info[2])
                doi_to_pmid.extend(l_pmid)
            if tool_info[1] not in doi_to_pmid and tool_info[1] != 'NA' :
                doi_to_pmid.append(tool_info[1])
            str_doi_to_pmid = '|'.join(doi_to_pmid)
            tool_info[1] = str_doi_to_pmid
            format_out.write('\t'.join(tool_info))
        else :
            if tool_info[1] != "NA":
                format_out.write(tool)

def getYear(pmids):
    l_year = []
    if len(pmids) > 100:
        x = 0
        while x < len(pmids):
            l_pmids = ','.join(pmids[x:x+100])
            resp = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id='+l_pmids+'&format=json&api_key=62f907a4b5c49135bc87dc6951c2110d4808&email=dardethomas@gmail.com')
            if resp.status_code != 200:
                print("This means something went wrong.")
            else :
                for i in pmids[x:x+100] :
                    response = resp.json()
                    date = response['result'][str(i)]['pubdate']
                    year = date.split(' ')[0]
                    l_year.append(year)
            x = x +100

        l_pmids = ','.join(pmids[x:len(pmids)])
        resp = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id='+l_pmids+'&format=json&api_key=62f907a4b5c49135bc87dc6951c2110d4808&email=dardethomas@gmail.com')
        if resp.status_code != 200:
            print("This means something went wrong.")
        else :
            for i in pmids[x:len(pmids)] :
                response = resp.json()
                date = response['result'][str(i)]['pubdate']
                year = date.split(' ')[0]
                l_year.append(year)

    else :
        l_pmids = ','.join(pmids)
        resp = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id='+l_pmids+'&format=json&api_key=62f907a4b5c49135bc87dc6951c2110d4808&email=dardethomas@gmail.com')
        if resp.status_code != 200:
            print("This means something went wrong.")
        else :
            print(pmids)
            for i in pmids :
                response = resp.json()
                try :
                    date = response['result'][str(i)]['pubdate']
                except :
                    print(response)
                year = date.split(' ')[0]
                l_year.append(year)

    return l_year

def getTrending(pmids):
    d_years = []
    for pmid in pmids :
        resp = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pubmed_citedin&id='+str(pmid)+'&format=json&api_key=62f907a4b5c49135bc87dc6951c2110d4808&tool=my_tool&email=my_email@example.com')
        #print(pmid)
        if resp.status_code == 200:
            response = resp.json()    
            for i in response['linksets']:
                if 'linksetdbs' in i :
                    for j in i['linksetdbs'] :
                        list_pmid = j['links']
                        for id in  list_pmid:
                            if id not in d_years :
                                d_years.append(str(id))
        else :
            d_years.append("NA")
    return d_years

def trendingInformation(file_in):
    file_id = open(file_in,'r')
    format_out = open(file_in+'_trending.txt','a')
    format_out.write('Tool'+'\t'+'Pmid'+'\t'+'DOI'+'\t'+'Annotation'+'\t'+'Input'+'\t'+'Input_format'+'\t'+'Oeration'+'\t'+'Output'+'\t'+'Output_format'+"\t"+'Homepage'+'\t'+'Citation'+'\n')
    i = 0
    max_tool = 10741
    for tool in file_id.readlines():
        tool_info = tool.split('\t')
        tool_info[-1] = tool_info[-1].replace('\n','')
        i += 1
        print(str(i)+'/'+str(max_tool))
        if 'NA' not in tool_info[1] :
            if '|' in tool_info[1] :
                l_pmid = tool_info[1].split('|')
                d_years = getTrending(l_pmid)
            else:
                d_years = getTrending([tool_info[1],'NA'])
            #print(d_years)
            d_years_str = '|'.join(d_years)
            format_out.write('\t'.join(tool_info)+'\t'+d_years_str+'\n')


def cutFile():
    file_id = open('../results/format_bttools_format.txt','r')
    x = 0
    y = 0
    file_out = open('../results/split/format_bttools_'+str(x)+'.txt','a')
    for tool in file_id.readlines():
        if y == 1000 :
            file_out.close()
            y = 0
            x += 1000
            file_out = open('../results/split/format_bttools_'+str(x)+'.txt','a')
        file_out.write(tool)
        y += 1

def getPMIDPubDate(file_in):
    i = 0
    max_tool = 10741
    file_id = open(file_in,'r')
    format_out = open(file_in+'_final.txt','a')
    format_out.write('Tool'+'\t'+'Pmid'+'\t'+'DOI'+'\t'+'Annotation'+'\t'+'Homepage'+'\t'+'Citation'+'\t'+'2018'+'\t'+'2017'+'\t'+'2016'+'\t'+'2015'+'\t'+'2014'+'\t'+'2013'+'\t'+'2012'+'\t'+'2011'+'\t'+'2010'+'\t'+'2009'+'\t'+'2008'+'\t'+'2007'+'\t'+'2006'+'\t'+'2005'+'\n')
    for tool in file_id.readlines():
        i += 1
        tool_info = tool.split('\t')
        print(str(i)+'/'+str(max_tool)+" - "+tool_info[-0])
        d_pmid = {'2018':0,'2017':0,'2016':0,'2015':0,'2014':0,'2013':0,'2012':0,'2011':0,'2010':0,'2009':0,'2008':0,'2007':0,'2006':0,'2005':0}
        tool_info[-1] = tool_info[-1].replace('\n','')
        pmids = tool_info[5]
        #print(pmids)
        if pmids != 'NA' :
            if '|' in pmids :
                l_pmid = pmids.split('|')
                l_years = getYear(l_pmid)
            else:
                l_years = getYear([pmids])
            for year in l_years :
                if year != 'NA' and year in d_pmid:
                    d_pmid[year] = d_pmid[year] + 1
            format_out.write('\t'.join(tool_info)+'\t'+str(d_pmid['2018'])+'\t'+str(d_pmid['2017'])+'\t'+str(d_pmid['2016'])+'\t'+str(d_pmid['2015'])+'\t'+str(d_pmid['2014'])+'\t'+str(d_pmid['2013'])+'\t'+str(d_pmid['2012'])+'\t'+str(d_pmid['2011'])+'\t'+str(d_pmid['2010'])+'\t'+str(d_pmid['2009'])+'\t'+str(d_pmid['2008'])+'\t'+str(d_pmid['2007'])+'\t'+str(d_pmid['2006'])+'\t'+str(d_pmid['2005'])+'\n')
        else :
            format_out.write('\t'.join(tool_info)+'\t'+str(d_pmid['2018'])+'\t'+str(d_pmid['2017'])+'\t'+str(d_pmid['2016'])+'\t'+str(d_pmid['2015'])+'\t'+str(d_pmid['2014'])+'\t'+str(d_pmid['2013'])+'\t'+str(d_pmid['2012'])+'\t'+str(d_pmid['2011'])+'\t'+str(d_pmid['2010'])+'\t'+str(d_pmid['2009'])+'\t'+str(d_pmid['2008'])+'\t'+str(d_pmid['2007'])+'\t'+str(d_pmid['2006'])+'\t'+str(d_pmid['2005'])+'\n')

#if __name__ == "__main__":
#    parser = argparse.ArgumentParser(description='Format R expression matrix for ChemPSy')
#    parser.add_argument('--file')
#    args = parser.parse_args()
#    getPMIDPubDate(args.file)


#jsonToPMIDcsv()
#getCitation()
trendingInformation('../results/20181126_bttools_citations.txt')


            