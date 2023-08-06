# Crosscore

*Crosscore* is part of [Project Crossbow](https://bitbucket.org/claughton/crossbow). It
allows you to create an autoscaling pool of instances in the cloud that can then be used with [crossflow](https://bitbucket.org/claughton/crossflow) to execute computational workflows.

Currently *Crosscore* supports [Amazon Web Services](https://aws.amazon.com) and 
[Google Cloud Platform](https://cloud.google.com).

## 1. Installation
### 1.1 Prerequisites

#### 1.1.1 Python Version
*Crosscore* requires Python 3.6 or higher. No version of Python 2 is supported.

#### 1.1.2 Cloud Provider Configuration
*Crosscore* supports both AWS and GCP. There are slightly different configuration processes depending on which you plan to use:

**AWS**

It is assumed that you have done what is required to give you programmatic access to your AWS account. This
will involve generating your *AWS AccessKey ID* and *Secret Access Key*, and installing them with `aws configure`.

In addition you need to make sure your account has the following permissions:

    Amazon EC2FullAccess

**GCP**

You need to have downloaded a .json file with your service account credentials - see [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) for details. Then you need to decide on an availability zone for your cluster - 
bear in mind that this will affect the range of instance types (particularly GPU accelerators) you will be able to launch.
With these in hand, create two environment variables:

    export GOOGLE_APPLICATION_CREDENTIALS=<path to credentials file>
    export GOOGLE_DEFAULT_AVAILABILITY_ZONE=<availability zone>

#### 1.1.3 Terraform
*Crosscore* uses [Terraform](https://www.terraform.io) to do the heavy lifting of cloud infrastructure
creation and management. Before you can use *Crosscore* you must install terraform accoring to their 
instructions. Once you can run:

    terraform -version

you have done enough.

#### 1.1.4 SSH
You will need an ssh public key (e.g., $HOME/.ssh/id_rsa.pub). If you don't already have this, use `ssh-keygen` to make it, then set an environment variable to
its location:

    export SSH_PUBLIC_KEY=<path to id_rsa.pub or equivalent>

### 1.2 Install the Crosscore Python Package
*Crosscore* is not currently in [pypi](https://pypi.org) so to install it use:

    pip install git+https://bitbucket.org/claughton/crosscore.git

If all goes smoothly, you can then check the installation is OK by running `xcore -h`:
    
    usage: xcore [-h] [-V] {status,start,restart,shutdown,daemon} ...
    
    Crosscore: Cloud clusters for distributed computing.
    
    positional arguments:
      {status,start,restart,shutdown,daemon}
        status              status of crosscore cluster
        start               create cloud resources
        restart             recreate cloud resources
        shutdown            terminate and delete all resources
        daemon              control the xcore daemon
    
    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit

### 1.3 Configuration
Produce an initial default configuration for *xcore* using the command:

    xcore-init <provider>

where <provider> is "aws" or "gcp".

This will run some checks that you have all the prerequisites, and create some configuration and template
files. These will be placed in $HOME/.xcore. 
The process may take quite a time, as it involves terraform creating your base cloud infrastructure.

Once complete, check the default configuration in $HOME/.xcore/config.yaml. In particular you may want to change `image_name` - the name of the machine image
used to create the worker instances, and the associated `image_owner`. Most other "interesting" parameters such as worker instance type and the maximum number of workers that can be launched, can be changed interactively so do not need editing here now.

### 1.4 Start up
Once you are happy with the configuration, run `xcore start` to create the base cloud infrastructure and launch the **Crosscore** daemon. The base infrastructure consists of a small (default t2.small/f1-micro) instance that runs the scheduler, the daemon listens for job requests and autoscales the cluster as required.

## 2. Run a test job
Create a small **crossflow** workflow, e.g.:

    from crossflow.kernels import SubprocessKernel
    from crossflow.clients import Client
    from crosscore import cluster

    sleeper = SubprocessKernel('sleep {n}; echo {n}')
    sleeper.set_inputs(['n'])
    sleeper.set_outputs(['STDOUT'])

    client = Client(address=cluster.get_url())
    result = client.submit(sleeper, 10)
    print(result.result())

If you run this Python script interactively in one window, you can use 
`xcore status` from another to follow the process of worker creation, the 
job being run, and the worker being deleted after.
         
## 3. Shut down the cluster
If you are not going to use the cluster for a while, you can shut down the scheduler instance and stop the daemon:

    xcore shutdown

When you want to use it again, you run `xcore restart`

## 4. Changing the instance type and cluster size
Within a script you can adjust the maximum number of instances that may be 
launched, and their instance type, before you submit the job, e.g.:

    ...
    # AWS example:
    cluster.set_worker_type('c5.xlarge')
    # GCP example:
    # cluster.set_worker_type('n1-standard-4', accelerator_type='nvidia-tesla-t4')
    cluster.set_max_workers(5)
    client = Client(cluster.get_url())
    ...

## 5. Changing the machine image

The workflows you can run using **crossflow** depends on the software installed on your worker nodes. Though you may be able to do some provisioning 
of these on the fly (i.e., within **crossflow** kernel definitions) most likely you will want to prepare machine images with your favourite
software stack pre-installed. Examples of how this can be done using [Packer](https://www.packer.io) are available in the `Packer` folder.

Note that if you change the machine image, you will need to restart **crosscore** (`crosscore shutdown; crosscore restart`).

## 6. Authors:

• Christian Suess
• Charlie Laughton charles.laughton@nottingham.ac.uk

## 7. Acknowlegements:

EPSRC Grant [EP/P011993/1](https://gow.epsrc.ukri.org/NGBOViewGrant.aspx?GrantRef=EP/P011993/1)

