

class File:
    @classmethod
    def read(self, path, mode = 'r'): 
        with open(path, mode) as blob:
            content = blob.read()
        return content