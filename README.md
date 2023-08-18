
  
<!-- PROJECT -->  
<p align="center">  
  <h3 align="center">   
   Ikea Assignment - Warehouse Software
  </h3>   
</p>  
  
<!-- ABOUT THE PROJECT -->  
## 🤔 Introduction  

Ikea Warehouse software to manage inventory(products and articles.)
<br />   
  
  
<!-- INSTALLATION -->  

# 🔨 Installation and Running

Install the required dependencies by running:

  
1. Clone this repository  
  
2. Run docker compose `docker-compose up -d --build` (be sure if your ports 8000 and 5433 are available)

3. Check the API running here http://localhost:8000/docs and try it out the endpoint.

<br />  
  
## 📚 Project Files Overview
- app
  - routes
    - `article.py`: article route with the endpoints. 
    - `product.py`: product route with the endpoints. 
  - `main.py`: main file to run the API service and swagger.
  - `models.py`: ORM Table Mapping.
  - `database.py`: Database connection.
- `requirements.txt`: A file containing project dependencies.
- `.gitignore`: Defines files that should be ignored by Git.
- `docker-compose.yml`: A Docker file to run Postgres Database,ETL Process and REST API(Fast API)

## 🔓 Author and Acknowledgements

- **Author**: [Paulo Mota](https://www.linkedin.com/in/paulo-mota-955218a2/)<br>
