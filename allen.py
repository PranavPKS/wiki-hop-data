from allennlp.predictors.coref import CorefPredictor
from allennlp.predictors.predictor import Predictor
import numpy as np

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


p1 = coref()
document = "Cuevas de San Marcos is a town and municipality in the province of Málaga, part of the autonomous community of Andalusia in southern Spain. The municipality is situated in the northern part of the Antequera region, on the border of the province of Córdoba from the river valley of Genil to the Sierra Malnombre and Camorro de Cuevas Altas. It is also located within the comarca of Nororma. It borders the provinces of Granada and Cordoba to the north, the comarcs of La Axarquía to the south and Antequera to the west. The town is situated at an altitude of 420 meters above sea level. By road Cuevas de San Marcos is located 88 kilometers from Málaga and 487 km from Madrid. It is a farming village, with a predominance of olive growing and oil production of the 'Hojiblanca' variety. Its name comes from its patron saint, Mark the Evangelist, and its famous Cave of Belda. Cuevas de San Marcos has a population of approximately 4,000 residents. It covers an area of about 37.50 km2. The natives are called Cuevachos."
print(p1.resolve(document))

#p2 = ner()
#document2 = "AllenNLP is a PyTorch-based natural language processing library developed at the Allen Institute for Artificial Intelligence in Seattle."
#result = p2.predict(document2)