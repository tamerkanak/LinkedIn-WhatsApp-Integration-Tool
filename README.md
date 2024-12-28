LinkedIn-WhatsApp Integration Tool

Overview

This tool integrates WhatsApp and LinkedIn to streamline connection requests. By listening to WhatsApp messages for LinkedIn profile links, the application automatically sends connection requests on LinkedIn. The GUI enables users to monitor and manage the integration process easily.

Features

WhatsApp Web QR Code Integration: Connects to WhatsApp Web and captures QR code for authentication.

LinkedIn Connection Requests: Automates sending LinkedIn connection requests for profiles shared via WhatsApp messages.

Real-Time Status Updates: Displays the current status of processes in the GUI.

Error Handling: Provides detailed error messages and warnings for seamless troubleshooting.

Installation

Prerequisites

Python 3.8 or higher

Google Chrome browser

ChromeDriver compatible with the installed Chrome version

Dependencies

Install the required Python libraries:

pip install selenium pillow tkinter

Usage Instructions

Steps to Run the Application

Clone the repository or download the script.

Ensure that ChromeDriver is in your system's PATH.

Run the script using:

python script_name.py

Enter your LinkedIn email and password in the GUI.

Scan the displayed QR code using WhatsApp Web.

The program will start listening for LinkedIn profile links in the specified WhatsApp chat and send connection requests automatically.

Key Functionalities

GUI Overview

Title Bar: Displays the application name.

Developer Information: Credits the creator of the tool.

LinkedIn Login: Accepts email and password for LinkedIn.

Status Section: Provides updates on current operations.

QR Code Display: Shows the QR code for WhatsApp Web authentication.

Automated Processes

Listens to a specific WhatsApp chat for LinkedIn profile links.

Processes messages to extract LinkedIn profile URLs.

Sends connection requests on LinkedIn for valid profile links.

Code Structure

Key Functions

generate_qr_image(driver, qr_label)

Captures and displays the WhatsApp Web QR code in the GUI.

select_chat(driver, chat_name, status_label)

Selects a specific chat in WhatsApp Web by its name.

process_messages(driver, status_label, processed_links, email)

Monitors messages for LinkedIn links and processes them.

start_process(email, password, status_label, qr_label)

Initiates the program, logs into LinkedIn, and starts listening to WhatsApp messages.

send_connection_request(driver, profile_url, email, status_label)

Handles sending connection requests on LinkedIn.

create_gui()

Sets up and displays the graphical user interface.

Additional Features

Error Handling: Includes try-except blocks to catch and report errors during execution.

Threading: Runs processes in the background to keep the GUI responsive.

Scroll Support: Enables smooth navigation in the GUI for lengthy content.

Limitations

Requires manual WhatsApp Web authentication for each session.

Limited to the specific chat name defined in the code.

May need updates to accommodate changes in LinkedIn or WhatsApp Web interfaces.

Future Enhancements

Add support for multiple chats.

Implement OAuth for LinkedIn login.

Include advanced error reporting and logging.

License

This tool is licensed under the MIT License. Feel free to use and modify it as needed.

Developer

Tamer KanakEmail: tamerkanak75@gmail.com

For any issues or contributions, please contact the developer or submit a pull request on GitHub.
