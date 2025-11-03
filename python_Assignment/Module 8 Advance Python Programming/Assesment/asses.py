import sqlite3
import re
from datetime import datetime, timedelta
import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

DB_PATH = 'libradesk_human.db'


class LibraryError(Exception):
    """Base exception for library-related problems."""
    pass

class NotAvailable(LibraryError):
    """Raised when a book copy is not available."""
    pass


class LibraryDB:
    def __init__(self, dbfile=DB_PATH):
        self.dbfile = dbfile
        self.conn = sqlite3.connect(self.dbfile)
        self.conn.row_factory = sqlite3.Row
        self._setup()

    def _setup(self):
        c = self.conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS members (
                        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT,
                        phone TEXT,
                        address TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS books (
                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        author TEXT,
                        genre TEXT,
                        isbn TEXT UNIQUE,
                        total_copies INTEGER DEFAULT 1,
                        avail_copies INTEGER DEFAULT 1
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS borrow (
                        borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        member_id INTEGER,
                        book_id INTEGER,
                        borrow_date TEXT,
                        due_date TEXT,
                        return_date TEXT,
                        fine REAL DEFAULT 0,
                        FOREIGN KEY(member_id) REFERENCES members(member_id),
                        FOREIGN KEY(book_id) REFERENCES books(book_id)
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS payments (
                        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        borrow_id INTEGER,
                        amount REAL,
                        paid_on TEXT,
                        method TEXT,
                        FOREIGN KEY(borrow_id) REFERENCES borrow(borrow_id)
                    )''')
        self.conn.commit()

        c.execute('SELECT COUNT(*) as cnt FROM users')
        if c.fetchone()['cnt'] == 0:
            c.execute('INSERT INTO users (username,password,role) VALUES (?,?,?)', ('admin','admin','admin'))
            c.execute('INSERT INTO users (username,password,role) VALUES (?,?,?)', ('librarian','libpass','librarian'))
            self.conn.commit()

 
    def authenticate(self, username, password):
        c = self.conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        row = c.fetchone()
        if row:
            return dict(row)
        return None

  
    def add_member(self, name, email, phone, address):
        c = self.conn.cursor()
        c.execute('INSERT INTO members (name,email,phone,address) VALUES (?,?,?,?)', (name,email,phone,address))
        self.conn.commit()
        return c.lastrowid

    def get_members(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM members')
        rows = c.fetchall()
        return [dict(r) for r in rows]

    def get_member(self, member_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM members WHERE member_id=?', (member_id,))
        r = c.fetchone()
        return dict(r) if r else None

 
    def add_book(self, title, author, genre, isbn, copies=1):
        c = self.conn.cursor()
        c.execute('INSERT INTO books (title,author,genre,isbn,total_copies,avail_copies) VALUES (?,?,?,?,?,?)',
                  (title,author,genre,isbn,copies,copies))
        self.conn.commit()
        return c.lastrowid

    def update_book(self, book_id, **kwargs):
        keys = ','.join([f+"=?" for f in kwargs.keys()])
        vals = list(kwargs.values())
        vals.append(book_id)
        c = self.conn.cursor()
        c.execute(f'UPDATE books SET {keys} WHERE book_id=?', vals)
        self.conn.commit()

    def get_book(self, book_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM books WHERE book_id=?', (book_id,))
        r = c.fetchone()
        return dict(r) if r else None

    def list_books(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM books')
        return [dict(r) for r in c.fetchall()]

    def search_books(self, pattern, field='title'):
    
        try:
            prog = re.compile(pattern, re.IGNORECASE)
        except re.error as e:
            raise LibraryError(f'Regex invalid: {e}')
        out = []
        for b in self.list_books():
            if field not in b:
                raise LibraryError('Invalid field for search')
            if prog.search(str(b[field])):
                out.append(b)
        return out

 
    def borrow_book(self, member_id, book_id, days=14):
        book = self.get_book(book_id)
        if not book:
            raise LibraryError('Book not found')
        if book['avail_copies'] <= 0:
            raise NotAvailable('No copies left')
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=days)
        c = self.conn.cursor()
        c.execute('INSERT INTO borrow (member_id,book_id,borrow_date,due_date) VALUES (?,?,?,?)',
                  (member_id,book_id,borrow_date.isoformat(), due_date.isoformat()))
        c.execute('UPDATE books SET avail_copies = avail_copies - 1 WHERE book_id=?', (book_id,))
        self.conn.commit()
        return c.lastrowid

    def return_book(self, borrow_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM borrow WHERE borrow_id=?', (borrow_id,))
        row = c.fetchone()
        if not row:
            raise LibraryError('Borrow record missing')
        if row['return_date']:
            raise LibraryError('Already returned')
        due = datetime.fromisoformat(row['due_date'])
        now = datetime.now()
        fine = 0.0
        if now > due:
            days = (now - due).days
            fine = self._calc_fine(days)
        c.execute('UPDATE borrow SET return_date=?, fine=? WHERE borrow_id=?', (now.isoformat(), fine, borrow_id))
        c.execute('UPDATE books SET avail_copies = avail_copies + 1 WHERE book_id=?', (row['book_id'],))
        self.conn.commit()
        return fine

    def _calc_fine(self, days, per_day=5.0):

        if days <= 0:
            return 0.0
        return round(days * per_day, 2)

    def overdue_list(self):
        c = self.conn.cursor()
        today = datetime.now().isoformat()
        q = '''SELECT br.borrow_id, m.name as member, b.title as book, br.due_date
               FROM borrow br
               JOIN members m ON br.member_id=m.member_id
               JOIN books b ON br.book_id=b.book_id
               WHERE br.return_date IS NULL AND br.due_date < ?'''
        c.execute(q, (today,))
        return [dict(r) for r in c.fetchall()]

    def most_borrowed(self, limit=10):
        c = self.conn.cursor()
        q = 'SELECT book_id, COUNT(*) as cnt FROM borrow GROUP BY book_id ORDER BY cnt DESC LIMIT ?'
        c.execute(q, (limit,))
        res = []
        for r in c.fetchall():
            book = self.get_book(r['book_id'])
            res.append({'book': book, 'count': r['cnt']})
        return res

    def export_invoice(self, borrow_id, path):
        c = self.conn.cursor()
        q = '''SELECT br.*, m.name as member, b.title as book
               FROM borrow br JOIN members m ON br.member_id=m.member_id
               JOIN books b ON br.book_id=b.book_id WHERE br.borrow_id=?'''
        c.execute(q, (borrow_id,))
        r = c.fetchone()
        if not r:
            raise LibraryError('Borrow record not found')
        fine = r['fine'] or 0.0
        tax = round(fine * 0.18, 2)
        total = round(fine + tax, 2)

        base, ext = os.path.splitext(path)
        if ext.lower() == '.csv':
            with open(path, 'w', newline='') as f:
                w = csv.writer(f)
                w.writerow(['borrow_id','member','book','borrow_date','due_date','return_date','fine','tax','total'])
                w.writerow([r['borrow_id'], r['member'], r['book'], r['borrow_date'], r['due_date'], r['return_date'] or '', fine, tax, total])
        else:
            with open(path, 'w') as f:
                f.write('INVOICE')
                f.write(f"Borrow ID: {r['borrow_id']}")
                f.write(f"Member: {r['member']}")
                f.write(f"Book: {r['book']}")
                f.write(f"Borrow: {r['borrow_date']}")
                f.write(f"Due: {r['due_date']}")
                f.write(f"Return: {r['return_date'] or ''}")
                f.write(f"Fine: {fine}")
                f.write(f"Tax: {tax}")
                f.write(f"Total: {total}")
        return path

class LibraryApp:
    def __init__(self, db: LibraryDB):
        self.db = db
        self.root = tk.Tk()
        self.root.title('LibraDesk - Human Style')
        self.user = None
        self._show_login()

    def _show_login(self):
        for w in self.root.winfo_children():
            w.destroy()
        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill='both', expand=True)

        ttk.Label(frm, text='Username:').grid(row=0, column=0)
        self.un = tk.StringVar()
        ttk.Entry(frm, textvariable=self.un).grid(row=0, column=1)

        ttk.Label(frm, text='Password:').grid(row=1, column=0)
        self.pw = tk.StringVar()
        ttk.Entry(frm, textvariable=self.pw, show='*').grid(row=1, column=1)

        ttk.Button(frm, text='Login', command=self._do_login).grid(row=2, column=0, columnspan=2, pady=10)

    def _do_login(self):
        u = self.un.get().strip()
        p = self.pw.get().strip()
        user = self.db.authenticate(u, p)
        if not user:
            messagebox.showerror('Login failed', 'Bad username/password')
            return
        self.user = user
        self._main_menu()

    def _main_menu(self):
        for w in self.root.winfo_children():
            w.destroy()
        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill='both', expand=True)

        ttk.Label(frm, text=f"Logged in as: {self.user['username']} ({self.user['role']})").grid(row=0, column=0, sticky='w')

        ttk.Button(frm, text='Add Member', command=self._dlg_add_member).grid(row=1, column=0, sticky='w', pady=4)
        ttk.Button(frm, text='Add Book', command=self._dlg_add_book).grid(row=2, column=0, sticky='w', pady=4)
        ttk.Button(frm, text='Search Books', command=self._dlg_search).grid(row=3, column=0, sticky='w', pady=4)
        ttk.Button(frm, text='Borrow Book', command=self._dlg_borrow).grid(row=4, column=0, sticky='w', pady=4)
        ttk.Button(frm, text='Return Book', command=self._dlg_return).grid(row=5, column=0, sticky='w', pady=4)
        ttk.Button(frm, text='Overdue Report', command=self._dlg_overdue).grid(row=6, column=0, sticky='w', pady=4)
        ttk.Button(frm, text='Most Borrowed', command=self._dlg_most_borrowed).grid(row=7, column=0, sticky='w', pady=4)
        ttk.Button(frm, text='Logout', command=self._logout).grid(row=8, column=0, sticky='w', pady=10)

    def _dlg_add_member(self):
        d = tk.Toplevel(self.root)
        d.title('Add Member')
        labels = ['Name','Email','Phone','Address']
        vars = {L: tk.StringVar() for L in labels}
        for i,L in enumerate(labels):
            ttk.Label(d, text=L).grid(row=i, column=0)
            ttk.Entry(d, textvariable=vars[L]).grid(row=i, column=1)
        def ok():
            try:
                self.db.add_member(vars['Name'].get(), vars['Email'].get(), vars['Phone'].get(), vars['Address'].get())
                messagebox.showinfo('Added','Member added successfully')
                d.destroy()
            except Exception as e:
                messagebox.showerror('Error', str(e))
        ttk.Button(d, text='Add', command=ok).grid(row=len(labels), column=0, columnspan=2, pady=6)

    def _dlg_add_book(self):
        if self.user['role'] != 'admin':
            messagebox.showerror('Permission', 'Only admin may add books')
            return
        d = tk.Toplevel(self.root)
        d.title('Add Book')
        fields = ['Title','Author','Genre','ISBN','Copies']
        vars = {f: tk.StringVar() for f in fields}
        for i,f in enumerate(fields):
            ttk.Label(d, text=f).grid(row=i, column=0)
            ttk.Entry(d, textvariable=vars[f]).grid(row=i, column=1)
        def ok():
            try:
                copies = int(vars['Copies'].get() or '1')
                self.db.add_book(vars['Title'].get(), vars['Author'].get(), vars['Genre'].get(), vars['ISBN'].get(), copies)
                messagebox.showinfo('OK','Book added')
                d.destroy()
            except Exception as e:
                messagebox.showerror('Error', str(e))
        ttk.Button(d, text='Add', command=ok).grid(row=len(fields), column=0, columnspan=2, pady=6)

    def _dlg_search(self):
        d = tk.Toplevel(self.root)
        d.title('Search Books')
        ttk.Label(d, text='Field (title/author/genre)').grid(row=0, column=0)
        field = tk.StringVar(value='title')
        ttk.Entry(d, textvariable=field).grid(row=0, column=1)
        ttk.Label(d, text='Regex pattern').grid(row=1, column=0)
        pat = tk.StringVar()
        ttk.Entry(d, textvariable=pat).grid(row=1, column=1)

        tree = ttk.Treeview(d, columns=('id','title','author','genre','avail'), show='headings')
        for col in tree['columns']:
            tree.heading(col, text=col)
        tree.grid(row=3, column=0, columnspan=2, sticky='nsew')

        def do_search():
            try:
                rows = self.db.search_books(pat.get(), field=field.get())
                for r in tree.get_children():
                    tree.delete(r)
                for b in rows:
                    tree.insert('', 'end', values=(b['book_id'], b['title'], b['author'], b['genre'], b['avail_copies']))
            except Exception as e:
                messagebox.showerror('Search error', str(e))
        ttk.Button(d, text='Search', command=do_search).grid(row=2, column=0, columnspan=2, pady=6)

    def _dlg_borrow(self):
        d = tk.Toplevel(self.root)
        d.title('Borrow')
        ttk.Label(d, text='Member ID').grid(row=0, column=0)
        mid = tk.StringVar()
        ttk.Entry(d, textvariable=mid).grid(row=0, column=1)
        ttk.Label(d, text='Book ID').grid(row=1, column=0)
        bid = tk.StringVar()
        ttk.Entry(d, textvariable=bid).grid(row=1, column=1)

        def go():
            try:
                borrow_id = self.db.borrow_book(int(mid.get()), int(bid.get()))
                messagebox.showinfo('OK', f'Borrowed, id={borrow_id}')
                d.destroy()
            except Exception as e:
                messagebox.showerror('Error', str(e))
        ttk.Button(d, text='Borrow', command=go).grid(row=2, column=0, columnspan=2, pady=6)

    def _dlg_return(self):
        d = tk.Toplevel(self.root)
        d.title('Return')
        ttk.Label(d, text='Borrow ID').grid(row=0, column=0)
        bid = tk.StringVar()
        ttk.Entry(d, textvariable=bid).grid(row=0, column=1)

        def go():
            try:
                fine = self.db.return_book(int(bid.get()))
                messagebox.showinfo('Returned', f'Fine: {fine}')
                if fine > 0:
                    if messagebox.askyesno('Invoice', 'Export invoice?'):
                        p = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files','*.txt'),('CSV','*.csv')])
                        if p:
                            self.db.export_invoice(int(bid.get()), p)
                            messagebox.showinfo('Saved', f'Saved to {p}')
                d.destroy()
            except Exception as e:
                messagebox.showerror('Error', str(e))
        ttk.Button(d, text='Return', command=go).grid(row=1, column=0, columnspan=2, pady=6)

    def _dlg_overdue(self):
        rows = self.db.overdue_list()
        d = tk.Toplevel(self.root)
        d.title('Overdue')
        tree = ttk.Treeview(d, columns=('id','member','book','due'), show='headings')
        for col in tree['columns']:
            tree.heading(col, text=col)
        tree.pack(fill='both', expand=True)
        for r in rows:
            tree.insert('', 'end', values=(r['borrow_id'], r['member'], r['book'], r['due_date']))

    def _dlg_most_borrowed(self):
        rows = self.db.most_borrowed()
        d = tk.Toplevel(self.root)
        d.title('Most Borrowed')
        tree = ttk.Treeview(d, columns=('title','count'), show='headings')
        for col in tree['columns']:
            tree.heading(col, text=col)
        tree.pack(fill='both', expand=True)
        for r in rows:
            tree.insert('', 'end', values=(r['book']['title'], r['count']))

    def _logout(self):
        self.user = None
        self._show_login()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':

    db = LibraryDB()
    print('Database initialized at', DB_PATH)
    app = LibraryApp(db)
    app.run()


