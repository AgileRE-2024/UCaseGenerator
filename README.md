### README for Designer: Use Case Tools

#### Overview
Designer: Use Case Tools is a web application designed to simplify the creation of software documentation. It allows users to generate various UML diagrams and specifications automatically, helping developers, analysts, and project managers document system requirements efficiently. 

#### Features
1. *Use Case Diagram*  
   - Input actor, features, and interactions to generate a visual Use Case Diagram.  
   - Ensures efficient system planning and documentation.

2. *Use Case Specification*  
   - Fill out a detailed specification template including actors, descriptions, scenarios, and conditions.  
   - Serves as a guideline for implementing functional requirements.

3. *Class Diagram*  
   - Create diagrams by entering class names, attributes, and operations.  
   - Supports defining relationships between classes.

4. *Activity Diagram*  
   - Automatically generate Activity Diagrams based on Use Case Specifications.  
   - Visualize system processes for clearer business understanding.

5. *Sequence Diagram*  
   - Enter boundary, controller, and entity details to create Sequence Diagrams.  
   - Illustrates object interactions and system execution flows.

#### Target Users
- *Software Developers*: For rapid UML diagram creation and accurate project documentation.  
- *System Analysts*: To streamline system analysis and requirement documentation.  
- *Project Managers*: For ensuring timely and structured documentation.  
- *General Users*: Intuitive interface designed for both technical and non-technical users.

#### Technology Stack
- *Frontend*: HTML, CSS, JavaScript  
- *Backend*: Django Framework (Python)  
- *Database*: MySQL  
- *Architecture*: MVC (Model-View-Controller)  
- *External API*: PlantUML for diagram generation  

#### System Requirements
- *Operating System*: Any OS with a web browser.  
- *Hardware*: Laptop or PC with internet access.  
- *Browser*: Modern browser with JavaScript enabled.

#### How to Use
1. *Input Data*: Navigate to the desired diagram or specification feature and fill in the required fields.  
2. *Generate Output*: Click "Generate" to produce the desired diagram or specification.

## Installation (Development Environment)

To set up and run the Designer: Use Case Tools project locally, follow these steps:

1. *Clone the Repository*:
   bash
   git clone <repository-url>
   

2. *Set Up a Virtual Environment*:
   Create and activate a virtual environment:
   bash
   python -m venv env
   source env/bin/activate # On Windows use `env\Scripts\activate`
   

3. *Install Dependencies*:
   Ensure you have Python installed, then run:
   bash
   pip install -r requirements.txt
   

4. *Start the Development Server*:
   Launch the server using:
   bash
   python manage.py runserver
   

5. *Access the Application*:
   Open your browser and navigate to http://127.0.0.1:8000/.


#### Contributions
This project is collaboratively developed by the following members:
- *Dzakwan Fiodora Syafi’i*: Use Case Diagram
- *Ahmad Ramdhan Najem Khimsa Salamy*: Use Case Specification, Activity Diagram
- *Alya Gita Ramadhani*: Class Diagram
- *Sisilia Leonita Pasaribu*: Sequence Diagram
- * *Muhammad Fadhil Putra Pratama*: Class Diagram and Sequence Diagram Front End


For additional details, please refer to the Software Requirements Specification (SRS) document.
