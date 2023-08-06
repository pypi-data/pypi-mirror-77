from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='aws_ecs_service',
    version='1.3.0',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    packages=find_packages(exclude=['venv', 'test']),
    description=(
        'AWS CDK package that manages ecs service resource.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        'aws_cdk.core>=1.60.0,<2.0.0',
        'aws_cdk.custom_resources>=1.60.0,<2.0.0',
        'aws_cdk.aws_lambda>=1.60.0,<2.0.0',
        'aws_cdk.aws_iam>=1.60.0,<2.0.0',
    ],
    author='Laimonas Sutkus',
    author_email='laimonas@idenfy.com, laimonas.sutkus@gmail.com',
    keywords='AWS CDK ECS CustomResource',
    url='https://github.com/idenfy/AwsEcsService.git',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
)
