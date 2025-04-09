
module "lambda" {
  source = "../"
}

resource "aws_iam_role" "sfn_iam_role" {
  name = var.sfn_role_name
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            Effect = "Allow"
            Action = "sts:AssumeRole"
            Pricipal = {
                Service = "states.amazonaws.com"
            }
        }
    ]
  })
}

resource "aws_iam_role_policy" "sfn_assumumtion_role" {
  name = "${var.sfn_role_name}-policy"
  role = aws_iam_role.sfn_iam_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            Sid = "AllowStepFunctionsToInvokeLambda"
            Effect = "Allow"
            Action = "lambda:InvokeFunction"
            Resource = "${module.lambda.lambda_arn}"
        }
    ]
  })
}

output "step_function_role_arn" {
  value = aws_iam_role.sfn_iam_role.arn
}