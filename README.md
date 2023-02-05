# bucket-pull

Small CLI command to download a bucket directory locally.  

```
# download whole bucket to a local dir
bucket-pull gs://mybucketname ./mybucketname

# download a directory and all it's content to a local dir
bucket-pull gs://mybucketname/mydir ./

```



## Auth & Permissions

The utility makes use of the Google SDK and by default will look for credentials according to: 

The account you are connecting with will need at least the following permission on the Bucket directory.
...
