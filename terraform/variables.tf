variable "ssh_key_filename" {
  description = "Path to ssh key file."
  default = "tfkey.pem"
}

variable "tf_key_name" {
  description = "Name of the ssh key"
  default = "TF_key"
}

variable "my_public_ip" {
  description = "IP to allow a connection to mongoDB"
  default = "127.0.0.1/32"
}
