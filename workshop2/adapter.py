import cx_Oracle

class ProcedureAdapter:

    def call_procedure(self):
        con = cx_Oracle.connect('127.0.0.1/orcl')  #localhost
        cur = con.cursor()     #connect
        myvar = cur.var(cx_Oracle.NUMBER)    #var for output
        cur.callproc('procedure name', (123, myvar))
        result = myvar.getvalue()
        cur.close()
        con.close()
        return result