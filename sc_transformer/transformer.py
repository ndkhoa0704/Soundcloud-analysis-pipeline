from .transformer.transformer import Transformer

class SoundCloud_Transformer(Transformer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def _transform_user(self):
        pass

    def _transform_tracks(self):
        pass

    def _transform_playlists(self):
        pass
    
    def transform(self):
        pass