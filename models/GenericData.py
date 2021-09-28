from models.base import session
from models.warning_config import Warning_config


class GenericData():

    def get_cnt_warning_config(self, guild_id):
        return session.query(Warning_config).filter(Warning_config.guild_id==guild_id).count()

if __name__ == '__main__':
    print('"Hello World')
    generic  = GenericData()
    print(generic.get_cnt_warning_config(276918614999695362))
