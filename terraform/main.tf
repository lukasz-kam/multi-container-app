resource "aws_security_group" "web_sg" {
  name_prefix = "web-sg-"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

   ingress {
    from_port   = 27017
    to_port     = 27017
    protocol    = "tcp"
    cidr_blocks = ["172.17.0.0/16", var.my_public_ip]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_key_pair" "tf_key" {
  key_name   = var.tf_key_name
  public_key = tls_private_key.rsa_key.public_key_openssh
}

resource "tls_private_key" "rsa_key" {
  algorithm = "RSA"
  rsa_bits = 4096
}

resource "local_file" "TF-key" {
  content = tls_private_key.rsa_key.private_key_pem
  filename = var.ssh_key_filename
}

resource "aws_instance" "flask_instance" {
  ami           = "ami-04b54ebf295fe01d7"
  instance_type = "t3.micro"
  security_groups = [aws_security_group.web_sg.name]

  associate_public_ip_address = true

  key_name = var.tf_key_name

  tags = {
    Name = "FlaskInstance"
  }

  provisioner "local-exec" {
    command = <<EOT
      echo "[flask_instance]" > ../ansible/inventory
      echo "${self.public_ip} ansible_ssh_user=ec2-user ansible_ssh_private_key_file=$(pwd)/${var.ssh_key_filename}" >> ../ansible/inventory
    EOT
  }
}