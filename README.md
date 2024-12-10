# multi-container-application

The code in the repo is used to create multi container application.
It creates flask app with mongoDB in docker containers.
Repo includes ansible playbook for creating self signed certificate
for securing mongoDB with TLS.
Github actions workflow is included for building and deploying
app to the EC2 instance.

### 1. Create EC2 instance with terraform
  ```
  cd terraform
  terraform init
  terraform apply
  ```

### 2. Upload secrets to the github repo secrets
  ```
  cd scripts
  python secrets_upload.py
  ```

### 3. Deploy app to the server
  ```
  Github actions deploy app to a server either manually by
  triggering a workflow, or automatically when files listed in a workflow change.
  ```

### Addidional info

  - You need to have AWS credentials in ~/.aws/credentials for terraform to work.
  - Your AWS role should have all the necessary permissions to create EC2 instances.
  - Create .env file based on .env.example in repo

Link to the project details: [https://roadmap.sh/projects/multi-container-service](https://roadmap.sh/projects/multi-container-service).