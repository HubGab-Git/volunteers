resource "aws_security_group" "rds_lambda" {
  name        = "rds-lambda"
  description = "RDS Security Group which allow only Lambda Security Gruop to connect Database"
  vpc_id      = aws_vpc.main.id
}

resource "aws_security_group" "lambda_rds" {
  name        = "lambda-rds"
  description = "Lambda Security Group which can connect RDS Database"
  vpc_id      = aws_vpc.main.id
}

resource "aws_vpc_security_group_ingress_rule" "allow_postgress" {
  security_group_id            = aws_security_group.rds_lambda.id
  referenced_security_group_id = aws_security_group.lambda_rds.id
  from_port                    = 5432
  ip_protocol                  = "tcp"
  to_port                      = 5432
}


resource "aws_vpc_security_group_egress_rule" "allow_postgress" {
  security_group_id            = aws_security_group.lambda_rds.id
  referenced_security_group_id = aws_security_group.rds_lambda.id
  from_port                    = 5432
  ip_protocol                  = "tcp"
  to_port                      = 5432
}

resource "aws_vpc_security_group_egress_rule" "allow_secretsmanager" {
  security_group_id            = aws_security_group.lambda_rds.id
  referenced_security_group_id = aws_security_group.allow_secretsmanager_access.id
  from_port                    = 443
  ip_protocol                  = "tcp"
  to_port                      = 443
}

resource "aws_security_group" "allow_secretsmanager_access" {
  vpc_id      = aws_vpc.main.id
  name        = "secret-manager-vpc-endpoint"
  description = "Allow to connect secret manager"
}

resource "aws_vpc_security_group_ingress_rule" "allow_secretsmanager" {
  security_group_id            = aws_security_group.allow_secretsmanager_access.id
  referenced_security_group_id = aws_security_group.lambda_rds.id
  from_port                    = 443
  ip_protocol                  = "tcp"
  to_port                      = 443
}

resource "aws_vpc_security_group_ingress_rule" "allow_secretsmanager_ingress" {
  security_group_id            = aws_security_group.lambda_rds.id 
  referenced_security_group_id = aws_security_group.allow_secretsmanager_access.id
  from_port                    = 443
  ip_protocol                  = "tcp"
  to_port                      = 443
}