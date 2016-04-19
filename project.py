# -*- coding: utf-8 -*-
"""
Created on Tue Feb 09 15:29:28 2016

@author: Saurabh
"""

from bottle import route, run, template, debug, request, static_file, redirect,get,post, auth_basic
import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from pivottablejs import pivot_ui

env = Environment(loader=FileSystemLoader('.'))
store = pd.HDFStore(r'C:\Users\Saurabh\OneDrive\Data science\project\data\store.h5')        
dfcanada = store['canada']
dfwestern = store['western']
dfoptions = store['options']
dfquestions = store['questions']
#data = pd.read_csv(r'C:\Users\Saurabh\OneDrive\Data science\project\data\NCHA-II SPRING 2013 CANADIAN REFERENCE GROUP-1R-BLIND-VERSAEVEL.csv')
#df = pd.DataFrame(data)
#df = df.convert_objects(convert_numeric=True)
#data = pd.read_csv(r'C:\Users\Saurabh\OneDrive\Data science\project\data\NCHA-II WEB SPRING 2013 WESTERN UNIVERSITY-1.csv')
#df1 = pd.DataFrame(data)
#df1 = df1.convert_objects(convert_numeric=True)


def filloptions(column,df):
    if column in dfoptions:
        df1 = df
        df1.index = dfoptions[column].dropna()
        df1.columns = ['Total Count']
        return df1
    else:
        df1 = df
        return df1

         

def check(username, password):
    if username == 'admin' and password == 'secret':
        return True
    else:
        return False
            
        
def decision_tree():
    features = df[["NQ47","NQ51","NQ55","NQ63","NQ37","NQ30G","NQ30F","NQ30J","NQ8A5"]]
    dfna = df.NQ45A1
    targetvariable = dfna    
    featureTrain, featureTest,targetTrain,targetTest =  train_test_split(features,targetvariable,test_size=.2)
    model = DecisionTreeClassifier(min_samples_leaf=50,min_samples_split=100)    
    fittedModel = model.fit(featureTrain,targetTrain)
    print confusion_matrix(targetTest,predictions)
    print accuracy_score(targetTest,predictions)
    return fittedModel

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename,root="./static")



@route('/')
@auth_basic(check)
def home():
    redirect ('/login')
    
    
@route('/login', method='GET')
@auth_basic(check)
def report_new():
    template = env.get_template("intro.html")
    template_vars = {"title" : "Sales Funnel Report - National",
                 "national_pivot_table": "hello"}
    return template.render(template_vars)
    
@route('/report', method='POST')
@auth_basic(check)
def report_new():
    column = request.forms.get('column')
    print column
    df1 = dfcanada[1:50]    
#    fig = plt.plot(df1)   
#    plt.xlabel('Choices')
#    plt.ylabel('Total counts')
#    plt.title('Line chart for total count')
#    plt.grid(True)
#    plt.savefig('graph.jpg')
    df1 = df1.to_html()
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("table.html")
    template_vars = {"title" : "NCHA data",
                 "national_pivot_table": df1}
    return template.render(template_vars)


@route('/table', method='GET')
@auth_basic(check)
def table():
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("table.html")
    template_vars = {"title" : "NCHA DATA",
                 "national_pivot_table": ""}
    # Render our file and create the PDF using our css style file
    return template.render(template_vars)


@route('/graph', method='GET')
@auth_basic(check)
def table():
    column = request.forms.get('column')
    x= pd.DataFrame(df.NQ30J.value_counts(sort=False)).to_html()
    y = pd.DataFrame(df.NQ31B2.value_counts(sort=False)).to_html()
    z = pd.DataFrame(df.NQ31A2.value_counts(sort=False)).to_html()
    a = pd.DataFrame(df.NQ31A6.value_counts(sort=False)).to_html()
    if column :        
        x = df.NQ8A5
        y = df.NQ45A1
        df1 = pd.DataFrame({'alcoholA5' : x, 'alcohol45A1' : y})
        df1 = df1.convert_objects(convert_numeric=True)
    #    fig = plt.plot(df1)  
        fig = df1.plot(kind='kde')
        ax = fig.get_figure()
        ax.savefig('static/graph.jpg')
#    plt.xlabel('Choices')
#    plt.ylabel('Total counts')
#    plt.title('Density chart for total count')
#    plt.grid(True)    
#    plt.savefig('static/graph.jpg')    
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("graph.html")
    template_vars = {"title" : "NCHA DATA",
                 "national_pivot_table": "","suicide":x,"anxiety":y,"depression":z,"panic":a}
    # Render our file and create the PDF using our css style file
    return template.render(template_vars)

@route('/create', method='GET')
@auth_basic(check)
def table():
    navigation = dfcanada.columns
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("create.html")
    template_vars = {"title" : "NCHA DATA",
                 "navigation": navigation}
    # Render our file and create the PDF using our css style file
    return template.render(template_vars)

@route('/create', method='POST')
def table():
    column = request.forms.get('columnname')
    data = request.forms.get('optradio')
    if data == 'western':
        df2 = dfwestern
    else:
        df2 = dfcanada
    a = df2[column].value_counts(sort=False)
    a = pd.DataFrame(a)
    a = filloptions(column,a)            
    fig = a.plot(kind='bar')
    ax = fig.get_figure()
    ax.savefig('static/graph1.jpg',bbox_inches='tight')
    plt.clf()
    b = pd.DataFrame(a).to_html()
    c = df2[df2['NQ51']<6][column].value_counts(sort=False)
    c = pd.DataFrame(c)
    c = filloptions(column,c)  
    fig = c.plot(kind='bar')
    ax = fig.get_figure()
    ax.savefig('static/undergraduate.jpg',bbox_inches='tight')
    plt.clf()
    d = pd.DataFrame(c).to_html()
    e = df2[df2['NQ51']>5][column].value_counts(sort=False)
    e = pd.DataFrame(e)
    e = filloptions(column,e)  
    fig = e.plot(kind='bar')
    ax = fig.get_figure()
    ax.savefig('static/graduate.jpg',bbox_inches='tight')
    plt.clf()
    f = pd.DataFrame(e).to_html() 
    if column in dfquestions:
        question = dfquestions[column]
    else:
        question = ['no match']
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("create_post.html")
    template_vars = {"title" : question[0],
                 "national_pivot_table": b,"undergraduate" : d ,"graduate" : f}
    # Render our file and create the PDF using our css style file
    return template.render(template_vars)


@route('/predict', method='GET')
@auth_basic(check)
def table():    
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("predict.html")
    template_vars = {"title" : "NCHA DATA"
                 }
    # Render our file and create the PDF using our css style file
    return template.render(template_vars)


@route('/predictpost', method='POST')
def predict_post():
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("predict_post.html")
    template_vars = {}    
    return template.render(template_vars)


@route('/pivot', method='GET')
@auth_basic(check)
def pivot():
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("pivot.html")
    template_vars = {"title" : "NCHA DATA"
                 }
    # Render our file and create the PDF using our css style file
    return template.render(template_vars)


@route('/highchart', method='GET')
@auth_basic(check)
def highchart():
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("highchart_example.html")
    template_vars = {"title" : "NCHA DATA"
                 }
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


@route('/create_post', method='POST')
def create_post():
    df2 = dfcanada
    a = df2['NQ1'].value_counts(sort=False)           
    return a.all()


debug(True)
run(reloader=True)
run(host='192.168.0.10', port=os.environ.get('PORT', 8000))

