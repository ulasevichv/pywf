class Dict(dict):
    def __init__(self, seq=None, **kwargs):
        # if seq is not None and isinstance(seq, dict):
        #     # Log.info(seq.__class__.__name__)
        #     # Log.info(seq)
        #     for key, value in seq.items():
        #
        #         # Log.info(key + ': ' + str(value))
        #         self[key] = value

        if seq is None:
            super().__init__()
        else:
            super().__init__(seq, **kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as ex:
            raise AttributeError(ex)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as ex:
            raise AttributeError(ex)

    def __repr__(self):
        feed = []
        for attributeName in self.keys():
            feed.append(attributeName + ': ' + str(self.__getattr__(attributeName)))
        return '<Dict>:' + "\n\t" + "\n\t".join(feed)
