import customtkinter as ctk
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI




load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

if GEMINI_API_KEY:
    client = OpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
else:
    client = None




ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class StudyMate(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("StudyMate — AI Study Assistant")
        self.geometry("1200x720")
        self.minsize(1050, 650)

        self.current_page = "Dashboard"

        self.colors = {
            "bg": "#0F1117",
            "sidebar": "#151821",
            "card": "#191D27",
            "card2": "#1E2330",
            "accent": "#6C63FF",
            "accent_hover": "#8178FF",
            "text": "#F5F7FA",
            "muted": "#9CA3AF",
            "success": "#35C759",
            "danger": "#FF5C5C",
            "border": "#292F3D"
        }

        self.configure(fg_color=self.colors["bg"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()

        self.content_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors["bg"],
            corner_radius=0
        )
        self.content_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.show_dashboard()


    

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=245,
            corner_radius=0,
            fg_color=self.colors["sidebar"]
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # Logo
        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        logo_frame.pack(
            padx=22,
            pady=(28, 35),
            fill="x"
        )

        logo_icon = ctk.CTkLabel(
            logo_frame,
            text="🎓",
            font=ctk.CTkFont(size=30)
        )
        logo_icon.pack(side="left")

        logo_text_frame = ctk.CTkFrame(
            logo_frame,
            fg_color="transparent"
        )
        logo_text_frame.pack(
            side="left",
            padx=10
        )

        ctk.CTkLabel(
            logo_text_frame,
            text="StudyMate",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color=self.colors["text"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo_text_frame,
            text="AI Study Assistant",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["muted"]
        ).pack(anchor="w")


        # Navigation title
        ctk.CTkLabel(
            self.sidebar,
            text="MAIN MENU",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color="#6F7787"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )


        # Navigation buttons
        self.nav_buttons = {}

        self.add_nav_button(
            "🏠",
            "Dashboard",
            self.show_dashboard
        )

        self.add_nav_button(
            "🤖",
            "AI Tutor",
            self.show_ai_tutor
        )

        self.add_nav_button(
            "📝",
            "Quiz",
            self.show_quiz
        )

        self.add_nav_button(
            "🌤️",
            "Weather",
            self.show_weather
        )

        self.add_nav_button(
            "📖",
            "Dictionary",
            self.show_dictionary
        )


        # Bottom settings
        bottom_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        bottom_frame.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )

        self.add_nav_button(
            "⚙️",
            "Settings",
            self.show_settings,
            parent=bottom_frame
        )


        # User card
        user_card = ctk.CTkFrame(
            self.sidebar,
            fg_color=self.colors["card"],
            corner_radius=14
        )
        user_card.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=(0, 5)
        )

        ctk.CTkLabel(
            user_card,
            text="👩🏻‍💻",
            font=ctk.CTkFont(size=25)
        ).pack(
            side="left",
            padx=12,
            pady=10
        )

        user_text = ctk.CTkFrame(
            user_card,
            fg_color="transparent"
        )
        user_text.pack(
            side="left",
            pady=8
        )

        ctk.CTkLabel(
            user_text,
            text="Student",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(anchor="w")

        ctk.CTkLabel(
            user_text,
            text="Keep learning 🚀",
            font=ctk.CTkFont(size=10),
            text_color=self.colors["muted"]
        ).pack(anchor="w")


    def add_nav_button(
        self,
        icon,
        text,
        command,
        parent=None
    ):

        if parent is None:
            parent = self.sidebar

        button = ctk.CTkButton(
            parent,
            text=f"  {icon}    {text}",
            height=44,
            corner_radius=10,
            anchor="w",
            fg_color="transparent",
            hover_color="#222735",
            text_color=self.colors["muted"],
            font=ctk.CTkFont(size=13),
            command=command
        )

        button.pack(
            fill="x",
            padx=12 if parent == self.sidebar else 0,
            pady=3
        )

        self.nav_buttons[text] = button


    def update_active_nav(self, active):

        for name, button in self.nav_buttons.items():

            if name == active:

                button.configure(
                    fg_color="#252A3A",
                    text_color=self.colors["text"]
                )

            else:

                button.configure(
                    fg_color="transparent",
                    text_color=self.colors["muted"]
                )


    

    def clear_content(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()


    def page_header(
        self,
        title,
        subtitle
    ):

        header = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        header.pack(
            fill="x",
            padx=35,
            pady=(30, 15)
        )

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=self.colors["text"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text=subtitle,
            font=ctk.CTkFont(size=13),
            text_color=self.colors["muted"]
        ).pack(
            anchor="w",
            pady=(5, 0)
        )


    def create_card(
        self,
        parent,
        width=None,
        height=None
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["card"],
            corner_radius=16,
            border_width=1,
            border_color=self.colors["border"]
        )

        if width:
            card.configure(width=width)

        if height:
            card.configure(height=height)

        return card


   

    def show_dashboard(self):

        self.clear_content()
        self.update_active_nav("Dashboard")

        self.page_header(
            "Good morning, Student 👋",
            "Ready to learn something new today?"
        )


        # Top stats
        stats_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        stats_frame.pack(
            fill="x",
            padx=35,
            pady=10
        )

        stats_frame.grid_columnconfigure(
            (0, 1, 2, 3),
            weight=1
        )

        self.stat_card(
            stats_frame,
            0,
            "📚",
            "Study Sessions",
            "12",
            "+3 this week"
        )

        self.stat_card(
            stats_frame,
            1,
            "🔥",
            "Current Streak",
            "7 Days",
            "Keep it going!"
        )

        self.stat_card(
            stats_frame,
            2,
            "📝",
            "Quizzes Done",
            "18",
            "85% avg. score"
        )

        self.stat_card(
            stats_frame,
            3,
            "⏱️",
            "Study Time",
            "14.5h",
            "This month"
        )


        # Lower section
        lower = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        lower.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(15, 30)
        )

        lower.grid_columnconfigure(0, weight=2)
        lower.grid_columnconfigure(1, weight=1)
        lower.grid_rowconfigure(0, weight=1)


        # Progress card
        progress_card = self.create_card(lower)
        progress_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        ctk.CTkLabel(
            progress_card,
            text="📈 Your Study Progress",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(22, 5)
        )

        ctk.CTkLabel(
            progress_card,
            text="Weekly learning goal",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["muted"]
        ).pack(
            anchor="w",
            padx=22
        )

        progress = ctk.CTkProgressBar(
            progress_card,
            height=12,
            corner_radius=6,
            progress_color=self.colors["accent"]
        )

        progress.pack(
            fill="x",
            padx=22,
            pady=(22, 8)
        )

        progress.set(0.72)

        progress_text = ctk.CTkFrame(
            progress_card,
            fg_color="transparent"
        )
        progress_text.pack(
            fill="x",
            padx=22
        )

        ctk.CTkLabel(
            progress_text,
            text="72% completed",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(side="left")

        ctk.CTkLabel(
            progress_text,
            text="7.2 / 10 hours",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=self.colors["muted"]
        ).pack(side="right")


        # Quick actions
        ctk.CTkLabel(
            progress_card,
            text="Quick Actions",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(35, 12)
        )

        quick_frame = ctk.CTkFrame(
            progress_card,
            fg_color="transparent"
        )
        quick_frame.pack(
            fill="x",
            padx=22
        )

        self.quick_button(
            quick_frame,
            "🤖 Ask AI",
            self.show_ai_tutor
        )

        self.quick_button(
            quick_frame,
            "📝 Take Quiz",
            self.show_quiz
        )

        self.quick_button(
            quick_frame,
            "📖 Dictionary",
            self.show_dictionary
        )


        # Right card
        activity_card = self.create_card(lower)
        activity_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        ctk.CTkLabel(
            activity_card,
            text="✨ Today's Focus",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(22, 15)
        )

        focus_items = [
            ("🤖", "Ask AI Tutor", "Clear your doubts"),
            ("🧠", "Practice Quiz", "Test your knowledge"),
            ("📖", "Learn a Word", "Expand vocabulary")
        ]

        for icon, title, desc in focus_items:

            item = ctk.CTkFrame(
                activity_card,
                fg_color=self.colors["card2"],
                corner_radius=12
            )

            item.pack(
                fill="x",
                padx=15,
                pady=6
            )

            ctk.CTkLabel(
                item,
                text=icon,
                font=ctk.CTkFont(size=22)
            ).pack(
                side="left",
                padx=12,
                pady=10
            )

            text_frame = ctk.CTkFrame(
                item,
                fg_color="transparent"
            )
            text_frame.pack(
                side="left",
                pady=8
            )

            ctk.CTkLabel(
                text_frame,
                text=title,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                )
            ).pack(anchor="w")

            ctk.CTkLabel(
                text_frame,
                text=desc,
                font=ctk.CTkFont(size=10),
                text_color=self.colors["muted"]
            ).pack(anchor="w")


    def stat_card(
        self,
        parent,
        column,
        icon,
        title,
        value,
        subtitle
    ):

        card = self.create_card(parent)

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=6
        )

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        top.pack(
            fill="x",
            padx=16,
            pady=(15, 3)
        )

        ctk.CTkLabel(
            top,
            text=icon,
            font=ctk.CTkFont(size=22)
        ).pack(side="left")

        ctk.CTkLabel(
            top,
            text=title,
            font=ctk.CTkFont(size=11),
            text_color=self.colors["muted"]
        ).pack(
            side="left",
            padx=8
        )

        ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=16,
            pady=(5, 0)
        )

        ctk.CTkLabel(
            card,
            text=subtitle,
            font=ctk.CTkFont(size=10),
            text_color=self.colors["success"]
        ).pack(
            anchor="w",
            padx=16,
            pady=(2, 15)
        )


    def quick_button(
        self,
        parent,
        text,
        command
    ):

        button = ctk.CTkButton(
            parent,
            text=text,
            height=38,
            corner_radius=10,
            fg_color=self.colors["card2"],
            hover_color="#2A3040",
            border_width=1,
            border_color=self.colors["border"],
            command=command
        )

        button.pack(
            side="left",
            padx=(0, 8)
        )


    
    def show_ai_tutor(self):

        self.clear_content()
        self.update_active_nav("AI Tutor")

        self.page_header(
            "AI Tutor 🤖",
            "Ask anything and learn with your personal AI study assistant."
        )


        main = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        main.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(5, 30)
        )


        # Chat area
        chat_card = self.create_card(main)
        chat_card.pack(
            fill="both",
            expand=True
        )


        # Chat header
        chat_header = ctk.CTkFrame(
            chat_card,
            fg_color="transparent"
        )
        chat_header.pack(
            fill="x",
            padx=22,
            pady=15
        )

        ctk.CTkLabel(
            chat_header,
            text="🤖 StudyMate AI",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).pack(side="left")

        self.ai_status = ctk.CTkLabel(
            chat_header,
            text="● Online",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["success"]
        )
        self.ai_status.pack(
            side="right"
        )


        # Chat textbox
        self.chat_box = ctk.CTkTextbox(
            chat_card,
            corner_radius=12,
            fg_color="#12151D",
            border_width=1,
            border_color=self.colors["border"],
            font=ctk.CTkFont(size=13),
            wrap="word"
        )

        self.chat_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        self.chat_box.insert(
            "end",
            "StudyMate AI 🤖\n\n"
            "Hi! I'm your AI study assistant.\n"
            "Ask me anything about your studies. 📚\n\n"
            "Try asking:\n"
            "• Explain KNN in simple words\n"
            "• What is a confusion matrix?\n"
            "• Explain OOP with an example\n\n"
        )

        self.chat_box.configure(
            state="disabled"
        )


        # Input area
        input_frame = ctk.CTkFrame(
            chat_card,
            fg_color="transparent"
        )
        input_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.question_entry = ctk.CTkEntry(
            input_frame,
            height=48,
            placeholder_text="Ask your study question...",
            corner_radius=12,
            border_width=1,
            border_color=self.colors["border"],
            fg_color="#12151D",
            font=ctk.CTkFont(size=13)
        )

        self.question_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.question_entry.bind(
            "<Return>",
            lambda event: self.ask_question()
        )

        ctk.CTkButton(
            input_frame,
            text="Ask AI  ➜",
            width=120,
            height=48,
            corner_radius=12,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.ask_question
        ).pack(
            side="left",
            padx=(10, 0)
        )


        # Clear button
        ctk.CTkButton(
            chat_card,
            text="Clear Chat",
            width=90,
            height=28,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#252A35",
            text_color=self.colors["muted"],
            command=self.clear_chat
        ).pack(
            anchor="e",
            padx=20,
            pady=(0, 12)
        )


    def clear_chat(self):

        self.chat_box.configure(state="normal")

        self.chat_box.delete(
            "1.0",
            "end"
        )

        self.chat_box.insert(
            "end",
            "StudyMate AI 🤖\n\n"
            "Chat cleared! Ask me a new question. 📚\n\n"
        )

        self.chat_box.configure(state="disabled")


    def ask_question(self):

        question = self.question_entry.get().strip()

        if not question:
            return

        if client is None:

            self.add_chat(
                "⚠️ Error",
                "Gemini API key not found. Please check your .env file."
            )

            return


        self.add_chat(
            "You",
            question
        )

        self.question_entry.delete(
            0,
            "end"
        )

        self.ai_status.configure(
            text="● Thinking...",
            text_color="#F59E0B"
        )

        self.update_idletasks()


        try:

            response = client.chat.completions.create(
                model="gemini-3.6-flash",
                messages=[
                    {
                        "role": "system",
                        "content":
                        "You are StudyMate AI, a friendly study tutor. "
                        "Explain concepts clearly and simply for college students. "
                        "Use examples and bullet points when useful."
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            answer = response.choices[0].message.content

            self.add_chat(
                "StudyMate AI 🤖",
                answer
            )

            self.ai_status.configure(
                text="● Online",
                text_color=self.colors["success"]
            )

        except Exception as e:

            self.add_chat(
                "⚠️ Error",
                str(e)
            )

            self.ai_status.configure(
                text="● Error",
                text_color=self.colors["danger"]
            )


    def add_chat(
        self,
        sender,
        message
    ):

        self.chat_box.configure(
            state="normal"
        )

        self.chat_box.insert(
            "end",
            f"\n{sender}\n"
        )

        self.chat_box.insert(
            "end",
            f"{message}\n"
        )

        self.chat_box.insert(
            "end",
            "\n" + "─" * 70 + "\n"
        )

        self.chat_box.see("end")

        self.chat_box.configure(
            state="disabled"
        )


   

    def show_quiz(self):

        self.clear_content()
        self.update_active_nav("Quiz")

        self.page_header(
            "Quiz Generator 📝",
            "Generate an AI-powered quiz to test your knowledge."
        )


        card = self.create_card(
            self.content_frame
        )

        card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(5, 30)
        )


        ctk.CTkLabel(
            card,
            text="Create a Quiz",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        ctk.CTkLabel(
            card,
            text="Enter a topic and StudyMate AI will create questions for you.",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["muted"]
        ).pack(
            anchor="w",
            padx=25
        )


        self.quiz_topic = ctk.CTkEntry(
            card,
            height=48,
            placeholder_text="Example: Machine Learning, Python, DBMS...",
            corner_radius=12
        )

        self.quiz_topic.pack(
            fill="x",
            padx=25,
            pady=20
        )


        ctk.CTkButton(
            card,
            text="✨ Generate Quiz",
            height=45,
            corner_radius=12,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.generate_quiz
        ).pack(
            padx=25,
            anchor="w"
        )


        self.quiz_output = ctk.CTkTextbox(
            card,
            height=350,
            corner_radius=12,
            fg_color="#12151D",
            font=ctk.CTkFont(size=13)
        )

        self.quiz_output.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )


    def generate_quiz(self):

        topic = self.quiz_topic.get().strip()

        if not topic:
            self.quiz_output.delete("1.0", "end")
            self.quiz_output.insert(
                "end",
                "⚠️ Please enter a topic first."
            )
            return

        if client is None:
            self.quiz_output.delete("1.0", "end")
            self.quiz_output.insert(
                "end",
                "⚠️ Gemini API key not found."
            )
            return


        self.quiz_output.delete(
            "1.0",
            "end"
        )

        self.quiz_output.insert(
            "end",
            "✨ Generating your quiz...\n\n"
        )

        self.update_idletasks()


        try:

            response = client.chat.completions.create(
                model="gemini-3.6-flash",
                messages=[
                    {
                        "role": "system",
                        "content":
                        "Create a student-friendly quiz. "
                        "Give 5 multiple choice questions with four options "
                        "and clearly mention the correct answer."
                    },
                    {
                        "role": "user",
                        "content":
                        f"Create a quiz about: {topic}"
                    }
                ]
            )

            quiz = response.choices[0].message.content

            self.quiz_output.delete(
                "1.0",
                "end"
            )

            self.quiz_output.insert(
                "end",
                quiz
            )

        except Exception as e:

            self.quiz_output.delete(
                "1.0",
                "end"
            )

            self.quiz_output.insert(
                "end",
                f"⚠️ Error:\n\n{e}"
            )


    

    def show_weather(self):

        self.clear_content()
        self.update_active_nav("Weather")

        self.page_header(
            "Weather 🌤️",
            "Check the current weather for any city."
        )


        card = self.create_card(
            self.content_frame
        )

        card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(5, 30)
        )


        self.weather_city = ctk.CTkEntry(
            card,
            height=48,
            placeholder_text="Enter city name...",
            corner_radius=12
        )

        self.weather_city.pack(
            fill="x",
            padx=25,
            pady=(30, 15)
        )


        ctk.CTkButton(
            card,
            text="🔍 Get Weather",
            height=45,
            corner_radius=12,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            command=self.get_weather
        ).pack(
            padx=25,
            anchor="w"
        )


        self.weather_result = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(size=18),
            justify="left"
        )

        self.weather_result.pack(
            padx=25,
            pady=40,
            anchor="w"
        )


    def get_weather(self):

        city = self.weather_city.get().strip()

        if not city:
            self.weather_result.configure(
                text="⚠️ Please enter a city."
            )
            return


        try:

            geo_url = (
                "https://geocoding-api.open-meteo.com/v1/search"
                f"?name={city}&count=1&language=en&format=json"
            )

            geo_response = requests.get(
                geo_url,
                timeout=10
            )

            geo_data = geo_response.json()

            if "results" not in geo_data:

                self.weather_result.configure(
                    text="❌ City not found."
                )

                return


            location = geo_data["results"][0]

            latitude = location["latitude"]
            longitude = location["longitude"]

            weather_url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitude={latitude}"
                f"&longitude={longitude}"
                "&current=temperature_2m,relative_humidity_2m,"
                "apparent_temperature,wind_speed_10m"
            )

            weather_response = requests.get(
                weather_url,
                timeout=10
            )

            weather = weather_response.json()["current"]

            result = (
                f"📍 {location['name']}\n\n"
                f"🌡️ Temperature: {weather['temperature_2m']}°C\n"
                f"💧 Humidity: {weather['relative_humidity_2m']}%\n"
                f"🌡️ Feels like: {weather['apparent_temperature']}°C\n"
                f"💨 Wind: {weather['wind_speed_10m']} km/h"
            )

            self.weather_result.configure(
                text=result
            )

        except Exception as e:

            self.weather_result.configure(
                text=f"⚠️ Error: {e}"
            )


   

    def show_dictionary(self):

        self.clear_content()
        self.update_active_nav("Dictionary")

        self.page_header(
            "Dictionary 📖",
            "Search meanings, examples and pronunciations."
        )


        card = self.create_card(
            self.content_frame
        )

        card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(5, 30)
        )


        self.dictionary_word = ctk.CTkEntry(
            card,
            height=48,
            placeholder_text="Enter an English word...",
            corner_radius=12
        )

        self.dictionary_word.pack(
            fill="x",
            padx=25,
            pady=(30, 15)
        )


        ctk.CTkButton(
            card,
            text="🔎 Search Word",
            height=45,
            corner_radius=12,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            command=self.search_dictionary
        ).pack(
            padx=25,
            anchor="w"
        )


        self.dictionary_output = ctk.CTkTextbox(
            card,
            corner_radius=12,
            fg_color="#12151D",
            font=ctk.CTkFont(size=13)
        )

        self.dictionary_output.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )


    def search_dictionary(self):

        word = self.dictionary_word.get().strip()

        if not word:

            self.dictionary_output.delete(
                "1.0",
                "end"
            )

            self.dictionary_output.insert(
                "end",
                "⚠️ Please enter a word."
            )

            return


        try:

            url = (
                "https://api.dictionaryapi.dev/api/v2/"
                f"entries/en/{word}"
            )

            response = requests.get(
                url,
                timeout=10
            )

            if response.status_code != 200:

                self.dictionary_output.delete(
                    "1.0",
                    "end"
                )

                self.dictionary_output.insert(
                    "end",
                    "❌ Word not found."
                )

                return


            data = response.json()[0]

            output = f"📖 {data['word']}\n\n"


            for meaning in data.get("meanings", []):

                output += (
                    f"Part of speech: "
                    f"{meaning.get('partOfSpeech', 'N/A')}\n\n"
                )

                for definition in meaning.get(
                    "definitions",
                    []
                )[:3]:

                    output += (
                        f"• {definition.get('definition', '')}\n"
                    )

                    example = definition.get(
                        "example"
                    )

                    if example:
                        output += (
                            f"  Example: {example}\n"
                        )

                    output += "\n"


            self.dictionary_output.delete(
                "1.0",
                "end"
            )

            self.dictionary_output.insert(
                "end",
                output
            )

        except Exception as e:

            self.dictionary_output.delete(
                "1.0",
                "end"
            )

            self.dictionary_output.insert(
                "end",
                f"⚠️ Error: {e}"
            )


   
    def show_settings(self):

        self.clear_content()
        self.update_active_nav("Settings")

        self.page_header(
            "Settings ⚙️",
            "Customize your StudyMate experience."
        )


        card = self.create_card(
            self.content_frame
        )

        card.pack(
            fill="x",
            padx=35,
            pady=10
        )


        # Appearance
        row = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=25,
            pady=20
        )

        text = ctk.CTkFrame(
            row,
            fg_color="transparent"
        )

        text.pack(side="left")

        ctk.CTkLabel(
            text,
            text="Appearance",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(anchor="w")

        ctk.CTkLabel(
            text,
            text="Choose your preferred theme",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["muted"]
        ).pack(anchor="w")


        self.theme_menu = ctk.CTkOptionMenu(
            row,
            values=[
                "Dark",
                "Light",
                "System"
            ],
            width=130,
            height=38,
            command=self.change_theme
        )

        self.theme_menu.pack(
            side="right"
        )

        self.theme_menu.set("Dark")


        # About
        about = self.create_card(
            self.content_frame
        )

        about.pack(
            fill="x",
            padx=35,
            pady=10
        )

        ctk.CTkLabel(
            about,
            text="🎓 About StudyMate",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 8)
        )

        ctk.CTkLabel(
            about,
            text=(
                "StudyMate is an AI-powered desktop study assistant "
                "designed to help students learn faster."
            ),
            font=ctk.CTkFont(size=12),
            text_color=self.colors["muted"],
            wraplength=700,
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 22)
        )


    def change_theme(self, choice):

        if choice == "Dark":
            ctk.set_appearance_mode("dark")

        elif choice == "Light":
            ctk.set_appearance_mode("light")

        else:
            ctk.set_appearance_mode("system")




if __name__ == "__main__":

    app = StudyMate()

    app.mainloop()