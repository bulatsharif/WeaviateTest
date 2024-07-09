
# Zakat Barakat API

#### **Project Description**:
- **Context and Problem**: Zakat is an obligatory type of almsgiving in Islam. Every muslim whose wealth passes through so-called Nisab threshold has to pay Zakat. However, calculating Zakat involves many assets which makes this process difficult. Most of the existing calculator oversimplify the process. Moreover, they often do not include a knowledge base with information about Zakat and other adjacent functionality. 
- **The project mission**: The software project *Zakat Barakat* aimes at fullfilling the existing functionality gap by providing comprehensive calculator, knowledge base, and several other functionalities.
- **This repository**: This repository represents the implementation of the API backend part of the project. The project divided into the *user application* and the *editor application*. The repository contains the API for both of the applications, which are handled in gitlab.






## Deployment

- **Docker**: The project uses the Docker to create a container and comfortly deploy the site. Therefore, to deploy the this repository one have to install Docker Desktop (if running locally) or Docker on the server.

  [Link to the Docker Desktop](https://www.docker.com/products/docker-desktop/)

  [Link to the Ubuntu Installion Guide](https://docs.docker.com/engine/install/ubuntu/)

- **Git**: After installation of the Docker, you have to install the Git onto the server or to the local computer:

  [Git Installation Guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

- **Cloning Repository**: The next step is to clone the repository into the working directory. This can be proceeded as follows:
  ```bash
    git clone https://github.com/bulatsharif/innopolis_cpp_summer_2024.git
  ```

- **API Keys**: The project uses several API's that is used both in calculations and in the vector database. To deploy the project succesfully you have to obtain API keys at:
  - [Mistal AI API](https://mistral.ai/)
  - [JinaAI API](https://jina.ai/)
  - [MetalPrice API](https://metalpriceapi.com/)
- **Environment variables**: The project uses to environment variables in order to secure the API keys. You have to define these variables on your machine/server. Among the aforementioned three API keys, one have to also define the HOST variable. In case of local machine, your configuration would be: 
  ```bash
  HOST=http://weaviate:8080

  ```
  In case of the server, you have to firstly obtain the IP of the server:
  ```bash
  HOST=http://your_ip:8080
  ```
  The final environment variables file should follow the format:
  ```
  JINA_AI_API_KEY=jina_555666777111333bbbb333xxxx
  MISTRAL_AI_API_KEY=555666777111333bbbb333xxxx
  METAL_PRICE_API_KEY=555666777111333bbbb333xxxx
  HOST=http://weaviate:8080
  ```
- **Running Docker**: After completion of steps above, you can finally run the site by running Docker Container:
  ```
    docker compose up
  ```
- **Accesing the swagger**: After succesfully running the Docker Container, you can open the swagger at the: "http://your_ip:8000/docs#/"




## Usage/Examples


You can use the API in your frontend application. To see how this API can be integrated into applications you can refer to the Flutter part repository of the application. 
Some examples of requests:
- Get Article from Knowledge Base:
```
curl -X 'GET' \
  'http://localhost:8000/knowledge-base/get-articles' \
  -H 'accept: application/json'
```
- Calculate Zakat Ushr:
```
curl -X 'POST' \
  'http://localhost:8000/calculator/zakat-ushr' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "crops": [
    {
      "type": "Buckwheat",
      "quantity": 100500
    }
  ],
  "is_ushr_land": true,
  "is_irrigated": true
}'
```
- Delete Organization
```
curl -X 'DELETE' \
  'http://localhost:8000/organization/edit/delete-organization/0fc1c03c-f96a-4925-963e-7aa7711fac89' \
  -H 'accept: application/json'
```
## Tech Stack

**Python API**: FastAPI, Pydantic

**Database**: Weaviate

**Deploy**: Docker


## License

[MIT License](https://choosealicense.com/licenses/mit/)

Copyright (c) [2024] [Zakat Barakat]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

