
resource "aws_s3_bucket" "mlops_bucket" {
  bucket = "mlops-projects-udemy"
}

resource "aws_iam_role" "mlops_role" {
  name = "mlops"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = var.user_arn
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}
resource "aws_iam_role_policy" "name" {
  name = "mlopsS3access"
  role = aws_iam_role.mlops_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:*",
          "s3-object-lambda:*"
        ]
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.mlops_bucket.bucket}",
          "arn:aws:s3:::${aws_s3_bucket.mlops_bucket.bucket}/*"
        ]
      }
    ]
  })
}

resource "aws_s3_account_public_access_block" "block_plublic" {
  depends_on              = [aws_s3_bucket.mlops_bucket]
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_policy" "role_access" {
    depends_on = [ aws_s3_bucket.mlops_bucket, aws_iam_role_policy.name ]
  bucket = aws_s3_bucket.mlops_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowRoleAccessOnly"
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.mlops_role.arn
        }
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.mlops_bucket.bucket}",
          "arn:aws:s3:::${aws_s3_bucket.mlops_bucket.bucket}/*"
        ]
      }
    ]
  })
}