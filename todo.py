import sqlite3
from bottle import route, run, template, debug, request, static_file, redirect,get,post
import pandas as pd
import numpy as np
#from pandas.core import format
from bs4 import BeautifulSoup
#from jinja2 import Environment, FileSystemLoader
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename,root="./static")

@route('/')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    return template('make_template', rows = result)


@route('/new', method='GET')
def add_task():
	return template('new_task.tpl')

@route('/new', method='POST')
def new_item():
    new = request.POST.get('task', '').strip()
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new,1))
    new_id = c.lastrowid
    conn.commit()
    c.close()
    return '<p>The new task was inserted into the database, the ID is %s </p>' % new_id 


@route('/report', method='GET')
def report_new():
    df = pd.read_csv(r'C:\Users\Saurabh\Downloads\12zpallagi.csv')
    sales_report = pd.pivot_table(df, index=["STATE", "zipcode"], values=["PREP", "N2"],aggfunc=[np.sum, np.mean], fill_value=0)                       
    shortrep = sales_report.head()
    inter = shortrep.to_html()
#    soup = BeautifulSoup(inter)
#    final = soup.table
#    final = format.HTMLFormatter(shortrep)                   
#    return template('report', report = final)
#    return inter
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("myreport.html")
    template_vars = {"title" : "Sales Funnel Report - National",
                 "national_pivot_table": inter}
    # Render our file and create the PDF using our css style file
    return template.render(template_vars)
    
@route('/graph', method='GET')
def report_new():
    df = pd.read_csv(r'C:\Users\Saurabh\Downloads\12zpallagi.csv')
    sales_report = pd.pivot_table(df, index=["STATE", "zipcode"], values=["PREP", "N2"],aggfunc=[np.sum, np.mean], fill_value=0)                       
    shortrep = sales_report.head()
    fig = plt.plot(shortrep)   
    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.title('Histogram of IQ')
    plt.grid(True)
    plt.savefig('graph.jpg')
    #a = fig.savefig('graph.jpg')
#    a = fig.savefig('graph.jpg')
    redirect('/report')

@route('/table', method='GET')
def table():
#    df = pd.read_csv(r'C:\Users\Saurabh\Downloads\12zpallagi.csv')
#    sales_report = pd.pivot_table(df, index=["STATE", "zipcode"], values=["PREP", "N2"],aggfunc=[np.sum, np.mean], fill_value=0)                       
#    shortrep = sales_report.head()
#    inter = shortrep.to_html()
#    soup = BeautifulSoup(inter)
#    final = soup.table
#    final = format.HTMLFormatter(shortrep)                   
#    return template('report', report = final)
#    return inter
    inter = ' '
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("table.html")
    template_vars = {"title" : "Sales Funnel Report - National",
                 "national_pivot_table": "hello"}
    # Render our file and create the PDF using our css style file
    return template.render(template_vars)



@route('/picture', method='POST')
def picture():
    inter = request.json['car']
#    for k,v in inter:
#        print k,v
    print inter    
    if inter == 'saab':
        return "<h1> Saurabh you </h1>"
    return "<h1> Hi how are you </h1>"

debug(True)
run(reloader=True)

