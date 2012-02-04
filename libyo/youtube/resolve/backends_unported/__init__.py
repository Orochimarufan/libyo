from abc import abstractmethod

class BackendFailedException(Exception):
    def __init__(self,exc=None):
        self.exc=exc
        super().__init__()

class AbstractBackend(object):
    def setup(self,video_id):
        self.video_id=video_id
    def resolve(self,video_id=None):
        if video_id is not None:
            self.setup(video_id)
        try:
            return self._resolve()
        except BackendFailedException as e:
            print(str(e.exc))
            return False
    @abstractmethod
    def _resolve(self):
        raise NotImplementedError()