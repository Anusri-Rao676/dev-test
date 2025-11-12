def AWS_CREDENTIALS_ID="476c9251-8767-468b-ac9b-ee729b46ba3a"
def BUCKET_NAME="target-19099"
pipeline{

    agent any
    stages{
        stage("checkout repo"){
            steps{
                git url: "https://github.com/sumanthskc/devops_aws_assignment.git" , branch: "feature"
            }
        }
        stage("ziping and uploading"){
            steps {
                
                sh "zip lambda_function.zip lambda_function.py"
                sh "ls -l"
                withCredentials([aws(credentialsId: AWS_CREDENTIALS_ID, variablePrefix: 'AWS')]) {
                    sh 'aws s3 cp lambda_function.zip s3://target-19099/'
                }
        }
        }
        stage("updating bucket"){
            steps{

                withCredentials([aws(credentialsId: AWS_CREDENTIALS_ID, variablePrefix: 'AWS')]){
                sh "aws lambda update-function-code \
                --function-name lambda_handler \
                --s3-bucket devops-eval-buck-1  \
                --s3-key lambda_function.zip \
                --publish"
                }

            }
        }
    }
}