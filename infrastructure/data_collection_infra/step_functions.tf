


resource "aws_sfn_state_machine" "wrokflow" {
  name = "state-machine-step-function"
  role_arn = module.iam.step_function_role_arn

  definition = jsonencode(
    {
      Comment = "STFU LOGIC: ths is the state machine for etxracting from API, and loading to S3"
      StartAt = "RunLambda"
      States = {

        APIWait = {
          Type = "Wait"
          Seconds = 3
          Next = "RunLambda"
        },

        RunLambda = {
            Type = "Task"
            Resource = "${aws_lambda_function.extract_anime_data.arn}"
            ResultPath = "$.stfuResult"
            OutputPath = "$.stfuResult"
            Next = "CheckPageStatus"
        },

        CheckPageStatus = {
          Type = "Choice"
          Choices = [
            {
              Variable = "$.continue"
              BooleanEquals = true
              Next = "APIWait"
            },
            {
              Variable = "$.continue"
              BooleanEquals = false
              Next = "StopStateMachine"
            }
          ]
        },

        StopStateMachine = {
          Type = "Succeed"
        }
      }
    }
  )
}