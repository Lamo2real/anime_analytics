#this is leveraged in the parennt module

output "lambda_execution_role_arn" {
  value = aws_iam_role.lambda_execution_role.arn
}

output "step_function_role_arn" {
  value = aws_iam_role.sfn_iam_role.arn
}