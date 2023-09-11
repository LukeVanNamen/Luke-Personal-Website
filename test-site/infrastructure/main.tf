resource "aws_lambda_function" "counter" {
    filename = data.archive_file.zip_the_python_code.output_path
    source_code_hash = data.archive_file.zip_the_python_code.output_base64sha256
    function_name = "counter"
    role = aws_iam_role.iam_for_lambda.arn
    handler = "func.handler"
    runtime = "python3.11"
}

# Might need to create a IAM role here for the Lambda function
resource "aws_iam_role" "iam_for_lambda" {
    name = "iam_for_lambda"
    assume_role_policy = <<EOF
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Effect": "Allow",
                "Sid":""
            }
        ]
    }
EOF
}

# Create IAM policy for allowing access to counter in DynamoDB Table
resource "aws_iam_policy" "new_policy_for_website" {
    name = "aws_iam_policy_for_personal_website"
    path = "/"
    description = "AWS IAM Policy for managing the Personal Website"
    policy = jsonencode(
        {
        "Version" : "2012-10-17",
        "Statement" : [
            {
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "arn:aws:logs:*:*:*",
                "Effect": "Allow"
            },
            {
                "Effect": "Allow",
                "Action":[
                    "dynamodb:UpdateItem",
                    "dynamodb:GetItem"
                ],
                "Resource":"arn:aws:dynamodb:*:*:table/myCounterTable"
            },
        ]
    })
}

# Attach policy above to role created above
resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_role" {
    role = aws_iam_role.iam_for_lambda.name
    policy_arn = aws_iam_policy.new_policy_for_website.arn
  
}

/*
# Create another policy for cross region access
resource "aws_iam_policy" "cross_region_access" {
    name = "aws_region_access"
    path = "/"
    description = "AWS IAM Policy for managing the DynamoDB Across Region"
    policy = jsonencode(
        {
        "Version": "2012-10-17",
        "Statement": [ 
            {
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Resource": "arn:aws:iam::750485601683:role/my-personal-site-CounterFunctionRole-1MQKZU2UFFRAO"
            }
        ]
    })
}

# Attach policy above to role created above
resource "aws_iam_role_policy_attachment" "attach_iam_cross_region_policy_to_role" {
    role = aws_iam_role.iam_for_lambda.name
    policy_arn = aws_iam_policy.cross_region_access.arn
}
*/

# Using Zip file to upload the lambda function
data "archive_file" "zip_the_python_code" {
    type = "zip"
    source_file = "${path.module}./Lambda/counter.py"
    output_path = "${path.module}./Lambda/packedlambda.zip"
}

# So Currently, I have it set up where we trigger the view count from DynamoDB from the APIGateway, but we can use a Lambda URL to do that. 
# Should look at deploying API here as well or instead eventually
resource "aws_lambda_function_url" "function_url" {
    function_name = aws_lambda_function.counter.function_name
    authorization_type = "NONE"  

    cors {
      allow_credentials = true
      allow_origins = ["*"]
      allow_methods = ["*"]
      allow_headers = ["date", "keep-alive"]
      expose_headers = ["keep-alive", "date"]
      max_age = 86400
    }
}