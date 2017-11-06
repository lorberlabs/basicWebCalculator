#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

    def post(self):
        rezultat = self.request.get("vnos")
        params = {"ime": rezultat}
        return self.render_template("hello.html", params=params)


class CalculatorHandler(BaseHandler):
    def get(self):
        return self.render_template("calculator.html")

    def post(self):
        prva = float(self.request.get("prva"))
        operacija = self.request.get("operacija")
        druga = float(self.request.get("druga"))
        rezultat = 0

        if operacija == "+":
            rezultat = prva + druga
        elif operacija == "-":
            rezultat = prva - druga
        elif operacija == "*":
            rezultat = prva * druga
        elif operacija == "/":
            rezultat = prva / druga

        params = {"rezultat": rezultat}
        return self.render_template("calculator.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/Kalkulator', CalculatorHandler)
], debug=True)
