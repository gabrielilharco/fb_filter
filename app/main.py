#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
import textrazor
import logging

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

    def post(self):
        try:
            self.response.headers['Content-Type'] = 'application/json'
            text_content = self.request.get('text_content') 
            n = int(self.request.get('size'))
            key_words = []
            for i in range (0,n):
                key_words.append(self.request.get(str(i)))
                #self.response.out.write(json.dumps({str(i):self.request.get(str(i))}))
            if text_content == "":
                self.response.out.write(json.dumps({"filtered" : "0"}))
                return
            #self.response.write(json.dumps({"post_id" : text_content}))  
            api_key = "f066781151a86f4a224a406a9a9d3aef5ea4096acae149ffd4beab02"
            score_min = 0.7
            block = False
            
            #key_words = ["Manga" ,"Soccer", "Sports", "Game of Thrones (TV series)", "Episode", "A Song of Ice and Fire", "Regulation", "Banks", "Macaco"]

            from textrazor import TextRazor
            client = TextRazor(api_key="f066781151a86f4a224a406a9a9d3aef5ea4096acae149ffd4beab02", extractors=["topics"])

            client.set_do_cleanup_HTML(False)
            response = client.analyze(text_content)


            if response.topics() != None:
                    entities = response.topics()
                    #entities.sort(key=lambda x: x.score, reverse=True)
                    seen = set()
                    #print("Words with high score:")
                    if entities != None:
                        try:
                            #print (type(entities))
                            for entity in entities:
                                if entity.id not in seen:
                                    for word in key_words:
                                        if entity.label.lower() in word.lower() and entity.score >= score_min:
                                            #print entity.label, entity.score
                                            block = True
                                    seen.add(entity.id)
                                #pass
                        except Exception:
                            pass

            if (block):
                ft = "1"
            else:
                ft = "0"
            self.response.out.write(json.dumps({"filtered" : ft}))
        except Exception:
            self.response.out.write(json.dumps({"filtered" : "0"}))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
