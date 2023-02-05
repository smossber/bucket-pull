# bucket-pull

Small CLI command to download a bucket directory locally.  
Aims to simulate `gsutil cp -r` when copying from a bucket to local path.

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

###  Some noteable differences 

gsutil seems to have this somewhat weird behaviour when the destination path doesn't exist

```
$ gsutil cp -r  gs://smoss-tech-test-bucket/mydir/ ./doesnotexist/actually/
$ echo $?
0
$ ls ./doesnotexist
ls: cannot access './doesnotexist': No such file or directory
```

It will not create the destination path (not that weird)  
but it won't complain either and end exits with 0.

Here bucket-pull diverge and throws an error instead.  
