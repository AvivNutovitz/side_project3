Terraform Readme:

this is a short menu of the Terraform component in the project, 
the deployment didn't go smoothly, i will describe more on that in person if you would like.

for the deployment I used terraform templates, 
the most important one is main.tf (defines the entire process of uploading the lambda and the api gateway to the AWS)
The following describes the component which were uploaded / used on the terraform along with aws provider:

- resource - the bucket object, uploaded the zip file containing the lambda to the s3 
- IAM role - gives the fitting permissions to the lambda function
- lambda function - A lambda function which will perform the prediction on the s3 stored model 	
- API gateway - connect the lambda function to an endpoint via HTTP Post, with the following json structure:
	{
		BucketName: "",
		ModelFile: "",
		WeightsFile: "",
		Data: ""
	}
	
When actually running the terraform, i simply created a plan and applied it via the tfvars file (containing the aws creds)
terraform init
terraform get
terraform plan
terraform apply


