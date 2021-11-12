import frappe


def execute():

    print("Deleting ESO Manual")
    frappe.db.sql("""Delete from `tabDocType` where name = 'Job Order' """)
    frappe.db.sql_ddl("""DROP TABLE IF EXISTS `tabJob Order`""")