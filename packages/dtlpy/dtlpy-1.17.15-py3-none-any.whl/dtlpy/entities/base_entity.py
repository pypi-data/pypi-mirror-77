from .. import miscellaneous


class BaseEntity(object):
    is_fetched = True

    def print(self, to_return=False):
        return miscellaneous.List([self]).print(to_return=to_return)

    def to_df(self, show_all=False):
        return miscellaneous.List([self]).to_df(show_all=show_all)

    # def __getattribute__(self, attr):
    #     if super(BaseEntity, self).__getattribute__(attr) is None:
    #         pass
    #     return super(BaseEntity, self).__getattribute__(attr)
