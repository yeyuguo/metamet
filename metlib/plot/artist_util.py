__all__ = ['ArtistIDManager']

class ArtistIDManager(object):
    def __init__(self):
        self.artist2ID = dict()
        self.ID2artist = dict()
        self.nowID = 1

    def isID(self, key):
        return isinstance(key, (int, long, np.integer))

    def get_new_ID(self):
        res = self.nowID
        self.nowID += 1
        return res

    def __getitem__(self, key):
        if self.isID(key):
            return self.ID2artist[key]
        else:
            return self.artist2ID[key]

    def __setitem__(self, key, value):
        if self.isID(key):
            if key in self.ID2artist:
                self.ID2artist[key].append(value)
            else:
                self.ID2artist[key] = [value]
            self.artist2ID[value] = key
            if key >= self.nowID:
                self.nowID = key + 1
        else:
            self.__setitem__(value, key)

    def __delitem__(self, key):
        if not self.isID(key):
            if key not in self.artist2ID:
                return
            key = self.artist2ID[key]
        for artist in self.ID2artist[key]:
            artist.remove()
            del self.artist2ID[artist]
        del self.ID2artist[key]

    def __contains__(self, key):
        return key in self.artist2ID or key in self.ID2artist

    def clear(self):
        self.artist2ID.clear()
        self.ID2artist.clear()
        self.nowID = 1

