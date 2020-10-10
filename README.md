# Create a Heatmap with Amazon Rekognition
This project adds a heatmap layer on top of a picture based on Amazon Rekognition detect labels function.

Here is an example picture from Amazon Bring-Your-Kids-To-Work Day. We can add a HeatMap layer on top of it and see which game attracks more kids.

<img src="https://github.com/aws-samples/amazon-rekognition-heatmap/blob/main/Kids_day.jpeg" width="400" height="400" /> <img src="https://github.com/aws-samples/amazon-rekognition-heatmap/blob/main/Kid_Day_Result.png" width="400" height="400" />

![Kids Day](https://github.com/aws-samples/amazon-rekognition-heatmap/blob/main/Kids_day.jpeg | width = 100)![Kids Day Result](https://github.com/aws-samples/amazon-rekognition-heatmap/blob/main/Kid_Day_Result.png | width = 100)

# Setup
## Prerequest
1. Create an [S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)
2. Upload the picture that you want to add a heatmap layer into the S3 bucket you just created. 

## Run the demo
This demo runs the code using Amazon SageMaker. You can choose any IDE you like to run the python code. 
1. [Create a Notebook instance](https://docs.aws.amazon.com/sagemaker/latest/dg/howitworks-create-ws.html) in Amazon SageMaker
  a. Notebook instance type: t2.medium
  b. IAM role: Create a new role. 
2. Click the instance you just created. In the Permissions and encryption section, click the IAM role ARN. This will bring you to the IAM page. Click the Attach ploicies button. Find the AmazonRekognitionFullAccess policy and attach it.Then go back to the SageMaker console page.
3. Download the HeatMap_Code.ipynb file from here and upload it into your Jupyter notebook.
4. Open the HeatMap_Code and change the parameters in the first cell. Then you can run the code and see a HeatMap layer been added on your picture.

## Customize your HeatMap
You can customize your HeatMap by changing the parameters in the optional section at the beginning when open the Jupyter notebook.
1. matrixhight: This parameter control the number of lines you will get on the HeatMap grid. The default number is 50.
2. matrixwidth: This parameter control the number of columns you will get on the HeatMap grid. The default number is 50.
3. DarkestColor: The HeatMap will provide gradient colors between the darkest color you set and the color white. The default color is Crimson Red (#990000)
4. LabelType: This HeatMap layer was first created to detect human group. The default value for this parameter is "Person". You can change this to any other labels that Amazon Rekognition support such as cars, trees, etc. It can be used to detect the density of other objects as well.



* Edit your repository description on GitHub

# Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

# License

This library is licensed under the MIT-0 License. See the LICENSE file.

