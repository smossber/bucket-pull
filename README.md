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

The utility makes use of the Google SDK and uses [Client-Provided Authentication](https://googleapis.dev/python/google-api-core/latest/auth.html#client-provided-authentication) 

The account you are connecting with will need at least `storage.buckets.get` on the bucket, which can be granted with the `roles/storage.legacyBucketReader`. 

```
gsutil iam ch serviceAccount:SERVICEACCOUNT@PROJECT.iam.gserviceaccount.com:legacyBucketReader  gs://bucket
```


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

### Notes on multi-processing

With the `-m` flag we can enable multi-processing.  

Here `bucket-pull` has opted for using the [`threading`](https://docs.python.org/3/library/threading.html#module-threading).  
So, not _true_ paralellism and we only ever make use of one CPU.  
However, since we are mostly IO bound (disk and network) there is  
still some gain to be had by using multiple threads waiting for IO.  

"very" scientific comparison:
```
# with multithreading
time ./bucket-pull.py gs://smoss-tech-test-bucket/mydir /tmp/ -m
...
Downloading to /tmp/mydir/32mb.file
Downloading to /tmp/mydir/128mb.file
Downloading to /tmp/mydir/64mb.file
Downloading to /tmp/mydir/a/1.txt
Downloading to /tmp/mydir/a/b/2.txt
./bucket-pull.py gs://smoss-tech-test-bucket/mydir /tmp/ -m  5.86s user 5.24s system 22% cpu 50.149 total

# single thread
time ./bucket-pull.py gs://smoss-tech-test-bucket/mydir /tmp/ 
...
Downloading to /tmp/mydir/128mb.file
Downloading to /tmp/mydir/32mb.file
Downloading to /tmp/mydir/64mb.file
Downloading to /tmp/mydir/a/1.txt
Downloading to /tmp/mydir/a/b/2.txt
./bucket-pull.py gs://smoss-tech-test-bucket/mydir /tmp/  4.80s user 4.38s system 12% cpu 1:13.83 total
```