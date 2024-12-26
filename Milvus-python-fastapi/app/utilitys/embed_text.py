"""
Class About Embeding data
"""

from sentence_transformers import SentenceTransformer

class Embeded:
    """
    Class empbed dagta
    """
    def embeded_text_by_lm(self, text, model_name="all-MiniLM-L6-v2"):
        """
        embeded_text
            embebding text to array float

        Args:
            text(str) : text for embed
            model_name (str) : model from embed default 'all-MiniLM-L6-v2'

            list of model_name can use
                all-MiniLM-L6-v2
                ll-MiniLM-L12-v2
                paraphrase-multilingual-MiniLM-L12-v2
                multi-qa-MiniLM-L6-cos-v1
        
        retrun : vector (array float)
        """

        model = SentenceTransformer(model_name)
        vector = model.encode(text).tolist()
        return vector
