import time, uuid
from datetime import datetime
from . import db


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)



class Follow(db.Model):
    __tablename__ = 'follows'

    # 记录关注者的id, 关注的id 和 关注的时间
    follower_id = db.Column(db.String(50), db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.String(50), db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    '''
        博客的登录用户类
    '''
    __tablename__ = 'users'

    # 基本信息
    id = db.Column(db.String(50), primary_key=True, default=next_id)
    name = db.Column(db.String(32), unique=True)
    username = db.Column(db.String(32))
    sex = db.Column(db.String(6))
    user_image = db.Column(db.String(128))
    about_me = db.Column(db.Text)
    created_at = db.Column(db.DateTime, index=True)

    # 其他状态信息
    status = db.Column(db.String(8), index=True)

    # 关联信息
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    classifytags = db.relationship('ClassifyTag', backref='user', lazy='dynamic')
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User name:%r>' % self.name


class Role(db.Model):
    '''
    博客的登录角色类
    '''
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    permission = db.Column(db.Integer, default=0)

    # 关联信息
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role name:%r>' % self.name


class ClassifyTag(db.Model):
    '''
    博客文章的分类标签
    '''
    ___tablename__ = 'classifytags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    # 关联信息
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'))


ClassifyTagRegistration = db.Table('classifytagregistration',
                                   db.Column('post_id', db.String(50), db.ForeignKey('posts.id')),
                                   db.Column('tag_id', db.Integer, db.ForeignKey(ClassifyTag.id)))


class Post(db.Model):
    '''
    博客的文章类
    '''
    __tablename__ = 'posts'

    id = db.Column(db.String(50), primary_key=True, default=next_id)
    title = db.Column(db.String(64), unique=True)
    type = db.Column(db.String(8))
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    status = db.Column(db.String(8))

    # 关联信息
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'))
    articletags = db.relationship('ArticleTag', backref='post', lazy='dynamic')
    classifytags = db.relationship('ClassifyTag', secondary=ClassifyTagRegistration,
                                   backref=db.backref('posts', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Role title:%r>' % self.title


class Comment(db.Model):
    '''
    博客的评论类
    '''
    __tablename__ = 'comments'

    id = db.Column(db.String(50), primary_key=True, default=next_id)
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    floor = db.Column(db.Integer)
    ref_id = db.Column(db.String(50), index=True, default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(8))

    # 关联信息
    author_id = db.Column(db.String(50), db.ForeignKey('users.id'))
    post_id = db.Column(db.String(50), db.ForeignKey("posts.id"))

    def __repr__(self):
        return '<Comment id:%r>' % self.id



class ArticleTag(db.Model):
    '''
    博客文章的文章标签
    '''
    __tablename__ = 'articletags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    # 关联信息
    post_id = db.Column(db.String(50), db.ForeignKey('posts.id'))


# class ExternalUser(db.Model):
#     '''
#     博客的外部用户类 如微博 QQ等
#     '''
#     pass
