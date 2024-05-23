resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = data.aws_availability_zone.this.name

  tags = {
    Name = "public-subnet"
  }
}

resource "aws_subnet" "private" {
  count             = 2 # Jedna subnet na każdą Availability Zone
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 2)
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
  tags = {
    Name = "private-subnet-${count.index}"
  }
}

resource "aws_db_subnet_group" "this" {
  name       = "db-subnet"
  subnet_ids = [aws_subnet.private[0].id, aws_subnet.private[1].id]
}