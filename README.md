**Demo Video** 

https://youtu.be/QKIbJRsfKrI


**AI Workout Planner Project**

**Table of Contents**

- **Overview**
- **Prerequisites**
- **Docker Image Details**
- **Build Instructions**
- **Run Instructions**
- **Load Balancer Configuration**
- **Testing Steps & Evidence**
- **API Information**
- **Challenges Faced**
- **Hardening Steps**
- **Credits**

**Overview**  
The AI Workout Planner application provides a user-friendly interface to interact with the AI Workout Planner API. The backend is developed in Python using Flask, containerized with Docker, and deployed on two Ubuntu-based web servers running Nginx. An HAProxy load balancer distributes traffic evenly between the two servers using a round-robin algorithm.

**Prerequisites**  

- **Docker**: Installed on the host machine for building and running containers.
- **Docker Hub Account**: For pulling/pushing images (optional for local use).
- **Ubuntu OS**: For web servers (Web01 and Web02) and the load balancer.
- **Nginx**: Installed on Web01 and Web02 for serving the application.
- **HAProxy**: Installed on the load balancer container.
- **API Key**: Obtain an API key from RapidAPI for the AI Workout Planner API.
- **curl**: For testing the load balancer.

**Docker Image Details**  
The project uses the following Docker images, available on Docker Hub under the mony66 repository:

| **Image Name**                        | **Tag** | **Image ID**   | **Size**     |
|---------------------------------------|---------|----------------|--------------|
| mony66/api_summative_alu-lb-01        | latest  | ea350ddec930   | 145.85 MB    |
| mony66/api_summative_alu-web-01       | latest  | ae99a5a071fc   | 341.16 MB    |
| mony66/api_summative_alu-web-02       | latest  | 80fe3d3db3c2   | 341.16 MB    |

**Docker Hub Repository**: mony66

**Build Instructions**  
To build the Docker images locally, follow these steps:

1. **Clone the Repository**:  
   ```bash
   git clone <your-repository-url>
   cd <repository-directory>
   ```

2. **Build the Web Server Image** (for api_summative_alu-web-01 and api_summative_alu-web-02):  
   ```bash
   docker build -t mony66/api_summative_alu-web-01:latest -f Dockerfile.web .
   docker build -t mony66/api_summative_alu-web-02:latest -f Dockerfile.web .
   ```

3. **Build the Load Balancer Image** (for api_summative_alu-lb-01):  
   ```bash
   docker build -t mony66/api_summative_alu-lb-01:latest -f Dockerfile.lb .
   ```

4. **Push Images to Docker Hub** (optional):  
   ```bash
   docker push mony66/api_summative_alu-web-01:latest
   docker push mony66/api_summative_alu-web-02:latest
   docker push mony66/api_summative_alu-lb-01:latest
   ```

**Note**: Ensure you have a Dockerfile.web for the web servers and a Dockerfile.lb for the load balancer in your project directory.

**Run Instructions**  
To run the application locally or on Web01/Web02:

1. **Run Web Server Containers**:  
   - On Web01:  
     ```bash
     docker run -d -p 80:80 --name web01 mony66/api_summative_alu-web-01:latest
     ```
   - On Web02:  
     ```bash
     docker run -d -p 80:80 --name web02 mony66/api_summative_alu-web-02:latest
     ```

2. **Run Load Balancer Container**:  
   ```bash
   docker run -d -p 80:80 --name lb01 mony66/api_summative_alu-lb-01:latest
   ```

3. **Environment Variables**:  
   Pass the API key as an environment variable to the web server containers:  
   ```bash
   docker run -d -p 80:80 -e RAPIDAPI_KEY=<your-api-key> --name web01 mony66/api_summative_alu-web-01:latest
   docker run -d -p 80:80 -e RAPIDAPI_KEY=<your-api-key> --name web02 mony66/api_summative_alu-web-02:latest
   ```

**Load Balancer Configuration**  
The load balancer uses HAProxy with a round-robin algorithm to distribute traffic between Web01 and Web02. Below is the relevant HAProxy configuration snippet:  
```haproxy
frontend http_front
   bind *:80
   default_backend web_backend

backend web_backend
   balance roundrobin
   server web01 <web01-ip>:80 check
   server web02 <web02-ip>:80 check
```

