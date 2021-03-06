from flask_restful import Resource

from backend.Session import auth_required
from backend.mongo import *
from util import args, jsonDict


class LearntCourse(Resource):
    name = 'learnt_course'

    @auth_required
    @args(require=['username'])
    def get(self, username):
        """
        Fetch a user's learnt course.
        :param username: Provided by *auth_required*
        :return: data: [cid] User's learnt course.
        """
        db = db_client[db_name]
        user = db.User.find_one({'username': username})
        if user is not None:
            return jsonDict(True, '', data=user['learnt_course'])
        else:
            return jsonDict(False, '用户不存在')

    @auth_required
    @args('cid', ('cids', list), require=['username'])
    def post(self, username, cids=None, cid=None):
        """
        Add learnt course(s) for certain user.
        :param username: Provided by *auth_required*
        :param cids: Bulker write to add user's learnt course, JSON list
        :param cid: Insert one learnt course, JSON data.
        :return:
        """
        db = db_client[db_name]
        if cids is not None:
            db.User.update({'username': username}, {'$addToSet': {'learnt_course': {'$each': cids}}})
        if cid is not None:
            db.User.update({'username': username}, {'$addToSet': {'learnt_course': cid}})
        if cid is None and cids is None:
            return jsonDict(False, '你至少需要提供一个参数，cid或者cids')
        return jsonDict(True, '添加成功', data=True)

    @auth_required
    @args('cid', ('cids', list), require=['username'])
    def delete(self, username, cids=None, cid=None):
        """
        Remove learnt course(s) for certain user.
        :param username: Provided by *auth_required*
        :param cids: Bulker remove user's learnt course, JSON list
        :param cid: Remove one learnt course, JSON data.
        :return:
        """
        db = db_client[db_name]
        if cids is not None:
            db.User.update({'username': username}, {'$pull': {'learnt_course': {'$in': cids}}})
        if cid is not None:
            db.User.update({'username': username}, {'$pull': {'learnt_course': cid}})
        if cid is None and cids is None:
            return jsonDict(False, '你至少需要提供一个参数，cid或者cids')
        return jsonDict(True, '删除成功', data=False)
