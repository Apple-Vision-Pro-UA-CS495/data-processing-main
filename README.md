Local:   
To run, create Python virtual environment.   
Install dependencies.  
Then, use this command to run the server: uvicorn server:app --host 0.0.0.0 --port 8000 --reload   
Run the client file to test.  
  
EC2:  
Start EC2 instance in AWS  
In terminal run: ssh -i path_to_pem_file\aws_pem.pem ec2-user@100.28.154.221 (This is for windows CMD)    
cd into "app" directory  
Run: uvicorn server:app --host 0.0.0.0 --port 8000  
When you are done, make sure to stop the server and stop the EC2 instance to save money  

For use in application:
Use this link to hit the Websocket server: ws://100.28.154.221:8000/ws   

