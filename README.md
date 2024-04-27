## **Project Structure**

``` bash
fastApi/
│
├── copywritingAgent/
│ ├── __init__.py
│ ├── router.py
│ ├── main.py
│ ├── .env
│
├── Dockerfile
├── README.md
├── docker-compose.yaml
└── requirements.txt
```


## Copywriting Agent API

This API provides endpoints for interacting with a copywriting agent. It allows users to generate copy for various purposes such as menu items, social media posts, advertising content, and newsletters.


## **How to Run**

1. **Download or Clone Repository:**
   - Download or clone the repository branch using the method of your choice. For example, if you have git installed on your machine, run the following command:
     ```bash
     https://github.com/jyotiyadav24/productionReady.git
     ```
     This will download the files into the ETL_pipeline folder.

2. **Ensure Python and Docker Installed:**
   - Ensure that both Python and Docker are installed on your machine.

3. **Navigate to the ETL_pipeline folder:**
   - Open a terminal and navigate to the fastApi folder:
     ```bash
     cd fastApi
     ```
   - Create a file named `.env` in the copywritingAgent folder and add the following credentials:
     
4. **Run Docker Images:**
   - Run the following command to start the Docker containers:
     ```bash
     docker-compose up
     ```
6. **Ensure Port Mapping:**
   - Ensure that the port mapping for the web application inside docker-compose.yml is set to port 8000, which is the default port.

7. **Test the Installation:**
   - Once the containers are running, you can test if the installation was successful by visiting the endpoints diiferent Endpoints below
     ```bash
     http://0.0.0.0:8000/docs/
     ```
8. **Stop Docker Containers:**
   - Open a new terminal and run the following command to stop the Docker containers:
     ```bash
     docker-compose down
     ```


## Endpoints
#### Process Menu
- **Endpoint:** `/menu/`
- **Method:** POST
- **Description:** Generates copy for menu items based on the provided goal.
- **Request Body:**
  - `goal`: str - The goal or purpose for generating the menu item copy.
- **Response:**
  - Returns the generated copy for the menu item.
 ![Alt text](<images/>)
    

#### Process Social Media
- **Endpoint:** `/socialMedia/`
- **Method:** POST
- **Description:** Generates copy for social media posts along with an optional image upload.
- **Request Body:**
  - `goal`: str - The goal or purpose for generating the social media post copy.
  - `image`: file - Optional. Image file to be included in the social media post.
- **Response:**
  - Returns the generated copy for the social media post.
 ![Alt text](<images/>)


#### Process Advertising
- **Endpoint:** `/advertising/`
- **Method:** POST
- **Description:** Generates copy for advertising content based on the provided goal and target interest.
- **Request Body:**
  - `goal`: str - The goal or purpose for generating the advertising content.
  - `interest`: str - The target interest or audience for the advertising content.
- **Response:**
  - Returns the generated copy for the advertising content.
 ![Alt text](<images/>)


#### Process Newsletter
- **Endpoint:** `/newsletter/`
- **Method:** POST
- **Description:** Generates copy for newsletter content based on the provided goal.
- **Request Body:**
  - `goal`: str - The goal or purpose for generating the newsletter content.
- **Response:**
  - Returns the generated copy for the newsletter content.
 ![Alt text](<images/>)


#### Error Handling
- If an error occurs during the processing of any request, the API will respond with an appropriate HTTP status code along with a detailed error message.
