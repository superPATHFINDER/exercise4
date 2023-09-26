import sqlite3

# Connect to a database or create a new database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# 创建Books表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID TEXT PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        ISBN TEXT,
        Status TEXT
    )
''')

# Create the Users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID TEXT PRIMARY KEY,
        Name TEXT,
        Email TEXT
    )
''')

# Create Reservations
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID TEXT PRIMARY KEY,
        BookID TEXT,
        UserID TEXT,
        ReservationDate TEXT,
        FOREIGN KEY (BookID) REFERENCES Books (BookID),
        FOREIGN KEY (UserID) REFERENCES Users (UserID)
    )
''')

# Prompts the user to select an action
while True:
    print("\n图书馆管理系统")
    print("1. 添加新书")
    print("2. 查找书籍详细信息")
    print("3. 查找图书的预订状态")
    print("4. 查找所有书籍")
    print("5. 修改/更新书籍信息")
    print("6. 删除书籍")
    print("7. 退出")

    choice = input("请选择操作 (1/2/3/4/5/6/7): ")

    if choice == '1':
        # ADD NEW BOOKS
        book_id = input("请输入新书的图书编号 (以LB开头): ")
        title = input("请输入书名: ")
        author = input("请输入作者: ")
        isbn = input("请输入ISBN: ")
        status = "Available"  # DEFAULT Available
        cursor.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)",
                       (book_id, title, author, isbn, status))
        conn.commit()
        print("新书已成功添加!")

    elif choice == '2':
        # SEARCH
        book_id = input("请输入图书编号 (以LB开头)：")
        cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
        book = cursor.fetchone()
        if book:
            print("图书详细信息:")
            print("图书编号:", book[0])
            print("书名:", book[1])
            print("作者:", book[2])
            print("ISBN:", book[3])
            print("状态:", book[4])
            # BOOKING
            cursor.execute("SELECT * FROM Reservations WHERE BookID = ?", (book_id,))
            reservations = cursor.fetchall()
            if reservations:
                print("预订状态:")
                for reservation in reservations:
                    print("ReservationID:", reservation[0])
                    print("UserID:", reservation[2])
                    print("ReservationDate:", reservation[3])
            else:
                print("没有预订记录。")
        else:
            print("找不到该图书。")

    elif choice == '3':
        #Find the book's scheduled status
        book_id = input("请输入图书编号 (以LB开头)：")
        cursor.execute("SELECT ReservationID, UserID FROM Reservations WHERE BookID = ?", (book_id,))
        reservations = cursor.fetchall()
        if reservations:
            print("图书的预订状态:")
            for reservation in reservations:
                print("ReservationID:", reservation[0])
                print("UserID:", reservation[1])
        else:
            print("没有预订记录。")

    elif choice == '4':
        # search all books
        cursor.execute("SELECT * FROM Books")
        books = cursor.fetchall()
        if books:
            print("所有书籍:")
            for book in books:
                print("图书编号:", book[0])
                print("书名:", book[1])
                print("作者:", book[2])
                print("ISBN:", book[3])
                print("状态:", book[4])
        else:
            print("图书库为空。")

    elif choice == '5':
        # renew book information
        book_id = input("请输入要修改的图书编号 (以LB开头): ")
        cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
        book = cursor.fetchone()
        if book:
            print("当前图书信息:")
            print("图书编号:", book[0])
            print("书名:", book[1])
            print("作者:", book[2])
            print("ISBN:", book[3])
            print("状态:", book[4])
            new_title = input("请输入新书名 (按Enter保持不变): ")
            new_author = input("请输入新作者 (按Enter保持不变): ")
            new_isbn = input("请输入新ISBN (按Enter保持不变): ")
            new_status = input("请输入新状态 (按Enter保持不变): ")
            if new_title:
                cursor.execute("UPDATE Books SET Title = ? WHERE BookID = ?", (new_title, book_id))
            if new_author:
                cursor.execute("UPDATE Books SET Author = ? WHERE BookID = ?", (new_author, book_id))
            if new_isbn:
                cursor.execute("UPDATE Books SET ISBN = ? WHERE BookID = ?", (new_isbn, book_id))
            if new_status:
                cursor.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))
            conn.commit()
            print("图书信息已更新!")
        else:
            print("找不到该图书。")

    elif choice == '6':
        # delete
        book_id = input("请输入要删除的图书编号 (以LB开头): ")
        cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
        book = cursor.fetchone()
        if book:
            # delete books
            cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
            # delete booking
            cursor.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
            conn.commit()
            print("图书已成功删除!")
        else:
            print("找不到该图书。")

    elif choice == '7':
        # exit
        print("感谢使用图书馆管理系统。")
        break

    else:
        print("无效的选择，请重新输入。")

# disconnect
conn.close()
