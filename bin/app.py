import web
import json
from scrap import Scrap

urls = (
  '/', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('templates/', base="layout")

class Index(object):
    def GET(self):
        return render.search()

    def POST(self):
        form = web.input(name="search", greet="Hello")
        dataJson = Scrap("%s" % (form.search)) 
        ##greeting = json.dumps(dataJson.getResponse(), indent=4, sort_keys=True)
        greeting = dataJson.getResponse()
        return render.index(greeting = greeting)

if __name__ == "__main__":
    app.run()