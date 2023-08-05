import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk.aws-events-targets",
    "version": "1.60.0",
    "description": "Event targets for Amazon EventBridge",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "project_urls": {
        "Source": "https://github.com/aws/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.aws_events_targets",
        "aws_cdk.aws_events_targets._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_events_targets._jsii": [
            "aws-events-targets@1.60.0.jsii.tgz"
        ],
        "aws_cdk.aws_events_targets": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.9.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-batch==1.60.0",
        "aws-cdk.aws-codebuild==1.60.0",
        "aws-cdk.aws-codepipeline==1.60.0",
        "aws-cdk.aws-ec2==1.60.0",
        "aws-cdk.aws-ecs==1.60.0",
        "aws-cdk.aws-events==1.60.0",
        "aws-cdk.aws-iam==1.60.0",
        "aws-cdk.aws-kinesis==1.60.0",
        "aws-cdk.aws-lambda==1.60.0",
        "aws-cdk.aws-sns==1.60.0",
        "aws-cdk.aws-sns-subscriptions==1.60.0",
        "aws-cdk.aws-sqs==1.60.0",
        "aws-cdk.aws-stepfunctions==1.60.0",
        "aws-cdk.core==1.60.0",
        "constructs>=3.0.2, <4.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
