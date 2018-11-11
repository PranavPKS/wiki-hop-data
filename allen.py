from allennlp.predictors.coref import CorefPredictor
from allennlp.predictors.predictor import Predictor
import numpy as np
import wikipedia

class coref:
    
    def __init__(self):
        self.predictor = CorefPredictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/coref-model-2018.02.05.tar.gz")
    
    def predict(self,document):
        return self.predictor.predict(document)
    
    def resolve(self,document):

        result = self.predict(document)        
        doc = result['document']
        clusters = result["clusters"]
        
        doc_dict={}
        for i in range(len(doc)):
            doc_dict[i] = doc[i]
        indices = []
        for i in range(len(clusters)):
            indices.append(clusters[i][0][1] - clusters[i][0][0])
        
        sort_indices = np.argsort(np.array(indices))
        
        for j in sort_indices:
            phrase = ' '.join(doc[clusters[j][0][0]:clusters[j][0][1]+1])
            for mention in clusters[j]:
                for i in range(mention[0],mention[1]+1):
                    doc_dict[i] = ''
                doc_dict[mention[0]] = phrase
            
        reg_doc=''
        for i in range(len(doc)):
            if doc_dict[i] != '':
                if doc_dict[i] in ['.',',']:
                    reg_doc = reg_doc + doc_dict[i]
                else:
                    reg_doc = reg_doc + ' ' + doc_dict[i]

        return reg_doc
        
class ner:
    
    def __init__(self):
        self.predictor = Predictor.from_path('https://s3-us-west-2.amazonaws.com/allennlp/models/fine-grained-ner-model-elmo-2018.08.31.tar.gz')
    
    def predict(self,document):
        return self.predictor.predict(document)

    def wikify(self,document):
        
        result = self.predict(document)        
        tags = result['tags']
        words = result['words']
        
        proc,temp_str ='<p>',''
        for i in range(len(words)):
            if tags[i]=='O':
                if temp_str:
                    title = wikipedia.search(temp_str)[0]
                    anchor = "<a href=\"" + wikipedia.page(title).url +"\" title=\""+title+"\"> " + temp_str + "</a>"
                    proc = proc + ' ' + anchor
                    temp_str = ''
                proc = proc + ' ' + words[i]
            else:
                temp_str = temp_str + ' ' + words[i]
            
        if temp_str:
            ne_coll.append(temp_str)
            proc = proc + ' ' + temp_str
            temp_str = ''
        proc = proc + "</p>"
        return proc        

p1 = coref()
document = "Cuevas de San Marcos is a town and municipality in the province of Málaga, part of the autonomous community of Andalusia in southern Spain. The municipality is situated in the northern part of the Antequera region, on the border of the province of Córdoba from the river valley of Genil to the Sierra Malnombre and Camorro de Cuevas Altas. It is also located within the comarca of Nororma. It borders the provinces of Granada and Cordoba to the north, the comarcs of La Axarquía to the south and Antequera to the west. The town is situated at an altitude of 420 meters above sea level. By road Cuevas de San Marcos is located 88 kilometers from Málaga and 487 km from Madrid. It is a farming village, with a predominance of olive growing and oil production of the 'Hojiblanca' variety. Its name comes from its patron saint, Mark the Evangelist, and its famous Cave of Belda. Cuevas de San Marcos has a population of approximately 4,000 residents. It covers an area of about 37.50 km2. The natives are called Cuevachos."
print(p1.resolve(document))

p2 = ner()
document2 = "Anthony Endrey was a Hungarian-Australian lawyer and author. He was a Queen's Counsel and Master of the Supreme Court in Victoria, Australia, and a member of the Victorian Bar. Endrey was born in Hungary, and graduated Doctor of Law from the University of Budapest. He was a research assistant at Friedricks-Wilhelm University in Berlin. He served in the Royal Hungarian Army during World War II, and was a prisoner of war in the Soviet Union until his release in 1945. He emigrated to Australia in 1949, and in order to practice in Australia he studied law at the University of Tasmania."
print(p2.wikify(document2))


    