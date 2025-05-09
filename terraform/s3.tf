# Create folders in S3 bucket
resource "aws_s3_object" "input_folder" {
  bucket = local.s3_config.bucket
  key    = "${local.s3_config.prefix}/input/"
  content_type = "application/x-directory"
}

resource "aws_s3_object" "output_folder" {
  bucket = local.s3_config.bucket
  key    = "${local.s3_config.prefix}/output/"
  content_type = "application/x-directory"
}

resource "aws_s3_object" "temp_folder" {
  bucket = local.s3_config.bucket
  key    = "${local.s3_config.prefix}/temp/"
  content_type = "application/x-directory"
}

resource "aws_s3_object" "scripts_folder" {
  bucket = local.s3_config.bucket
  key    = "${local.s3_config.prefix}/scripts/"
  content_type = "application/x-directory"
}

# Upload staging script to S3
resource "aws_s3_object" "handle_schema_change_job_script" {
  bucket = local.s3_config.bucket
  key    = "${local.s3_config.prefix}/scripts/handle_schema_change_job.py"
  source = "${path.module}/../scripts/glue_jobs/handle_schema_change_job.py"
  etag   = filemd5("${path.module}/../scripts/glue_jobs/handle_schema_change_job.py")
}

# Upload logger utility to S3
resource "aws_s3_object" "logger_utility" {
  bucket = local.s3_config.bucket
  key    = "${local.s3_config.prefix}/scripts/utils/logger.py"
  source = "${path.module}/../scripts/glue_jobs/utils/logger.py"
  etag   = filemd5("${path.module}/../scripts/glue_jobs/utils/logger.py")
}
