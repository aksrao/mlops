resource "random_string" "unique_name" {
  length  = "4"
  special = false
}

resource "aws_s3_bucket" "mlops_bucket" {
  bucket = "mlops${random_string.unique_name.id}"
}

resource "aws_iam_role" "mlops" {
  name = "mlops"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com" 
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}
resource "aws_iam_role_policy" "name" {
  name = "mlopss3access"
  role = aws_iam_role.mlops.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
            "s3:*",
            "s3-object-lambda:*"
        ]
        Resource = [
          aws_s3_bucket.mlops_bucket.arn,
          "${aws_s3_bucket.mlops_bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_s3_account_public_access_block" "block_plublic" {
    depends_on = [ aws_s3_bucket.mlops_bucket ]
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
}
resource "aws_s3control_bucket_policy" "role_access" {
    bucket = aws_s3_bucket.mlops_bucket.id
    policy = jsonencode({
        Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowRoleAccessOnly"
        Effect    = "Allow"
        Principal = {
          AWS = data.aws_iam_role.mlops_role.arn
        }
        Action    = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.secure_bucket.arn,
          "${aws_s3_bucket.secure_bucket.arn}/*"
        ]
      }
    ]
    })
}