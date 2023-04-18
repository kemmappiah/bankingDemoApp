from tkinter import *
from tkinter import messagebox as mb
import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host="localhost",
                                         database="bankDemo",
                                         user="root",
                                         password="pa$$W0rd5",
                                         auth_plugin="mysql_native_password")
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        window = Tk()
        window.geometry('500x500')
        window.title('EMMAPP BANKING APP')

        manual_credit = StringVar()
        search_menu_txt = StringVar()
        shop_name_txt = StringVar()
        shop_amount_txt = StringVar()
        rec_name_txt = StringVar()
        rec_amt_txt = StringVar()
        ref_entry_txt = StringVar()

        act_bal_lbl = Label(window, text='CURRENT ACCOUNT BALANCE:', font=('Cambria', 12, 'bold'))
        act_bal_lbl.place(x=30, y=50)
        act_balance_window = Label(window, font=('Cambria', 15))
        act_balance_window.place(x=300, y=50)
        credit_instruction = Label(window, text='Credit my account with GH¢')
        credit_instruction.place(x=30, y=100)
        credit_entry = Entry(window, textvariable=manual_credit)
        credit_entry.place(x=200, y=100)

        debit_types = Label(window, text='Choose Debit Type')
        debit_types.place(x=30, y=150)

        search_menu_txt.set('Choose One')
        drop_down = OptionMenu(window, search_menu_txt, 'Purchase', 'Remittance')
        drop_down.place(x=150, y=150)

        debits_frame = Frame(window, height=250, width=460)
        debits_frame.place(x=20, y=185)

        db_connection_lbl = Label(window, width=50)
        db_connection_lbl.place(x=70, y=470)


        def confirm_debit():
            user_choice = search_menu_txt.get()
            if user_choice == 'Purchase':
                for widgets in debits_frame.winfo_children():
                    widgets.destroy()
                shop_name_lbl = Label(debits_frame, text='Shop Name/Item')
                shop_name_lbl.place(x=30, y=10)
                shop_name_entry = Entry(debits_frame, textvariable=shop_name_txt)
                shop_name_entry.place(x=150, y=10)
                shop_amount_lbl = Label(debits_frame, text='Total Amount')
                shop_amount_lbl.place(x=30, y=60)
                shop_amount_entry = Entry(debits_frame, textvariable=shop_amount_txt)
                shop_amount_entry.place(x=150, y=60)

                def shop_payment():
                    global current_balance
                    global act_balance_window
                    if shop_name_entry.get() == '' or shop_amount_entry.get() == '' \
                            or not shop_amount_entry.get().isdigit():
                        mb.showerror('Error', 'Either a field is empty or has inappropriate value')
                    else:
                        shop_amount = float(shop_amount_entry.get())
                        if shop_amount > current_balance:
                            mb.showwarning('Shop Purchase', 'Low Bank Balance - Credit your account first!')
                        else:
                            new_amount = current_balance - shop_amount
                            act_balance_window.config(text='GH¢' + str(new_amount))

                            insertion_to_table = """INSERT INTO shop_transactions (initial_bal, shop_name, total_amount, 
                                                    current_bal, date_time) VALUES (%s,%s,%s,%s,now()) """
                            generated_items = (current_balance, shop_name_entry.get(), shop_amount, new_amount)
                            cursor.execute(insertion_to_table, generated_items)
                            connection.commit()
                            insertion_to_master = """INSERT INTO account_master (initial_balance, shop_name, 
                                shop_amount, current_balance, date_time) VALUES (%s,%s,%s,%s,now()) """
                            master_items = (current_balance, shop_name_entry.get(), shop_amount, new_amount)
                            cursor.execute(insertion_to_master, master_items)
                            connection.commit()
                            new_bal_select_query = '''select current_balance from account_master ORDER BY id DESC 
                            LIMIT 1'''
                            cursor.execute(new_bal_select_query)
                            new_query_result = cursor.fetchone()
                            current_balance = new_query_result[0]
                            act_balance_window.config(text='GH¢' + str(current_balance))
                            print(cursor.rowcount, "Record inserted successfully into shop_transactions table")
                            shop_entries = [shop_name_txt, shop_amount_txt]
                            for item in shop_entries:
                                item.set('')
                            mb.showinfo('Shop Payment', 'Payment of GH¢' + str(shop_amount) + ' successfully made to '
                                        + shop_name_entry.get())

                shop_auth_btn = Button(debits_frame, text='Authorize Payment', command=shop_payment)
                shop_auth_btn.place(x=30, y=110)
            else:
                for widgets in debits_frame.winfo_children():
                    widgets.destroy()
                receiver_name_lbl = Label(debits_frame, text='Name of Receiver')
                receiver_name_lbl.place(x=30, y=10)
                receiver_name_entry = Entry(debits_frame, textvariable=rec_name_txt)
                receiver_name_entry.place(x=150, y=10)
                receiver_amount_lbl = Label(debits_frame, text='Total Amount')
                receiver_amount_lbl.place(x=30, y=60)
                receiver_amount_entry = Entry(debits_frame, textvariable=rec_amt_txt)
                receiver_amount_entry.place(x=150, y=60)
                ref_label = Label(debits_frame, text='Reference')
                ref_label.place(x=30, y=110)
                ref_entry = Entry(debits_frame, textvariable=ref_entry_txt)
                ref_entry.place(x=150, y=110)

                def remittance_payment():
                    global current_balance
                    global act_balance_window
                    if receiver_name_entry.get() == '' or receiver_amount_entry.get() == '' \
                            or not receiver_amount_entry.get().isdigit() or ref_entry.get() == '':
                        mb.showerror('Error', 'Either a field is empty or has inappropriate value')
                    else:
                        send_amount = float(receiver_amount_entry.get())
                        if send_amount > current_balance:
                            mb.showwarning('Remittance', 'Low Bank Balance - Credit your account first!')
                        else:
                            new_amount = current_balance - send_amount
                            act_balance_window.config(text='GH¢' + str(new_amount))

                            insertion_to_table = """INSERT INTO remittances (initial_balance,receiver_name,sent_amount, 
                                                send_ref,current_balance,date_time) VALUES (%s,%s,%s,%s,%s,now()) """
                            generated_items = (current_balance, receiver_name_entry.get(), send_amount, ref_entry.get(),
                                               new_amount)
                            cursor.execute(insertion_to_table, generated_items)
                            connection.commit()
                            insertion_to_master = """INSERT INTO account_master (initial_balance,receiver,sent_amount, 
                                                                            send_ref,current_balance,date_time) 
                                                                            VALUES (%s,%s,%s,%s,%s,now()) """
                            master_items = (current_balance, receiver_name_entry.get(), send_amount, ref_entry.get(),
                                            new_amount)
                            cursor.execute(insertion_to_master, master_items)
                            connection.commit()
                            new_bal_select_query = '''select current_balance from account_master ORDER BY id DESC 
                            LIMIT 1'''
                            cursor.execute(new_bal_select_query)
                            new_query_result = cursor.fetchone()
                            current_balance = new_query_result[0]
                            act_balance_window.config(text='GH¢' + str(current_balance))
                            print(cursor.rowcount, "Record inserted successfully into remittances table")
                            remittance_entries = [rec_name_txt, rec_amt_txt, ref_entry_txt]
                            for item in remittance_entries:
                                item.set('')
                            mb.showinfo('Remittance', 'Payment of GH¢' + str(send_amount) + ' successfully made to '
                                        + receiver_name_entry.get())

                remittance_auth_btn = Button(debits_frame, text='Authorize Payment', command=remittance_payment)
                remittance_auth_btn.place(x=30, y=170)


        confirm_debit_btn = Button(window, text='Confirm', command=confirm_debit)
        confirm_debit_btn.place(x=300, y=150)

        balance_select_query = '''select current_balance from account_master ORDER BY id DESC LIMIT 1'''
        cursor.execute(balance_select_query)
        query_result = cursor.fetchone()
        current_balance = query_result[0]
        act_balance_window.config(text='GH¢' + str(current_balance))

        def credit_my_account():
            if credit_entry.get().isdigit():
                global current_balance
                current_amount = float(credit_entry.get())
                current_balance += current_amount
                act_balance_window.config(text='GH¢' + str(current_balance))
                insertion_to_table = """INSERT INTO owner_credits (credit_amount, actual_balance, 
                                                            date_time) VALUES (%s,%s,now()) """
                generated_items = (current_amount, current_balance)
                cursor.execute(insertion_to_table, generated_items)
                connection.commit()
                insertion_to_master = """INSERT INTO account_master (credit_amount, current_balance, 
                                                            date_time) VALUES (%s,%s,now()) """
                master_items = (current_amount, current_balance)
                cursor.execute(insertion_to_master, master_items)
                connection.commit()
                print(cursor.rowcount, "Record inserted successfully owner_credits table")
                mb.showinfo('Credit Account', 'Account Credited successfully with GH¢' + str(current_amount))
                manual_credit.set('')
            else:
                mb.showwarning('Credit Account', 'Enter a numerical value')

        credit_enter = Button(window, text='Go', font=('Cambria', 9, 'bold'), command=credit_my_account)
        credit_enter.place(x=350, y=100)

        window.mainloop()
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


