import cgi
import urllib
import json
import datetime
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2


# def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
#     """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
#     return ndb.Key('Guestbook', guestbook_name)




def check_ward (user_id, post_id) :
    lis = ndb.gql ("SELECT * FROM Ward WHERE userid = '%(user_id)s' AND postid = '%(post_id)s'"%{"user_id": user_id, "post_id" : post_id})
    lis = list(lis)
    if not lis:
        return False
    return True

def timedelta_to_microtime(tempo):
    td = tempo - datetime.datetime(2014, 5, 2, 10, 20, 0, 0)
    return td.microseconds + (td.seconds + td.days * 86400) * 1000000

class Ward(ndb.Model):
    userid = ndb.StringProperty(required=True)
    postid = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'Hello' : 'World'}))


class SearchAPI(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'  
        # console.log('Search Api')
        user_id = self.request.get('user_id')
        post_id = self.request.get('post_id')

        if not user_id or not post_id:
            # console.log("Null Atributes")
            return

        if check_ward(user_id, post_id):
            self.response.write(json.dumps({'status' : 'true', 'post_id' : post_id}))
        else:
            self.response.write(json.dumps({'status' : 'false', 'post_id' : post_id}))

    def get(self):
        self.error(405)

class InsertAPI(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'  
        # console.log('Insert Api ')
        user_id = self.request.get('user_id')
        post_id = self.request.get('post_id')

        # Check null atributes
        if not user_id or not post_id:
            # console.log("Null Atributes")
            return

        if not check_ward(user_id, post_id):
            ward = Ward(userid = user_id, postid = post_id)
            ward.put()
            # console.log("Post inserted")
        # else:
            # console.log("Post already exists")

        self.response.write(json.dumps({"post_id" : post_id}))


    def get(self):
        self.error(405)


class QueryAPI(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        user_id = self.request.get('user_id')

        # Check null atributes
        if not user_id:
            # console.log("Null Atributes")
            return

        warded_posts = ndb.gql("SELECT * FROM Ward WHERE userid = '%(user_id)s'"%{"user_id": user_id})

        warded_postsID = [{'post_id': w.postid, 'time': timedelta_to_microtime(w.date) } for w in warded_posts]

        self.response.write(json.dumps(warded_postsID))

    def get(self):
        self.error(405)

class DeleteAPI(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'  
        # console.log('Delete Api ')
        user_id = self.request.get('user_id')
        post_id = self.request.get('post_id')

        # To DO
        # Check null atributes
        if not user_id or not post_id:
            self.response.write(json.dumps({"post_id" : post_id}))
            # console.log("Null Atributes")
            return

        wards = ndb.gql("SELECT * FROM Ward WHERE userid = '%(user_id)s' and postid = '%(post_id)s'" %{ "user_id" : user_id,
                                                                                                        "post_id" : post_id})
        # To Do
        if list(wards):
            for w in wards:
                w.key.delete()
                # console.log("Post deleted")
        # else:
            # console.log("Post not found")

        #Pensar no caso de deletar usuarios
        self.response.write(json.dumps({"post_id" : post_id}))

        
        # self.redirect('/')
    def get(self):
        self.error(405)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/search', SearchAPI),
    ('/insert', InsertAPI),
    ('/delete', DeleteAPI), 
    ('/query', QueryAPI)
], debug=True)
