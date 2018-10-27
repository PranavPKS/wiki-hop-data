# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import wikipedia
import pandas as pd
from bs4 import BeautifulSoup as bs
import re
import glob
import pickle

# =============================================================================
# dis_links = wikipedia.page("Wikipedia:Links to (disambiguation) pages/A-K").links + wikipedia.page("Wikipedia:Links to (disambiguation) pages/L-Z").links
# 
# print(len(dis_links))
# 
# linkss = bs(wikipedia.page("Wikipedia:Links to (disambiguation) pages/A-K").html(),"lxml").findAll("a", href=re.compile("^(/wiki/)+([A-Za-z0-9_:()])+")) + bs(wikipedia.page("Wikipedia:Links to (disambiguation) pages/L-Z").html(),"lxml").findAll("a", href=re.compile("^(/wiki/)+([A-Za-z0-9_:()])+"))
# 
# print(len(linkss))
# 
# ord_unfil_links=[]
# for link in linkss:
#     try:
#         ord_unfil_links.append(link['title'])
#     except:
#         continue
#     
# all_page_titles = [x for x in ord_unfil_links if x in dis_links]
# 
# print(len(all_page_titles))
# 
# 
# 
# i=0
# for title in all_page_titles:
#     i=i+1
#     if i%1000==0:
#         print(" ",i, end="", flush=True)
#     if title in all_files:
#         continue
#     try:
#         curr_page = wikipedia.page(title)
#         unfil_tags = bs(curr_page.html(),"lxml").findAll("a", href=re.compile("^(/wiki/)+([A-Za-z0-9_:()])+"))
#     
#         ord_unfil_links_inner = []
#         for tag in unfil_tags:
#             try:
#                 ord_unfil_links_inner.append(tag['title'])
#             except:
#                 continue
#         temp_links = curr_page.links
# 
#         with open("link_texts/"+title+".txt",'w') as fo:
#             temp = "\n".join([x for x in ord_unfil_links_inner if x in temp_links])
#             fo.write(temp)
#             #print(all_titles[title])
#     except:
#         continue
# 
# =============================================================================
all_files = sorted([x[11:].replace(".txt","") for x in glob.glob("link_texts/*")])
    
all_titles={}
for title in all_files:
    with open("link_texts/"+title+".txt",'r') as fo:
        all_titles[title]=[]
        for line in fo:
            all_titles[title].append(line.strip())    
    

def get_para(word,listt):
    for para in listt:
        if word.lower() in para.lower():
            return get_para(word,para.split("\n\n")) if "\n\n" in para else para
    return -1
        
print("started\n")        
page_links_paras=[]
i=0
for title in all_titles:
    page_name = title.replace(' (disambiguation)','')
    i=i+1
    if i%100==0:
        print(" ",i, end="", flush=True)
    if i%1000==0:
        print("\n")
    for phrase in all_titles[title]:
        try:
            page_blocks = wikipedia.page(phrase).content.split("\n\n\n")
            url = wikipedia.page(phrase).url
            para = get_para(page_name,page_blocks)
            if para != -1:
                ind = para.lower().find(page_name.lower())
                span = str(ind)+"-"+str(ind+len(page_name))
                page_links_paras.append([page_name,phrase,url,para,span])
                with open("disambi.pkl",'wb') as fi:
                    pickle.dump(page_links_paras,fi)
            
        except:
            continue
        
print("\nDone!")
