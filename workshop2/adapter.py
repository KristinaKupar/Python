import cx_Oracle

class ProcedureAdapter:

    def call_procedure(self):
        con = cx_Oracle.connect('pythonhol/welcome@127.0.0.1/orcl')
        cur = con.cursor()
        myvar = cur.var(cx_Oracle.NUMBER)
        cur.callproc('procedure name', (123, myvar))
        result = myvar.getvalue()
        cur.close()
        con.close()
        return result