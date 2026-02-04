import ttkbootstrap as tb
from ttkbootstrap.constants import PRIMARY, SECONDARY, SUCCESS, DANGER, WARNING, INFO
from ttkbootstrap.dialogs import Messagebox
from book_management import BookManagement
from member_management import MemberManagement
from issue_return import IssueReturn
from PIL import Image, ImageTk


class LibraryDashboard:
    def __init__(self, root, role="user"):  # Default to "user" as string
        self.root = root
        self.role = role
        self.root.title("Library Dashboard")
        self.root.geometry("800x500")

        # Title
        tb.Label(self.root, text="Library Dashboard", font=("Arial", 18, "bold"), bootstyle=PRIMARY).pack(pady=10)

        # Sidebar
        self.sidebar = tb.Frame(self.root, bootstyle="secondary", width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)  # Prevent shrinking

        # Main content area (right side)
        self.main_frame = tb.Frame(self.root, bootstyle="dark")
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Add role-based controls
        if self.role == "admin":
            self.add_admin_controls()
        elif self.role == "librarian":
            self.add_librarian_controls()
        elif self.role == "user":
            self.add_user_controls()
        self.add_sidebar_logo()   
        self.show_welcome_screen()
        # ✅ Add profile card at bottom
        self.add_profile_card()

    def add_admin_controls(self):

        tb.Button(
            self.sidebar,
            text="📚 Manage Books",
            bootstyle="success-outline",
            command=self.open_book_management
        ).pack(fill="x", pady=6, padx=12)

        tb.Button(
            self.sidebar,
            text="👥 Manage Members",
            bootstyle="success-outline",
            command=self.open_member_management
        ).pack(fill="x", pady=6, padx=12)

        tb.Button(
            self.sidebar,
            text="🔄 Issue / Return Books",
            bootstyle="info-outline",
            command=self.open_issue_return
        ).pack(fill="x", pady=6, padx=12)

        tb.Button(
            self.sidebar,
            text="🗑 Delete Book",
            bootstyle="danger-outline",
            command=self.delete_book
        ).pack(fill="x", pady=6, padx=12)

        tb.Button(
            self.sidebar,
            text="📑 Export Reports",
            bootstyle="warning-outline",
            command=self.export_reports
        ).pack(fill="x", pady=6, padx=12)


    def add_librarian_controls(self):

        tb.Button(
            self.sidebar,
            text="📚 Manage Books",
            bootstyle="success-outline",
            command=self.open_book_management
        ).pack(fill="x", pady=6, padx=12)

        tb.Button(
            self.sidebar,
            text="🔄 Issue / Return Books",
            bootstyle="info-outline",
            command=self.open_issue_return
        ).pack(fill="x", pady=6, padx=12)

    def add_user_controls(self):

        tb.Button(
            self.sidebar,
            text="📖 My Borrowed Books",
            bootstyle="info-outline",
            command=self.open_history
        ).pack(fill="x", pady=6, padx=12)

    
    def add_sidebar_logo(self):
        try:
            sidebar_width = 200  # same as your sidebar width

            img = Image.open("assets/library.png")
            img = img.resize((sidebar_width, 90), Image.LANCZOS)

            self.sidebar_logo = ImageTk.PhotoImage(img)

            logo_label = tb.Label(self.sidebar, image=self.sidebar_logo)
            logo_label.pack(side="bottom", fill="x")

        except Exception as e:
            print("Sidebar logo error:", e)

    def add_profile_card(self):

        # Profile container at bottom of sidebar
        self.profile_frame = tb.Frame(
            self.sidebar,
            bootstyle="dark",
            padding=12
        )
        self.profile_frame.pack(side="bottom", fill="x", pady=15)

        # ✅ Avatar icon (NO IMAGE FILE)
        tb.Label(
            self.profile_frame,
            text="👤",
            font=("Segoe UI", 34),
            bootstyle="light"
        ).pack(pady=(0, 5))

        # Admin/User name
        tb.Label(
            self.profile_frame,
            text="Admin User",
            font=("Segoe UI", 11, "bold"),
            bootstyle="light"
        ).pack()

        # Role display
        tb.Label(
            self.profile_frame,
            text=f"Role: {self.role.upper()}",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        ).pack(pady=(0, 8))

        # Logout button
        tb.Button(
            self.profile_frame,
            text="Logout",
            bootstyle="danger-outline",
            command=self.logout
        ).pack(fill="x")


        
    def logout(self):
        Messagebox.show_info("Logout", "You have been logged out!")

        # Close dashboard window
        self.root.destroy()

        # Optionally reopen login screen here later


    
    # Placeholder methods - replace with real functionality later
    def open_book_management(self):
        self.clear_main_frame()
        BookManagement(self.main_frame)


    def open_member_management(self):
        self.clear_main_frame()
        MemberManagement(self.main_frame)


    def open_issue_return(self):
        self.clear_main_frame()
        IssueReturn(self.main_frame)


    def delete_book(self):
        self.clear_main_frame()
        tb.Label(self.main_frame, text="Delete Book (Admin Only)", 
                 font=("Arial", 16)).pack(pady=20)

    def export_reports(self):
        self.clear_main_frame()
        tb.Label(self.main_frame, text="Export Reports (Admin Only)", 
                 font=("Arial", 16)).pack(pady=20)

    def open_history(self):
        self.clear_main_frame()
        tb.Label(self.main_frame, text="Your Borrowed Books History", 
                 font=("Arial", 16)).pack(pady=20)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
    def show_welcome_screen(self):
        self.clear_main_frame()
        self.add_watermark()

        tb.Label(
            self.main_frame,
            text="Welcome! Select an option from the sidebar.",
            font=("Segoe UI", 16, "bold"),
            bootstyle="info"
        ).pack(pady=(40, 20))
              
        
    def add_watermark(self):
        try:
            wm = Image.open("assets/watermark.jpg").convert("RGBA")
            wm = wm.resize((700, 460), Image.LANCZOS)

            # Reduce opacity
            alpha = wm.split()[3]
            alpha = alpha.point(lambda p: p * 0.04)  # 8% opacity
            wm.putalpha(alpha)

            self.watermark_img = ImageTk.PhotoImage(wm)

            watermark_label = tb.Label(
                self.main_frame,
                image=self.watermark_img,
                bootstyle="inverse-dark"
            )
            watermark_label.place(relx=0.5, rely=0.5, anchor="center")

        except Exception as e:
            print("Watermark error:", e)

    def fade_in_image(self, img_path):
        base_img = Image.open(img_path).convert("RGBA")
        base_img = base_img.resize((360, 220), Image.LANCZOS)

        self.fade_frames = []
        for i in range(0, 21):
            alpha = int(200 * (i / 20))
            img = base_img.copy()
            img.putalpha(alpha)
            self.fade_frames.append(ImageTk.PhotoImage(img))

        self.fade_label = tb.Label(self.main_frame, bootstyle="inverse-dark")
        self.fade_label.pack(pady=20)

        self._fade_step = 0
        self.animate_fade()

    def animate_fade(self):
        if self._fade_step < len(self.fade_frames):
            self.fade_label.configure(image=self.fade_frames[self._fade_step])
            self.fade_label.image = self.fade_frames[self._fade_step]
            self._fade_step += 1
            self.root.after(40, self.animate_fade)

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = LibraryDashboard(root, role="admin")  # Change to "librarian" or "user" to test roles
    root.mainloop()