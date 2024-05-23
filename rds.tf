resource "aws_db_instance" "db" {
  identifier                          = "${local.name}-db"
  allocated_storage                   = 5
  db_name                             = "${local.name}db"
  engine                              = "postgres"
  instance_class                      = "db.t3.micro"
  username                            = "postgres"
  manage_master_user_password         = true
  storage_encrypted                   = true
  multi_az                            = false
  availability_zone                   = data.aws_availability_zone.this.name
  db_subnet_group_name                = aws_db_subnet_group.this.name
  vpc_security_group_ids              = [aws_security_group.rds_lambda.id]
  apply_immediately                   = true
  storage_type                        = "standard"
  iam_database_authentication_enabled = true
  enabled_cloudwatch_logs_exports     = ["upgrade", "postgresql"]
  skip_final_snapshot                 = true
}