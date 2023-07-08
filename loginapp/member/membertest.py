# import pymysql

# conn = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='1234',
#     db='www',
#     charset='utf8'
# )

# cursor = conn.cursor()

# sql = "SELECT * FROM test_table"
# cursor.execute(sql)

# result = cursor.fetchall()

# print(result)

# conn.close()




# sql = "INSERT INTO users (id, password) VALUES (%s, %s)"
# id = input("아이디를 입력하세요: ")
# password = input("비밀번호를 입력하세요: ")
# cursor.execute(sql, (id, password))

# conn.commit()

# conn.close()



# ###############################################################
# def setMemberInsert(mem_id, mem_pass, mem_email) :
#     try:
#         conn, cursor = getDBConn_Cursor()
        
    

#         sql = """Insert Into member(mem_id, mem_pass, mem_email) 
#                         Values(:mem_id, :mem_pass, :mem_email)"""
                        
#         cursor.execute(sql, mem_id=mem_id, mem_pass=mem_pass,mem_email=mem_email)
        
#         conn.commit()
#     except:    
#         DBClose(cursor, conn)
#         return "no"
    
#     DBClose(cursor, conn)
#     return "OK"

# def setMemberDelete(mem_id, mem_pass, mem_email):
#     try:
#         conn, cursor = getDBConn_Cursor()
        
#         sql = """Delete Into member(mem_id, mem_pass,  mem_email) 
#                         Values(:mem_id, :mem_pass, :mem_email)"""
                        
#         cursor.execute(sql, mem_id=mem_id, mem_pass=mem_pass, mem_email=mem_email)
        
#         conn.commit()
#     except:    
#         DBClose(cursor, conn)
#         return "no"
    
#     DBClose(cursor, conn)
#     return "OK"

# def getFetchOne(colname,row):
#     ### 컬럼명 조회하기
    
#     col=[]

#     for i in colname:
#         col.append(i[0].lower())
        
#     dict_col ={}
#     for i in range(0,len(row),1):
#             dict_col[col[i]] =row[i]
    
#     return dict_col 

# def getLogin(p_id, p_pass) :
#     ### DB접속하기
#     conn, cursor = getDBConn_Cursor()
    
#     sql = """
#             Select * From member
#             where mem_id =: mem_id 
#               And mem_pass =: mem_pass
#     """
#     cursor.execute(sql, mem_id=p_id, mem_pass=p_pass)
    
#     rows = cursor.fetchone()
    
#     ### 조회결과가 없으면 바로 리턴
#     if rows == None :
#         ### DB연결 해제하기
#         DBClose(cursor, conn)
#         ## 성공여부
#         return {"rs" : "no"}
    
#     ### 컬럼명 조회하기
#     colname = cursor.description  
    
#     ### {}형태로 변환
#     dict_col = getFetchOne(colname, rows)
    
#     ### 성공 여부 저장
#     dict_col["rs"] = "yes"
    
#     ### DB연결 해제하기
#     DBClose(cursor, conn)
    
#     return dict_col


# def setMemberUpdate(mem_id, mem_pass, mem_email) :

#     try:
#         conn, cursor = getDBConn_Cursor()
        
        
#         sql = """Update member 
#                 Set
#                     mem_pass = '{}', 
#                     mem_email = '{}'
#                 where mem_id='{}'
#                     """.format( mem_pass, mem_email, mem_id )           
                    
#         cursor.execute(sql)
        
#         conn.commit()
#     except:    
#         DBClose(cursor, conn)
#         return "no", sql
    
#     DBClose(cursor, conn)
#     return "OK", sql

# def getmypage(mem_id) :
#     conn, cursor = getDBConn_Cursor()
    
#     sql= """
#             Select * From member
#             where mem_id =: mem_id 
#         """
#     cursor.execute(sql, mem_id=mem_id)

#     rows = cursor.fetchone()
#     colname = cursor.description

#     dict_col = getFetchOne(colname,rows)
#     DBClose(cursor, conn)
    
#     return dict_col


        