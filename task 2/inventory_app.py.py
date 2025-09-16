import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# ---------------- Authentication Window ----------------
class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Inventory Management Login")

        tk.Label(master, text="Username").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(master, text="Password").grid(row=1, column=0, padx=10, pady=10)

        self.username = tk.Entry(master)
        self.password = tk.Entry(master, show='*')

        self.username.grid(row=0, column=1, padx=10, pady=10)
        self.password.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(master, text="Login", command=self.login).grid(row=2, column=1, pady=10)

    def login(self):
        uname = self.username.get()
        pwd = self.password.get()

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (uname, pwd))
        if cursor.fetchone():
            self.master.destroy()
            root = tk.Tk()
            InventorySystem(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials")
        conn.close()


# ---------------- Inventory System GUI ----------------
class InventorySystem:
    def __init__(self, master):
        self.master = master
        master.title("Inventory Management System")

        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Product Name").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.frame, text="Quantity").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.frame, text="Price").grid(row=2, column=0, padx=10, pady=5)

        self.name_entry = tk.Entry(self.frame)
        self.quantity_entry = tk.Entry(self.frame)
        self.price_entry = tk.Entry(self.frame)

        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=5)
        self.price_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.frame, text="Add Product", command=self.add_product).grid(row=3, column=1, pady=10)

        self.tree = ttk.Treeview(master, columns=("ID", "Name", "Quantity", "Price"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.pack(pady=20)
        self.tree.bind('<Double-1>', self.on_item_select)

        tk.Button(master, text="Update Selected", command=self.update_product).pack(side=tk.LEFT, padx=20)
        tk.Button(master, text="Delete Selected", command=self.delete_product).pack(side=tk.LEFT)
        tk.Button(master, text="Low Stock Report", command=self.low_stock_report).pack(side=tk.RIGHT, padx=20)

        self.load_products()

    def load_products(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor.execute("SELECT * FROM products")
        for product in cursor.fetchall():
            self.tree.insert('', 'end', values=product)
        conn.close()

    def add_product(self):
        name = self.name_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()

        if not name or not quantity.isdigit() or not self.is_float(price):
            messagebox.showerror("Invalid Data", "Enter valid data.")
            return

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
                       (name, int(quantity), float(price)))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product added!")
        self.load_products()

    def on_item_select(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])
        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, values[2])
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, values[3])

    def update_product(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select Item", "Select a product first.")
            return

        values = self.tree.item(selected, 'values')
        prod_id = values[0]

        name = self.name_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()

        if not name or not quantity.isdigit() or not self.is_float(price):
            messagebox.showerror("Invalid Data", "Enter valid data.")
            return

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET name=?, quantity=?, price=? WHERE id=?",
                       (name, int(quantity), float(price), prod_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product updated!")
        self.load_products()

    def delete_product(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select Item", "Select a product first.")
            return

        values = self.tree.item(selected, 'values')
        prod_id = values[0]

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (prod_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Deleted", "Product deleted!")
        self.load_products()

    def low_stock_report(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE quantity < 5")
        low_stock = cursor.fetchall()
        conn.close()

        report = "\n".join([f"ID: {p[0]}, Name: {p[1]}, Qty: {p[2]}, Price: {p[3]}" for p in low_stock]) \
            or "No low stock products."

        messagebox.showinfo("Low Stock Report", report)

    @staticmethod
    def is_float(val):
        try:
            float(val)
            return True
        except ValueError:
            return False


# ---------------- Run Program ----------------
if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()
