import os
import random
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk


class AddStudent:
    def __init__(self, data_processor):
        self.data_processor = data_processor

    '''----------------------------------------------------------------------------------------------------------------- ''' 

    def get_random_image(self, folder_path):
        files = os.listdir(folder_path)
        image_files = [file for file in files if file.endswith(('.png', '.jpg'))]
        if not image_files:
            raise FileNotFoundError("No image files found in the specified folder.")
        random_image = random.choice(image_files)
        return os.path.join(folder_path, random_image)
    

    def show_student_ui(self, view_profile_frame, student: object):
        print(f"displaying student {student}:")
        if not student:
            return
        
        label = ctk.CTkLabel(view_profile_frame, text=f"{student.get_name()}'s     Profile", font=("Mojang", 26), text_color="white", corner_radius=0, width=10)
        label.pack(pady=50, padx=150, anchor="w")

        folder_path = "app/images/face"
        random_image_path = self.get_random_image(folder_path)

        original_image = Image.open(random_image_path)
        resized_image = original_image.resize((200, 200), Image.LANCZOS) 
        student_image = ImageTk.PhotoImage(resized_image)

        self.label = ctk.CTkLabel(
            view_profile_frame,
            text=f"{student}",
            font=("Mojang", 20),
            text_color="white",
            image=student_image,   
            compound="left",                
            justify="left",
        )
        self.label.image = student_image  
        self.label.pack(pady=0, padx=150, anchor="w")


    def show_reg_ui(self, register_frame):
        """
        Create the student registration UI.
        """
        print("showing registration frame")
        scroll_frame = ctk.CTkScrollableFrame(register_frame, fg_color="#303030")
        scroll_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        self.lblErrors = ctk.CTkLabel(scroll_frame, text="", font=("Segoe UI", 15), text_color="red")
        self.lblErrors.pack(pady=10)  
    
        self.register_txt = ["Name", "Age", "Student  ID", "Email  Address", "Phone  Number"]
        self.register_entry = []
        for i in range(len(self.register_txt)):
            label = ctk.CTkLabel(scroll_frame, text=self.register_txt[i], font=("Mojang", 20), text_color="white", width=13, anchor="e")
            label.pack(pady=5, padx=20, anchor="w")  
            entry = ctk.CTkEntry(scroll_frame, width=40, font=("Segoe UI", 20), text_color="white")
            entry.pack(pady=5, padx=20, fill="x") 
            self.register_entry.append(entry)

        register_btn = ctk.CTkButton(scroll_frame, width=30, text="Register Student", font=("Mojang", 20), text_color="white", fg_color="#009047", hover_color="#064d2a", border_spacing=20, corner_radius=0, command=self.check_entries)
        register_btn.pack(pady=20)

    def check_entries(self):
        """
        Validate and create a new student from form input.
        """
        errors = []
        for i in range(len(self.register_entry)):
            if not self.register_entry[i].get().strip():  # Check for empty fields
                errors.append(f"You forgot to add the {self.register_txt[i]}!\n")

        if not errors:
            attributes = [
                self.register_entry[0].get().strip(),
                self.register_entry[1].get().strip(),
                self.register_entry[2].get().strip(),
                self.register_entry[3].get().strip(),
                self.register_entry[4].get().strip(),
            ]

            # result is either a student object if it successfully added a student or a dictionary containing errors
            result = self.data_processor.add_student_to_program(*attributes)

            if not isinstance(result, dict):
                self.lblErrors.configure(text="")

                response = CTkMessagebox(message="The student registration was successful.",
                    icon="check", option_1="Continue")
            
                response_get = response.get()

                if response_get:
                    for entry in self.register_entry:
                        entry.delete(0, ctk.END)
            else:
                self.lblErrors.configure(
                text=f"The Student ID {attributes[2]} is already taken"
            )
        else:
            self.lblErrors.configure(
                text=f"\n{''.join(errors)}"
            )