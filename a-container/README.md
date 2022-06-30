# soho-caddie

You can easily create quotes and invoices with this application.  
Back end of this system is built in Python, Flask, SQLite, etc., that is easy to customize.  
And, the View layer uses Vue.js and is effective for design changes.  
Want to use another DBMS of your choice instead of SQLite?  
OK!   
As you like!  
We adopted SQLAlchemy as the SQL wrapper. You can use any DBMS that it supports.  

## Get started

1.Make the docker image

```
$docker build -t scaddie:0.1 .
```

2.Run the docker image

```
$docker run -d -it --name scaddie -p 5001:80 scaddie:0.1
```

2.Brawse soho-caddie page

```
http://<your sever IP>:5001
```
If you can see "HelloWorld!" ,it does working

```
http://<your sever IP>:5001/invoice-page
```

Can you see INVOICE ?  
Congratulations!!
