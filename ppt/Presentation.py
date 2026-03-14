from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Logo or decorative line
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Formula 1: The Pinnacle of Motorsport', 0, 1, 'R')
        self.line(10, 20, 200, 20)
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def slide_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(10)

    def slide_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 8, body)
        self.ln()

# Create PDF object
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)

# --- Slide 1: Title ---
pdf.add_page()
pdf.set_font('Arial', 'B', 24)
pdf.ln(50)
pdf.cell(0, 10, 'Formula 1', 0, 1, 'C')
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 10, 'The Pinnacle of Motorsport', 0, 1, 'C')
pdf.ln(20)
pdf.set_font('Arial', 'I', 14)
pdf.cell(0, 10, 'Engineering, Strategy, and Speed', 0, 1, 'C')

# --- Slide 2 ---
pdf.add_page()
pdf.slide_title('What is Formula 1?')
pdf.slide_body(
    "• The 'Formula': A strict set of rules (engine, chassis, fuel) that all teams must follow.\n\n"
    "• Global Series: Races take place in roughly 24 locations across 5 continents (e.g., Monaco, Silverstone, Las Vegas).\n\n"
    "• Two Championships:\n"
    "   1. Drivers' Championship (Individual glory)\n"
    "   2. Constructors' Championship (Team engineering & prize money)\n\n"
    "• Key Stat: Cars accelerate from 0 to 100 km/h in roughly 2.6 seconds."
)

# --- Slide 3 ---
pdf.add_page()
pdf.slide_title('The Car: An Engineering Marvel')
pdf.slide_body(
    "• Aerodynamics: Wings push the car down (Downforce) to stick to the track. An F1 car generates enough suction to drive upside down on a ceiling.\n\n"
    "• The Power Unit: A 1.6L V6 Turbo Hybrid engine. It is the most efficient engine in the world (over 50% thermal efficiency).\n\n"
    "• The Halo: A titanium bar above the cockpit that protects the driver's head from debris and crashes."
)

# --- Slide 4 ---
pdf.add_page()
pdf.slide_title('The Teams & Drivers')
pdf.slide_body(
    "• 10 Teams: There are 2 cars per team, making 20 drivers on the grid.\n\n"
    "• The Big Names: Ferrari, Mercedes, Red Bull, McLaren.\n\n"
    "• Team Dynamics: Your teammate is your biggest rival because they have the exact same car as you.\n\n"
    "• Legends: Michael Schumacher, Lewis Hamilton, Ayrton Senna, Max Verstappen."
)

# --- Slide 5 ---
pdf.add_page()
pdf.slide_title('The Race Weekend Format')
pdf.slide_body(
    "• Friday (Practice): Teams test their car setup and gather data on the track.\n\n"
    "• Saturday (Qualifying): Drivers try to set the fastest single lap. The fastest driver takes 'Pole Position' (1st place start).\n\n"
    "• Sunday (The Grand Prix): The main race (usually ~300km or 2 hours).\n\n"
    "• Pit Stops: Mechanics change all 4 tires in roughly 2.0 seconds."
)

# --- Slide 6 ---
pdf.add_page()
pdf.slide_title('Understanding the Flags')
pdf.slide_body(
    "• Green Flag: Go / Track Clear.\n\n"
    "• Yellow Flag: Hazard ahead (slow down, no passing).\n\n"
    "• Blue Flag: Let the faster car pass (you are being lapped).\n\n"
    "• Red Flag: Session stopped (bad crash or weather).\n\n"
    "• Chequered Flag: Race Over / Winner."
)

# --- Slide 7 ---
pdf.add_page()
pdf.slide_title('How Scoring Works (2026 Rules)')
pdf.slide_body(
    "Only the Top 10 finishers score points:\n\n"
    "• 1st Place: 25 Points\n"
    "• 2nd Place: 18 Points\n"
    "• 3rd Place: 15 Points\n"
    "• ...down to 10th Place: 1 Point.\n\n"
    "Note: Consistency is key. Winning one race is good, but finishing high in every race wins championships."
)

# --- Slide 8 ---
pdf.add_page()
pdf.slide_title('Why is it so Popular?')
pdf.slide_body(
    "• High Tech: It uses NASA-level engineering and technology.\n\n"
    "• High Stakes: One small mistake can cost millions of dollars.\n\n"
    "• The 'Soap Opera': The sport is full of rivalries, radio arguments, and team politics.\n\n"
    "• Access: Shows like 'Drive to Survive' have brought fans closer to the action than ever before."
)

# --- Output ---
pdf.output("F1_Presentation.pdf")
print("PDF generated successfully: F1_Presentation.pdf")