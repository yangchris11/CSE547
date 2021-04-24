# -*- coding: utf-8 -*-
"""hw1_p1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17gyjavqBpDF2iL9FYAHfkQzeNwTF6TCw
"""

!pip install pyspark
!pip install -U -q PyDrive
!apt install openjdk-8-jdk-headless -qq
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# Authenticate and create the PyDrive client
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

from google.colab import drive
drive.mount('/content/drive')

import pyspark
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark import SparkContext, SparkConf
from pyspark.sql import functions as F

import numpy as np
import pandas as pd

# create the context
conf = SparkConf().setAppName("App")
conf = (conf.setMaster('local[*]')
        .set('spark.executor.memory', '6G')
        .set('spark.driver.memory', '45G')
        .set('spark.driver.maxResultSize', '10G'))
sc = pyspark.SparkContext(conf=conf)
spark = SparkSession.builder.getOrCreate()

# load the data
data = sc.textFile('soc-LiveJournal1Adj.txt')

def lambda_process_line(line):
    user_id, friend_ids = line.split('\t')
    if friend_ids != '':
        friend_ids_lst = friend_ids.split(',')
    else:
        friend_ids_lst = []
    return (user_id, friend_ids_lst)

def lambda_make_pairs(line):
    user_id = line[0]
    friend_ids = line[1]
    pairs = []
    # first-degree friendship:
    for friend_id in friend_ids:
        pair = (user_id, friend_id)
        if user_id > friend_id:
            pair = (friend_id, user_id)
        pairs.append((pair, 0))
    # second-degree friendship:
    for i in range(len(friend_ids)-1):
        for j in range(i+1, len(friend_ids)):
            pair = (friend_ids[i], friend_ids[j])
            if friend_ids[i] > friend_ids[j]:
                pair = (friend_ids[j], friend_ids[i])
            pairs.append((pair, 1))
    return pairs

# step 1
processed_data = data.map(lambda line: lambda_process_line(line))
all_friend_pairs = processed_data.flatMap(lambda line: lambda_make_pairs(line))

# step 2
mutual_friend_pairs = all_friend_pairs.groupByKey().filter(lambda pair: 0 not in pair[1]).flatMapValues(lambda x: x)

# step 3
reduced_mutual_friend_pairs = mutual_friend_pairs.reduceByKey(lambda x, y: x+y)

# step 4
recommend_friend_pairs = reduced_mutual_friend_pairs.flatMap(lambda pair: [(pair[0][0], (pair[0][1], pair[1])), (pair[0][1], (pair[0][0], pair[1]))]).groupByKey().mapValues(list)

# step 5
sorted_recommend_friend_pairs = recommend_friend_pairs.map(lambda user: (user[0], sorted(user[1], key = lambda x: (-x[1], int(x[0])))))

result = sorted_recommend_friend_pairs.collect()

# problem 1.c

user_ids = ['11', '924', '8941', '8942', '9019', '9020', '9021', '9022', '9990', '9992', '9993']

for user_id in user_ids:
    for line in result:
        cur_id, recommendations = line
        if cur_id == user_id:
            recommendation_ids = []
            for recommendation in recommendations:
                recommendation_ids.append(recommendation[0])
            print(user_id, recommendation_ids)

# output recommendations
with open("output.txt","w+") as file:
    for line in result:
        cur_id, recommendations = line
        recommendation_ids = []
        for recommendation in recommendations:
            recommendation_ids.append(recommendation[0])
        new_line = str(cur_id) + '\t' + ','.join(recommendation_ids) + '\n'
        file.write(new_line)