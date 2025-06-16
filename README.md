# **Omniversify Keystroke Visualizer ⌨️🖱️✨**

A simple, modern, and highly configurable open-source tool to display your keystrokes and mouse actions on screen. Perfect for creating tutorials, live streaming, presentations, or just making your screencasts look more professional\! 🚀

Created during an episode of the **\#MGDB (Moroccan Game Developer Blog)**, this tool is built with flexibility in mind.

### **🌟 Features**

* **Keyboard, Click & Scroll Display:** Visualizes every input, including keyboard keys, mouse clicks (LMB, RMB, MMB), and scroll wheel actions (▲/▼).  
* **Highly Customizable:** Control the look, feel, and position of the overlay using a simple config.ini file. No code editing required\!  
* **Custom Fonts & Colors:** Easily change the font, size, color, and background to match your brand or desktop theme.  
* **Flexible Positioning:** Place the overlay anywhere on your screen: top, bottom, center, or any of the corners, with fine-tuned pixel offsets.  
* **Lightweight & Cross-Platform:** Built with Python and standard libraries, making it efficient and easy to run on most Linux distributions.

### **🚀 Setup & Installation**

Getting the visualizer up and running is easy. Just follow these three steps.

#### **1\. Get the Files**

First, clone this repository or download the files to a directory on your computer.

git clone \<your-repo-url-here\>  
cd omniversify-keystroke-visualizer

You should have two main files in your directory:

* visualizer.py (The main application)  
* config.ini (The configuration file)

#### **2\. Install Dependencies**

This tool requires Python 3 and a few libraries.

a) Install pip and tkinter:  
These packages are often required on Linux systems.

* **On Debian/Ubuntu:**  
  sudo apt update  
  sudo apt install python3-pip python3-tk

* **On Fedora:**  
  sudo dnf install python3-pip python3-tkinter

* **On Arch Linux:**  
  sudo pacman \-Syu python-pip tk

b) Install pynput:  
This is the Python library used to listen for keyboard and mouse input.  
pip install pynput

#### **3\. Run the Application**

Once the dependencies are installed, you can run the visualizer from your terminal:

python visualizer.py

The application will start running in the background. To stop it, simply press Ctrl+C in the terminal where it's running.

### **⚙️ Configuration (config.ini)**

The magic of this tool lies in the config.ini file. Open it with any text editor to change how the visualizer looks and behaves.

#### **\[Appearance\] Section**

| Setting | Description | Example |
| :---- | :---- | :---- |
| font\_family | The name of the font to use. Must be installed on your system. | Tajawal |
| font\_size | The size of the font. | 24 |
| text\_color | The color of the text. Can be a name or hex code. | white |
| bg\_color | The background color of the key overlay. | \#2E2E2E |
| padding\_x | Horizontal space (in pixels) inside the key. | 20 |
| padding\_y | Vertical space (in pixels) inside the key. | 10 |
| duration\_ms | How long the key stays on screen, in milliseconds. | 1500 |

#### **\[Position\] Section**

| Setting | Description | Example |
| :---- | :---- | :---- |
| position | The base position of the overlay on the screen. | bottom-left |
| y\_offset | An extra vertical offset in pixels. Negative values move it up. | \-150 |
| x\_offset | An extra horizontal offset in pixels. | 50 |

**Available position options:**

* top-left, top-center, top-right  
* center  
* bottom-left, bottom-center, bottom-right

### **❤️ Contributing**

This is an open-source project\! Contributions are welcome. Feel free to fork the repository, make improvements, and submit a pull request. You can also open an issue to report a bug or suggest a new feature.