provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "v2c_ec2" {
  ami           = "ami-0c2d94d94a7ff4f77"  # Ubuntu 22.04 LTS
  instance_type = "t2.micro"

  key_name               = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.v2c_sg.id]
  user_data              = file("setup.sh")

  tags = {
    Name = "V2C-ML-Backend"
  }
}

resource "aws_security_group" "v2c_sg" {
  name        = "v2c-sg-ml"
  description = "Allow SSH and Flask"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "v2c_logs" {
  bucket = "v2c-driving-logs-${random_id.bucket_suffix.hex}"
  force_destroy = true
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}
