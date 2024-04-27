# **Project Structure**

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


# Copywriting Agent API

This API provides endpoints for interacting with a copywriting agent. It allows users to generate copy for various purposes such as menu items, social media posts, advertising content, and newsletters.

## Endpoints

### Process Menu
- **Endpoint:** `/menu/`
- **Method:** POST
- **Description:** Generates copy for menu items based on the provided goal.
- **Request Body:**
  - `goal`: str - The goal or purpose for generating the menu item copy.
- **Response:**
  - Returns the generated copy for the menu item.
 
    

### Process Social Media
- **Endpoint:** `/socialMedia/`
- **Method:** POST
- **Description:** Generates copy for social media posts along with an optional image upload.
- **Request Body:**
  - `goal`: str - The goal or purpose for generating the social media post copy.
  - `image`: file - Optional. Image file to be included in the social media post.
- **Response:**
  - Returns the generated copy for the social media post.



### Process Advertising
- **Endpoint:** `/advertising/`
- **Method:** POST
- **Description:** Generates copy for advertising content based on the provided goal and target interest.
- **Request Body:**
  - `goal`: str - The goal or purpose for generating the advertising content.
  - `interest`: str - The target interest or audience for the advertising content.
- **Response:**
  - Returns the generated copy for the advertising content.



### Process Newsletter
- **Endpoint:** `/newsletter/`
- **Method:** POST
- **Description:** Generates copy for newsletter content based on the provided goal.
- **Request Body:**
  - `goal`: str - The goal or purpose for generating the newsletter content.
- **Response:**
  - Returns the generated copy for the newsletter content.



## Error Handling
- If an error occurs during the processing of any request, the API will respond with an appropriate HTTP status code along with a detailed error message.