**Reloading HAProxy**:  
To apply configuration changes without downtime:  
```bash
docker exec lb01 haproxy -f /usr/local/etc/haproxy/haproxy.cfg -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)
```

Replace <web01-ip> and <web02-ip> with the actual IP addresses of Web01 and Web02.

**Testing Steps & Evidence**  
To verify that the round-robin load balancing works:

1. **Set Custom Headers**:  
   - Configure Nginx on Web01 to include a custom header:  
     ```nginx
     add_header X-Served-By web01;
     ```
   - On Web02:  
     ```nginx
     add_header X-Served-By web02;
     ```

2. **Test with curl**:  
   Run the following command multiple times to request the load balancer IP:  
   ```bash
   curl -I http://<load-balancer-ip>
   ```

   Inspect the response headers. The X-Served-By header alternates between web01 and web02, confirming round-robin load balancing.

**Example Output**:  
```
HTTP/1.1 200 OK
X-Served-By: web01
...

HTTP/1.1 200 OK
X-Served-By: web02
...
```

**API Information**  
The application uses the AI Workout Planner API from RapidAPI, which provides four endpoints:  

- **Generate Workout Plan**: Creates personalized workout plans.  
- **Nutrition Advice**: Provides dietary recommendations.  
- **Exercise Details**: Offers detailed information about specific exercises.  
- **Food Plate Analysis**: Analyzes a food plate from a provided URL.  

**Official Documentation**: AI Workout Planner API on RapidAPI  
To use the API, sign up on RapidAPI, subscribe to the AI Workout Planner API, and obtain an API key. Pass the API key as an environment variable (see Run Instructions).

**Challenges Faced**  
During development, I encountered several challenges:  

- **API Complexity**: The AI Workout Planner API has four distinct endpoints, each serving different functions (workout planning, nutrition advice, exercise details, and food plate analysis). Integrating these endpoints required careful handling of their unique requirements and response formats. I overcame this by thoroughly studying the API documentation and implementing modular code to handle each endpoint separately.  
- **Backend Development**: Using Python with Flask for the backend provided security benefits but required significant effort to configure properly. I spent considerable time ensuring secure API key handling and optimizing Flask for production use.  
- **Load Balancing**: Setting up HAProxy for round-robin load balancing was initially complex. Ensuring proper configuration and verifying traffic distribution required multiple iterations. I resolved this by testing with custom headers and curl, as described in Testing Steps & Evidence.

**Hardening Steps**  
To secure the application and avoid baking sensitive information like API keys into the Docker images:  

- **Environment Variables**: Pass the RapidAPI key as an environment variable during container runtime (see Run Instructions). This ensures the key is not hardcoded in the image or source code.  
- **Docker Secrets**: For production, consider using Docker Secrets to manage sensitive data. Example:  
  ```bash
  echo "<your-api-key>" | docker secret create rapidapi_key -
  docker service create --secret rapidapi_key mony66/api_summative_alu-web-01:latest
  ```  
- **.env File**: Locally, store the API key in a .env file and load it using a library like python-dotenv. Ensure the .env file is included in .gitignore to prevent accidental commits.  
- **Nginx Configuration**: Use Nginx to enforce HTTPS and restrict access to sensitive endpoints if necessary.

**Credits**  

- **AI Workout Planner API Developers**: Thank you to the team behind the AI Workout Planner API on RapidAPI for providing a robust and feature-rich API.  
- **RapidAPI**: For hosting and managing the API, making integration straightforward. [RapidAPI](https://rapidapi.com)  
- **Flask Community**: For providing extensive documentation and resources for building secure Python backends. [Flask Documentation](https://flask.palletsprojects.com)  
- **HAProxy**: For the reliable load balancing solution. [HAProxy Documentation](http://www.haproxy.org)  
- **Docker**: For enabling containerization and simplifying deployment. [Docker Documentation](https://docs.docker.com)  
- **Nginx**: For serving the application efficiently. [Nginx Documentation](https://nginx.org/en/docs/)
  
**Screenshots of testing the load balancer** 

<img width="1076" height="726" alt="Image" src="https://github.com/user-attachments/assets/5b14b89d-9e8c-42b9-8ea5-cad06d05f907" />

**Demo Video**
https://youtu.be/QKIbJRsfKrI
