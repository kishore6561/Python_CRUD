from flask import Flask,request,jsonify,make_response
from flask_restful import Resource
import pymysql

class Mysqlconnect(Resource):
    def get(self):
        mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="1111",
        database="employees"
        )

        result_list=[]
        mycursor = mydb.cursor()
        flag = 0
        while flag==0:
            id =int(input("enter id : "))
            fname = input("enter fname : ")
            lname = input("enter lname : ")
            dept = input("enter dept : ")
            project = input("enter project : ")
            address = input("enter address : ")
            dob = input("enter dob : ")
            gender = input("enter gender : ")
            flag = int(input("0_continue 1_commit : "))
            
            if flag !=1:
                sql2 = "INSERT INTO Employeeinfo(Empid,EmpFname,emplname,department,project,Address,DOB,Gender) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(id,fname,lname,dept,project,address,dob,gender)
                mycursor.execute(sql2)
                