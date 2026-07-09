import os
import pickle
import warnings
# Suppress sklearn unpickling version warnings if installed
try:
    from sklearn.exceptions import InconsistentVersionWarning
    warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
except ImportError:
    pass
warnings.filterwarnings("ignore", category=UserWarning)

class AyurMLModelLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AyurMLModelLoader, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if self._initialized:
            return
            
        self.vectorizer = None
        self.tfidf_matrix = None
        self.chunks = []
        
        # Resolve absolute path to the model file in the root workspace directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'ayurveda_model.pkl'))
        
        self._load_model()
        self._initialized = True
        
    def _load_model(self):
        """Loads the pickled TF-IDF vectorizer, matrix, and chunks"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.vectorizer = data.get('vectorizer')
                    self.tfidf_matrix = data.get('tfidf_matrix')
                    self.chunks = data.get('chunks', [])
                print(f"[OK] CCRAS ML Model loaded successfully from {self.model_path} (Chunks: {len(self.chunks)})")
            except Exception as e:
                print(f"[ERROR] Failed to load CCRAS ML Model: {str(e)}")
        else:
            print(f"[WARN] CCRAS ML Model not found at path: {self.model_path}")
            
    def get_model_data(self):
        return {
            'vectorizer': self.vectorizer,
            'tfidf_matrix': self.tfidf_matrix,
            'chunks': self.chunks
        }
