#from allen import coref, ner
import MySQLdb
import re

class relev_data:

    def __init__(self):
        self.db = MySQLdb.connect(host="",  # your host
                             user="",  # username
                             passwd="",  # password
                             db="wiki_db", charset='utf8', use_unicode=True)  # name of the database
    
    
    def possible_disambiguation_pages(self, spaced_title):
        '''
        Get the possible titles from the database that might be the page for given title.
        Look from the disambiguation pages and try to find all
        :param title: string
        :return: [disamguation_page_id, full_text_score, page_name, num_inlinks, num_views]
        '''
        #spaced_title = normalizeTitle(title)
        spaced_title_boolean = " ".join(['+{}'.format(w.strip()) for w in spaced_title.split()])
        query = '''
        select distinct c.dis_page, c.score, c.outlink, c.num_inlinks, views from
            (select * from 
                (select * from  
                    (select pages, Page.name as dis_page, match(spaced_title) against ("%s") as score from 
                        category_pages, Page where category_pages.id = 19205681 and 
                        match(spaced_title) against ("%s" in boolean mode) and 
                        pageId = pages
                    ) a, links where a.pages = inlink
                ) b, inlink_count where b.outlink = inlink_count.name) c, page_views
                where c.outlink = page_views.name order by c.num_inlinks desc;
        ''' %(spaced_title, spaced_title_boolean)
        return self.fetch_all(query)
    
    def possible_disambiguation_pages_simple(self, spaced_title):
        #spaced_title = normalizeTitle(title)
        spaced_title_boolean = " ".join(['+{}'.format(w.strip()) for w in spaced_title.split()])
        query = '''
                select name, match(spaced_title) against ("%s") as score from Page
                where match(spaced_title) against ("%s" in boolean mode) 
                order by score desc;
                ''' % (spaced_title, spaced_title_boolean)
        return self.fetch_all(query)
    
    def fetch_one(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row
    
    def fetch_all(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    

html_eg = """<p> <a href="https://en.wikipedia.org/wiki/Anthony_Endrey" title="Anthony Endrey">  Anthony Endrey</a> was a <a href="https://en.wikipedia.org/wiki/Hungarian" title="Hungarian">  Hungarian</a> - <a href="https://en.wikipedia.org/wiki/Australia" title="Australia">  Australian</a> lawyer and author . He was a Queen 's Counsel and Master of <a href="https://en.wikipedia.org/wiki/Supreme_court" title="Supreme court">  the Supreme Court</a> in <a href="https://en.wikipedia.org/wiki/Victoria" title="Victoria">  Victoria</a> , <a href="https://en.wikipedia.org/wiki/Australia" title="Australia">  Australia</a> , and a member of <a href="https://en.wikipedia.org/wiki/Victorian_Bar" title="Victorian Bar">  the Victorian Bar</a> . <a href="https://en.wikipedia.org/wiki/Anthony_Endrey" title="Anthony Endrey">  Endrey</a> was born in <a href="https://en.wikipedia.org/wiki/Hungary" title="Hungary">  Hungary</a> , and graduated Doctor of Law from <a href="https://en.wikipedia.org/wiki/Corvinus_University_of_Budapest" title="Corvinus University of Budapest">  the University of Budapest</a> . He was a research assistant at <a href="https://en.wikipedia.org/wiki/Anthony_Endrey" title="Anthony Endrey">  Friedricks - Wilhelm University</a> in <a href="https://en.wikipedia.org/wiki/Berlin" title="Berlin">  Berlin</a> . He served in <a href="https://en.wikipedia.org/wiki/Royal_Hungarian_Army" title="Royal Hungarian Army">  the Royal Hungarian Army</a> during <a href="https://en.wikipedia.org/wiki/World_War_II" title="World War II">  World War II</a> , and was a prisoner of war in <a href="https://en.wikipedia.org/wiki/Soviet_Union" title="Soviet Union">  the Soviet Union</a> until his release in <a href="https://en.wikipedia.org/wiki/1945" title="1945">  1945</a> . He emigrated to <a href="https://en.wikipedia.org/wiki/Australia" title="Australia">  Australia</a> in <a href="https://en.wikipedia.org/wiki/1949" title="1949">  1949</a> , and in order to practice in <a href="https://en.wikipedia.org/wiki/Australia" title="Australia">  Australia</a> he studied law at <a href="https://en.wikipedia.org/wiki/University_of_Tasmania" title="University of Tasmania">  the University of Tasmania</a> .</p>"""
search_res = re.findall(r"<a href=\"[A-Za-z.:/0-9_]+\" title=\"[A-Za-z0-9 ]*\">([A-Za-z0-9 ]*)</a>",html_eg)

test = relev_data()

#res = test.possible_disambiguation_pages('Hungarian')
#outs = [x[2] for x in res]

count, res_count, cor_count = 0,0,0
with open("entity_names.txt",'r') as fo:
    for line in fo:
        entity = line.strip().replace('_',' ')
        count += 1
        res = test.possible_disambiguation_pages_simple(entity)
        if res:
            res_count += 1
            if len(res)>15:
                res = res[:15]
            #print(entity)
            outs = [x[0] for x in res]
            for pred in outs:
                if entity.lower() in pred.lower():
                    #print(entity.lower(),"-----",pred.lower())
                    cor_count += 1
                    break
        if count%500 == 0:
            print(count, res_count, cor_count)
            
            