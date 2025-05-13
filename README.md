##Project##


## AI_SW개발자 과정 05/13 finalprojectDay ##
## Team Member : 강태훈, 임정환, 박성호 ##
강태훈 : 기획서, 간단한 보고, 구현코드
임정환 : 시연, 간단한 보고, 구현코드
박성호 : 기획서, 간단한 보고, 구현코드



##📋 Project Structure##

/your-flask-project
    /static
        /images
            police_logo.png   ← Police logo image
        /css
            style.css         ← Web page styles
    /templates
        index.html           ← Main web page
    app.py                    ← Flask server code
    requirements.txt          ← List of required libraries

##How to use##
1. Clone the Project
First, you need to clone the project from GitHub.

1.1 Install Git
Windows:

Download and install Git from Git download page.

Mac/Linux:

Open the terminal and install Git using the following command:


sudo apt install git  # Ubuntu/Linux
brew install git      # Mac
1.2 Clone the Project from GitHub
bash

git clone https://github.com/yourusername/smoking-detection-system.git
cd smoking-detection-system
2. Install Required Libraries
To run the project, you need to install the libraries listed in requirements.txt.

2.1 Set Up Virtual Environment (Optional)
It’s recommended to use a virtual environment to avoid dependency conflicts with other projects.


# Create a virtual environment (Windows)
python -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate

# Activate the virtual environment (Mac/Linux)
source venv/bin/activate
2.2 Install the Required Libraries
bash

pip install -r requirements.txt
3. Download the YOLOv5 Model
The project uses the YOLOv5 model to detect smokers. You need the best.pt model file.

3.1 Prepare the YOLOv5 Model
If you already have the best.pt model file, place it in the models/ folder.

If you need to download a new model, you can get it from the YOLOv5 GitHub.

4. Set Up Webcam
The project uses the webcam to stream video in real-time and detect smokers. Make sure your webcam is properly connected.

4.1 Check Webcam Connection
Ensure that the webcam is correctly connected. On Windows, check the Device Manager. On Linux, use the lsusb command to verify the connection.

4.2 Allow Camera Access (Browser)
Make sure the browser has permission to use the camera for video streaming. Allow camera access when prompted by the browser.

5. Run the Server
Start the Flask server to launch the web application.

5.1 Run the Flask Server
bash
python app.py
The server will run, and you can access the web application at http://127.0.0.1:5000/.

5.2 Access the Web App
Open a browser and go to http://127.0.0.1:5000/.

You should see the video stream where the system detects smokers in real-time.

6. Smoking Detection and Data Logging
6.1 Detecting Smokers
While streaming the video in the web application, if a smoker is detected, a warning message ("Stop Smoking Please.") will appear on the screen.

The detected smoker data is logged in the server’s smoker folder.

6.2 Viewing Smoking Statistics
On the web page, you can view the smoking statistics, including the number of times smoking was detected.

The statistics will update each time a smoker is detected.

7. Shut Down the Project
To stop the project, terminate the Flask server.




# Stop the server by pressing Ctrl + C
8. Additional Setup (Optional)
Adjust Camera Index: If the webcam does not work, try changing the camera index in the code from cv2.VideoCapture(0) to another number.

Train the Model: If you want higher accuracy, you can fine-tune the YOLOv5 model or perform additional training for better performance.


