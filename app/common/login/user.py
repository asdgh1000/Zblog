from flask_login import UserMixin
from ..mongoDb import user as user_db, community
from ... import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)


class User(UserMixin):
    def __init__(self, user_info):
        self.name = user_info['name']
        self.pwd = user_info['pwd']
        self.user_id = str(user_info['_id'])
        self.committee = {}
        if 'community_id' in user_info:
            self.community_id = str(user_info['community_id'])
            committee_info_ids = community.get_committee_info_id(self.community_id)
            self.committee[1] = str(committee_info_ids['committee_info_id'])
            self.committee[2] = str(committee_info_ids['property_info_id'])
            self.committee[3] = str(committee_info_ids['community_info_id'])
        else:
            self.community_id = None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    @staticmethod
    def get_user_by_id(user_id):
        userInfo = user_db.get_user_by_id(user_id)
        return User(userInfo)
