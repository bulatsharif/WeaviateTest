# Deploy

### Building flutter main application
To build the flutter application, you have to follow the guides at the [Flutter site](https://docs.flutter.dev/get-started/install/windows/desktop) to install flutter on your machine.
Go to the "Install the Flutter SDK" header and choose "Download and install" instead of "Use VS code to install". Follow the guidelines.
Now you need to create some folder where you will save the application. Create it, and open terminal and follow to the folder.
```@bash
cd Desktop
mkdir flutter_app
cd flutter_app
```
After that, you have to clone the repository with the application.
```@bash
git clone https://gitlab.pg.innopolis.university/d.fatkullina/zakatcalcteam55.git
```
Now perform the following commands:
```@bash
cd zakatcalcteam55
cd flutter_app
flutter config --enable-web
flutter build web
```

### Preparing server
Now you have to login to your server via ssh or other methods.
The flutter application wil run nginx, therefore you have to perform the commands bellow
```@bash
sudo apt update
sudo apt upgrade
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```
We will transfer the build files via scp, therefore, you need to open port 22
```@bash
sudo ufw allow 22
```
Also, we will make some working directory. We have done this being in the **root** directory.
```@bash
cd root
mkdir ZakatSecond
cd ZakatSecond
```

### Transfering files
Go to your folder that created for flutter application,  go to flutter_app, go to build, go to web, and copy the path to the folder. In the end, you should something like below:
```@bash
C:\Users\username\Desktop\flutter_app\zakatcalcteam55\flutter_app\build\web
# The following example is for windows, it may vary depending on OS
```
Now you need to transfer the build files to the server. Consider the command bellow
```@bash
scp -r C:\username\Desktop\flutter_app\zakatcalcteam55\flutter_app\build\web\* username_for_server@your_server_ip:path/to/created/directory/
```
As an example, consider the command that we implemented:
```@bash
scp -r C:\Users\username\Desktop\flutter_app\zakatcalcteam55\flutter_app\build\web\* root@10.90.137.169:~/ZakatSecond/
```
Afterwards the server will ask you to enter password, do it.
### Server settings and running flutter application
Now you have your project in the root directory. However, it will cause some permission exceptions. Therefore, we will copy our project to another place
```@bash
sudo mkdir -p /var/www/zakatsecond/web 
sudo cp -r /root/ZakatSecond/* /var/www/zakatsecond/web/
```
Let give permissions in this folder:
```@bash
sudo chown -R www-data:www-data /var/www/zakatsecond/web
sudo chmod -R 755 /var/www/zakatsecond/web
```
Now, lets make the nginx config
```@bash
sudo nano /etc/nginx/sites-available/flutter_app
```
Enter the following:
```@bash
server { 
	listen 80; 
	server_name 10.90.137.169; # REPLACE IT WITH YOUR IP

	root /var/www/zakatsecond/web; 
	index index.html; 
	location / { 
	try_files $uri $uri/ /index.html; 
	} 
}
```

Press ctrl+x, then Y to save, then enter
Now perform these commands:
```@bash
sudo ln -s /etc/nginx/sites-available/flutter_app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```
Now  you can to the ip address and check out the application: http://10.90.137.169

### Backend

  
- **Docker**: The backend uses docker to deploy it. (It is not used for Flutter since nobody does that and we couldnt find any workable guide for that)
  
  [Link to the Docker Desktop](https://www.docker.com/products/docker-desktop/)  
  
  [Link to the Ubuntu Installion Guide](https://docs.docker.com/engine/install/ubuntu/)  
  
  
- **Cloning Repository**: The next step is to clone the repository into the working directory. This can be proceeded as follows:  
 ```  
   git clone https://github.com/bulatsharif/WeaviateTest.git  
 ```  
- **API Keys**: The project uses several API's that is used both in calculations and in the vector database. To deploy the project succesfully you have to obtain API keys at:  
  - [Mistal AI API](https://mistral.ai/)  
  - [JinaAI API](https://jina.ai/)  
  - [MetalPrice API](https://metalpriceapi.com/)  
- **Environment variables**: The project uses to environment variables in order to secure the API keys. You have to define these variables on your machine/server. Among the aforementioned three API keys, one have to also define the HOST variable.
In case of the server, you have to firstly obtain the IP of the server:  
```
  HOST=http://your_ip:8080  
 ```  
 The final environment variables file should follow the format:  
  ```  
  JINA_AI_API_KEY=jina_555666777111333bbbb333xxxx  
 MISTRAL_AI_API_KEY=555666777111333bbbb333xxxx 
 METAL_PRICE_API_KEY=555666777111333bbbb333xxxx 
 HOST=http://weaviate:8080
  ```  
**How to define environment variables?**
You can do that by going to the directory with the backend. In my case it is WeaviateTest
```
cd WeaviateTest
touch .env
nano .env
```
Enter the values, press ctrl+x, then y, then enter. Now you  have set them.
 - **Running Docker**: After completion of steps above, you can finally run the site by running Docker Container:  
  ```  
   docker compose up  
 ```
 - **Accesing the swagger**: After succesfully running the Docker Container, you can open the swagger at the: "http://your_ip:8000/docs#/"

### Editor application
The beginning deployment of flutter application was an warmup :3
Now you need to delete the existing configuration
```@bash
sudo rm /etc/nginx/sites-enabled/flutter_app
```
At this moment you should already have zakatcalcteam55 folder. Creator another folder, could be named editor
```
mkdir editor
cd editor
```
Clone the repository
```
git clone https://gitlab.pg.innopolis.university/rai.sabirov/editor.git
```
Go to the editor folder and build the application
```
flutter config --enable-web
cd editor
flutter config --enable-web
flutter build web
```
If there is some error, try to put these commands in random order and perform, and try to go out one folder up (to main editor folder) and also play with the commands. Eventually your build will be created.
As above, copy the path to the directory
```
C:\Users\username\Desktop\editor\editor
```
Go to your server, again to the root directory, and make some folder for the editor
```
mkdir editor
cd editor
```
Now you can copy the editor build to the recently created directory
```
scp -r C:\Users\username\Desktop\editor\editor\build\web\* root@10.90.137.169:~/editor/
```
Now copy these 
```
sudo mkdir -p /var/www/editor/web
sudo cp -r /root/editor/* /var/www/editor/web/
sudo chown -R www-data:www-data /var/www/editor/web
sudo chmod -R 755 /var/www/editor/web
```
Afterwards, let's configure the nginx config
```
sudo nano /etc/nginx/sites-available/multi_flutter_apps
```
Enter following:
```
server {
    listen 80;
    server_name 10.90.137.169; # REPLACE IT WITH YOUR IP

    location /app1/ {
        alias /var/www/zakatsecond/web/;
        try_files $uri $uri/ /index.html;
    }

    location /app2/ {
        alias /var/www/editor/web/;
        try_files $uri $uri/ /index.html;
    }
}
```

Now move to the directory /var/www/editor/web, and change the index.html, you should have this:
```
<head> 
	<base href="/app2/"> 
	<!-- other head elements --> 
</head>
```
Do the same but in /var/www/zakatsecond/web/
```
<head>
    <base href="/app1/">
    <!-- other head elements -->
</head>

```
Apply the final commands:
```
sudo ln -s /etc/nginx/sites-available/multi_flutter_apps /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Now you can access the main app at:
http://10.90.137.169/app1/
And editor at:
http://10.90.137.169/app2/
And swagger at:
http://10.90.137.169:8000/docs
